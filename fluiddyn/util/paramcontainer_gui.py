"""Qt based GUI for parameters (:mod:`fluiddyn.util.paramcontainer_gui`)
========================================================================

Provides:

.. autoclass:: QtParamContainer
   :members:
   :private-members:

"""

import os
import subprocess
from copy import deepcopy

# try to be able to import without Qt implementation
try:
    from matplotlib.backends.qt_compat import QtCore, QtWidgets
except ImportError:
    if "GITLAB_CI" not in os.environ:
        raise
else:
    try:
        _fromUtf8 = QtCore.QString.fromUtf8
    except AttributeError:

        def _fromUtf8(s):
            return s

    try:
        _encoding = QtWidgets.QApplication.UnicodeUTF8

    except AttributeError:

        def _translate(context, text, disambig):
            return QtWidgets.QApplication.translate(context, text, disambig)

    else:

        def _translate(context, text, disambig):
            return QtWidgets.QApplication.translate(
                context, text, disambig, _encoding
            )


from fluiddyn.util import time_as_str


class QtParamContainer:
    """QWidget application framework for loading, editing, saving and launching
    a job from a ParamContainer object.

    """

    def __init__(
        self, params, top=False, module_run_from_xml="fluidimage.run_from_xml"
    ):
        self.params = deepcopy(params)
        self.module_run_from_xml = module_run_from_xml
        full_tag_dot = params._make_full_tag()
        self.full_tag = full_tag_dot.replace(".", "_")

        self.labels = {}
        self.lines_edit = {}
        self.buttons = {}

        self.qt_params_children = {}

        key_attribs = params._get_key_attribs()
        tag_children = params._tag_children

        self.page_main = QtWidgets.QWidget()
        self.page_main.setObjectName(_fromUtf8("page_main_" + self.full_tag))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(
            _fromUtf8("verticalLayout_" + self.full_tag)
        )

        if self.params._contains_doc():
            self.pushButton_doc = QtWidgets.QPushButton(self.page_main)
            self.pushButton_doc.setText("Display doc " + full_tag_dot)
            self.verticalLayout.addWidget(self.pushButton_doc)
            self.pushButton_doc.released.connect(self.params._print_docs)

        if len(key_attribs) > 0:
            self.page_attribs = QtWidgets.QWidget()
            self.page_attribs.setObjectName(
                _fromUtf8("page_attribs_" + self.full_tag)
            )

            self.formLayout_attribs = QtWidgets.QFormLayout(self.page_attribs)
            self.formLayout_attribs.setContentsMargins(0, 0, 0, 0)
            self.formLayout_attribs.setObjectName(
                _fromUtf8("formLayout_" + self.full_tag)
            )

            i = -1
            for key in key_attribs:
                i += 1
                label = self.labels[key] = QtWidgets.QLabel(self.page_attribs)
                label.setObjectName(
                    _fromUtf8("label_" + self.full_tag + "_" + key)
                )
                self.formLayout_attribs.setWidget(
                    i, QtWidgets.QFormLayout.LabelRole, label
                )

                line = self.lines_edit[key] = QtWidgets.QLineEdit(
                    self.page_attribs
                )
                line.setObjectName(_fromUtf8("line_" + self.full_tag + "_" + key))
                self.formLayout_attribs.setWidget(
                    i, QtWidgets.QFormLayout.FieldRole, line
                )

                label.setText(_translate("MainWindow", key, None))

                line.setText(
                    _translate("MainWindow", repr(self.params[key]), None)
                )

                if key == "path":
                    i += 1

                    def choose_name():
                        fileName = QtWidgets.QFileDialog.getOpenFileName(
                            self.page_attribs, "OpenFile"
                        )
                        self.lines_edit["path"].setText("'" + fileName + "'")

                    self.buttons[key] = QtWidgets.QPushButton(self.page_attribs)
                    self.formLayout_attribs.setWidget(
                        i, QtWidgets.QFormLayout.FieldRole, self.buttons[key]
                    )
                    self.buttons[key].setText("Navigate to choose the path")
                    self.buttons[key].released.connect(choose_name)

            self.verticalLayout.addWidget(self.page_attribs)

        if len(tag_children) > 0:
            self.toolBox = QtWidgets.QToolBox(self.page_main)

            for tag in tag_children:
                qtparam = self.qt_params_children[tag] = self.__class__(
                    self.params[tag]
                )

                self.toolBox.addItem(
                    qtparam.page_main, _fromUtf8(full_tag_dot + "." + tag)
                )

            self.verticalLayout.addWidget(self.toolBox)

        if top:
            self.pushButton_xml = QtWidgets.QPushButton(self.page_main)
            self.pushButton_xml.setText("Display as xml")
            self.verticalLayout.addWidget(self.pushButton_xml)
            self.pushButton_xml.released.connect(self.print_as_xml)

            self.pushButton_default = QtWidgets.QPushButton(self.page_main)
            self.pushButton_default.setText("Reset to default parameters")
            self.verticalLayout.addWidget(self.pushButton_default)
            self.pushButton_default.released.connect(self.reset_default_values)

            self.pushButton_launch = QtWidgets.QPushButton(self.page_main)
            self.pushButton_launch.setText("Launch computation")
            self.verticalLayout.addWidget(self.pushButton_launch)
            self.pushButton_launch.released.connect(self.launch)

    def set_values(self, params):
        for key in params._get_key_attribs():
            self.lines_edit[key].setText(
                _translate("MainWindow", repr(params[key]), None)
            )

        for tag in params._tag_children:
            self.qt_params_children[tag].set_values(params[tag])

    def reset_default_values(self):
        self.set_values(self.params)

    def produce_params(self):
        params = deepcopy(self.params)
        self.modif_params(params)
        return params

    def print_as_xml(self):
        params = self.produce_params()
        params._print_as_xml()

    def modif_params(self, params):
        for key in self.params._get_key_attribs():
            params[key] = eval(str(self.lines_edit[key].displayText()))

        for tag in self.params._tag_children:
            self.qt_params_children[tag].modif_params(params[tag])

    def launch(self):
        params = self.produce_params()

        path_dir = "tmp_fluiddyn_params"
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)

        path = params._save_as_xml(
            path_file=os.path.join(
                path_dir, params._tag + time_as_str() + ".xml"
            ),
            find_new_name=True,
        )
        retcode = subprocess.call(
            ["python", "-m", self.module_run_from_xml, path]
        )
        return retcode
