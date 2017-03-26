from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QSettings
from artistic_video.artistic_image import ArtisticVideo
from Preferences import CONTENT_WEIGHT_ID, STYLE_WEIGHT_ID, TV_WEIGHT_ID, TEMPORAL_WEIGHT_ID, LEARNING_RATE_ID, \
    ITERATIONS_ID, OUTPUT_LOCATION_ID, CONTENT_WEIGHT, STYLE_WEIGHT, TV_WEIGHT, TEMPORAL_WEIGHT, LEARNING_RATE, \
    STYLE_SCALE, ITERATIONS, OUTPUT_LOCATION
from Progressbar import  Progressbar


class Worker(QThread):

    def __init__(self):
        QThread.__init__(self)

        self.is_work_in_progress = False
        self.content_image = None
        self.style_image = None

        self.pogress_bar = Progressbar()

    def __del__(self):
        self.wait()

    def init_values(self, content_image_path, style_image_path):
        self.content_image = content_image_path
        self.style_image = style_image_path

    # define signals
    work_started = pyqtSignal()
    work_finished = pyqtSignal()

    def run(self):
        """
        :return: 
        """
        # start the work only if there is no other instance running
        if not self.is_running():
            self.work_started.emit()
            self.is_work_in_progress = True
            settings = QSettings()
            content_weight = float(settings.value(CONTENT_WEIGHT_ID, str(CONTENT_WEIGHT)))
            style_weight = float(settings.value(STYLE_WEIGHT_ID, str(STYLE_WEIGHT)))
            tv_weight = float(settings.value(TV_WEIGHT_ID, str(TV_WEIGHT)))
            temporal_weight = float(settings.value(TEMPORAL_WEIGHT_ID, str(TEMPORAL_WEIGHT)))
            learning_rate = float(settings.value(LEARNING_RATE_ID, str(LEARNING_RATE)))
            iterations = int(settings.value(ITERATIONS_ID, str(ITERATIONS)))
            output_location = settings.value(OUTPUT_LOCATION_ID, OUTPUT_LOCATION)

            artistic = ArtisticVideo()
            self.pogress_bar.show()
            self.pogress_bar.cancel_progress.connect(artistic.stop_running)

            artistic.stylize('imagenet-vgg-verydeep-19.mat',
                             self.content_image,
                             [self.style_image],
                             output_location,
                             iterations,
                             content_weight,
                             style_weight,
                             tv_weight,
                             temporal_weight,
                             learning_rate,
                             False)

            self.work_finished.emit()
            self.is_work_in_progress = False

    def is_running(self):
        return self.is_work_in_progress
