##################### merge subtitles 

import re
from datetime import timedelta

def parse_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    subtitles = []
    blocks = re.split('\n\n', content.strip())
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 2:
            continue
        
        time_match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})', lines[1])
        if not time_match:
            continue
        
        start_time = timedelta(hours=int(time_match[1]), minutes=int(time_match[2]), seconds=int(time_match[3]), milliseconds=int(time_match[4]))
        end_time = timedelta(hours=int(time_match[5]), minutes=int(time_match[6]), seconds=int(time_match[7]), milliseconds=int(time_match[8]))
        
        text = ' '.join(lines[2:])
        subtitles.append((start_time, end_time, text))
    
    return subtitles

def merge_subtitles(subtitles, interval=30):
    merged = []
    temp_text = []
    interval_start = None
    
    for start, end, text in subtitles:
        if interval_start is None:
            interval_start = start
        
        if (start - interval_start).total_seconds() < interval:
            temp_text.append(text)
        else:
            merged.append((interval_start, start, ' '.join(temp_text)))
            temp_text = [text]
            interval_start = start
    
    if temp_text:
        merged.append((interval_start, start, ' '.join(temp_text)))
    
    return merged

def save_merged_subtitles(merged_subs, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for start, end, text in merged_subs:
            file.write(f"{str(start)} --> {str(end)}\n{text}\n\n")

# Usage
######################################################
# srt_file = 'ind_vs_pak.srt'  # Replace with your SRT file
# output_file = 'ind_vs_pak_merged.txt'
# subtitles = parse_srt(srt_file)
# merged_subs = merge_subtitles(subtitles, interval=30)
# save_merged_subtitles(merged_subs, output_file)

# print("Merged subtitles saved successfully.")

#################################################

