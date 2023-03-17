import cv2
import argparse
import os
from time_lapse import output, source

print("CONVERTING.")
print("Step 1: |", end="")

# Config
# TODO: Add Arg Parser for (src_file, dst_file, ram/hdd mode, frame_rate, speed_multiplier)
# TODO: Maybe add support for checking expected ram usage given parameters. (Ask to confirm if still go ahead in RAM mode, otherwise, switch to HDD Mode)
source_file_path = "./source.mp4"  # Input video file
dest_vid_name = "./destination.mp4"  # Output video file
speed_multiplier = 20  # Overall multiplier of source video speed to output video speed
hardware_mode = 1  # 0: Direct, 1: RAM, 2: HDD
out_frame_rate = 25  # Desired output frame rate
temp_dir = "./temp/"  # Directory to store frames in HDD mode
skip_n_frames = 1  # Keep every n frame from the source video
src_frame_rate = 60 # TODO: Get Source video frame rate

kept_frame_count = 0
frames = []
first_frame = None


# Split video into frames and store them
def extract_frames_from_source(src_path, skip_n_frames, mode = 1): # mode 1: RAM, mode 2: HDD
    global kept_frame_count, frames, first_frame
    step_1_progress = 0

    vidObj = cv2.VideoCapture(src_path)
    count = 0
    kept_frame_count = 1
    success = 1
    total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

    target_frames = total_frames / skip_n_frames

    # print(f"total frame {total_frames}")
    while success:
        success, image = vidObj.read()

        if(count == 0):
            first_frame = image

        if count % skip_n_frames == 0:
            # Only keep every n images
            if mode == 1:
                frames.append(image)
            elif(mode == 2):
                if os.path.isdir(temp_dir):
                    cv2.imwrite(f"{temp_dir}frame_{kept_frame_count}.jpg", image)
                    frames.append(f"{temp_dir}frame_{kept_frame_count}.jpg")
                else:
                    print(
                        "\nTemp directory does not exist, either create it as 'temp', or re-run program in RAM buffered mode."
                    )
                    quit()

            kept_frame_count += 1

            # Progress bar stuff
            if (kept_frame_count / target_frames * 100) - step_1_progress > 5:
                step_1_progress = step_1_progress + 5
                print("o", end="")
        count += 1


if __name__ == "__main__":

    if not os.path.exists(source_file_path):
        print("Unable to open '{}'\nPlease check the path and try again.".format(source_file_path))
        quit()

    skip_n_frames = int(speed_multiplier * (out_frame_rate / src_frame_rate) )

    if hardware_mode == 0:
        # Direct mode
        step_1_progress = 0

        vidObj = cv2.VideoCapture(source_file_path)

        count = 0
        kept_frame_count = 1
        success = 1
        total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

        target_frames = total_frames / skip_n_frames

        success, image = vidObj.read()
        first_frame = image

    else:
        # RAM or HDD buffered mode
        extract_frames_from_source(source_file_path, skip_n_frames, hardware_mode)

    print("|\nComplete")
    if hardware_mode != 0:
        print(f"Created {kept_frame_count} images")


    # Step 2: Reconstruct frames into video
    print("Step 2: |", end="")
    step_2_progress = 0
    img_count = 0
    height, width, layers = first_frame.shape

    out_video= cv2.VideoWriter(
        dest_vid_name,
        cv2.VideoWriter_fourcc("m", "p", "4", "v"),
        out_frame_rate,
        (width, height),
    )

    if hardware_mode == 0:
        # Direct mode

        while success:
            success, image = vidObj.read()

            if count % skip_n_frames == 0:
                out_video.write(image)

            img_count = img_count + 1

            if (img_count / kept_frame_count * 100) - step_2_progress > 5:
                step_2_progress = step_2_progress + 5
                print("o", end="")


    elif hardware_mode == 1:
        # RAM buffered mode

        for image in frames:
            out_video.write(image)
            img_count = img_count + 1

            if (img_count / kept_frame_count * 100) - step_2_progress > 5:
                step_2_progress = step_2_progress + 5
                print("o", end="")

    elif hardware_mode == 2:
        # HDD Buffered mode
        #frames = [img for img in os.listdir(temp_dir) if img.endswith(".jpg")]

        for image in frames:
            out_video.write(cv2.imread(os.path.join(temp_dir, image)))
            img_count = img_count + 1

            if (img_count / kept_frame_count * 100) - step_2_progress > 5:
                step_2_progress = step_2_progress + 5
                print("o", end="")

    cv2.destroyAllWindows()
    out_video.release()

    print("|\nComplete")
