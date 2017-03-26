from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import pyqtSlot, pyqtSignal
from gui.Ui_ProgressbarImage import Ui_ProgressDialogImage
from gui.Ui_ProgressbarVideo import Ui_ProgressDialogVideo
from gui.Ui_ProgressbarVideoOpticalFlow import Ui_ProgressDialogVideoOpticalFlow


class ProgressBar(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

    cancel_progress = pyqtSignal()

    def show(self):
        super().show()
        self._reset()

    def _reset(self):
        raise NotImplementedError

    def hook_up(self, artistic):
        raise NotImplementedError

    def unhook(self, artistic):
        raise NotImplementedError

    @pyqtSlot()
    def cancel_btn_pressed(self):
        self.cancel_progress.emit()

    def set_to_ok(self):
        self.ui.cancelButton.setText("OK")
        self.ui.cancelButton.clicked.connect(self.close)

    def set_status(self, status):
        self.ui.statusLabel.setText(status)


class ProgressbarImage(ProgressBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_ProgressDialogImage()
        self.ui.setupUi(self)
        self.ui.cancelButton.clicked.connect(self.cancel_btn_pressed)

    def _reset(self):
        self.ui.iterationsBar.setValue(0)
        self.ui.cancelButton.setText("Cancel")
        self.ui.statusLabel.setText("")

    def hook_up(self, artistic):
        artistic.iter_changed.connect(self.update_iter_bar)

    def unhook(self, artistic):
        artistic.iter_changed.disconnect(self.update_iter_bar)

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)


class ProgressbarVideo(ProgressBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_ProgressDialogVideoOpticalFlow()
        self.ui.setupUi(self)
        self.ui.cancelButton.clicked.connect(self.cancel_btn_pressed)

    def _reset(self):
        self.ui.iterationsBar.setValue(0)
        self.ui.framesBar.setValue(0)
        self.ui.cancelButton.setText("Cancel")
        self.ui.statusLabel.setText("")

    def hook_up(self, artistic):
        artistic.iter_changed.connect(self.update_iter_bar)
        artistic.frame_changed.connect(self.update_frame_bar)

    def unhook(self, artistic):
        artistic.iter_changed.disconnect(self.update_iter_bar)
        artistic.frame_changed.disconnect(self.update_frame_bar)

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)

    @pyqtSlot(int, int)
    def update_frame_bar(self, current, maximum):
        self.ui.framesBar.setMaximum(maximum)
        self.ui.framesBar.setValue(current)


class ProgressbarVideoOpticalFlow(ProgressBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_ProgressDialogVideo()
        self.ui.setupUi(self)
        self.ui.cancelButton.clicked.connect(self.cancel_btn_pressed)

    def show(self):
        super().show()
        self._reset()

    def _reset(self):
        self.ui.iterationsBar.setValue(0)
        self.ui.framesBar.setValue(0)
        self.ui.cancelButton.setText("Cancel")
        self.ui.statusLabel.setText("")

    def hook_up(self, artistic):
        artistic.iter_changed.connect(self.update_iter_bar)
        artistic.frame_changed.connect(self.update_frame_bar)

    def unhook(self, artistic):
        artistic.iter_changed.disconnect(self.update_iter_bar)
        artistic.frame_changed.disconnect(self.update_frame_bar)

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)

    @pyqtSlot(int, int)
    def update_frame_bar(self, current, maximum):
        self.ui.framesBar.setMaximum(maximum)
        self.ui.framesBar.setValue(current)