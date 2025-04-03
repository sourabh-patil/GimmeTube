# import yt_dlp
# import os

# # Function to download YouTube video using yt-dlp
# def download_youtube_video(url, output_path):
#     ydl_opts = {
#         'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Ensures best quality
#         'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Saves file in output_path
#         'merge_output_format': 'mp4',  # Ensures merged video is in MP4 format
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=True)
#         video_filename = info_dict['requested_downloads'][0]['filepath']  # Correctly fetches saved filename
#         return video_filename

# # URL of the YouTube video
# youtube_url = "https://www.youtube.com/watch?v=Nl3qsm16iTM"
# output_path = './'  # Directory where the video will be saved

# # Download the video
# video_filename = download_youtube_video(youtube_url, output_path)

# print(f"Video downloaded successfully:\nVideo Path: {video_filename}")


################################

# import subprocess
# import os

# def extract_frames_and_save_timestamps(input_video, frames_per_minute):
#     # Get video length using ffprobe (ffmpeg's metadata tool)
#     command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_video]
#     video_length = float(subprocess.check_output(command).decode("utf-8").strip())  # Video length in seconds
    
#     # Calculate time intervals based on the number of frames per minute
#     total_frames = frames_per_minute * (video_length // 60)  # Total frames for the entire video
#     time_intervals = [i * (video_length / total_frames) for i in range(int(total_frames))]
    
#     # Create output directory for frames if not exists
#     output_dir = "/home/spatil2/sentinel_llama_3.2/output_frames"
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     # Create a file to store timestamps for cropping later
#     timestamp_file = "timestamps.txt"
    
#     with open(timestamp_file, "w") as file:
#         # Extract frames at each timestamp
#         for timestamp in time_intervals:
#             # Format the timestamp to HH:MM:SS
#             hours = int(timestamp // 3600)
#             minutes = int((timestamp % 3600) // 60)
#             seconds = int(timestamp % 60)
#             formatted_time = f"{hours:02d}_{minutes:02d}_{seconds:02d}"
            
#             # Construct the output filename with timestamp
#             output_filename = os.path.join(output_dir, f"frame_{formatted_time}.jpg")
            
#             # Extract the frame at the current timestamp
#             command = [
#                 "ffmpeg", "-i", input_video, "-ss", str(timestamp), "-vframes", "1", "-q:v", "2", output_filename
#             ]
            
#             subprocess.run(command, check=True)
#             print(f"Frame saved at {formatted_time} as {output_filename}")
            
#             # Save timestamp to file for cropping later
#             file.write(f"{timestamp}\n")

#     print(f"All frames extracted successfully! Timestamps saved to {timestamp_file}")

# # Example usage:
# input_video = "input_video.mp4"  # Replace with your input video path
# frames_per_minute = 5  # Define how many frames you want per minute
# extract_frames_and_save_timestamps(input_video, frames_per_minute)


##########################################

# import yt_dlp

# # Function to download subtitles
# def download_subtitles(video_url, lang="en", save_path="subtitles.srt"):
#     ydl_opts = {
#         "writesubtitles": True,  # Enable subtitle download
#         "subtitleslangs": [lang],  # Language of subtitles
#         "subtitlesformat": "srt",  # Save in SRT format
#         "skip_download": True,  # Don't download the video, only subtitles
#         "outtmpl": save_path  # Output file
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#         print(f"Subtitles downloaded and saved as: {save_path}")

# # Example Usage
# video_url = "https://www.youtube.com/watch?v=Nl3qsm16iTM"  # Replace with actual video URL
# download_subtitles(video_url, lang="en", save_path="video_subtitles.srt")

######################################

###################### merge subtitles 

# import re
# from datetime import timedelta

# def parse_srt(srt_file):
#     with open(srt_file, 'r', encoding='utf-8') as file:
#         content = file.read()
    
#     subtitles = []
#     blocks = re.split('\n\n', content.strip())
    
#     for block in blocks:
#         lines = block.split('\n')
#         if len(lines) < 2:
#             continue
        
#         time_match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
#         if not time_match:
#             continue
        
#         start_time = timedelta(hours=int(time_match[1]), minutes=int(time_match[2]), seconds=int(time_match[3]), milliseconds=int(time_match[4]))
#         end_time = timedelta(hours=int(time_match[5]), minutes=int(time_match[6]), seconds=int(time_match[7]), milliseconds=int(time_match[8]))
        
#         text = ' '.join(lines[2:])
#         subtitles.append((start_time, end_time, text))
    
#     return subtitles

# def merge_subtitles(subtitles, interval=30):
#     merged = []
#     temp_text = []
#     interval_start = None
    
#     for start, end, text in subtitles:
#         if interval_start is None:
#             interval_start = start
        
#         if (start - interval_start).total_seconds() < interval:
#             temp_text.append(text)
#         else:
#             merged.append((interval_start, start, ' '.join(temp_text)))
#             temp_text = [text]
#             interval_start = start
    
#     if temp_text:
#         merged.append((interval_start, start, ' '.join(temp_text)))
    
#     return merged

# def save_merged_subtitles(merged_subs, output_file):
#     with open(output_file, 'w', encoding='utf-8') as file:
#         for start, end, text in merged_subs:
#             file.write(f"{str(start)} --> {str(end)}\n{text}\n\n")

# # Usage
# srt_file = 'ind_vs_pak.srt'  # Replace with your SRT file
# output_file = 'ind_vs_pak_merged.txt'
# subtitles = parse_srt(srt_file)
# merged_subs = merge_subtitles(subtitles, interval=30)
# save_merged_subtitles(merged_subs, output_file)

# print("Merged subtitles saved successfully.")

##################################################


import ffmpeg

# Define input video file
input_video = "ind_vs_pak.mp4"
output_video = "output_fused.mp4"

# List of timestamps
time_stamps = [
    {'end': '0:10:39.300000', 'start': '0:10:06.240000'},
    {'end': '1:09:53.600000', 'start': '1:09:21.299000'},
    {'end': '1:11:59.500000', 'start': '1:11:28.980000'},
    {'end': '1:17:23.500000', 'start': '1:16:50.880000'},
    {'end': '1:17:54.700000', 'start': '1:17:23.520000'},
    {'end': '1:19:01.100000', 'start': '1:18:30.320000'},
    {'end': '1:27:20.200000', 'start': '1:26:49.739000'},
    {'end': '1:34:43.300000', 'start': '1:34:12.179000'},
    {'end': '1:36:49.300000', 'start': '1:36:17.639000'},
    {'end': '1:37:20.800000', 'start': '1:36:49.380000'}
]

# Step 1: Crop video clips
segment_files = []
for i, ts in enumerate(time_stamps):
    start_time = ts['start']
    end_time = ts['end']
    output_segment = f"segment_{i}.mp4"
    
    # Crop the video
    ffmpeg.input(input_video, ss=start_time, to=end_time).output(output_segment, c="copy").run(overwrite_output=True)
    segment_files.append(output_segment)

# Step 2: Create a text file listing all segments for concatenation
concat_file = "concat_list.txt"
with open(concat_file, "w") as f:
    for seg in segment_files:
        f.write(f"file '{seg}'\n")

# Step 3: Concatenate the segments
ffmpeg.input(concat_file, format="concat", safe=0).output(output_video, c="copy").run(overwrite_output=True)

print(f"Final fused video saved as {output_video}")