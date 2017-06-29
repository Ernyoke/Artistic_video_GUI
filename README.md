# Artistic_video_GUI

The project's goal is the develop a GUI application where the user can transfer the artistic style from well known pictures painted by hungarian artists to their chosen images\videos.

# Dependencies
* Python 3.5 or above: https://www.python.org/downloads/ (for Windows recommended to use Anaconda: https://www.continuum.io/downloads)
* Tensorflow: https://www.tensorflow.org/
* opencv 3.0.0 or above: https://github.com/opencv/opencv
* PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5, https://www.qt.io/qt5-9/
* SciPy: https://www.scipy.org/

# Running on GPU
It is strongly recommended to use GPU for machine learning. In order of this, the following dependencies have to be met:
* CUDA compatible video card with CUDA toolkid installed: https://developer.nvidia.com/cuda-downloads
* cudnn: https://developer.nvidia.com/cudnn

# Other dependencies for running tests and additional scripts
* matplotlib: https://matplotlib.org/
* gpustats: https://github.com/wookayin/gpustat

# Neural network dependencies:
The code uses VGG-19 preloaded neural net which can be downloaded from here: http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat

# Running the code:
`python3 Main.py`

*Note:* The project was developed under Jetbrains PyCharm IDE, in order to execute from here you have to run the Main.py.

*Note2:* The optical flow (deepmatching, deepflow) are not supported under Windows. It is recommended to use a Linux based operating system instead.

# Documentation
This project is part of my master's thesis. The documentation is written in hungarian using Latex. It can be built from doc\documentation\ folder with the following command: 
`pdflatex DeepArt.tex`



