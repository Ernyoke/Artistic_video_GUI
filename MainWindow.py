from gui.Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QGraphicsScene, QGraphicsView, QSizePolicy, QFrame, QLabel, \
    QVBoxLayout, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QSize, Qt, QCoreApplication, pyqtSlot, pyqtSignal
import os
from Preferences import PreferencesDialog
from artistic_video.utils import get_input_type, InputType, NotSupportedInput, get_separator
from Worker import Worker

VIDEO_ICON = 'input/video_icon.png'


class SelectableGraphicsView(QGraphicsView):

    # abusing the language like a b0$$
    on_focus = pyqtSignal(QGraphicsView)

    def __init__(self, scene, parent, path_to_image, path_to_icon):
        super(SelectableGraphicsView, self).__init__(scene, parent)
        self.path_to_image = path_to_image
        self.path_to_icon = path_to_icon
        self.style_not_focused = 'border-style: solid ; border-width: 2px; border-color: black;'
        self.style_focused = 'border-style: solid ; border-width: 2px; border-color: blue;'
        self.style_hovered = 'border-style: solid ; border-width: 2px; border-color: white;'
        self.setStyleSheet(self.style_not_focused)

    def focusInEvent(self, QFocusEvent):
        self.focus()
        self.on_focus.emit(self)

    def focus(self):
        self.setStyleSheet(self.style_focused)

    def un_focus(self):
        self.setStyleSheet(self.style_not_focused)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._set_application_properties()

        # set up slot connection
        self.ui.browseButton.clicked.connect(self._browse_button_clicked)

        self.ui.actionExit.triggered.connect(self._exit)
        self.ui.actionAbout.triggered.connect(self._about)
        self.ui.actionPreferences.triggered.connect(self._preferences)
        self.preferences_dialog = PreferencesDialog(self)

        self.ui.okButton.pressed.connect(self._ok_button_pressed)

        # read styles
        sep = get_separator()
        self.style_views = [
            self._create_style_view(os.getcwd() + sep + 'styles' + sep + 'styles' + sep + 'style1.jpg',
                                    os.getcwd() + sep + 'styles' + sep + 'icons' + sep + 'style1.jpg', 'style1'),
            self._create_style_view(os.getcwd() + sep + 'styles' + sep + 'styles' + sep + 'style2.jpg',
                                    os.getcwd() + sep + 'styles' + sep + 'icons' + sep + 'style1.jpg', 'style2'),
            self._create_style_view(os.getcwd() + sep + 'styles' + sep + 'styles' + sep + 'style3.jpg',
                                    os.getcwd() + sep + 'styles' + sep + 'icons' + sep + 'style3.jpg', 'style3'),
            self._create_style_view(os.getcwd() + sep + 'styles' + sep + 'styles' + sep + 'style4.jpg',
                                    os.getcwd() + sep + 'styles' + sep + 'icons' + sep + 'style4.jpg', 'style4'),
            self._create_style_view(os.getcwd() + sep + 'styles' + sep + 'styles' + sep + 'style5.jpg',
                                    os.getcwd() + sep + 'styles' + sep + 'icons' + sep + 'style5.jpg', 'style5')]

        self.focused_style = self.style_views[0]
        self.focused_style.focus()

        input_image_scene = QGraphicsScene()
        input_image_scene.addPixmap(self._read_input_pixmap(os.getcwd() + '/other/original.png'))
        self.ui.inputImageView.setScene(input_image_scene)

        stylized_image_scene = QGraphicsScene()
        stylized_image_scene.addPixmap(self._read_input_pixmap(os.getcwd() + '/other/stylized.png'))
        self.ui.styleImageView.setScene(stylized_image_scene)

        self.selected_file_path = None

        # init the worker thread
        self.worker = Worker()
        self.worker.work_started.connect(self._disable_ok_btn)
        self.worker.work_finished.connect(self._enable_ok_btn)


    def _set_application_properties(self):
        QCoreApplication.setOrganizationName("Sapientia EMTE");
        QCoreApplication.setOrganizationDomain("https://github.com/Ernyoke/Artistic_video_GUI");
        QCoreApplication.setApplicationName("Deepart");

    def _create_style_view(self, style_path, path_to_icon, style_name):
        pixmap = self._read_input_pixmap(style_path)
        if pixmap is not None:

            # create a scene which will handle the graphical image
            scene = QGraphicsScene(self)
            scene.addPixmap(pixmap)

            # create the the widget which will display the image
            graphics_view = SelectableGraphicsView(scene, self, style_path, path_to_icon)

            # set its maximum size to 100 by 100 pixels
            graphics_view.setMaximumSize(QSize(100, 100))

            # set the size policy to fixed so the widgets wont change their size
            size_policy = QSizePolicy()
            size_policy.setHorizontalPolicy(QSizePolicy.Fixed)
            size_policy.setVerticalPolicy(QSizePolicy.Fixed)
            graphics_view.setSizePolicy(size_policy)

            # disable the scrollbars for the graphics view
            graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # display the widget with a label indicating the stlye name
            frame = QFrame(self.ui.scrollArea)
            vertical_layout = QVBoxLayout(frame)
            frame.setLayout(vertical_layout)
            frame.setMaximumSize(QSize(120, 150))
            vertical_layout.addWidget(graphics_view)
            title_label = QLabel(style_name, frame)
            title_label.setAlignment(Qt.AlignHCenter)
            vertical_layout.addWidget(title_label)
            self.ui.horizontalLayout_2.addWidget(frame)

            # connect the signal and slots
            graphics_view.on_focus.connect(self._style_selector)

            return graphics_view

    @pyqtSlot()
    def _browse_button_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilters(["Images (*.png *.jpg)", "Videos(*.gif, *.mp4)"])
        if file_dialog.exec_():
            if len(file_dialog.selectedFiles()) > 0:
                self.selected_file_path = file_dialog.selectedFiles()[0]
                self.ui.browseLineEdit.setText(self.selected_file_path)
                pixmap = self._read_input_pixmap(self.selected_file_path)
                if pixmap is not None:
                    scene = QGraphicsScene()
                    scene.addPixmap(pixmap)
                    self.ui.inputImageView.setScene(scene)
                else:
                    print("isnull")

    def _read_input_pixmap(self, path):

        def load_image(path):
            image = QImage()
            if image.load(path):
                return QPixmap.fromImage(image)

        try:
            if get_input_type(path) == InputType.IMAGE:
                return load_image(path)
            elif get_input_type(path) == InputType.VIDEO:
                return load_image(VIDEO_ICON)
        except NotSupportedInput:
            return None

    @pyqtSlot(SelectableGraphicsView)
    def _style_selector(self, graphics_view):
        # if selection was changed, don't focus other styles, focus just the one selected
        for view in self.style_views:
            if view != graphics_view:
                view.un_focus()
                self.focused_style = view

    @pyqtSlot()
    def _about(self):
        title = "About"
        content = "Copyright @ Ervin Szilagyi, Sapientia EMTE 2017"
        QMessageBox.about(self, title, content)

    @pyqtSlot()
    def _ok_button_pressed(self):
        self.worker.init_values(self.selected_file_path, self.focused_style.path_to_image)
        self.worker.start()

    @pyqtSlot()
    def _preferences(self):
        self.preferences_dialog.show()

    @pyqtSlot()
    def _exit(self):
        self.close()

    @pyqtSlot()
    def _disable_ok_btn(self):
        self.ui.okButton.setEnabled(False)

    @pyqtSlot()
    def _enable_ok_btn(self):
        self.ui.okButton.setEnabled(True)