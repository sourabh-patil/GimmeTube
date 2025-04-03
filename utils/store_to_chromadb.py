import chromadb
import re
from datetime import timedelta

def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    chunks = []
    blocks = re.split('\n\n', content.strip())
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 2:
            continue
        
        time_match = re.match(r'(\d{1,2}):(\d{2}):(\d{2}\.\d+?) --> (\d{1,2}):(\d{2}):(\d{2}\.\d+?)', lines[0])
        if not time_match:
            continue
        
        start_time = timedelta(hours=int(time_match[1]), minutes=int(time_match[2]), seconds=float(time_match[3]))
        end_time = timedelta(hours=int(time_match[4]), minutes=int(time_match[5]), seconds=float(time_match[6]))
        
        text = ' '.join(lines[1:]).strip()
        chunks.append((str(start_time), str(end_time), text))
    
    return chunks


def store_in_chromadb(chunks):
    client = chromadb.PersistentClient(path="chroma_db")  # Persistent storage
    collection = client.get_or_create_collection(name="subtitles")
    
    for i, (start, end, text) in enumerate(chunks):
        metadata = {"start": start, "end": end}
        collection.add(documents=[text], metadatas=[metadata], ids=[str(i)])
    
    print("Chunks stored successfully in ChromaDB.")



### Usage 

# file_path = 'ind_vs_pak_merged.txt'  # Replace with your text file
# chunks = parse_txt(file_path)
# store_in_chromadb(chunks)