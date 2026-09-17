# License audit

Status: Milestone 0 deliverable, written 2026-09-13 on branch `m0-audit` (drafted at commit `3cdb957`;
fact-checked 2026-09-13 at commit `d323afa`).
Scope: every dependency, the Java runtime, every model snapshot under `models/`, NeuroSem's own
license, and redistribution scenarios. **This is not legal advice.** No lawyer reviewed it. It records
what each primary source says, where sources disagree, and what Neel has to decide (DECISIONS N-05).

## In plain English

1. Every piece NeuroSem uses belongs to someone, and each owner attached rules.
2. Think of each model file as a recipe card someone lent us.
3. An MIT card says: copy it and change it freely, but keep the owner's notice on the card.
4. The LGPL card (the NeuroML2 HH example) says: you may change it, but any changed copy you hand out stays under the LGPL (or the stricter GPL), not our BSD license.
5. A few reference files (`.mep` spike times) sit in folders that only say "cite us". They give no permission to hand out copies.
6. Our tools (pyNeuroML, jNeuroML, eFEL) are LGPL too. Using them unchanged, installed by pip, is the simple case.
7. Publishing a Docker image is different: the image itself would hand out Java (Temurin) and the LGPL jar. That brings notice and source-offer duties.
8. Nothing has been published. Git is local only, and every release choice is Neel's (D-003, N-01, N-05).
9. Section 11 lists the decisions. Section 10 lists what is still unverified.

---

## 1. Method and limits

Sources, in order of authority:

1. License texts in the installed packages, the pinned model snapshots and the local Temurin
   archive, read on 2026-09-13.
2. Upstream primary sources retrieved on 2026-09-13: GitHub license API, raw README files, PyPI JSON,
   the SPDX license list, and the Adoptium and Zenodo web pages.
3. Milestone 0 evidence files, each already checked by an independent verifier:
   `docs/m0_evidence/tools/*.research.json` with `*.verify.json` (where they differ, the verify file wins),
   `docs/m0_evidence/fixtures/`, `docs/m0_evidence/model_curation/license_evidence.json`, and
   `docs/m0_evidence/critique/INTEG.json` issue `INTEG-10` together with its skeptic verdict. The skeptic
   lowered that issue from high to medium, a pre-release checklist item.
   Check numbers cited below (for example "check 3") count entries of each verify file's `checks`
   array from 1; those files carry no explicit check ids.

Commands run for this audit (all read-only; scratch output in `work/tmp/m0docs/license_audit/`):

- `.venv/Scripts/python work/tmp/m0docs/license_audit/pkg_meta.py`: reads `License`,
  `License-Expression`, license classifiers and license-like files for every installed distribution
  through `importlib.metadata`. Output: `pkg_meta.json`.
- `head`/`wc`/`sha256sum` on the license files inside `.venv/Lib/site-packages/*.dist-info/licenses/`.
- `python -m pip show modelspec quantities certifi pymongo msgpack neo` (reads `Required-by`).
- A `zipfile` listing of `.venv/Lib/site-packages/pyneuroml/lib/jNeuroML-0.14.0-jar-with-dependencies.jar`:
  license-like entries, embedded `pom.xml` `<licenses>` blocks, `NeuroML2CoreTypes/`.
- `cat .tools/jdk-21.0.12.1+1/NOTICE .tools/jdk-21.0.12.1+1/release`; `ls legal/`; `head` of
  `legal/java.base/{LICENSE,ASSEMBLY_EXCEPTION}`.
- `curl -s https://api.github.com/repos/<owner>/<repo>/license` for 14 repositories. Output:
  `github_license_api_2026-09-13.txt`.
- `curl` of `https://raw.githubusercontent.com/NeuroML/Documentation/main/README.md`,
  `https://raw.githubusercontent.com/NeuroML/jNeuroML/v0.14.0/README.md`,
  `https://pypi.org/pypi/modelspec/0.4.0/json`, and the SPDX `licenses.json` / `exceptions.json`
  (list version `1dd5767`, release date 2026-09-10).
- WebFetch of `https://adoptium.net/docs/faq/` and `https://about.zenodo.org/policies/`. These pages
  were read through a summarising fetch tool, so the wording below may be paraphrased.
- `grep -rIl -i -E "licen|copyright|LGPL" models --include=*.nml --include=*.xml --include=*.mep --include=*.omt`
  (no hits), `git ls-files models`, `cat .dockerignore`, `find results -name "*.nml" -o -name "*.xml"`.

Limits:

- SPDX identifiers below are copied **as each source states them**. Where a source uses a deprecated
  identifier, the SPDX list status is noted next to it.
- Transitive licenses inside compiled wheels and inside the jNeuroML jar were read only as far as each
  file's first lines and the embedded metadata. Anything beyond that is marked unverified.
- Legal interpretation (for example, whether a Python import creates a "Combined Work") is outside
  this document's competence and is flagged as an open question.

## 2. Summary

| area | finding | risk now | action before any public release |
|---|---|---|---|
| Python dependencies (78 metadata entries = 77 distinct distributions, since `neurosem` is listed twice; 75 lock pins) | Permissive, LGPL, or MPL-2.0 (certifi, file-level copyleft). No installed distribution declares GPL (non-LGPL) in its metadata (eFEL ships the GPL v3 text only because LGPL v3 incorporates it). | low | Record discrepancies (3.2); keep license files when bundling. |
| Metadata vs license text | libNeuroML (BSD-2-Clause metadata, three-clause text); eFEL (LGPL-3.0-or-later text, "3.0" headers); **modelspec (LGPLv3 metadata, Apache-2.0 LICENSE file; new finding)** | low | Comply with the stricter reading; optionally ask upstream (outward-facing, Neel). |
| jNeuroML jar | LGPL-3.0 per GitHub; only-vs-or-later **unverified**; bundles many third-party libraries | low (not redistributed) | Enumerate bundled licenses before any image is published. |
| Java runtime | Temurin 21.0.12.1+1, GPL-2.0 with Classpath Exception (NOTICE); local copy git-ignored | low (not redistributed) | Keep `legal/` and `NOTICE` intact; meet GPLv2 source duties if an image is published. |
| Model snapshots (tracked in Git: 196 files) | MIT for all OSB NeuroML2 files; LGPL-3.0 for the NeuroML2 HH example; **5 tracked `.mep` files sit in citation-only carve-out folders** | medium at first public push | Decide how to handle carve-out files and LGPL mutants (N-05). |
| Mutants / transforms | Written only to git-ignored `work/`. Raw run records hold no model files. | none today | Choose: redistribute under upstream licenses, or ship regeneration scripts. |
| Docker image | Never built. `COPY . .` would include `models/`. | none today | Decide whether to publish an image at all. |
| Zenodo | No deposit made. Withdrawn records keep a tombstone. | none today | Settle licensing before the first deposit. |
| NeuroSem license | BSD-3-Clause, provisional (D-018) | low | Neel confirms code, documentation and data licenses. |

