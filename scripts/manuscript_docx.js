// Build the submission Word file from the manuscript Markdown.
//   node scripts/manuscript_docx.js [in.md] [out.docx]
// Journal rules applied here: 10-point Times Roman, automatic page numbers, references inserted from
// references_apa7.md, figures placed under their captions (Fig1-Fig5 from the journal artwork folder),
// line numbers for reviewers.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType,
  ShadingType, AlignmentType, ImageRun, Footer, PageNumber, LevelFormat, BorderStyle,
  LineNumberRestartFormat,
} = require("docx");

const REPO = "C:/Users/gurra/NeuroSem";
const IN = process.argv[2] || path.join(REPO, "docs/manuscript/MANUSCRIPT_V2.md");
let src = fs.readFileSync(IN, "utf8").replace(/\r/g, "");
src = src.split("## Open items before submission")[0];         // notes to the authors, not the paper
src = src.replace(/^\*Draft v[\s\S]*?\*\n/m, "");              // drafting note, not part of the paper
const REFS = fs.readFileSync(path.join(REPO, "docs/manuscript/references_apa7.md"), "utf8")
  .replace(/\r/g, "").trim();
src = src.replace("See `references_apa7.md`, inserted here at compile time (APA 7, alphabetical).", REFS);
const out = process.argv[3] || path.join(REPO, "docs/manuscript/MANUSCRIPT_v2.0.docx");
const FIGS = [1, 2, 3, 4, 5].map(n => path.join(REPO, "results/figures/heldout-v1/journal", `Fig${n}.png`));
const FONT = "Times New Roman", SIZE = 20, CONTENT = 9360;   // 10-point, as the journal asks

// ---- inline formatting: **bold**, *italic*, `code`, \* escapes
function runs(text, base = {}) {
  text = text.replace(/\\\*/g, "\u0000");
  const parts = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) parts.push({ t: text.slice(last, m.index) });
    const tok = m[0];
    if (tok.startsWith("**")) parts.push({ t: tok.slice(2, -2), bold: true });
    else if (tok.startsWith("`")) parts.push({ t: tok.slice(1, -1), code: true });
    else parts.push({ t: tok.slice(1, -1), italics: true });
    last = m.index + tok.length;
  }
  if (last < text.length) parts.push({ t: text.slice(last) });
  return parts.map(p => new TextRun({
    text: p.t.replace(/\u0000/g, "*"), bold: p.bold || base.bold, italics: p.italics || base.italics,
    font: p.code ? "Consolas" : FONT, size: p.code ? SIZE - 2 : (base.size || SIZE),
  }));
}

const para = (text, opts = {}) => new Paragraph({
  children: runs(text, opts.run || {}), spacing: { after: 120, line: 360 }, ...opts.p,
});

function table(lines) {
  const rows = lines.filter((l, i) => i !== 1).map(l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim()));
  const n = rows[0].length;
  const len = Array.from({ length: n }, (_, j) => Math.max(...rows.map(r => (r[j] || "").length), 4));
  const tot = len.reduce((a, b) => a + b, 0);
  let widths = len.map(x => Math.max(900, Math.round(CONTENT * x / tot)));
  const s = widths.reduce((a, b) => a + b, 0);
  widths = widths.map(w => Math.round(w * CONTENT / s));
  widths[n - 1] += CONTENT - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: "999999" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: CONTENT, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0,
      children: widths.map((w, j) => new TableCell({
        width: { size: w, type: WidthType.DXA }, borders,
        shading: i === 0 ? { type: ShadingType.CLEAR, fill: "E8EEF4", color: "auto" } : undefined,
        margins: { top: 60, bottom: 60, left: 90, right: 90 },
        children: [new Paragraph({ children: runs(r[j] || "", { bold: i === 0, size: 18 }) })],
      })),
    })),
  });
}

function image(file) {
  const buf = fs.readFileSync(file);
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);   // PNG IHDR
  const width = 620;
  return new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 240, after: 120 },
    children: [new ImageRun({ type: "png", data: buf, transformation: { width, height: Math.round(width * h / w) } })],
  });
}

// ---- block parser
const lines = src.split("\n");
const body = [];
let i = 0, buf = [], inFigures = false;
const flush = () => { if (buf.length) { body.push(para(buf.join(" "))); buf = []; } };
while (i < lines.length) {
  const l = lines[i];
  if (/^# /.test(l)) { flush(); body.push(new Paragraph({ heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER,
      spacing: { after: 240 }, children: runs(l.slice(2), { bold: true, size: 32 }) })); i++; continue; }
  if (/^## /.test(l)) { flush(); inFigures = /Figure captions|Figure legends/.test(l);
      body.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 160 }, children: runs(l.slice(3), { bold: true, size: 28 }) })); i++; continue; }
  if (/^### /.test(l)) { flush(); body.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 }, children: runs(l.slice(4), { bold: true, size: 24 }) })); i++; continue; }
  if (/^---\s*$/.test(l)) { flush(); i++; continue; }
  if (/^\|/.test(l)) { flush(); const t = []; while (i < lines.length && /^\|/.test(lines[i])) t.push(lines[i++]);
      body.push(table(t)); body.push(new Paragraph({ spacing: { after: 120 }, children: [] })); continue; }
  const bullet = l.match(/^- (.*)/), num = l.match(/^(\d+)\. (.*)/);
  if (bullet || num) { flush();
      let text = (bullet ? bullet[1] : num[2]); i++;
      while (i < lines.length && /^\s{2,}\S/.test(lines[i])) text += " " + lines[i++].trim();
      body.push(new Paragraph({ numbering: { reference: bullet ? "bullets" : "numbers", level: 0 },
          spacing: { after: 80, line: 320 }, children: runs(text) })); continue; }
  if (!l.trim()) { flush(); i++; continue; }
  if (inFigures && /^\*Files:/.test(l)) { i++; continue; }            // repository note, not for readers
  if (inFigures && /^\*\*Fig\. (\d)\*\*/.test(l)) { flush();
      const k = Number(l.match(/^\*\*Fig\. (\d)/)[1]); if (FIGS[k - 1]) body.push(image(FIGS[k - 1])); }
  if (/^[¹²³]/.test(l)) { flush(); body.push(para(l.trim(), { p: { spacing: { after: 40 } } })); i++; continue; }
  buf.push(l.trim()); i++;
}
flush();

const doc = new Document({
  creator: "Neel Gurram", title: "Manuscript draft v0.1",
  styles: { default: { document: { run: { font: FONT, size: SIZE } } } },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
  ] },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
      lineNumbers: { countBy: 1, restart: LineNumberRestartFormat.CONTINUOUS },
    },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }) },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log("wrote", out, b.length, "bytes"); });
