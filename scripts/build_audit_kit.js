// Build the shareable human-audit kit (Word packet + Excel answer sheet) from the files written by
// scripts/build_audit_kit.py. Needs the npm packages `docx` and `exceljs`.
//   node scripts/build_audit_kit.js results/tables/heldout-v1/audit/kit
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, ImageRun, Footer, PageNumber, LevelFormat, BorderStyle, PageBreak,
} = require("docx");
const ExcelJS = require("exceljs");

const KIT = path.resolve(process.argv[2]);
const BUILD = path.join(KIT, "build");
const { meta, faults } = JSON.parse(fs.readFileSync(path.join(BUILD, "kit.json"), "utf8"));
const FONT = "Calibri", CONTENT = 9360;

const t = (text, o = {}) => new TextRun({ text: String(text), font: o.mono ? "Consolas" : FONT, size: o.size || 22,
  bold: o.bold, italics: o.italics, color: o.color });
const p = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [t(children)],
  spacing: { after: o.after ?? 120, line: 300 }, ...o.p });
const h1 = s => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 160 }, children: [t(s, { bold: true, size: 30 })] });
const h2 = s => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 100 }, children: [t(s, { bold: true, size: 25 })] });
const bullet = (children) => new Paragraph({ numbering: { reference: "b", level: 0 }, spacing: { after: 60, line: 290 },
  children: Array.isArray(children) ? children : [t(children)] });
const num = (children) => new Paragraph({ numbering: { reference: "n", level: 0 }, spacing: { after: 60, line: 290 },
  children: Array.isArray(children) ? children : [t(children)] });
const fmt = v => { if (v === "" || v === null || v === undefined) return "–"; const x = Number(v);
  if (!Number.isFinite(x)) return String(v); if (x === 0) return "0"; const a = Math.abs(x);
  return (a >= 1000 || a < 0.001) ? x.toExponential(3) : Number(x.toPrecision(4)).toString(); };
const stepName = lv => ({ "1": "h", "2": "h/2", "4": "h/4" }[lv] || lv);

const border = { style: BorderStyle.SINGLE, size: 4, color: "A0A0A0" };
function table(header, rows, widths, o = {}) {
  const w = widths.map(x => Math.round(x * CONTENT / widths.reduce((a, b) => a + b, 0)));
  w[w.length - 1] += CONTENT - w.reduce((a, b) => a + b, 0);
  const cell = (s, j, head) => new TableCell({ width: { size: w[j], type: WidthType.DXA },
    borders: { top: border, bottom: border, left: border, right: border },
    shading: head ? { type: ShadingType.CLEAR, fill: "E3EAF2", color: "auto" } : (o.shadeFirst && j === 0 ? { type: ShadingType.CLEAR, fill: "F4F6F8", color: "auto" } : undefined),
    margins: { top: 50, bottom: 50, left: 80, right: 80 },
    children: [new Paragraph({ children: [t(s, { size: o.size || 18, bold: head || (o.shadeFirst && j === 0) })] })] });
  return new Table({ width: { size: CONTENT, type: WidthType.DXA }, columnWidths: w,
    rows: [...(header ? [new TableRow({ tableHeader: true, children: header.map((s, j) => cell(s, j, true)) })] : []),
           ...rows.map(r => new TableRow({ children: r.map((s, j) => cell(s, j, false)) }))] });
}
const gap = () => new Paragraph({ spacing: { after: 80 }, children: [] });
const YELLOW = "FFF8D6", BLUE = "DCE6F0";
const box = (s, w, o = {}) => new TableCell({ width: { size: w, type: WidthType.DXA }, columnSpan: o.span,
  borders: { top: border, bottom: border, left: border, right: border },
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
  margins: { top: 70, bottom: o.tall ? 1000 : 70, left: 90, right: 90 },
  children: [new Paragraph({ children: [t(s, { size: 19, bold: o.bold })] })] });

