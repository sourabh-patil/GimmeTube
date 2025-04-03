from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import os
import ffmpeg
from fastapi.middleware.cors import CORSMiddleware
from flashrank import Ranker, RerankRequest
import chromadb
import yaml
from datetime import timedelta

with open('app_config.yaml') as f:
    config = yaml.safe_load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.10.0.207:5173"],  # Only allow React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# # Simulating a function that returns video timestamps based on a query
# def process_query(query):
#     return [{"start": "00:00:10", "end": "00:00:15"}, {"start": "00:01:00", "end": "00:01:05"}]





# # Function to extract video segments and merge them
# def crop_and_fuse_video(time_stamps, input_video="/media/HDD4TB1/sourabh/gimme_my_stuff/data/video_inputs/ind_vs_pak.mp4", output_video="output.mp4"):
#     segment_files = []
    
#     # Extract each segment using FFmpeg
#     for i, ts in enumerate(time_stamps):
#         start, end = ts["start"], ts["end"]
#         segment_file = f"segment_{i}.mp4"
#         ffmpeg.input(input_video, ss=start, to=end).output(segment_file, c="copy").run(overwrite_output=True)
#         segment_files.append(segment_file)

#     # Create a file list for merging
#     with open("concat.txt", "w") as f:
#         for seg in segment_files:
#             f.write(f"file '{seg}'\n")

#     # Merge the segments
#     ffmpeg.input("concat.txt", format="concat", safe=0).output(output_video, c="copy").run(overwrite_output=True)
#     return output_video




def crop_and_fuse_video(time_stamps, input_video="/media/HDD4TB1/sourabh/gimme_my_stuff/data/video_inputs/ind_vs_pak.mp4", output_video="output.mp4"):
    """
    Using ffmpeg-python, crop segments from the input_video using each set of timestamps and then concatenate them.
    Returns the filename of the fused output video.
    """
    segment_files = []
    # Step 1: Crop video segments for each timestamp entry
    for i, ts in enumerate(time_stamps):
        start_time = ts['start']
        end_time = ts['end']
        output_segment = f"segment_{i}.mp4"
        try:
            # Crop using input's ss (start) and to (end) with stream copy (no re-encode)
            ffmpeg.input(input_video, ss=start_time, to=end_time).output(output_segment, c="copy").run(overwrite_output=True)
            segment_files.append(output_segment)
        except Exception as e:
            print('ERROR in segmenting video')
    
    if not segment_files:
        print("No segments found")
        return None

    # Step 2: Write a concat file listing all segments
    concat_file = "concat_list.txt"
    with open(concat_file, "w") as f:
        for seg in segment_files:
            f.write(f"file '{seg}'\n")
    
    # Step 3: Concatenate the segments into the final video
    try:
        #ffmpeg.input(concat_file, format="concat", safe=0).output(output_video, c="copy").run(overwrite_output=True)
        ffmpeg.input(concat_file, format="concat", safe=0).output(output_video, vcodec="libx264", acodec="aac").run(overwrite_output=True)

    except Exception as e:
        print('ERROR in joining segments')
        return None
    
    return output_video







##############################
# Helper Functions
##############################

def search_similar_chunks(query, top_k=10):
    """
    Perform similarity search on subtitles collection.
    """
    client = chromadb.PersistentClient(path=config.get('DB_PATH'))
    collection = client.get_collection(name=config.get('COLLECTION_NAME'))
    results = collection.query(query_texts=[query], n_results=top_k)
    return results

def time_to_seconds(time_str):
    """
    Convert timestamp string 'H:M:S.sss...' into a timedelta.
    """
    h, m, s = map(float, time_str.split(':'))
    return timedelta(hours=int(h), minutes=int(m), seconds=s)

def process_query(query):
    """
    Run similarity search and flashrank reranking on the query.
    Then sort the passages by their 'start' timestamp.
    Returns a list of dictionaries that have keys 'start' and 'end' inside the 'meta' field.
    """
    results = search_similar_chunks(query, top_k=20)
    print(f"QUERY : {query}")

    # Build list of passages with meta and text information
    passages = [
        {"id": idx, "text": doc, "meta": meta}  
        for idx, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]))
    ]
    
    # Rerank the passages using flashrank
    ranker = Ranker()
    rerank_request = RerankRequest(query=query, passages=passages)
    reranked_results = ranker.rerank(rerank_request)
    
    # Sort the passages by the 'start' timestamp in meta
    sorted_data = sorted(reranked_results[:5], key=lambda x: time_to_seconds(x['meta']['start']))
    
    print(f'RERANKED AND SORTED RESULTS : \n\n\n')

    for curr in sorted_data:
        print(curr['text'])
        print(curr['meta'])
    # Extract only the meta field (assuming meta contains 'start' and 'end')
    time_stamps = [item['meta'] for item in sorted_data]
    return time_stamps




# API Endpoint: Process query and return processed video URL
@app.post("/process/")
async def process(query: str = Form(...)):
    try:
        time_stamps = process_query(query)
        final_video = crop_and_fuse_video(time_stamps)
        return {"video_url": f"/video/{final_video}"}
    except Exception as e:
        return {"error": str(e)}

# API Endpoint: Serve the processed video file
VIDEO_PATH = os.path.abspath("output.mp4")  # Get full path

@app.get("/video/{filename}")
async def get_video(filename: str):
    if filename != "output.mp4":
        return {"error": "Invalid filename"}, 400

    if os.path.exists(VIDEO_PATH):
        return FileResponse(VIDEO_PATH, media_type="video/mp4")

    return {"error": "File not found"}, 404

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)
