#!/usr/bin/env python3
"""Isolated menu geometry regression; no application or personal profile needed."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

source = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="kos-menu-sizing-") as directory:
    work = Path(directory)
    shutil.copytree(source, work / "demo-ui")
    shutil.copytree(source.parent / "Icons", work / "Icons")
    (work / "demo-ui/controls/qmldir").write_text(
        "singleton LiquidStyle 1.0 LiquidStyle.qml\n"
        "singleton ControlForm 1.0 ControlForm.qml\n"
    )
    runner = shutil.which("qmltestrunner") or "/usr/lib/qt6/bin/qmltestrunner"
    result = subprocess.run(
        [runner, "-input", str(work / "demo-ui/tests/tst_popover_menu.qml")],
        env=dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software"),
        timeout=30,
    )
    raise SystemExit(result.returncode)
