# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressbar.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(631, 185)
        self.gridLayout = QtWidgets.QGridLayout(ProgressDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.cancelButton = QtWidgets.QPushButton(ProgressDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(ProgressDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.iterationsBar = QtWidgets.QProgressBar(self.frame)
        self.iterationsBar.setProperty("value", 24)
        self.iterationsBar.setObjectName("iterationsBar")
        self.gridLayout_2.addWidget(self.iterationsBar, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.framesBar = QtWidgets.QProgressBar(self.frame)
        self.framesBar.setProperty("value", 24)
        self.framesBar.setObjectName("framesBar")
        self.gridLayout_2.addWidget(self.framesBar, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Progress"))
        self.cancelButton.setText(_translate("ProgressDialog", "Cancel"))
        self.label.setText(_translate("ProgressDialog", "Iterations:"))
        self.label_2.setText(_translate("ProgressDialog", "Frames:"))

