import { useState } from "react";

function App() {
    const [query, setQuery] = useState("");
    const [videoUrl, setVideoUrl] = useState("");

    // const handleSubmit = async (e) => {
    //     e.preventDefault();
    //     const formData = new FormData();
    //     formData.append("query", query);

    //     // Send request to FastAPI backend
    //     const response = await fetch("http://172.10.0.207:8765/process/", {
    //         method: "POST",
    //         body: formData,
    //     });

    //     const data = await response.json();
    //     if (data.video_url) {
    //         setVideoUrl("http://172.10.0.207:8765" + data.video_url);
    //     } else {
    //         alert(data.error);
    //     }
    // };

    const handleSubmit = async (e) => {
      e.preventDefault();
      const formData = new FormData();
      formData.append("query", query);
  
      const response = await fetch("http://172.10.0.207:8765/process/", {
          method: "POST",
          body: formData,
      });
  
      const data = await response.json();
      if (data.video_url) {
          console.log("Video URL received:", data.video_url);
          setVideoUrl(`http://172.10.0.207:8765${data.video_url}`);  // Corrected URL
      } else {
          alert(data.error);
      }
  };
  


    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h2>Video Search & Processing</h2>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter query"
                style={{ padding: "10px", margin: "10px" }}
            />
            <button onClick={handleSubmit} style={{ padding: "10px" }}>
                Process
            </button>
            {videoUrl && (
                <div>
                    <h3>Processed Video</h3>
                    <video controls width="600">
                        <source src={videoUrl} type="video/mp4" />
                    </video>
                </div>
            )}
        </div>
    );
}

export default App;