// Fill-in answer box: the auditor types X in one cell per row and writes notes in the last row.
function answerBox(n) {
  const w = [3400, 1490, 1490, 1490, 1490];
  const row = (q, open) => new TableRow({ children: [box(q, w[0], { bold: true }),
    ...open.map((o, j) => box(o ? "" : "–", w[j + 1], { fill: o ? YELLOW : "F2F2F2" }))] });
  return new Table({ width: { size: CONTENT, type: WidthType.DXA }, columnWidths: w, rows: [
    new TableRow({ children: [box(`Your answers for fault ${n} (type X)`, w[0], { bold: true, fill: BLUE }),
      ...["Yes", "No", "Unsure", "N/A"].map((h, j) => box(h, w[j + 1], { bold: true, fill: BLUE }))] }),
    row("Q1  Edit matches its label?", [1, 1, 1, 0]),
    row("Q2  Assigned class plausible?", [1, 1, 1, 0]),
    row("Q3  Detection plausible?", [1, 1, 1, 1]),
    new TableRow({ children: [box("Confidence: type X under one", w[0], { bold: true }),
      box("High", w[1], { fill: YELLOW }), box("Medium", w[2], { fill: YELLOW }), box("Low", w[3], { fill: YELLOW }),
      box("–", w[4], { fill: "F2F2F2" })] }),
    new TableRow({ children: [box("Notes (required for any No or Unsure):", CONTENT, { bold: true, span: 5, fill: YELLOW, tall: true })] }),
  ] });
}

// ------------------------------------------------------------------ front matter
const body = [];
body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
  children: [t("Human audit packet", { bold: true, size: 40 })] }));
body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
  children: [t("Neuron model validation study: held-out evaluation", { size: 26 })] }));
body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 360 },
  children: [t(`For Samyak Singh and Naithik Somisetti · ${faults.length} faults · prepared ${meta.generated_utc.slice(0, 10)}`, { italics: true, size: 20, color: "555555" })] }));

body.push(new Table({ width: { size: CONTENT, type: WidthType.DXA }, columnWidths: [3900, 5460], rows: [
  ["Auditor name", ""], ["Date completed", ""], ["I worked alone and did not see the automated check (Yes / No)", ""],
].map(([k, v]) => new TableRow({ children: [box(k, 3900, { bold: true, fill: BLUE }), box(v, 5460, { fill: YELLOW })] })) }));
body.push(gap());

body.push(h1("1. What you are doing and why"));
body.push(p("We took six published computer models of single neurons and made small, deliberate edits (\"faults\") to them. Then we checked whether the usual test (re-running the one simulation shipped with each model, called the canonical test) notices the change, and whether a short set of extra stimuli does better."));
body.push(p("The paper can only rely on these faults if a person has checked that they are what the software says they are. That is your job. You are checking three things for each fault: was the edit made as labelled, is the category it was put in believable, and is the evidence that it was detected believable."));
body.push(p([t("Your answers are the independent check. ", { bold: true }), t("Disagreeing with the software is a useful result, not a failure. If something looks wrong or you are not sure, say so.")]));

body.push(h1("2. Rules"));
[ "Work on your own. Do not compare answers with each other until you have both submitted.",
  "Do not ask Neel or any AI tool what the answer should be. Use only this packet. (A separate automated check exists; you will see it after you submit, so it cannot influence you.)",
  "\"Unsure\" is an allowed answer. Guessing \"yes\" is worse than an honest \"unsure\".",
  "Write a short note whenever you answer No or Unsure, saying what you saw.",
  "Expected time: about 1 to 2 hours. You do not need to finish in one sitting.",
].forEach(s => body.push(bullet(s)));

