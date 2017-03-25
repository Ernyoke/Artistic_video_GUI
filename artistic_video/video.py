import artistic_video.utils as utils


FRAME_NAME = 'frame%05d'

SYS_PLATFORM = utils.get_os_type()
SEPARATOR = utils.get_separator()


def _ffmpeg():
    """
    This method returns the path of the ffmpeg executable under Windows systems. It is expected
    that the executable is coupled with this script and its location path is under:
    windows/bin/ffmpeg.exe - for Windows operating systems
    /linux/bin/ffmpeg - for Linux operating systems
    :return: a string which contains the command line needed to run ffmpeg
    """
    if SYS_PLATFORM == utils.OS.WIN:
        return ".\\windows\\bin\\ffmpeg.exe"
    elif SYS_PLATFORM == utils.OS.LINUX:
        return utils.get_main_path()+"/linux/bin/ffmpeg"
    return None


def convert_to_frames(video_path, output_folder="frames", ext=".png"):
    """
    This function transforms a video into frames.
    :param video_path: A string with the path to the video which will be cut into frames
    :param output_folder: A string with the path of the folder for the output frames. It is mandatory that
    the folder already is created.
    :param ext: A string with the extension for the output frames (should be: png, jpg, etc...)
    :return: An integer which is the error code of the ffmpeg termination. If the process is successful
    than 0 will be returned.
    """
    frames = utils.get_files_from_folder(output_folder)
    frames.sort()
    error_code = 0

    if len(frames) != 0:
        print("Warning: " + output_folder + " is not empty, ffmpeg will not be launched!")
    else:
        file_name = utils.get_base_name(video_path)
        arguments = ["-i", video_path, "-f image2", output_folder+SEPARATOR+file_name+"_"+FRAME_NAME+ext]
        error_code = utils.run_binary(_ffmpeg(), arguments)
        if error_code == 0:
            frames = utils.get_files_from_folder(output_folder)
            frames.sort()

    return error_code, [output_folder + SEPARATOR + f for f in frames]


def convert_to_video(output_name="ffmpeg_vid", ext=".mp4",
                     frames_folder="frames", frame_name=FRAME_NAME, frame_ext=".png"):
    """
    This function converts a list of frames into a video.
    :param output_name: A string with the path to the output video.
    :param ext: A string with the extension of the output video (should be: mp4, avi, etc...)
    :param frames_folder: A string with the name of the frames which will be converted into a video.
    :param frame_name: A string containing the structure of a frame name (ex. frame%05d)
    :param frame_ext: A string with the extension of the input frames. (should be: png, jpg, ext...)
    :return: An integer which is the error code of the ffmpeg termination. If the process is successful
    than 0 will be returned.
    """
    arguments = ["-i", frames_folder+SEPARATOR+frame_name+frame_ext, output_name+ext]
    error_code = utils.run_binary(_ffmpeg(), arguments)
    return error_code


def make_opt_flow(frame1, frame2, output_folder="frames"+SEPARATOR+"flow"):
    """
    This function creates the forward and backward optical flow for the given frames.
    :param frame1: a string containing the first frame path
    :param frame2: a string containing the second frame path
    :param output_folder: a string containing the output folder. It is recommended that the folder should be empty,
    otherwise the flow files wont be created.
    :return: A tuple with the file names of the 2 optical flow files.
    """

    if SYS_PLATFORM == utils.OS.LINUX:
        flow_command_line = "./linux/bin/run-deepflow.sh"
    else:
        return

    # get the file name without extension for the input frames
    frame1_file_name = utils.get_base_name(frame1)
    frame2_file_name = utils.get_base_name(frame2)

    # get the output file name for the .flo files
    forward_flow = output_folder + SEPARATOR + frame1_file_name + "_" + frame2_file_name + "_forward.flo"
    backward_flow = output_folder + SEPARATOR + frame1_file_name + "_" + frame2_file_name + "_backward.flo"

    # check if the forward .flo file exists. If not, then compute it.
    if not utils.file_exists(forward_flow):
        args_forward = [frame1, frame2, forward_flow]
        print("Creating forward optical flow for frames: " + frame1_file_name + " and " + frame2_file_name + "...")
        utils.run_binary(flow_command_line, args_forward)

    # check if the backward .flo file exists. If not, then compute it.
    if not utils.file_exists(backward_flow):
        args_backward = [frame2, frame1, backward_flow]
        print("Creating backward optical flow for frames: " + frame1_file_name + " and " + frame2_file_name + "...")
        utils.run_binary(flow_command_line, args_backward)

    # run the consistency for both .flo files
    return forward_flow, backward_flow,\
           _run_consistency_check(forward_flow, backward_flow, output_folder),\
           _run_consistency_check(backward_flow, forward_flow, output_folder)


def _run_consistency_check(forward_flow, backward_flo, output_folder="frames"+SEPARATOR+"flow"):
    """
    Runs the consistencyChecker for the forward and backward .flo files.
    :param forward_flow: A string with the path of the first .flo file
    :param backward_flo: A string with the path of the second .flo file
    :param output_folder: Optional - A String withe path of the output folder.
    :return: A string with filename created.
    """
    file_name = utils.get_base_name(forward_flow) + "_reliable.txt"
    print("Running consistency for " + file_name + "...")
    if not utils.file_exists(file_name):
        if SYS_PLATFORM == utils.OS.LINUX:
            command = "./linux/bin/consistencyChecker"
        else:
            return

        arguments = [forward_flow, backward_flo, output_folder+SEPARATOR+file_name]
        utils.run_binary(command, arguments)
        return output_folder+file_name
