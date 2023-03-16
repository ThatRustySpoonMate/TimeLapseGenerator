import cv2
import argparse
import os
from os import path
from time_lapse import output, source

print("CONVERTING.")
print("Step 1: |", end='')

# Config
# TODO: Add Arg Parser for (src_file, dst_file, ram/hdd mode, frame_rate, speed_multiplier)
source_file = "./source.mp4" # Input video file
dest_vid_name = "./destination.mp4" # Output video file
speed_multiplier = 1 # TODO: Implement -- Overall multiplier of source video speed to output video speed
hardware_mode = 1 # 0: RAM, 1: HDD
out_frame_rate = 25 # Output frame rate
temp_dir = "./temp/" # Directory to store frames in HDD mode
skip_n_frames = 20 # Keep every n frame from the source video

kept_frame_count = 0
frames = []

# Split video into frames and store them
def FrameCapture(path, skip_n_frames, outfile):
    global kept_frame_count, frames
    step_1_progress = 0

    vidObj = cv2.VideoCapture(path)
    count = 0
    kept_frame_count = 1
    success = 1
    total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

    target_frames = total_frames/skip_n_frames


    #print(f"total frame {total_frames}")
    while success:
        success, image = vidObj.read()
        if count % skip_n_frames == 0:
            # Only keep every n images
            if(hardware_mode == 0):
                frames.append(image)
            else:
                cv2.imwrite(f"{outfile}frame_{kept_frame_count}.jpg", image)
            kept_frame_count +=1

            # Progress bar stuff
            if( (kept_frame_count / target_frames * 100) - step_1_progress > 5):
                step_1_progress = step_1_progress + 5
                print("o", end='')
        count +=1

        
    print("|")
    print("Complete")
    print(f"Created {kept_frame_count} images")

if __name__ == '__main__':
    
    if path.exists(source_file):
        if path.isdir(temp_dir):
            FrameCapture(source_file, skip_n_frames = skip_n_frames, outfile = temp_dir)
        else:
            print("Directory does not exists")
            quit()
    else:
        print("File does not exist")
        quit()

    


    # Step 2: Reconstruct frames into video
    print("Step 2: |", end='')
    step_2_progress = 0

    # Method 2
    img_count = 0

    if(hardware_mode == 0):
        # RAM buffered mode
        first_frame = frames[0]
        height, width, layers = first_frame.shape

        video = cv2.VideoWriter(dest_vid_name, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), out_frame_rate, (width,height))

        for image in frames:
            video.write(image) 
            img_count = img_count + 1

            if( (img_count / kept_frame_count * 100) - step_2_progress > 5):
                    step_2_progress = step_2_progress + 5
                    print("o", end='')


    if(hardware_mode == 1):
        # HDD Buffered mode
        images = [img for img in os.listdir(temp_dir) if img.endswith(".jpg")]
        frame = cv2.imread(os.path.join(temp_dir, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(dest_vid_name,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), out_frame_rate, (width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(temp_dir, image)))
            img_count = img_count + 1

            if( (img_count / kept_frame_count * 100) - step_2_progress > 5):
                    step_2_progress = step_2_progress + 5
                    print("o", end='')


    cv2.destroyAllWindows()
    video.release()

    print("|")
    print("Complete")  
