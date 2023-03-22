import "./App.css";
import { useState } from "react";
import { request } from "./request";

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [queryResult, setQueryResult] = useState({ doc_list: [] });

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      // 👇 Get input value
      console.log("Search query is: ", searchQuery);
      request({ query: searchQuery }).then((result) => {
        setQueryResult(result);
        console.log(result);
      });
    }
  };

  const getFileIconClass = (extension) => {
    switch (extension) {
      case ".txt":
        return "fa fa-file-text-o";
      case ".jpeg":
      case ".png":
      case ".jpg":
      case ".ppm":
      case ".tiff":
      case ".bmp":
        return "fa fa-file-image-o";
      case ".docx":
        return "fa fa-file-word-o";
      case ".pdf":
        return "fa fa-file-pdf-o";
      default:
        return "fa fa-file-text-o";
    }
  };

  const parseLocation = (location) => {
    return location.substring(1).replaceAll("/", " > ");
  };

  return (
    <div className="App">
      <div className="container">
        <br />
        <br />
        <div>
          <img src="logo2.png" height="200" />
        </div>
        <br />
        <br />
        <div className="search-box">
          <button className="btn-search" onSubmit={request}>
            <i className="fas fa-search"></i>
          </button>
          <input
            type="text"
            class="input-search"
            value={searchQuery}
            onChange={(event) => setSearchQuery(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type to Search..."
          />
        </div>
        <div id="query-results">
          {queryResult.doc_list.map((resp, index) => {
            return (
              <div class="cards">
                <div class="cards-image">
                  <i className={getFileIconClass(resp.file_extension)}></i>
                </div>

                <div class="cards-box">
                  <h1 class="cards-title">
                    {resp.file_name}
                    {resp.file_extension}
                  </h1>

                  <div class="cards-content">
                    <p> {parseLocation(resp.file_location)} </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default App;
