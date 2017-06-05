from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from gui.Ui_Preferences import Ui_PreferencesDialog
from PyQt5.Qt import QDoubleValidator, QIntValidator, QSettings, pyqtSlot
import os
from artistic_video.Utils import get_separator, get_os_type, OS

CONTENT_WEIGHT = 5e0
STYLE_WEIGHT = 1e2
TV_WEIGHT = 1e2
TEMPORAL_WEIGHT = 1e0
LEARNING_RATE = 1e1
STYLE_SCALE = 1.0
ITERATIONS = 500
OUTPUT_LOCATION = os.getcwd() + get_separator() + 'output' + get_separator()
VGG_LOCATION = os.getcwd() + get_separator() + 'imagenet-vgg-verydeep-19.mat'
USE_DEEPFLOW = 'False'

CONTENT_WEIGHT_ID = 'preferences/content_weight'
STYLE_WEIGHT_ID = 'preferences/style_weight'
TV_WEIGHT_ID = 'preferences/tv_weight'
TEMPORAL_WEIGHT_ID = 'preferences/temporal_weight'
LEARNING_RATE_ID = 'preferences/learning_rate'
ITERATIONS_ID = 'preferences/iterations'
OUTPUT_LOCATION_ID = 'preferences/output_location'
VGG_LOCATION_ID = 'preferences/vgg_location'
USE_DEEPFLOW_ID = 'preferences/use_deepflow'


def str_to_bool(str):
    if str.lower() == 'true':
        return True
    return False


def boo_to_str(bool):
    if bool:
        return 'True'
    return 'False'


