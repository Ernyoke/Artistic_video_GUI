from PyQt5.QtWidgets import QDialog
from gui.Ui_Preferences import Ui_PreferencesDialog


class PreferencesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PreferencesDialog()
        print(self.ui)