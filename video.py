import os
import cv2
from moviepy.editor import *
import numpy as np

def create_video(image_folder, output_video, audio_file, width=720, height=1280):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()

    frame_rate = 1  # Number of frames per second
    images_duration = len(images) / frame_rate  # Calculate total duration of images

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video, fourcc, frame_rate, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)

        # Calculate dimensions to fit the image within the video frame without resizing
        frame_height, frame_width, _ = frame.shape
        scale_w = width / frame_width
        scale_h = height / frame_height
        scale = min(scale_w, scale_h)

        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)

        # Calculate position to center the image in the video frame
        x_offset = int((width - new_width) / 2)
        y_offset = int((height - new_height) / 2)

        # Resize the image to fit within the video frame
        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Create a black frame of video size
        video_frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Place the resized image onto the black frame to fit the video dimensions
        video_frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_frame

        video.write(video_frame)

    cv2.destroyAllWindows()
    video.release()

    # Create a video clip from the generated video
    video_clip = VideoFileClip(output_video)

    # Trim the audio duration to match the duration of the images
    audio_clip = AudioFileClip(audio_file)
    audio_clip = audio_clip.set_duration(images_duration)

    # Combine the video clip with the adjusted audio clip
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac')
    final_clip.close()

if __name__ == "__main__":
    image_folder_path = "/Users/flavio.mendes/Downloads/Trilha.info/Identidade Visual/LOGO/PNG"
    output_video_path = "video.mp4"
    audio_file_path = "/Users/flavio.mendes/Downloads/OneRepublic - Counting Stars.mp3"

    create_video(image_folder_path, output_video_path, audio_file_path, width=720, height=1280)