body.push(h1("3. The ten-minute background"));
body.push(p([t("Neuron model. ", { bold: true }), t("A set of equations describing how a nerve cell's voltage changes. Its ion channels (sodium, potassium, calcium and others) let current in or out. Each channel has settings such as how many channels there are (conductance), the voltage their current pushes toward (reversal potential), and how fast their gates open and close.")]));
body.push(p([t("Stimulus (protocol). ", { bold: true }), t("A pattern of current injected into the cell, like a step or a ramp. The cell responds by changing voltage and, if pushed hard enough, firing spikes (sharp upward blips, the tall lines in the graphs).")]));
body.push(p([t("Features. ", { bold: true }), t("Numbers measured from the voltage: how many spikes, when the first spike happens, the gaps between spikes, spike height, and so on.")]));
body.push(p([t("Tolerance. ", { bold: true }), t("How big a difference must be before it counts. It is set from the original model alone, so that tiny numerical noise never counts as a change.")]));
body.push(p([t("h and h/2. ", { bold: true }), t("The simulation is run twice, with a normal time step (h) and half that step (h/2). A difference only counts as a detection if it shows up at both. Some faults were checked a third time at h/4.")]));
body.push(p([t("Two separate kinds of evidence. ", { bold: true }), t("The assigned class is decided from the summary features only. Separately, the whole voltage trace is compared (spike count, spike timing, overall voltage difference). These are kept apart on purpose. So a fault can be class 4 (\"no feature change\") and still show whole-trace differences: that means the change was only visible in the raw trace. This is expected, not a contradiction.")]));
body.push(p([t("The stimuli used:", { bold: true })]));
body.push(table(["Name in the tables", "What it is"], Object.entries(meta.protocols).map(([k, v]) => [k, v]), [30, 70]));
body.push(gap());
body.push(p([t("Categories (the \"assigned class\"):", { bold: true })]));
body.push(table(["Class", "Meaning"], Object.entries(meta.classes).map(([k, v]) => [k, v]), [34, 66]));

body.push(h1("4. How to answer the three questions"));
body.push(h2("Question 1: Does the edit match its label?"));
body.push(p("Each fault page shows the exact lines of the model file before (−, red) and after (+, green) the edit. Check that the change is what the label says. For example, \"multiply conductance by 0.5\" should turn 0.0675 into 0.03375 in the condDensity value of one channel, and nothing else should change. Answer No if the numbers do not match the label, the wrong thing changed, or extra things changed."));
body.push(h2("Question 2: Is the assigned class plausible?"));
body.push(p("Compare the class with the feature evidence (the first evidence table). Remember that the class ignores whole-trace differences (section 3). If the class says the canonical test missed it, the canonical test (P00_canonical) should not appear among the detections at both h and h/2, but some other stimulus should. If the class says it would not run, there should be no measurements. If it says no change, there should be no detections at both step sizes."));
body.push(h2("Question 3: Is the detection plausible?"));
body.push(p("Look at the evidence tables and the graph. A detection means the difference is bigger than the tolerance, at h and at h/2. In the graph, black is the original model and orange dashed is the edited one: where they separate, the behaviour changed. For the key faults, the top graph (canonical test) should look nearly identical while the lower graph shows the difference. Answer N/A if nothing was detected."));

body.push(h1("5. How to submit"));
[ "Save a copy of this document with your name in the file name, for example Audit_Packet_Samyak.docx.",
  "Fill in the yellow box on the first page: your name, the date, and whether you worked alone.",
  "Each fault's section ends with a yellow answer box. Type an X in one cell per row, and write a note whenever you answer No or Unsure.",
  "Send your finished document back to Neel. Only then compare answers with each other.",
].forEach(s => body.push(num(s)));

body.push(h1("6. Summary of the faults"));
body.push(table(["#", "Group", "Model", "Change", "Assigned class"],
  faults.map(f => [String(f.n), f.membership.join(" + "), f.model_id, f.operator, f.assigned_class]), [5, 20, 22, 25, 28], { size: 16 }));

