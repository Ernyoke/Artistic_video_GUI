from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QSettings
from artistic_video.ArtisticVideo import ArtisticVideo
from Preferences import CONTENT_WEIGHT_ID, STYLE_WEIGHT_ID, TV_WEIGHT_ID, TEMPORAL_WEIGHT_ID, LEARNING_RATE_ID, \
    ITERATIONS_ID, OUTPUT_LOCATION_ID, VGG_LOCATION_ID, USE_DEEPFLOW_ID, CONTENT_WEIGHT, STYLE_WEIGHT, TV_WEIGHT, TEMPORAL_WEIGHT, LEARNING_RATE, \
    STYLE_SCALE, ITERATIONS, OUTPUT_LOCATION, VGG_LOCATION, USE_DEEPFLOW, str_to_bool


class Worker(QThread):
    """
    This class is subclassing QThread, which means it wont have a separate event loop. It is important that an instance 
    of this thread will outlive the time taken to finish the Worker.run() method, otherwise it will block the caller's
    event loop.
    """

    def __init__(self):
        QThread.__init__(self)

        self.is_work_in_progress = False
        self.content_image = None
        self.style_image = None

        self.progress_bar = None

    show_progress_bar = pyqtSignal()

    def __del__(self):
        self.wait()

    def launch(self, progress_bar, content_image_path, style_image_path):
        self.progress_bar = progress_bar

        self.content_image = content_image_path
        self.style_image = style_image_path

        # start the thread
        self.start()

    # define signals
    work_started = pyqtSignal()
    work_finished = pyqtSignal()
    display_image = pyqtSignal(str)

    def run(self):
        """
        This method should run on a separate thread. It should not be called explicitly. It will be launched when the
        Worker.start() method is called.
        :return: Does not have a return value.
        """
        # start the work only if there is no other instance running
        if not self.is_running():

            # get the parameters from the QSettings
            settings = QSettings()
            content_weight = float(settings.value(CONTENT_WEIGHT_ID, str(CONTENT_WEIGHT)))
            style_weight = float(settings.value(STYLE_WEIGHT_ID, str(STYLE_WEIGHT)))
            tv_weight = float(settings.value(TV_WEIGHT_ID, str(TV_WEIGHT)))
            temporal_weight = float(settings.value(TEMPORAL_WEIGHT_ID, str(TEMPORAL_WEIGHT)))
            learning_rate = float(settings.value(LEARNING_RATE_ID, str(LEARNING_RATE)))
            iterations = int(settings.value(ITERATIONS_ID, str(ITERATIONS)))
            output_location = settings.value(OUTPUT_LOCATION_ID, OUTPUT_LOCATION)
            vgg_location = settings.value(VGG_LOCATION_ID, VGG_LOCATION)
            use_deepflow = str_to_bool(settings.value(USE_DEEPFLOW_ID, USE_DEEPFLOW))

            artistic = ArtisticVideo()
            # connect the progressbar to the ArtisticVideo
            self.progress_bar.hook_up(artistic)

            # connect the progressbar to the Worker
            self.show_progress_bar.connect(self.progress_bar.show)

            # set up the Progressbar dialog. Connect the Cancel button to the stop_running method from the
            # ArtisticVideo. This should be able to close the ongoing process.
            self.show_progress_bar.emit()

            # emit work_started signal for the MainWindow
            self.work_started.emit()
            self.is_work_in_progress = True

            stylized_path = artistic.stylize(vgg_location,
                                             self.content_image,
                                             [self.style_image],
                                             output_location,
                                             iterations,
                                             content_weight,
                                             style_weight,
                                             tv_weight,
                                             temporal_weight,
                                             learning_rate,
                                             use_deepflow)

            self.work_finished.emit()
            if stylized_path is not None:
                self.display_image.emit(stylized_path)

            # disconnect the Cancel button from the ArtisticVideo. Change the Cancel button status to OK and hook it
            # up with the Worker.exit() slot.
            self.progress_bar.unhook(artistic)

            # disconnect the Worker from the ProgressBar
            self.show_progress_bar.disconnect(self.progress_bar.show)

            self.progress_bar.set_to_ok()
            self.is_work_in_progress = False

    def is_running(self):
        return self.is_work_in_progress
