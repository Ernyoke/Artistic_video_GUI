from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import pyqtSlot, pyqtSignal
from gui.Ui_Progressbar import Ui_ProgressDialog


class Progressbar(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_ProgressDialog()
        self.ui.setupUi(self)
        self.ui.cancelButton.clicked.connect(self.cancel_btn_pressed)

    cancel_progress = pyqtSignal()

    def show(self):
        super().show()
        self._reset()

    def _reset(self):
        self.ui.iterationsBar.setValue(0)
        self.ui.framesBar.setValue(0)
        self.ui.cancelButton.setText("Cancel")
        self.ui.statusLabel.setText("")

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)

    @pyqtSlot(int, int)
    def update_frame_bar(self, current, maximum):
        self.ui.framesBar.setMaximum(maximum)
        self.ui.framesBar.setValue(current)

    @pyqtSlot()
    def cancel_btn_pressed(self):
        self.cancel_progress.emit()

    def set_to_ok(self):
        self.ui.cancelButton.setText("OK")
        self.ui.cancelButton.clicked.connect(self.close)

    def set_status(self, status):
        self.ui.statusLabel.setText(status)