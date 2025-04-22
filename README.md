# GimmeTube

https://github.com/user-attachments/assets/02debe23-2ff6-44b4-b82d-91b9474a1c27

# 🏏 Automated Sports Highlight Generator

This project allows you to generate highlight videos based on natural language queries using a full match video and its subtitle file (SRT). It's built to work best with sports videos that have high-quality, manually created commentary subtitles.

---

## 📌 Steps Followed

1. **Select a sports video** with detailed commentary and a corresponding `.srt` file that includes timestamps.  
   ⚠️ Avoid auto-generated `.srt` files as they tend to have many transcription errors.  
   _Example used: India vs Pakistan, T20 World Cup 2022 (1.5-hour video)._

2. **Split the commentary** into 30-second chunks and store them in a vector database using embeddings.

3. **Enter a query** (e.g., “Kohli’s sixes” or “last over wickets”). Relevant commentary chunks and their timestamps are retrieved from the vector DB.

4. **Rerank the results** to ensure the most relevant and high-quality segments are selected.

5. **Trim and stitch** the original video using the selected timestamps to create a highlight video.

---

## 🛠️ How to Run

### Backend

```bash
uvicorn main:app --host 0.0.0.0 --reload --port 8777
```

### Frontend

```bash
npm run dev
```

### View

1. Open the URL exposed by the frontend (e.g., `http://localhost:3000`).
2. Type in your query.
3. Wait for the system to generate the fused highlight video.
4. Watch and enjoy your personalized highlight reel!

---

## 🔧 Scope for Improvement

- ✅ **LLM Integration**: Use large language models to refine and spell-check `.srt` files, especially auto-generated ones.
- ✅ **Vision-Language Models**: Incorporate models to extract fine-grained, activity-based details from each video chunk.
- ✅ **Advanced Embeddings**: Use state-of-the-art embedding models (e.g., OpenAI, Cohere, BGE) for improved semantic search.
- ✅ **Better UI/UX**: Enhance the frontend for a smoother and more interactive user experience.
- ✅ **Backend Optimization**: Reduce processing time and eliminate bottlenecks for a more seamless experience.

---

## 💡 Future Possibilities

- 🔍 Create an **intelligent agent** that searches the internet for relevant sports videos based on a user’s query.
- 📅 Automatically download the video, extract subtitles, create embeddings, and suggest highlight segments.
- 📊 Extend to non-sports content like educational lectures, news coverage, or podcasts with video.
- 🤖 Enable dynamic highlight generation with user feedback loops and real-time updates.

---

Enjoy building your own smart video highlight generator! 🚀
