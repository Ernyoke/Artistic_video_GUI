# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressbar_video.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialogVideo(object):
    def setupUi(self, ProgressDialogVideo):
        ProgressDialogVideo.setObjectName("ProgressDialogVideo")
        ProgressDialogVideo.resize(631, 185)
        self.gridLayout = QtWidgets.QGridLayout(ProgressDialogVideo)
        self.gridLayout.setObjectName("gridLayout")
        self.cancelButton = QtWidgets.QPushButton(ProgressDialogVideo)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(ProgressDialogVideo)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.iterationsBar = QtWidgets.QProgressBar(self.frame)
        self.iterationsBar.setProperty("value", 24)
        self.iterationsBar.setObjectName("iterationsBar")
        self.gridLayout_2.addWidget(self.iterationsBar, 1, 1, 1, 1)
        self.statusLabel = QtWidgets.QLabel(self.frame)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout_2.addWidget(self.statusLabel, 3, 1, 1, 1)
        self.framesBar = QtWidgets.QProgressBar(self.frame)
        self.framesBar.setProperty("value", 24)
        self.framesBar.setObjectName("framesBar")
        self.gridLayout_2.addWidget(self.framesBar, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 4, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 2, 1, 1)

        self.retranslateUi(ProgressDialogVideo)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialogVideo)

    def retranslateUi(self, ProgressDialogVideo):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialogVideo.setWindowTitle(_translate("ProgressDialogVideo", "Progress"))
        self.cancelButton.setText(_translate("ProgressDialogVideo", "Cancel"))
        self.label.setText(_translate("ProgressDialogVideo", "Iterations:"))
        self.label_2.setText(_translate("ProgressDialogVideo", "Frames:"))
        self.label_3.setText(_translate("ProgressDialogVideo", "Status:"))
        self.statusLabel.setText(_translate("ProgressDialogVideo", "TextLabel"))

