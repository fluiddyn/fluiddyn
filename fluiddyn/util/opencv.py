"""Import OpenCV
================
Convenience module to import OpenCV

"""

# to avoid using Qt libs included in opencv
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
