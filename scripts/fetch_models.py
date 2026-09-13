"""Fetch pinned NeuroML model snapshots with provenance.

Downloads entry files from a commit-pinned GitHub raw URL, follows NeuroML
``<include href>`` and LEMS ``<Include file>`` references recursively, verifies
SHA-256 against previously recorded hashes when available, and writes a
``PROVENANCE.json`` next to each snapshot. Licenses must be verified *before*
a source is added to SOURCES (see LICENSE_AUDIT.md).

Usage:  python scripts/fetch_models.py [--dest models/raw]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import posixpath
import re
import sys
import urllib.request
from pathlib import Path

INCLUDE_RE = re.compile(r"<(?:include\s+href|Include\s+file)\s*=\s*\"([^\"]+)\"", re.IGNORECASE)
# NeuroML core type libraries are built into jNeuroML; never fetched.
BUILTIN_PREFIXES = ("NeuroML2CoreTypes/", "Cells.xml", "Networks.xml", "Simulation.xml", "Inputs.xml", "Channels.xml", "Synapses.xml", "PyNN.xml")

SOURCES = [
    {
        "snapshot": "PospischilEtAl2008@049081c3",
        "repo": "OpenSourceBrain/PospischilEtAl2008",
        "sha": "049081c39357d9e7c478b63ef7b10f374d1c50f4",
        "license": "MIT (NeuroML2/ directory); NEURON_ORIG and NEURON_MODIFIED carry a citation condition",
        "license_url": "https://github.com/OpenSourceBrain/PospischilEtAl2008/blob/049081c39357d9e7c478b63ef7b10f374d1c50f4/LICENSE",
        "citation": "Pospischil M, Toledo-Rodriguez M, Monier C, Piwkowska Z, Bal T, Fregnac Y, Markram H, Destexhe A (2008). Minimal Hodgkin-Huxley type models for different classes of cortical and thalamic neurons. Biological Cybernetics 99(4-5):427-441. doi:10.1007/s00422-008-0263-8",
        "entries": [
            "LICENSE", "CITATION.md",
            "NeuroML2/cells/RS/RS.net.nml", "NeuroML2/cells/RS/LEMS_RS.xml", "NEURON_MODIFIED/.test.RS.spikes.mep",
            "NeuroML2/cells/LTS/LTS.net.nml", "NeuroML2/cells/LTS/LEMS_LTS.xml", "NEURON_MODIFIED/.test.LTS.spikes.mep",
            "NeuroML2/cells/FS/FS.net.nml", "NeuroML2/cells/FS/LEMS_FS.xml", "NEURON_MODIFIED/.test.FS.spikes.mep",
            "NeuroML2/cells/IB/IB.net.nml", "NeuroML2/cells/IB/LEMS_IB.xml", "NEURON_MODIFIED/.test.IB.spikes.mep",
        ],
    },
    {
        "snapshot": "NeuroML2@a5f5dadc",
        "repo": "NeuroML/NeuroML2",
        "sha": "a5f5dadccd23606e683eaa0dd58dd2c3b2a7ed58",
        "license": "LGPL-3.0 (LICENSE.lesser)",
        "license_url": "https://github.com/NeuroML/NeuroML2/blob/a5f5dadccd23606e683eaa0dd58dd2c3b2a7ed58/LICENSE.lesser",
        "citation": "Hodgkin AL, Huxley AF (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. J Physiol 117(4):500-544. doi:10.1113/jphysiol.1952.sp004764 (NeuroML2 teaching implementation)",
        "entries": ["LICENSE.lesser", "examples/NML2_SingleCompHHCell.nml", "LEMSexamples/LEMS_NML2_Ex5_DetCell.xml", "LEMSexamples/test/.test.ex5.mep"],
    },
    {
        "snapshot": "WangBuzsaki1996@c5322844",
        "repo": "OpenSourceBrain/WangBuzsaki1996",
        "sha": "c532284492c3e421a7f8e88b3090af8ffee8cf6a",
        "license": "MIT (NeuroML2/ directory); ModelDB_NEURON and NEURON carry a citation condition",
        "license_url": "https://github.com/OpenSourceBrain/WangBuzsaki1996/blob/c532284492c3e421a7f8e88b3090af8ffee8cf6a/LICENSE",
        "citation": "Wang X-J, Buzsaki G (1996). Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model. J Neurosci 16(20):6402-6413. doi:10.1523/jneurosci.16-20-06402.1996",
        "entries": ["LICENSE", "CITATION.md", "NeuroML2/LEMS/WangBuzsaki.cell.nml", "NeuroML2/LEMS/WangBuzsaki.net.nml", "NeuroML2/LEMS/LEMS_WangBuzsaki.xml", ".test.wb.mep"],
    },
]

# SHA-256 recorded independently during the Milestone 0 fixture audit
# (docs/m0_evidence/fixtures/fixture_candidates.json).
EXPECTED = {
    "NeuroML2/cells/RS/RS.cell.nml": "a01d50a9cfac89343407ac3f5d638a4468cbffa2d599f9ff5a3413447fcbdb46",
    "NeuroML2/cells/RS/RS.net.nml": "2c8b333a0d2fa4e893fa6635a020956e09a86ea7dcbc95b5d1068d3f14ceb816",
    "NeuroML2/cells/RS/LEMS_RS.xml": "095f40cd8db08ba8bd1d74200feeb6e9544f8c68e47d9a494fae70719d29d3ce",
    "NeuroML2/channels/Na/Na.channel.nml": "7b019f4406eff251ffdbcdbd6dafd8c5f3731e1682ef5922b0eead6efe3a9eb6",
    "NeuroML2/channels/Kd/Kd.channel.nml": "6cc779cd5ad536e8e22631d89e62690be8954b1cfc85aaec06f479f528bdb4b9",
    "NeuroML2/channels/IM/IM.channel.nml": "9a1fbbc8756fcbbb2e92a62107eb72b8acd5bb95c5d77bb7f5ad09bb2213e8a9",
    "NeuroML2/channels/Leak/Leak.channel.nml": "41eb0263b1be315c429f64d040ca5eb34277da05031b01d94381859d01360f9d",
    "NEURON_MODIFIED/.test.RS.spikes.mep": "be5f0ed4b631a831ddbdd26e09930f56098bd2d33735c4379602457de94fa903",
    "NeuroML2/cells/LTS/LTS.cell.nml": "d63981d49223580804c8514a66791388eb6c6adef4a4c03c40046a9b87abfbb3",
    "NeuroML2/cells/LTS/LTS.net.nml": "4fa58713603da893fec1ad523a6b292922e167809b3a85fdf61a753122f8f771",
    "NeuroML2/cells/LTS/LEMS_LTS.xml": "96c5294d5b1a5bbdb0be6904e4fe0d7d1173447017b095de729f1242fe32299f",
    "NeuroML2/channels/IT/IT.channel.nml": "cc0afdc743130a38ee6736abecdb14384eae3fc57c74975740b1a38be3d3026f",
    "NeuroML2/channels/Ca/Ca.nml": "2bd89c887c3f4183253a560100dec2cca9dcf61379df5522e2d5ef9e9e1d44e3",
    "NEURON_MODIFIED/.test.LTS.spikes.mep": "e7613955d2f054d81295daeb0aac7f493ef3eea32c8f7cdee68b58e0de338c96",
    "NeuroML2/cells/FS/FS.cell.nml": "65a9c01beb6f2cf94ea0b35464e1b7206b8ecb219cefedca2c8b328847a1e4ae",
    "NeuroML2/cells/FS/FS.net.nml": "57a01d939e8dc42775f822844a85fa50947cdfd00115763de04090c07aecdba9",
    "NeuroML2/cells/FS/LEMS_FS.xml": "dc3cd1df9b8fd4046b62a13693ebd6a9ce53b831961ca9bd138024253a507154",
    "NEURON_MODIFIED/.test.FS.spikes.mep": "b8380949af98d4fb596e4734bb1f88b0301897d5fc07827795f29f00572930f0",
    "NeuroML2/cells/IB/IB.cell.nml": "99a3cc410042d45794f5e314e1060ff99e9718f6aac70d4725d7df9bab7ce59c",
    "NeuroML2/cells/IB/IB.net.nml": "24c5b1c1c989a50378659b265cb8efd358659903015c1c59c49b2c88c4aa9363",
    "NeuroML2/cells/IB/LEMS_IB.xml": "582ebefedd5b1b230d302ca71b8952f7ff866e49be94ff0e2bde852ced92fb8c",
    "NeuroML2/channels/IL/IL.channel.nml": "e13560db5f57abfb9ebc9cc44679d6248ba43b134d25a6fa730ad74f78b53b91",
    "NEURON_MODIFIED/.test.IB.spikes.mep": "63265a0ef69e2cf860ded35c2df2a323bc4f2005a24ac4277ee96cd6f5775fdd",
    "examples/NML2_SingleCompHHCell.nml": "5bc68caece1b5a10c4b16d7ead4045b7add061aa3096f6a5dea8a54bd445d404",
    "LEMSexamples/LEMS_NML2_Ex5_DetCell.xml": "cad3c94fbc4f14b8aa1af457c1cbad33e76497c955890ad556d27c06104c3fac",
    "LEMSexamples/test/.test.ex5.mep": "ba6898adf96a636928b44119e29b957c71ef7d0019c422d43d0616614a0c0e63",
    "LICENSE.lesser": "97628afebc60f026f5c2b25d7491c46a5c4ee61f693e7cfa07fbd2c03605979b",
    "NeuroML2/LEMS/WangBuzsaki.cell.nml": "1ef15bd09c3d7d2beb23954aa1b827a12306549bf6e2a08750355bb89fbf8760",
    "NeuroML2/LEMS/WangBuzsaki.net.nml": "ecc8d8d7e195eba8d56bca02a55fda0ed44dbda898c5f726d9041a796ed5c1fb",
    "NeuroML2/LEMS/LEMS_WangBuzsaki.xml": "62b506cb1223915dbc2d00dca902d8d80bfdbc489975c4e3d587b198fea5e621",
    ".test.wb.mep": "e34069b36f9327e93b7e04a5f1457dc6efb3b60abf4489cbcdee97d5da16bf91",
    "CITATION.md": None,  # differs per repository; hashed on download, not pre-recorded for both
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "neurosem-fetch/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch_source(src: dict, dest_root: Path) -> dict:
    base = f"https://raw.githubusercontent.com/{src['repo']}/{src['sha']}/"
    out_dir = dest_root / src["snapshot"]
    queue = list(src["entries"])
    seen: dict[str, dict] = {}
    while queue:
        rel = posixpath.normpath(queue.pop(0))
        if rel in seen or rel.startswith(BUILTIN_PREFIXES) or rel.startswith(".."):
            continue
        url = base + rel
        try:
            data = fetch(url)
        except urllib.error.HTTPError as exc:
            raise SystemExit(f"{src['snapshot']}: cannot fetch {rel} ({exc.code}) from {url}") from exc
        digest = sha256(data)
        expected = EXPECTED.get(rel)
        status = "not-prerecorded" if expected is None else ("match" if expected == digest else "MISMATCH")
        if status == "MISMATCH":
            raise SystemExit(f"hash mismatch for {rel}: got {digest}, expected {expected}")
        target = out_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        seen[rel] = {"url": url, "sha256": digest, "bytes": len(data), "hash_check": status}
        if rel.endswith((".nml", ".xml")):
            text = data.decode("utf-8", errors="replace")
            for inc in INCLUDE_RE.findall(text):
                if inc.startswith(("http://", "https://")) or inc.startswith(BUILTIN_PREFIXES):
                    continue  # remote, or a NeuroML core-type library built into jNeuroML
                queue.append(posixpath.join(posixpath.dirname(rel), inc))
    prov = {
        "snapshot": src["snapshot"],
        "repository": f"https://github.com/{src['repo']}",
        "commit": src["sha"],
        "license": src["license"],
        "license_url": src["license_url"],
        "citation": src["citation"],
        "downloaded_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "files": dict(sorted(seen.items())),
    }
    (out_dir / "PROVENANCE.json").write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")
    return prov


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dest", default="models/raw")
    args = ap.parse_args(argv)
    dest = Path(args.dest)
    for src in SOURCES:
        prov = fetch_source(src, dest)
        n = len(prov["files"])
        bad = [k for k, v in prov["files"].items() if v["hash_check"] == "not-prerecorded"]
        print(f"{src['snapshot']}: {n} files; not pre-recorded (hashed now): {bad}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