// ------------------------------------------------------------------ one section per fault
for (const f of faults) {
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(h1(`Fault ${f.n} of ${faults.length}`));
  const change = [f.operator_meaning, f.factor != null ? `factor ${f.factor}` : null, f.delta_mV != null ? `shift ${f.delta_mV} mV` : null]
    .filter(Boolean).join("; ");
  body.push(table(null, [
    ["Fault ID", f.variant_id], ["Group", f.membership.join(" + ")], ["Model", `${f.model_name} (${f.model_id})`],
    ["Label (what the edit claims to be)", `${f.operator}: ${change}`],
    ["Severity", f.severity || "–"], ["Run status", f.run_status || "–"],
    ["Assigned class", `${f.assigned_class}: ${f.class_meaning}`],
    ["Detected (features) by", f.detecting_protocols.length ? f.detecting_protocols.join(", ") : "nothing"],
  ], [30, 70], { shadeFirst: true, size: 19 }));

  body.push(h2("The exact change (Question 1)"));
  if (!f.diff.length) body.push(p([t("No model file changed. This fault changes only how the simulation is run (a numerical setting), so compare the label with the run settings described above.", { italics: true })]));
  for (const d of f.diff) {
    body.push(p([t("File: ", { bold: true, size: 19 }), t(d.file, { mono: true, size: 17 })], { after: 40 }));
    for (const ln of d.lines) {
      const col = ln.startsWith("- ") ? "B00020" : ln.startsWith("+ ") ? "1B7F3B" : ln.startsWith("@@") ? "777777" : "333333";
      body.push(new Paragraph({ spacing: { after: 0, line: 240 }, children: [t(ln || " ", { mono: true, size: 15, color: col, bold: ln.startsWith("- ") || ln.startsWith("+ ") })] }));
    }
    if (d.truncated) body.push(p([t("(longer diff shortened)", { italics: true, size: 17 })]));
    body.push(gap());
  }

  body.push(h2("Evidence (Questions 2 and 3)"));
  if (f.feature_detections.length) {
    body.push(p([t("Feature differences that exceeded tolerance:", { bold: true, size: 20 })], { after: 60 }));
    const rows = f.feature_detections.slice(0, 16).map(d => [stepName(d.level_factor), d.protocol_id, d.feature, fmt(d.ref_value), fmt(d.var_value), fmt(d.diff), fmt(d.tau)]);
    body.push(table(["Step", "Stimulus", "Feature", "Original", "Edited", "Difference", "Tolerance"], rows, [8, 22, 18, 13, 13, 13, 13], { size: 16 }));
    if (f.feature_detections.length > 16) body.push(p([t(`(${f.feature_detections.length - 16} more rows not shown)`, { italics: true, size: 17 })]));
    body.push(gap());
  } else body.push(p([t("No feature differences exceeded tolerance.", { italics: true })]));
  if (f.trace_detections.length) {
    body.push(p([t("Whole-voltage-trace differences that exceeded tolerance:", { bold: true, size: 20 })], { after: 60 }));
    const rows = f.trace_detections.slice(0, 14).map(d => [stepName(d.level_factor), d.protocol_id,
      { spike_timing: "spike timing (largest shift, ms)", spike_count: "spike count", trace_rmse: "overall voltage difference (RMS, mV)" }[d.metric] || d.metric,
      fmt(d.ref_value), fmt(d.var_value), fmt(d.diff), fmt(d.tau)]);
    body.push(table(["Step", "Stimulus", "Measure", "Original", "Edited", "Difference", "Tolerance"], rows, [8, 20, 26, 11, 11, 12, 12], { size: 16 }));
    if (f.trace_detections.length > 14) body.push(p([t(`(${f.trace_detections.length - 14} more rows not shown)`, { italics: true, size: 17 })]));
    body.push(gap());
  }
  if (f.figure) {
    const buf = fs.readFileSync(path.join(BUILD, f.figure));
    const w = buf.readUInt32BE(16), hgt = buf.readUInt32BE(20), width = 600;
    body.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width, height: Math.round(width * hgt / w) } })] }));
    body.push(p([t("Black: original model. Orange dashed: edited model. Where the lines separate, the behaviour changed.", { italics: true, size: 18 })]));
  }
  body.push(gap());
  body.push(answerBox(f.n));
}

const doc = new Document({
  creator: "Neel Gurram", title: "Human audit packet",
  styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  numbering: { config: [
    { reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "n", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [t("Human audit packet · page ", { size: 16, color: "777777" }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: "777777" })] })] }) },
    children: body }],
});

