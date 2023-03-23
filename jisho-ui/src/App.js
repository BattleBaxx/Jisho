import "./App.css";
import { useState } from "react";
import { request } from "./request";

function App() {
  const [searchQuery, setSearchQuery] = useState("");
  const [queryResult, setQueryResult] = useState({ doc_list: [] });

  const [extension, setExtension] = useState("all");
  const [folder, setFolder] = useState("");

  const [minSize, setMinSize] = useState(null);
  const [maxSize, setMaxSize] = useState(null);

  const [minTime, setMinTime] = useState(null);
  const [maxTime, setMaxTime] = useState(null);

  const supportedExtensionList = [".txt", "jpeg", ".png", ".jpg", ".ppm", ".tiff", ".bmp", ".docx", ".pdf"];

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      // 👇 Get input value
      console.log("Search query is: ", searchQuery);
      console.log(extension);
      const options = {};
      if (extension !== "all") {
        options.extension = extension;
      }
      if (folder.trim().length !== 0) {
        options.file_location = folder;
      }
      if (minSize) {
        options.min_size = minSize;
      }
      if (maxSize) {
        options.max_size = maxSize;
      }
      if (minTime) {
        options.start_time = minTime;
      }
      if (maxTime) {
        options.end_time = maxTime;
      }
      console.log(options);
      request({ query: searchQuery, ...options }).then((result) => {
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
      <div id="filter-container">
        <div id="filter-box">
          <img src="filter.png" width="70" />
          <div>
            <label>Extension</label>
            <select value={extension} onChange={(event) => setExtension(event.target.value)}>
              <option value="all"> All </option>
              {supportedExtensionList.map((value, index) => {
                return <option value={value}> {value} </option>;
              })}
            </select>
          </div>
          <div>
            <label>Folder</label>
            <input
              type="text"
              id="folder-filter-input"
              value={folder}
              onChange={(event) => setFolder(event.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>
          <div>
            <label>Min Size</label>
            <input
              type="number"
              id="min-size-input"
              value={minSize}
              onChange={(event) => setMinSize(event.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>
          <div>
            <label>Max Size</label>
            <input
              type="number"
              id="max-size-input"
              value={maxSize}
              onChange={(event) => setMaxSize(event.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>
          <div>
            <label>Modified After</label>
            <input
              type="datetime-local"
              id="min-mod"
              value={minTime}
              onChange={(event) => setMinTime(event.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>
          <div>
            <label>Modified Before</label>
            <input
              type="datetime-local"
              id="max-mod"
              value={maxTime}
              onChange={(event) => setMaxTime(event.target.value)}
              onKeyDown={handleKeyDown}
            />
          </div>
        </div>
      </div>
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
