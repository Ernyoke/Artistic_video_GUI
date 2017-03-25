
# launch the script using the following arguments:
# python3 main.py input_image style_image1 [style_image2 ...] -i number_of_iterations
# example: python3 main.py images/girl.jpg images/style.jpg -i 100

from artistic_video.artistic_image import create_image
import numpy as np
import scipy.misc
from artistic_video.image import imread, imsave
from artistic_video.video import convert_to_frames, convert_to_video, make_opt_flow
from artistic_video.utils import get_input_type, InputType


def stylize(network_path,
            content_image_path,
            style_images_path,
            output_path,
            iterations,
            content_weight,
            style_weight,
            tv_veight,
            temporal_veight,
            learning_rate,
            use_deepflow=False):
    frame = np.zeros([1, 1, 1], dtype=np.float)
    frame_list = []

    # read the input image
    content_type = get_input_type(content_image_path)
    if content_type == InputType.IMAGE:
        frame = imread(content_image_path)
    elif content_type == InputType.VIDEO:

        # try to cut the video intro frames
        error_code, frame_list = convert_to_frames(content_image_path, 'frames', '.png')
        frame = imread(frame_list[0])

        if error_code == 0:

            # try to create the optical flow for every frame
            use_deep_flow = False
            if use_deep_flow:
                forward_flow_list = {}
                backward_flow_list = {}
                forward_consistency_list = {}
                backward_consistency_list = {}
                for i in range(0, len(frame_list)-1):
                    forward_flow, backward_flow, forward_consistency, backward_consistency\
                        = make_opt_flow(frame_list[i], frame_list[i+1])
                    forward_flow_list[frame_list[i]] = forward_flow
                    backward_flow_list[frame_list[i]] = backward_flow
                    forward_consistency_list[frame_list[i]] = forward_consistency
                    backward_consistency_list[frame_list[i]] = backward_consistency

        else:
            print("Exited with ffmpeg error code: ", error_code)
            return

    # read the style images
    style_images = []
    for style_image in style_images_path:
        style_images.append(imread(style_image))

    content_shape = frame.shape
    for i in range(len(style_images)):
        style_scale = 1.0

        # resize style images
        style_images[i] = scipy.misc.imresize(style_images[i], style_scale *
                                              content_shape[1] / style_images[i].shape[1])

    if content_type == InputType.IMAGE:
        print("Stylizing image", content_image_path)
        for iteration, image in create_image(
                network_path=network_path,
                content_image=frame,
                styles_images=style_images,
                iterations=iterations,
                content_weight=content_weight,
                style_weight=style_weight,
                tv_weight=tv_veight,
                learning_rate=learning_rate,
                use_deepflow=False
        ):
            imsave(output_path + str('out.jpg') + '.jpg', image)

    elif content_type == InputType.VIDEO:
        for index, frame_name in enumerate(frame_list):
            print('Stylizing frame', frame_name)
            frame = imread(frame_name)
            if index == 0:
                for iteration, image in create_image(
                        network_path=network_path,
                        content_image=frame,
                        styles_images=style_images,
                        iterations=iterations,
                        content_weight=content_weight,
                        style_weight=style_weight,
                        tv_weight=tv_veight,
                        learning_rate=learning_rate,
                        use_deepflow=False
                ):
                    imsave(output_path + str(index) + '.jpg', image)
            else:
                prev_frame_name = frame_list[index - 1]
                current_backward_flow = backward_flow_list[frame_name]
                current_forward_consistency = forward_consistency_list[frame_name]
                for iteration, image in create_image(
                        network_path=network_path,
                        content_image=frame,
                        styles_images=style_images,
                        iterations=iterations,
                        content_weight=content_weight,
                        style_weight=style_weight,
                        tv_weight=tv_veight,
                        learning_rate=learning_rate,
                        use_deepflow=True,
                        prev_frame=prev_frame_name,
                        backw_flow_path=current_backward_flow,
                        forw_cons_path=current_forward_consistency
                ):
                    imsave(output_path + str(index) + '.jpg', image)
        # convert_to_video("output_ffmpeg", ".mp4", "frames")

