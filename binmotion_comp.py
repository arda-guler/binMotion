import numpy as np
import cv2
import os
import sys

IGNORE_FILES = ['binmotion_raw.py', 'binmotion_comp.py',
                'output_compressed.mp4', 'output_raw.avi']

def read_video_frames_from_file(x, y, filename):
    total_pixels_per_frame = x * y

    # binary mode reading
    with open(filename, 'rb') as f:
        frames = []
        
        while True:
            frame_data = f.read(total_pixels_per_frame * 3)
            if not frame_data:
                break
            
            frame = np.zeros((y, x, 3), dtype=np.uint8)
            
            for i in range(0, len(frame_data), 3):
                pixel_index = i // 3
                row = pixel_index // x
                col = pixel_index % x
                
                r = frame_data[i]
                g = frame_data[i+1] if i+1 < len(frame_data) else 0
                b = frame_data[i+2] if i+2 < len(frame_data) else 0
                
                frame[row, col] = [r, g, b]
            
            frames.append(frame)
    
    return frames

def read_video_frames_from_directory(x, y):
    directory = os.getcwd()
    all_files = sorted(f for f in os.listdir(directory) if os.path.isfile(f) and f not in IGNORE_FILES)

    all_frames = []
    total_files = len(all_files)
    for i, filename in enumerate(all_files):
        print(f"Processing file: {filename}")
        
        frames = read_video_frames_from_file(x, y, filename)
        num_frames = len(frames)
        
        all_frames.extend(frames)
        
##        for j, frame in enumerate(frames):
##            progress = (j + 1) / num_frames * 100
##            print(f"Writing file: {filename}. Progress: {progress:.2f}%")
    
    return all_frames

def export_video(frames, x, y, output_filename, fps=30):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (x, y))

    for frame in frames:
        out.write(frame)

    out.release()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        x = 640
        y = 480

    output_filename = 'output_compressed.mp4'

    frames = read_video_frames_from_directory(x, y)
    export_video(frames, x, y, output_filename)