class PreferencesDialog(QDialog):
    def __init__(self, parent):
        """
        Constructor of the PreferencesDialog.
        :param parent: A QWidget type (most likely the MainWindow) which is the parent widget of the dialog. 
        """
        super().__init__(parent)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self._set_validators()

        self.settings = QSettings()

        # connect signals and slots
        self.ui.defaultValuesButton.clicked.connect(self._use_default_values)
        self.ui.buttonBox.accepted.connect(self._save_inputs)
        self.ui.outputFolderBrowseButton.clicked.connect(self._browse_output_folder)
        self.ui.vggBrowseButton.clicked.connect(self._browse_vgg)

        # disable "Use deepflow" checkbox under Microsoft Windows.
        self.ui.deepFlowCheckBox.setDisabled(get_os_type() == OS.WIN)

    def _set_validators(self):
        """
        This methods sets validation rules for the input fields. It should be called only once when the 
        PreferencesDialog is instantiated.
        :return: Has no return values.
        """
        self.ui.contentWeightInput.setValidator(QDoubleValidator(self))
        self.ui.styleWeightInput.setValidator(QDoubleValidator(self))
        self.ui.tvWeightInput.setValidator(QDoubleValidator(self))
        self.ui.temporalWeightInput.setValidator(QDoubleValidator(self))
        self.ui.learningRateInput.setValidator(QDoubleValidator(self))
        self.ui.iterationsInput.setValidator(QIntValidator(0, 5000, self))

    def show(self):
        """
        By calling this method the dialog gets visible. Also, the input widgets are set to their corresponding states.
        :return:
        """
        self._init_inputs()
        super().show()

    @pyqtSlot()
    def _init_inputs(self):
        """
        This method is called when the dialog is shown. It sets the initial values of the input fields and other
        widgets.
        :return: Has no return values. 
        """
        self.ui.contentWeightInput.setText(str(self.settings.value(CONTENT_WEIGHT_ID, str(CONTENT_WEIGHT))))
        self.ui.styleWeightInput.setText(str(self.settings.value(STYLE_WEIGHT_ID, str(STYLE_WEIGHT))))
        self.ui.tvWeightInput.setText(str(self.settings.value(TV_WEIGHT_ID, str(TV_WEIGHT))))
        self.ui.temporalWeightInput.setText(str(self.settings.value(TEMPORAL_WEIGHT_ID, str(TEMPORAL_WEIGHT))))
        self.ui.learningRateInput.setText(str(self.settings.value(LEARNING_RATE_ID, str(LEARNING_RATE))))
        self.ui.iterationsInput.setText(str(self.settings.value(ITERATIONS_ID, str(ITERATIONS))))
        self.ui.outputFolderInput.setText(str(self.settings.value(OUTPUT_LOCATION_ID, OUTPUT_LOCATION)))
        self.ui.vggInput.setText(str(self.settings.value(VGG_LOCATION_ID, VGG_LOCATION)))
        self.ui.deepFlowCheckBox.setChecked(str_to_bool(self.settings.value(USE_DEEPFLOW_ID, USE_DEEPFLOW)))

    @pyqtSlot()
    def _use_default_values(self):
        """
        This method sets the default values for the widgets.
        :return: Has no return values.
        """
        self.ui.contentWeightInput.setText(str(CONTENT_WEIGHT))
        self.ui.styleWeightInput.setText(str(STYLE_WEIGHT))
        self.ui.tvWeightInput.setText(str(TV_WEIGHT))
        self.ui.temporalWeightInput.setText(str(TEMPORAL_WEIGHT))
        self.ui.learningRateInput.setText(str(LEARNING_RATE))
        self.ui.iterationsInput.setText(str(ITERATIONS))
        self.ui.outputFolderInput.setText(OUTPUT_LOCATION)
        self.ui.vggInput.setText(VGG_LOCATION)
        self.ui.deepFlowCheckBox.setChecked(USE_DEEPFLOW)

    @pyqtSlot()
    def _save_inputs(self):
        """
        Saves the input values from the widget by using QSettings.
        :return: Has no return values.
        """
        content_weight = float(self.ui.contentWeightInput.text())
        style_weight = float(self.ui.styleWeightInput.text())
        tv_weight = float(self.ui.tvWeightInput.text())
        temporal_weight = float(self.ui.temporalWeightInput.text())
        learning_rate = float(self.ui.learningRateInput.text())
        iterations = float(self.ui.iterationsInput.text())
        output_location = self.ui.outputFolderInput.text()
        vgg_location = self.ui.vggInput.text()
        use_deepflow = self.ui.deepFlowCheckBox.isChecked()
        if not os.path.isdir(output_location):
            self.show_error_dialog("Output folder {} does not exist!".format(output_location))
        elif not os.path.isfile(vgg_location):
            self.show_error_dialog("VGG input {} does not exist!".format(vgg_location))
        else:
            self.settings.setValue(CONTENT_WEIGHT_ID, content_weight)
            self.settings.setValue(STYLE_WEIGHT_ID, style_weight)
            self.settings.setValue(TV_WEIGHT_ID, tv_weight)
            self.settings.setValue(TEMPORAL_WEIGHT_ID, temporal_weight)
            self.settings.setValue(LEARNING_RATE_ID, learning_rate)
            self.settings.setValue(ITERATIONS_ID, iterations)
            self.settings.setValue(OUTPUT_LOCATION_ID, output_location)
            self.settings.setValue(VGG_LOCATION_ID, vgg_location)
            self.settings.setValue(USE_DEEPFLOW_ID, boo_to_str(use_deepflow))

    @pyqtSlot()
    def _browse_output_folder(self):
        """
        A slot method for the "Browse" button used for browsing the output folder location.
        :return: Has no return values.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly)
        if file_dialog.exec_():
            if len(file_dialog.selectedFiles()) > 0:
                selected_folder = file_dialog.selectedFiles()[0]
                self.ui.outputFolderInput.setText(selected_folder)

    @pyqtSlot()
    def _browse_vgg(self):
        """
        A slot method for the "Browse" button used for browsing the VGG(.mat) file  location.
        :return: Has no return values.
        """
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("VGG (*.mat)")
        if file_dialog.exec_():
            if len(file_dialog.selectedFiles()) > 0:
                selected_folder = file_dialog.selectedFiles()[0]
                self.ui.outputFolderInput.setText(selected_folder)

    @pyqtSlot(str)
    def show_error_dialog(self, message):
        """
        Shows an error dialog to the user with the input message.
        :param message: A string holding the error message.
        :return: Has no return value.
        """
        error_message = QMessageBox(self)
        error_message.setWindowTitle("Error!")
        error_message.setText(message)
        error_message.setIcon(QMessageBox.Critical)
        error_message.exec_()
