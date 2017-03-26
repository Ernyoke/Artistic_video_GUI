# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressbar_video_with_opticalflow.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialogVideoOpticalFlow(object):
    def setupUi(self, ProgressDialogVideoOpticalFlow):
        ProgressDialogVideoOpticalFlow.setObjectName("ProgressDialogVideoOpticalFlow")
        ProgressDialogVideoOpticalFlow.resize(635, 247)
        self.gridLayout = QtWidgets.QGridLayout(ProgressDialogVideoOpticalFlow)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(ProgressDialogVideoOpticalFlow)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 3, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(ProgressDialogVideoOpticalFlow)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 1, 1, 1)
        self.framesBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.framesBar.setProperty("value", 24)
        self.framesBar.setObjectName("framesBar")
        self.gridLayout_3.addWidget(self.framesBar, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.iterationsBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.iterationsBar.setProperty("value", 24)
        self.iterationsBar.setObjectName("iterationsBar")
        self.gridLayout_3.addWidget(self.iterationsBar, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 0, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 3, 2, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.statusLabel = QtWidgets.QLabel(ProgressDialogVideoOpticalFlow)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(ProgressDialogVideoOpticalFlow)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(ProgressDialogVideoOpticalFlow)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.opticalFrameBar = QtWidgets.QProgressBar(self.groupBox)
        self.opticalFrameBar.setProperty("value", 24)
        self.opticalFrameBar.setObjectName("opticalFrameBar")
        self.gridLayout_2.addWidget(self.opticalFrameBar, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)

        self.retranslateUi(ProgressDialogVideoOpticalFlow)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialogVideoOpticalFlow)

    def retranslateUi(self, ProgressDialogVideoOpticalFlow):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialogVideoOpticalFlow.setWindowTitle(_translate("ProgressDialogVideoOpticalFlow", "Progress"))
        self.cancelButton.setText(_translate("ProgressDialogVideoOpticalFlow", "Cancel"))
        self.groupBox_2.setTitle(_translate("ProgressDialogVideoOpticalFlow", "DeepArt"))
        self.label_2.setText(_translate("ProgressDialogVideoOpticalFlow", "Frames:"))
        self.label.setText(_translate("ProgressDialogVideoOpticalFlow", "Iterations:"))
        self.statusLabel.setText(_translate("ProgressDialogVideoOpticalFlow", "TextLabel"))
        self.label_3.setText(_translate("ProgressDialogVideoOpticalFlow", "Status:"))
        self.groupBox.setTitle(_translate("ProgressDialogVideoOpticalFlow", "Optical Flow"))
        self.label_4.setText(_translate("ProgressDialogVideoOpticalFlow", "Frames:"))