## 3. Python dependencies

### 3.1 Core scientific stack

"Installed metadata" comes from `importlib.metadata` in `.venv` (command in section 1).
"Upstream" comes from the evidence files or from the GitHub license API on 2026-09-13.

| package (version) | installed metadata | license file shipped in the wheel | upstream | discrepancy / note |
|---|---|---|---|---|
| pyNeuroML 1.3.22 | `License: LGPL-3.0-only`; classifier LGPLv3 | `LICENSE.lesser` (LGPL v3 text, SHA-256 `da7eabb7…`) | GitHub API: `LICENSE.lesser`, `LGPL-3.0`; PyPI and setup.cfg `LGPL-3.0-only` (`pyneuroml-jneuroml.verify.json` check 3) | GitHub uses `LGPL-3.0`, which is **deprecated** on the SPDX list (2026-09-10); the maintainer metadata says `-only`. The wheel **bundles the jNeuroML jar** (section 4). |
| libNeuroML 0.6.7 | `License: BSD-2-Clause`; classifier "BSD License" | `LICENSE` (10 lines, SHA-256 `cd1a1dc1…`) | GitHub API today: `BSD-3-Clause` | **Discrepancy.** The text has two bulleted conditions plus a third, unbulleted non-endorsement clause, so it reads as three-clause BSD. Treat it as BSD-3-Clause (obey all three conditions). The wheel also ships NeuroML schema files (`neuroml/nml/NeuroML_v2.3.1.xsd` and older). The same schema is published in the LGPL-3.0 NeuroML2 repository; whether the bundled copies carry a separate license was **not checked**. |
| eFEL 5.7.34 | `License: LGPLv3`; no `License-Expression`; classifier LGPLv3 | `LICENSE.txt`, `COPYING` (GPL v3), `COPYING.less` (LGPL v3), `AUTHORS.txt` | GitHub API today: `NOASSERTION`; DataCite `lgpl-3.0` (`efel.verify.json` checks 6, 7, 8, 17) | **Discrepancy.** `LICENSE.txt` grants LGPL "either version 3 of the License, or (at your option) any later version", which is LGPL-3.0-or-later. Source headers (`efel/__init__.py`, `efel/api.py`, grep today) say "version 3.0" with no or-later clause. `LICENSE.txt` refers to `COPYING.lesser`, but the file is named `COPYING.less`. It also says examples and tests are BSD-licensed and that external dependencies are LGPL or BSD. The duties for an unmodified v3 copy are the same either way. The package contains a compiled extension (`cppcore.cp312-win_amd64.pyd`). |
| PyLEMS 0.6.9 | `License: LGPL-3.0-only`; classifier LGPLv3 | `LICENSE.lesser` | GitHub API today: `LGPL-3.0` | Same `-only` vs deprecated `LGPL-3.0` naming as pyNeuroML. |
| neuromllite 0.6.1 | `License: LGPL-3.0-only`; no license classifier | `LICENSE.lesser` (SHA-256 `97628afe…`, byte-identical to the NeuroML2 snapshot's `LICENSE.lesser`) | GitHub API today: `LGPL-3.0` | none |
| modelspec 0.4.0 (required by neuromllite) | `License: LGPLv3`; classifier LGPLv3 | `LICENSE` = **Apache License 2.0** (201 lines, SHA-256 `c71d239d…`) | GitHub API today: `ModECI/modelspec` `Apache-2.0`; PyPI JSON today: `LGPLv3`, `license_expression` null | **New discrepancy** (not in the M0 evidence). Metadata says LGPLv3; the shipped license file and GitHub say Apache-2.0. Conservative handling: keep the Apache-2.0 file and treat the package as possibly LGPL. It is used unmodified and only transitively. |
| numpy 2.5.3 | `License-Expression: BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0` | several bundled license files | not re-checked | none |
| scipy 1.18.1 | full BSD text in `License`; classifier BSD | `LICENSE.txt` plus bundled component licenses | not re-checked | none |
| lxml 6.1.3 | `License: BSD-3-Clause` | `LICENSE.txt`, `LICENSES.txt` | not re-checked | none |
| pandas 3.0.5 / matplotlib 3.11.2 / PyYAML 6.0.3 | BSD 3-Clause text / matplotlib license agreement (classifier "Python Software Foundation License") / MIT | shipped | not re-checked | matplotlib also ships DejaVu and STIX font licenses. |

### 3.2 All other installed distributions

Values are exactly what installed metadata states. "Expr" means `License-Expression`, "Lic" means the
`License` field, "cls" means classifier. Dev-only tools are pinned in `requirements.lock` too.

| distribution | version | stated license | note |
|---|---|---|---|
| airspeed | 0.7.1 | Lic: BSD text; cls: BSD | |
| annotated-types | 0.8.0 | Expr: MIT | |
| anyio | 4.15.1 | Expr: MIT | |
| attrs | 26.1.0 | Expr: MIT | |
| blosc2 | 4.13.0 | Expr: BSD-3-Clause | Also ships `miniexpr/LICENSE`, `LICENSE-LIBTCC`, `LICENSE-SLEEF` and `LICENSE-TINYEXPR` (the last opens "zlib License"); the others were **not read** (unverified). |
| cachetools | 7.1.8 | Expr: MIT | |
| cattrs | 26.2.0 | Lic: MIT | |
| certifi | 2026.7.22 | Lic: MPL-2.0 | File-level copyleft; used unmodified. |
| colorama | 0.4.6 | cls: BSD only | No `License` field. |
| contourpy | 1.4.0 | Expr: BSD-3-Clause | |
| coverage | 7.16.0 | Lic: Apache-2.0 | dev tool; ships NOTICE.txt |
| cycler | 0.12.1 | Lic: BSD text; cls: BSD | |
| dill | 0.4.1 | Lic: BSD-3-Clause | |
| dnspython | 2.8.0 | Lic: ISC | |
| docstring_parser | 0.18.0 | Lic: MIT | |
| fonttools | 4.65.0 | Lic: MIT | `LICENSE.external` not read |
| graphviz | 0.21 | Expr: MIT | |
| h11 | 0.16.0 | Lic: MIT | |
| h2 | 4.4.1 | Expr: MIT | |
| h5py | 3.16.0 | Expr: BSD-3-Clause | Bundled `licenses/hdf5.txt`, `license.txt`, `pytables.txt`, `python.txt`, `stdint.txt` and `lzf/LICENSE.txt` not read. |
| hpack | 4.2.0 | Expr: MIT | |
| httpcore | 1.0.9 | Expr: BSD-3-Clause | |
| httpx | 0.28.1 | Lic: BSD-3-Clause | |
| hyperframe | 6.1.0 | Lic: MIT text | |
| idna | 3.19 | Expr: BSD-3-Clause | |
| iniconfig | 2.3.0 | Expr: MIT | |
| kiwisolver | 1.5.1 | Lic: Kiwi licensing terms text; cls: BSD | |
| markdown-it-py | 4.2.0 | cls: MIT only | |
| matplotlib-scalebar | 0.9.0 | Expr: BSD-2-Clause | |
| mdurl | 0.1.2 | cls: MIT only | |
| mpmath | 1.3.0 | Lic: "BSD"; cls: BSD | Clause count not stated in metadata. |
| msgpack | 1.2.2 | Expr: Apache-2.0 | |
| natsort | 8.4.0 | Lic: MIT | |
| ndindex | 1.10.1 | Lic: MIT | |
| neo | 0.14.5 | Expr: BSD-3-Clause | required by efel |
| networkx | 3.6.1 | Expr: BSD-3-Clause | |
| numexpr | 2.14.2 | Expr: MIT | |
| packaging | 26.3 | Expr: Apache-2.0 OR BSD-2-Clause | |
| pillow | 12.3.0 | Expr: MIT-CMU | |
| pip | 26.2.1 | Expr: MIT | installer; not in the lock |
| pluggy | 1.6.0 | Lic: MIT | |
| ppft | 1.7.8 | Lic: BSD-3-Clause | |
| progressbar2 | 4.6.0 | Lic: BSD-3-Clause | |
| py-cpuinfo | 9.0.0 | Lic: MIT | |
| pydantic / pydantic_core | 2.13.5 / 2.46.5 | Expr: MIT | |
| Pygments | 2.21.0 | Expr: BSD-2-Clause | |
| pymongo | 4.18.1 | Expr: Apache-2.0 | required by modelspec |
| pyparsing | 3.3.2 | Expr: MIT | |
| pytest / pytest-cov | 9.1.1 / 7.1.0 | Expr: MIT | dev tools |
| python-dateutil | 2.9.0.post0 | Lic: "Dual License"; cls: BSD and Apache | |
| python-utils | 4.0.1 | Expr: BSD-3-Clause | |
| quantities | 0.16.4 | no `License` field, no classifier | Required by neo. The shipped `doc/user/license.rst` holds two three-clause BSD texts: Quantities (Copyright 2012 Darren Dale) and Scimath (Copyright 2006 Enthought, Inc.). GitHub API for NeuralEnsemble/python-quantities returned "Not Found" today. |
| rich | 15.0.0 | Lic: MIT | |
| ruff | 0.16.7 | Expr: MIT | dev tool |
| six | 1.17.0 | Lic: MIT | |
| sympy | 1.14.0 | Lic: "BSD"; cls: BSD | |
| tables | 3.11.1 | Lic: "BSD 3-Clause License" | |
| tabulate | 0.10.0 | Expr: MIT | |
| threadpoolctl | 3.6.0 | Lic: BSD-3-Clause | |
| typing-inspection | 0.4.4 | Expr: MIT | |
| typing_extensions | 4.16.0 | Expr: PSF-2.0 | |
| tzdata | 2026.4 | Lic: Apache-2.0 | |
| neurosem | 0.1.0.dev0 | full BSD-3-Clause text (section 7) | editable install, listed twice by `importlib.metadata` |

### 3.3 Audited tools that are not dependencies

- **OSBModelValidation (OMV) 0.4.0**: `LGPL-3.0-only` (`omv.verify.json` check 5). It is **not** in
  `requirements.lock`, `environment.yml`, `Dockerfile`, `Makefile`, `pyproject.toml` or
  `.github/workflows/ci.yml` (grep, 2026-09-13). Its required dependency pyrx 0.3.0 declares `GPLv2`
  on PyPI and has no license file on GitHub (`omv.verify.json` third additional finding). This matters
  only if OMV is added as a secondary baseline (N-06).
- **SciUnit 0.2.8**: MIT. **NeuronUnit**: MIT in metadata only; the repository has no LICENSE file
  (`sciunit-neuronunit.verify.json` checks 2, 3, 22, 23). Neither is used. Do not copy NeuronUnit code.

## 4. The jNeuroML jar and what it bundles

File: `.venv/Lib/site-packages/pyneuroml/lib/jNeuroML-0.14.0-jar-with-dependencies.jar`,
SHA-256 `45ee565a65a66008a3b41935358d11b7c19cb6b5a67bbec22481d519f53db931` (matches D-004).
It has 12,980 entries and 63 embedded `pom.xml` files. NeuroSem runs it as a separate process
(`java -jar`, D-005) and does not modify it.

| component (embedded pom) | license as stated | source |
|---|---|---|
| jNeuroML 0.14.0 (`org.neuroml:jNeuroML`) | LGPL-3.0 (GitHub API today: `LICENSE.lesser`). README at v0.14.0, line 99: distributed under the GNU Lesser General Public License, **no version qualifier**. The embedded pom has no `<licenses>` block. | GitHub API 2026-09-13; `pyneuroml-jneuroml.verify.json` check 10 |
| jLEMS 0.12.0 (`org.lemsml:jlems`) | MIT (GitHub API today, `LEMS/jLEMS`). 0.12.0 has no release tag (D-004). | GitHub API 2026-09-13 |
| org.neuroml.model / org.neuroml.export / neuroml2-base-definitions 1.11.0 | LGPL-3.0 (GitHub API today for model and export). The jar also contains `NeuroML2CoreTypes/` (11 entries) and `Schemas/`, which come from the LGPL-3.0 NeuroML2 repository. | GitHub API 2026-09-13; `pyneuroml-jneuroml.verify.json` check 16; jar listing (11 `NeuroML2CoreTypes/` and 27 `Schemas/` entries). The upstream origin of those entries is inferred from their names, not byte-compared (unverified). |
| Jackson 2.18.2, Woodstox, json-simple | Apache License 2.0 (embedded pom) | jar listing |
| stax2-api, staxmate | "The BSD License" / "BSD" (embedded pom) | jar listing |
| JAXB XSOM, dtd-parser | Eclipse Distribution License 1.0 (embedded pom). `META-INF/NOTICE.md` says EDL 1.0 with `SPDX-License-Identifier: BSD-3-Clause`. | jar listing |
| jtidy | "Java HTML Tidy License" (embedded pom) | jar listing |
| FastDoubleParser | `META-INF/FastDoubleParser-NOTICE` says MIT, but `META-INF/FastDoubleParser-LICENSE` contains the Apache 2.0 text. `META-INF/thirdparty-LICENSE` credits fast_float (MIT). | jar listing (discrepancy, unverified which applies) |
| Jing (`META-INF/jing-copying.html`) | copying conditions of Thai Open Source Software Center Ltd; text not read in full | jar listing |
| Apache Velocity, Commons BeanUtils | NOTICE files present; `META-INF/LICENSE` and `LICENSE.txt` are Apache 2.0 text | jar listing |
| log4j 2.17.1, commons-lang/lang3/collections, slf4j, JSBML 1.4 and extensions, biojava, ncsa.hdf object 2.12, xstream 1.3.1, javaparser, JAXB runtime 2.3.5, jaxb2-basics 0.12.0, jakarta.xml.bind-api 2.3.3, istack-commons 3.0.12, com.sun.activation 1.2.2, org.neuroml.import 1.11.0, org.neuroml1.model 1.11.0 | **no license stated in the embedded pom** (probably inherited from parent poms that are not in the jar) | **unverified** |
| (unattributed files) `LICENSE.md` at the jar root and `META-INF/LICENSE.md` | BSD-style text, "Copyright (c) 2017 Oracle and/or its affiliates" (first lines read only); which component they belong to is not stated | **unverified** |

Consequence: NeuroSem does not itself copy the jar when a user installs it from pip, so there is
nothing for NeuroSem to redistribute there. Publishing an image that contains the jar would
redistribute all of the components above (section 8.3).

## 5. Java runtime: Eclipse Temurin

Local copy: `.tools/jdk-21.0.12.1+1/` (git-ignored). It was extracted from
`OpenJDK21U-jdk_x64_windows_hotspot_21.0.12.1_1.zip`, SHA-256 `f9d6e191…8b4e`, verified against
`https://api.adoptium.net/v3/assets/latest/21/hotspot` (`.tools/jdk_provenance.json`, D-004).
Its `release` file states `IMPLEMENTOR="Eclipse Adoptium"`, `IMPLEMENTOR_VERSION="Temurin-21.0.12.1+1"`,
`IMAGE_TYPE="JDK"` and `SOURCE_REPO="https://github.com/adoptium/jdk21u.git"`.

What the primary sources say:

- **`NOTICE` in the archive** (read 2026-09-13): the program is made available under "the GNU
  General Public License, version 2, with the Classpath Exception". The file carries
  `SPDX-License-Identifier: GPL-2.0 WITH Classpath-exception-2.0`. For version 9 and later, license
  and third-party information is under `legal/`. It also includes trademark notes (Eclipse Temurin is
  an Eclipse Foundation trademark; Java trademarks belong to Oracle) and a cryptography export notice.
- **`legal/`**: 70 module folders. `legal/java.base/` holds `LICENSE` (GPL v2 text, with the
  "CLASSPATH" EXCEPTION at line 326), `ASSEMBLY_EXCEPTION` (the separate "OpenJDK Assembly
  Exception", which describes Oracle's OpenJDK Code as GPL version 2 **only**),
  `ADDITIONAL_LICENSE_INFO`, and third-party notices (aes, asm, c-libutl, cldr, icu, public_suffix,
  siphash, unicode, wepoll, zlib).
- **Adoptium FAQ** (`https://adoptium.net/docs/faq/`, fetched 2026-09-13 through a summarising tool):
  it states the same license and that the binaries are provided at no cost.
- **SPDX list** (2026-09-10): `GPL-2.0`, the identifier used in `NOTICE`, is deprecated. A
  non-deprecated rendering would be `GPL-2.0-only WITH Classpath-exception-2.0`. This is an
  inference by this audit from the "version 2 only" wording in `ASSEMBLY_EXCEPTION`; Adoptium does
  not state that expression. The SPDX exceptions list also has `OpenJDK-assembly-exception-1.0`,
  which the archive ships but `NOTICE` does not name. Whether that exception belongs in the expression
  is **unverified**. `Classpath-exception-2.0` is on the current exceptions list.
- The `adoptium/temurin-build` repository is Apache-2.0 (GitHub API today). That covers the build
  scripts, not the JDK binaries.

The Docker image (never built) would install the Temurin **JRE** 21.0.12.1+1 through
`scripts/bootstrap_java.py`. That script extracts the whole archive (`safe_extract`, no file
filtering), so `legal/` should be preserved. The JRE archive's own legal files were **not
inspected** (unverified).

## 6. Model snapshots

All eight Open Source Brain (OSB) LICENSE files contain the **same MIT body**. The SHA-256 of the text
from "The MIT License" to end of file is `527f24f11b97976e…` for all eight (command in section 1).
The body opens with "Copyright © 2018 Open Source Brain developers" and "All rights reserved"; the
full MIT permission grant follows, so the grant is explicit. The only difference between files is a
preamble that carves some directories out of MIT. No `.nml`, `.xml`, `.mep` or `.omt` file in
`models/` contains its own license or copyright notice (grep, no hits). So the only MIT notice to
keep is each snapshot's `LICENSE` file, which should travel next to any copy (this audit's reading
of the MIT text, not a legal opinion).

GitHub's license API reports `NOASSERTION` for every OSB repository here: all six candidates
(`license_evidence.json`), Pospischil and Wang-Buzsaki (`fixture_verify.json` D1, D2). This includes
the three repositories whose LICENSE has **no** preamble. `docs/model_curation_candidates.md` section 3
attributes NOASSERTION to the preamble; for those three the cause must be something else, probably the
non-standard header text. GitHub does not state a reason, so this is **unverified**.

### 6.1 Snapshots in `models/raw/` (tracked in Git)

| snapshot | license (file, SHA-256 at fetch) | carve-outs in the LICENSE preamble | files in the snapshot that fall under a carve-out | `.mep` files and their status | citation |
|---|---|---|---|---|---|
| `NeuroML2@a5f5dadc` (NeuroML/NeuroML2 `a5f5dadc…`) | LGPL v3 text, `LICENSE.lesser`, `97628afe…`; GitHub `LGPL-3.0` | none | none | `LEMSexamples/test/.test.ex5.mep`: LGPL-3.0 (no carve-out) | No CITATION.md upstream. The manifest cites Hodgkin & Huxley 1952 as NeuroSem's own attribution, not an upstream condition. The tree has **no GPL-3.0 text**, although LGPL v3 incorporates GPL v3 (`fixture_verify.json` D9). Whether upstream means `-only` or `-or-later` is not stated (unverified). |
| `PospischilEtAl2008@049081c3` | OSB MIT, `e51615a6…`; GitHub NOASSERTION | `NEURON_ORIG`, `NEURON_MODIFIED`: "provided on condition of citing the ModelDB entry and original publication as outlined in CITATION.md" | `NEURON_MODIFIED/.test.{FS,IB,LTS,RS}.spikes.mep` (4 files, all tracked) | **These 4 `.mep` files carry the citation condition and no stated copy or modify permission** (`fixture_verify.json` D1; confirmed by reading LICENSE today). Every `NeuroML2/` file is MIT. | CITATION.md "respectfully ask[s]" citation of Pospischil et al. 2008, ModelDB 123623 and Zenodo `10.5281/zenodo.1936638`. That is a request for MIT files and a **condition** for the carve-out files. |
| `WangBuzsaki1996@c5322844` | OSB MIT, `18c4dd2b…`; GitHub NOASSERTION | `ModelDB_NEURON`, `NEURON` (citation condition); `Brian` (own `license.txt`) | none (only `NeuroML2/LEMS/*`, root `.test.wb.mep`, CITATION.md and LICENSE were fetched) | `.test.wb.mep` at repository root: MIT | Wang & Buzsaki 1996; ModelDB 26997; Zenodo badge `latestdoi/54382632` |

### 6.2 Snapshots in `models/candidates/` (tracked; nothing included in the study)

Source: `docs/model_curation_candidates.md` section 3, `license_evidence.json`, and the snapshot
files read today.

| snapshot | carve-outs | `.mep` in snapshot → status | citation (CITATION.md) | note |
|---|---|---|---|---|
| `PyloricNetwork@e97696fc` | none | none | Prinz, Bucher, Marder 2004 (Nat Neurosci); "Prinz AA, Thirumalai V, Marder E. J Neurosci. 2003" | **Citation mismatch:** the manifest (Crossref) cites Prinz, Billimoria, Marder 2003, *J Neurophysiol*, while the upstream CITATION.md names a different 2003 paper. Resolve before citing. |
| `GranCellLayer@cee86047` | none | none | Maex & De Schutter 1998; Zenodo `10.5281/zenodo.1495073` | CITATION.md links to "LICENCE", but the file is named `LICENSE` (cosmetic). |
| `SmithEtAl2013-L23DendriticSpikes@179c596e` | none | `NEURON/test/.test.mep` → MIT (the preamble-free LICENSE covers the whole repository) | Smith, Smith, Branco & Häusser 2013; Zenodo badge `30966621` | MIT here rests on the preamble-free LICENSE text alone; GitHub reports NOASSERTION. |
| `MiglioreEtAl14_OlfactoryBulb3D@eaad1c8f` | `NEURON`, `NEURON_FULL` | `NeuroML2/Channels/test/.test.12.mep`, `.test.35.mep` → MIT | Migliore et al. 2014; ModelDB 151681 | The soma test cells were "exported from NEURON ModelView" but sit outside the carve-outs, so they are MIT by the text. |
| `SolinasEtAl-GolgiCell@ab450696` (screened out) | `NEURON`, `NEURON_2007` | `NEURON/test/.test.soma.mep` → **carve-out: citation condition, no stated copy permission** (tracked) | Solinas et al. 2007; ModelDB 112685 | Screened out on validity grounds, but its files are still in Git. |
| `PinskyRinzelModel@a9aa9c90` (screened out) | `XPP` | `NeuroML2/twoCompartment/.test.fig2.mep` → MIT | Pinsky & Rinzel 1994; ModelDB 35358 | |

Thirteen OSB repositories with NeuroML2 cells but **no license** were excluded without downloading any
model file (`license_evidence.json` `screened_no_license`). With no license, all rights stay reserved
(GitHub documentation cited in `critique/INTEG.json` issue `INTEG-10`, point 4).

### 6.3 Do the OMV `.mep` reference files carry the citation condition?

Eleven `.mep` files are tracked (`git ls-files models | grep .mep`).

- **Citation condition only, no redistribution permission stated (5 files):** the four Pospischil
  `NEURON_MODIFIED/.test.*.spikes.mep` and Solinas `NEURON/test/.test.soma.mep`.
- **MIT (5 files):** Wang-Buzsaki `.test.wb.mep`, Smith `NEURON/test/.test.mep`, Migliore `.test.12.mep`
  and `.test.35.mep`, Pinsky-Rinzel `.test.fig2.mep`.
- **LGPL-3.0 (1 file):** NeuroML2 `LEMSexamples/test/.test.ex5.mep`.

The carve-out wording says "Code located there". A `.mep` file is YAML holding spike times (for
example `.test.RS.spikes.mep`: five spike times). Whether "code" covers such a data file is not stated.
The conservative reading, used by the verifier and the skeptic, is that it does. NeuroSem's code does
not read any `.mep` file (`grep -rn "\.mep" src/neuraxis`: no hits); the files are kept only as
provenance. The NEURO and INTEG skeptic verdicts recommend not vendoring them, and referencing them by
URL plus hash instead.

## 7. NeuroSem's own license

- `LICENSE`: BSD 3-Clause, "Copyright (c) 2026, Neel Gurram". A footer limits its scope to "NeuroSem's
  own source code and documentation", states that model files keep their licenses and that
  dependencies are used unmodified, and marks the choice as provisional.
- Consistent declarations: `pyproject.toml` (`license = { file = "LICENSE" }`), `CITATION.cff`
  (`license: BSD-3-Clause`), and the Dockerfile OCI label `org.opencontainers.image.licenses="BSD-3-Clause"`.
  Installed metadata carries the full text but no `License-Expression`.
- Status: provisional (D-018), awaiting Neel (N-05).

**Compatibility with LGPL dependencies used unmodified.** This is an analysis, not legal advice.

1. The source repository ships **no** LGPL library code. `git ls-files` shows no tracked `.jar`,
   `.xsd` or NeuroML2 core-type file; `requirements.lock` only names versions, and users install the
   libraries with pip. Distributing NeuroSem's source therefore conveys no LGPL library.
2. NeuroSem imports pyNeuroML, PyLEMS, neuromllite and eFEL as Python modules, and starts the jNeuroML
   jar as a separate `java -jar` process. LGPL v3 section 4 lets a "Combined Work" be conveyed "under
   terms of your choice" that do not restrict modifying the library, provided notices, license copies
   and a way to relink are supplied. BSD-3-Clause adds no such restriction, so on this reading the two
   licenses do not appear to conflict (not a legal opinion). Whether a Python import or a subprocess call makes a "Combined Work" at all is a legal
   question (**unverified**). It matters only when libraries are bundled (section 8.3).
3. The repository **does** convey third-party model files verbatim (196 tracked files under
   `models/`, of which 9 are NeuroSem's own `PROVENANCE.json` records), including the LGPL NeuroML2 example. For those, the LGPL and GPL v3 texts must
   accompany the copy. `LICENSE.lesser` is present; the GPL v3 text is not (section 6.1).
4. Not audited: whether any NeuroSem source file contains code adapted from an LGPL or GPL project.
   Nothing indicates this, but no line-by-line check was done.
5. Open question, not assessed: how AI-assisted authorship (AI_USE_LOG.md) bears on the copyright
   notice. This needs a human answer if it matters for the release.

**Documentation and data.** The LICENSE footer puts NeuroSem documentation under BSD-3-Clause. No
license has been chosen for generated data (traces, features, tables). Common alternatives are
CC-BY-4.0 for documentation and CC-BY-4.0 or CC0-1.0 for data; the choice is Neel's (L-02, L-03).

## 8. Redistribution scenarios

### 8.1 Pushing the Git repository publicly (N-01)

A public push redistributes the tracked `models/` tree:

- MIT files: the MIT text grants redistribution if the notice is kept. The LICENSE file travels with
  each snapshot; no further action identified.
- LGPL NeuroML2 files: the license texts permit verbatim copies if the license texts accompany them. **Add the GPL v3 text**,
  which LGPL v3 incorporates (`fixture_verify.json` D9).
- The five carve-out `.mep` files: no redistribution permission is stated. Options: remove them from
  the public tree and reference them by URL plus hash; keep them with the citation and a note that no
  license is granted; or ask the OSB maintainers (outward-facing).

### 8.2 Generated mutants and valid transforms

What the code does today:

- `models.materialize` copies a snapshot, minus `PROVENANCE.json`, into a workspace.
- `mutations.base.generate_mutants` writes each variant to `root/<model_id>/<variant_id>/` with a
  `variant.json`.
- Workspaces live under `paths.work: work` (`configs/study.yaml`), which is git-ignored.
- Raw run records in `results/raw/` store `run.json`, feature JSON, `traces.npz` and
  `simulator_output_tail.txt`, identifying the variant only by `variant_tree_sha256`. On 2026-09-13 (fact-check at `d323afa`)
  there are 716 local run directories under `results/raw/pilot/` holding 622 `run.json` files
  (512 `run_kind: probe`, 110 `run_kind: canonical`). The count grows as pilot runs continue. None is
  tracked (`git ls-files results`: 0 files), but `results/` is **not** git-ignored, so a careless
  `git add` would track them. There is no `.nml` or `.xml` file under `results/`.
- **So no mutant or transform file is redistributed today.** Whether `variant.json` quotes upstream
  file text was not checked.

If mutant or transform files are ever published (in the repository, a supplement, a Zenodo record,
or agent-study patches, which the spec publishes "where redistribution is permitted"):

| source license | what a mutant is | obligations (from the license texts) |
|---|---|---|
| MIT (Pospischil `NeuroML2/`, Wang-Buzsaki, candidates) | modified copy | Keep the copyright and permission notice (ship the snapshot LICENSE). Marking changes is not required by MIT but is good practice. |
| LGPL-3.0 (`nml2_hh_example`) | modified version of a covered work | It cannot be relicensed under BSD-3-Clause. It must stay under LGPL v3 (or GPL v3; LGPL section 2). GPL v3 section 5(a), incorporated by LGPL v3, requires "prominent notices stating that you modified it, and giving a relevant date". Ship `LICENSE.lesser` and the GPL v3 text. Whether a NeuroML model file counts as a "Library" in LGPL's sense is a legal question (**unverified**); treating it as covered is the conservative reading. |
| Carve-out (citation-only) | not applicable: NeuroSem does not mutate `.mep` files | Do not redistribute (8.1). |

Alternative (INTEG skeptic, revised recommendation): publish **regeneration** instead of files, meaning
the pinned upstream commit and file hashes plus the operator, site, seed and variant id. Variant ids
hash (model, operator, site), and `variant.json` records `tree_sha256`, so a regenerated tree can be
checked against the published hash. This avoids redistributing modified LGPL files. If files are
published anyway, add per-file license metadata (REUSE `REUSE.toml`), a license column in the mutation
and transform manifests, and a `reuse lint` CI step (skeptic recommendation, medium severity).

### 8.3 Publishing a Docker image

The Dockerfile says it has "NEVER BUILT". If it is built and **published**, the image would contain:

- the `python:3.12.14-slim-trixie` base image (Debian packages and CPython; their licenses were **not
  enumerated**, unverified);
- the Temurin JRE (declared in the JDK's `NOTICE` as GPL v2 with the Classpath Exception; see section 5 for the SPDX rendering; the JRE's own notices were not inspected);
- every wheel in `requirements.lock`, including the LGPL pyNeuroML wheel with the jNeuroML jar and all
  its bundled libraries (section 4), the LGPL eFEL compiled extension, and certifi (MPL-2.0);
- the whole repository (`COPY . .`). `.dockerignore` does not exclude `models/` or `results/raw/*/run.json`,
  so the image would carry the MIT and LGPL model files **and the five carve-out `.mep` files**.

Obligations when publishing the image (license text sections; the interpretation is unverified):

- Keep every license and notice file intact: dist-info `licenses/`, the Temurin `legal/` folder and
  `NOTICE`, and the jar's `META-INF` files.
- **Temurin (GPL v2 section 3):** accompany the binary with the source, or with a written offer valid for
  at least three years. Option 3(c), passing on the offer received, "is allowed only for noncommercial
  distribution" and only when the binary was received with such an offer. The upstream source repository
  is named in the `release` file; whether pointing to it satisfies section 3 for a re-distributor is
  **unverified**.
- **LGPL v3 components (jar, pyNeuroML, PyLEMS, neuromllite, eFEL; GPL v3 section 6 by incorporation):**
  provide the Corresponding Source for the exact versions. Under 6(d) the source may sit on a different
  server "operated by you or a third party", provided there are "clear directions next to the object
  code saying where to find the Corresponding Source", and you remain responsible that it stays available.
- Also: the Apache-2.0 NOTICE files (Velocity, BeanUtils) must travel with the jar; the MIT model notices
  must be kept.

Note from the INTEG skeptic: installing the jar at build time does not avoid these duties. A published
image contains the jar either way. The simplest option is to publish **only the Dockerfile**, which pins
versions, digests and the jar hash, and let users build the image themselves.

### 8.4 Archiving raw results on Zenodo

Zenodo policies (`https://about.zenodo.org/policies/`, fetched 2026-09-13 through a summarising tool):

- Users may deposit content "for which they possess the appropriate rights".
- Content must not violate copyright.
- Files may be open, embargoed, restricted or closed.
- A withdrawn record leaves a tombstone page and keeps its DOI and URL.
- The limit is 50 GB per record, with larger quotas available case by case.

What a raw-results deposit would contain today: traces (`traces.npz`, float32 mV), feature JSON,
`run.json`, and the tail of the jLEMS console output. No model files are included.

- For LGPL-sourced runs, GPL v3 section 2 (incorporated by LGPL v3) says: "The output from running a
  covered work is covered by this License only if the output, given its content, constitutes a covered
  work." The MIT license has no output clause. Whether simulated traces attract any copyright is a legal
  question (**unverified**).
- A Zenodo archive of a GitHub release would contain the repository, so everything in 8.1 applies,
  including the carve-out `.mep` files and the missing GPL v3 text. Because withdrawal keeps a tombstone,
  fix licensing **before** the first deposit.
- Choose and state a license for NeuroSem-generated data in the deposit metadata (L-03).
- D-003 already forbids any public release or DOI without Neel.

## 9. Documentation and third-party text

| source | license as stated | evidence | implication |
|---|---|---|---|
| docs.neuroml.org (built from `NeuroML/Documentation`) | CC-BY-4.0. README line 20: "The documentation is licensed under the CC-By License", linking `creativecommons.org/licenses/by/4.0/`. | `curl` of the raw README, 2026-09-13; GitHub license API: Not Found (no license file detected); `neuroml-lems.verify.json` check 43. A direct fetch of `https://docs.neuroml.org/` returned no readable content today. | Attribution is required if text or figures are reused. Whether any NeuroSem document reuses docs.neuroml.org text beyond citation was **not audited**. |
| SciUnit documentation | states the MIT license | `sciunit-neuronunit.verify.json` check 19 | none |
| eFEL paper (Bioinformatics 2026) | CC BY 4.0 (as reported; the check confirms the Crossref record) | `efel.verify.json` check 16 | CC BY 4.0 permits reuse with attribution, if that license applies to the figure in question. |
| NeuronUnit bioRxiv preprint | `cc_by_nc_nd` | `sciunit-neuronunit.verify.json` check 40 | ND terms do not permit sharing adaptations; cite only. |
| Citation File Format specification repository | CC-BY-4.0 | `venues-policy.verify.json` check 48 | none (the format is used, not copied) |
| NeuroSem documentation | BSD-3-Clause via the LICENSE footer | `LICENSE` | Decision L-02. |

## 10. Open questions and unverified items

1. jNeuroML: LGPL-3.0-only or -or-later (README and LICENSE.lesser give no qualifier; no source header checked).
2. NeuroML2 repository: -only or -or-later (bare LGPL v3 text; no statement found).
3. eFEL: intended expression (`LICENSE.txt` says or-later; headers say 3.0).
4. modelspec 0.4.0: LGPLv3 metadata vs Apache-2.0 LICENSE file.
5. libNeuroML: BSD-2-Clause metadata vs three-clause text; license of its bundled XSD copies.
6. Licenses of jar components with no license in the embedded pom (section 4); FastDoubleParser NOTICE (MIT) vs LICENSE file (Apache text).
7. blosc2 bundled `LICENSE-LIBTCC`, `LICENSE-SLEEF`, `miniexpr/LICENSE`; h5py and fonttools bundled license files (not read).
8. Licenses of Debian packages in the Docker base image; the Temurin JRE archive's `legal/` contents.
9. Whether "Code located there" in the OSB carve-outs covers `.mep` data files.
10. Why GitHub reports NOASSERTION for preamble-free OSB LICENSE files.
11. Whether Python imports or subprocess calls form an LGPL "Combined Work"; whether a NeuroML file is a "Library"; whether simulator output attracts copyright.
12. Whether pointing to upstream source repositories satisfies GPL v2 section 3 and GPL v3 section 6 for a published image.
13. Prinz 2003 citation: Crossref-verified *J Neurophysiol* paper (manifest) vs *J Neurosci* paper (upstream CITATION.md).
14. Whether `variant.json` edit records quote upstream file text.
15. The Adoptium FAQ and Zenodo policy wording were read through a summarising fetch tool and may be paraphrased; the Temurin `NOTICE` file and the downloaded license texts are the byte-level sources.
16. Temurin SPDX expression: whether `GPL-2.0-only WITH Classpath-exception-2.0` is accurate, and whether `OpenJDK-assembly-exception-1.0` should also appear (section 5).
17. Origin of the unattributed Oracle BSD-style `LICENSE.md` files in the jNeuroML jar; whether the jar's `NeuroML2CoreTypes/` and `Schemas/` entries are byte-identical to the LGPL NeuroML2 repository.

## 11. Decisions for Neel

All of these refine **DECISIONS N-05** ("Code license, and how to handle LGPL model files if mutants
are redistributed"). Related entries: N-01 (public repository), N-06 (OMV baseline), N-09 (candidate
models), D-003 (no release or DOI without Neel). No row below has been acted on.

| id | decision | options | Claude's recommendation (provisional) | needed before |
|---|---|---|---|---|
| L-01 | Code license | keep BSD-3-Clause / MIT / Apache-2.0 / other | Keep BSD-3-Clause (D-018); no conflict with LGPL dependencies used unmodified was found (section 7; not a legal opinion). | first public push (N-01) |
| L-02 | Documentation license | BSD-3-Clause as now / CC-BY-4.0 | CC-BY-4.0 for `docs/`, so reuse terms match docs.neuroml.org. | first public push |
| L-03 | License for generated data (traces, features, tables) | CC-BY-4.0 / CC0-1.0 / none stated | State one explicitly in the repository and in Zenodo metadata. | first Zenodo deposit |
| L-04 | LGPL mutants of `nml2_hh_example` | publish them under LGPL-3.0 with notices / publish regeneration scripts and hashes only / exclude the model from shared artefacts | Regeneration scripts and hashes; if files are published, keep LGPL-3.0, mark changes with dates, ship the LGPL and GPL texts. | any release of variants or agent-study patches |
| L-05 | The five carve-out `.mep` files tracked in Git (4 Pospischil, 1 Solinas) | remove from the public tree and reference by URL plus SHA-256 / keep with citation and a "no license granted" note / ask OSB maintainers | Remove from the public tree and reference by URL plus hash (NEURO and INTEG skeptic verdicts). NeuroSem code does not read them. | first public push |
| L-06 | GPL v3 text alongside the NeuroML2 snapshot's `LICENSE.lesser` | add a copy next to the snapshot (outside the hashed upstream files) / leave as is | Add it before any redistribution. | first public push |
| L-07 | Publish a Docker image? | publish the Dockerfile only / publish an image and meet GPL v2, LGPL and Apache NOTICE duties | Dockerfile only, unless an image is truly needed. If one is, first enumerate section 4 and the base image, and exclude the carve-out `.mep` files from the build context. | any registry push |
| L-08 | Per-file license metadata | REUSE `REUSE.toml` + license column in the mutation/transform manifests + `reuse lint` in CI / manifest column only / nothing | REUSE metadata, the manifest column and the CI lint (medium-severity pre-release item). | public release |
| L-09 | Upstream clarification (outward-facing) | ask libNeuroML (2- vs 3-clause), modelspec (LGPL vs Apache), eFEL (only vs or-later), jNeuroML (only vs or-later) / do not ask | Optional. Conservative handling works without answers. Neel decides whether to contact maintainers. | none (nice to have) |
| L-10 | Prinz 2003 citation | use the Crossref-verified manifest citation / add the CITATION.md paper as well | Cite both until checked against the model's source; record the choice. | before any candidate enters the study (N-09) |
| L-11 | Human licensing review | review by a qualified person before release / accept this audit | Get a human review of sections 8.2 to 8.4 before the M10 release; this audit is not legal advice. | public release |
| L-12 | OMV as a secondary baseline (N-06) | add OMV (LGPL-3.0-only; its dependency pyrx declares GPLv2) / do not add | If added, run it outside the frozen image, or record pyrx's license first. | adding OMV |
