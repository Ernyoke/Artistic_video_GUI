from PyQt5.QtWidgets import QDialog
from PyQt5.Qt import pyqtSlot, pyqtSignal, Qt
from gui.Ui_ProgressbarImage import Ui_ProgressDialogImage
from gui.Ui_ProgressbarVideo import Ui_ProgressDialogVideo
from gui.Ui_ProgressbarVideoOpticalFlow import Ui_ProgressDialogVideoOpticalFlow


class ProgressBar(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

    cancel_progress = pyqtSignal()
    display_stylized_image = pyqtSignal(str)

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

    @pyqtSlot(str)
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
        artistic.set_status.connect(self.set_status)
        artistic.frame_changed.connect(self.update_frame_bar)
        self.cancel_progress.connect(artistic.stop_running, Qt.DirectConnection)

    def unhook(self, artistic):
        artistic.iter_changed.disconnect(self.update_iter_bar)
        artistic.set_status.disconnect(self.set_status)
        self.cancel_progress.disconnect(artistic.stop_running)

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)

    @pyqtSlot(int, int, str)
    def update_frame_bar(self, current, maximum, stylized_image_path):
        self.display_stylized_image.emit(stylized_image_path)


class ProgressbarVideo(ProgressBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_ProgressDialogVideo()
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
        artistic.set_status.connect(self.set_status)
        self.cancel_progress.connect(artistic.stop_running, Qt.DirectConnection)

    def unhook(self, artistic):
        artistic.iter_changed.disconnect(self.update_iter_bar)
        artistic.frame_changed.disconnect(self.update_frame_bar)
        artistic.set_status.disconnect(self.set_status)
        self.cancel_progress.disconnect(artistic.stop_running)

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum, ):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)

    @pyqtSlot(int, int, str)
    def update_frame_bar(self, current, maximum, stylized_image_path):
        self.ui.framesBar.setMaximum(maximum)
        self.ui.framesBar.setValue(current)
        self.display_stylized_image.emit(stylized_image_path)


class ProgressbarVideoOpticalFlow(ProgressBar):

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_ProgressDialogVideoOpticalFlow()
        self.ui.setupUi(self)
        self.ui.cancelButton.clicked.connect(self.cancel_btn_pressed)

    def show(self):
        super().show()
        self._reset()

    def _reset(self):
        self.ui.iterationsBar.setValue(0)
        self.ui.framesBar.setValue(0)
        self.ui.opticalFlowBar.setValue(0)
        self.ui.cancelButton.setText("Cancel")
        self.ui.statusLabel.setText("")

    def hook_up(self, artistic):
        artistic.iter_changed.connect(self.update_iter_bar)
        artistic.frame_changed.connect(self.update_frame_bar)
        artistic.flow_created.connect(self.update_flow_bar)
        artistic.set_status.connect(self.set_status)
        self.cancel_progress.connect(artistic.stop_running, Qt.DirectConnection)

    def unhook(self, artistic):
        artistic.iter_changed.disconnect(self.update_iter_bar)
        artistic.frame_changed.disconnect(self.update_frame_bar)
        artistic.flow_created.disconnect(self.update_flow_bar)
        artistic.set_status.disconnect(self.set_status)
        self.cancel_progress.disconnect(artistic.stop_running)

    @pyqtSlot(int, int)
    def update_iter_bar(self, current, maximum):
        self.ui.iterationsBar.setMaximum(maximum)
        self.ui.iterationsBar.setValue(current)

    @pyqtSlot(int, int, str)
    def update_frame_bar(self, current, maximum, stylized_image_path):
        self.ui.framesBar.setMaximum(maximum)
        self.ui.framesBar.setValue(current)
        self.display_stylized_image.emit(stylized_image_path)

    @pyqtSlot(int, int)
    def update_flow_bar(self, current, maximum):
        self.ui.opticalFlowBar.setMaximum(maximum)
        self.ui.opticalFlowBar.setValue(current)