"""Import OpenCV
================
Convenience module to import OpenCV

"""

import os
import subprocess
import sys
from pathlib import Path

is_conda = (Path(sys.prefix) / "conda-meta").exists()

if not is_conda and not os.environ.get(
    "FLUIDDYN_NO_QTPY_INIT_BEFORE_OPENCV_IMPORT", False
):
    # to avoid using Qt libs included in opencv
    try:
        subprocess.run(
            [
                sys.executable,
                "-c",
                "from qtpy import QtWidgets; QtWidgets.QApplication([])",
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        pass
    else:
        try:
            from qtpy import QtWidgets
        except (RuntimeError, ImportError):
            pass
        else:
            QtWidgets.QApplication([])


try:
    import cv2

    error_import_cv2 = False
except ModuleNotFoundError as error:
    cv2 = None
    error_import_cv2 = error
