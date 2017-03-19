from PyQt5.QtWidgets import QDialog
from gui.Ui_Preferences import Ui_PreferencesDialog
from PyQt5.Qt import QDoubleValidator, QIntValidator, QSettings, pyqtSlot

CONTENT_WEIGHT = 5e0
STYLE_WEIGHT = 1e2
TV_WEIGHT = 1e2
TEMPORAL_WEIGHT = 1e0
LEARNING_RATE = 1e1
STYLE_SCALE = 1.0
ITERATIONS = 500
OUTPUT_FOLDER = 'output/'

CONTENT_WEIGHT_ID = 'preferences/content_weight'
STYLE_WEIGHT_ID = 'preferences/style_weight'
TV_WEIGHT_ID = 'preferences/tv_weight'
TEMPORAL_WEIGHT_ID = 'preferences/temporal_weight'
LEARNING_RATE_ID = 'preferences/learning_rate'
ITERATIONS_ID = 'preferences/iterations'


class PreferencesDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self._set_validators()

        self.settings = QSettings()

        self._init_inputs()

        self.ui.defaultValuesButton.clicked.connect(self._use_default_values)
        self.ui.buttonBox.accepted.connect(self._save_inputs)

    def _set_validators(self):
        self.ui.contentWeightInput.setValidator(QDoubleValidator(self))
        self.ui.styleWeightInput.setValidator(QDoubleValidator(self))
        self.ui.tvWeightInput.setValidator(QDoubleValidator(self))
        self.ui.temporalWeightInput.setValidator(QDoubleValidator(self))
        self.ui.learningRateInput.setValidator(QDoubleValidator(self))
        self.ui.iterationsInput.setValidator(QIntValidator(0, 5000, self))

    def show(self):
        super().show()
        self._init_inputs()

    @pyqtSlot()
    def _init_inputs(self):
        self.ui.contentWeightInput.setText(str(self.settings.value(CONTENT_WEIGHT_ID, str(CONTENT_WEIGHT))))
        self.ui.styleWeightInput.setText(str(self.settings.value(STYLE_WEIGHT_ID, str(STYLE_WEIGHT))))
        self.ui.tvWeightInput.setText(str(self.settings.value(TV_WEIGHT_ID, str(TV_WEIGHT))))
        self.ui.temporalWeightInput.setText(str(self.settings.value(TEMPORAL_WEIGHT_ID, str(TEMPORAL_WEIGHT))))
        self.ui.learningRateInput.setText(str(self.settings.value(LEARNING_RATE_ID, str(LEARNING_RATE))))
        self.ui.iterationsInput.setText(str(self.settings.value(ITERATIONS_ID, str(ITERATIONS))))

    @pyqtSlot()
    def _use_default_values(self):
        self.ui.contentWeightInput.setText(str(CONTENT_WEIGHT))
        self.ui.styleWeightInput.setText(str(STYLE_WEIGHT))
        self.ui.tvWeightInput.setText(str(TV_WEIGHT))
        self.ui.temporalWeightInput.setText(str(TEMPORAL_WEIGHT))
        self.ui.learningRateInput.setText(str(LEARNING_RATE))
        self.ui.iterationsInput.setText(str(ITERATIONS))

    @pyqtSlot()
    def _save_inputs(self):
        content_weight = float(self.ui.contentWeightInput.text())
        style_weight = float(self.ui.styleWeightInput.text())
        tv_weight = float(self.ui.tvWeightInput.text())
        temporal_weight = float(self.ui.temporalWeightInput.text())
        learning_rate = float(self.ui.learningRateInput.text())
        iterations = float(self.ui.iterationsInput.text())
        self.settings.setValue(CONTENT_WEIGHT_ID, content_weight)
        self.settings.setValue(STYLE_WEIGHT_ID, style_weight)
        self.settings.setValue(TV_WEIGHT_ID, tv_weight)
        self.settings.setValue(TEMPORAL_WEIGHT_ID, temporal_weight)
        self.settings.setValue(LEARNING_RATE_ID, learning_rate)
        self.settings.setValue(ITERATIONS_ID, iterations)