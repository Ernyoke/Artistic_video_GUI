@echo off

pyuic5 -o Ui_MainWindow.py mainwindow.ui
pyuic5 -o Ui_Preferences.py preferences.ui
pyuic5 -o Ui_ProgressbarImage.py progressbar_image.ui
pyuic5 -o Ui_ProgressbarVideo.py progressbar_video.ui
pyuic5 -o Ui_ProgressbarVideoOpticalFlow.py progressbar_video_with_opticalflow.ui