// ------------------------------------------------------------------ Excel answer sheet
async function sheet() {
  const wb = new ExcelJS.Workbook();
  wb.creator = "Neel Gurram";
  const ws = wb.addWorksheet("Answers", { views: [{ state: "frozen", ySplit: 7 }] });
  ws.columns = [{ width: 5 }, { width: 38 }, { width: 22 }, { width: 22 }, { width: 26 }, { width: 30 },
                { width: 16 }, { width: 16 }, { width: 16 }, { width: 13 }, { width: 50 }];
  ws.getCell("A1").value = "Human audit answer sheet: held-out evaluation";
  ws.getCell("A1").font = { bold: true, size: 14 };
  ws.getCell("A2").value = "Save a copy with your name. Work alone. Use the drop-downs. Add a note for every No or Unsure.";
  ws.getCell("A2").font = { italic: true, color: { argb: "FF555555" } };
  ws.getCell("A3").value = "Auditor name:"; ws.getCell("A3").font = { bold: true };
  ws.getCell("A4").value = "Date:"; ws.getCell("A4").font = { bold: true };
  ws.getCell("A5").value = "I worked alone and did not see the automated check (Yes/No):"; ws.getCell("A5").font = { bold: true };
  for (const r of ["C3", "C4", "F5"]) { ws.getCell(r).fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FFFFF4CC" } }; }
  ws.getCell("F5").dataValidation = { type: "list", allowBlank: true, formulae: ['"Yes,No"'] };
  const head = ["#", "Fault ID", "Group", "Model", "Label (change)", "Assigned class",
                "Q1 Edit matches label?", "Q2 Class plausible?", "Q3 Detection plausible?", "Confidence", "Notes (required for No / Unsure)"];
  const hr = ws.getRow(7);
  head.forEach((h, j) => { const c = hr.getCell(j + 1); c.value = h; c.font = { bold: true };
    c.fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FFE3EAF2" } };
    c.alignment = { wrapText: true, vertical: "middle" }; c.border = { bottom: { style: "thin" } }; });
  hr.height = 32;
  faults.forEach((f, i) => {
    const r = ws.getRow(8 + i);
    [f.n, f.variant_id, f.membership.join(" + "), f.model_id, f.operator, f.assigned_class].forEach((v, j) => { r.getCell(j + 1).value = v; });
    for (const [col, opts] of [[7, '"Yes,No,Unsure"'], [8, '"Yes,No,Unsure"'], [9, '"Yes,No,Unsure,N/A"'], [10, '"High,Medium,Low"']]) {
      const c = r.getCell(col);
      c.dataValidation = { type: "list", allowBlank: true, formulae: [opts] };
      c.fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FFFFF4CC" } };
      c.border = { top: { style: "hair" }, bottom: { style: "hair" }, left: { style: "hair" }, right: { style: "hair" } };
    }
    r.getCell(11).alignment = { wrapText: true, vertical: "top" };
    r.getCell(11).fill = { type: "pattern", pattern: "solid", fgColor: { argb: "FFFFF4CC" } };
  });
  const guide = wb.addWorksheet("How to answer");
  guide.getColumn(1).width = 110;
  ["Q1 Edit matches label: does the before/after change in the packet do exactly what the label says, and nothing else?",
   "Q2 Class plausible: does the evidence support the assigned class (see section 3 of the packet for what each class means)?",
   "Q3 Detection plausible: do the differences exceed their tolerances at h and h/2, and does the graph show a real difference? N/A if nothing was detected.",
   "Confidence: how sure you are about this row overall.",
   "Unsure is an allowed answer. Disagreeing with the software is useful. Always explain No or Unsure in Notes."]
    .forEach((s, i) => { guide.getCell(`A${i + 1}`).value = s; guide.getCell(`A${i + 1}`).alignment = { wrapText: true }; });
  await wb.xlsx.writeFile(path.join(KIT, "Audit_Answer_Sheet.xlsx"));
}

Packer.toBuffer(doc).then(async b => {
  fs.writeFileSync(path.join(KIT, "Audit_Packet.docx"), b);
  fs.writeFileSync(path.join(KIT, "README.txt"),
    "Human audit kit\r\n\r\n1. Read Audit_Packet.docx (sections 1-5 first).\r\n" +
    "2. Save a copy with your name and type your answers into the yellow boxes (one per fault).\r\n" +
    "3. Work alone; send your document to Neel before comparing with anyone.\r\n\r\n" +
    `Generated ${meta.generated_utc} from commit ${meta.git_commit.slice(0, 8)}.\r\n`);
  console.log("wrote Audit_Packet.docx and README.txt in", KIT);
});
