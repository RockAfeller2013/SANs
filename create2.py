import os
import json

VIDEO_EXTS = {'.mp4', '.webm', '.ogg'}

def scan_videos(base_dir):
    videos = {}
    for root, _, files in os.walk(base_dir):
        rel_dir = os.path.relpath(root, base_dir)
        if rel_dir == '.':
            rel_dir = ''
        vids = [f for f in files if os.path.splitext(f)[1].lower() in VIDEO_EXTS]
        if vids:
            vids.sort(key=lambda x: (try_int(x), x))
            videos[rel_dir] = vids
    return videos

def try_int(filename):
    name = os.path.splitext(filename)[0]
    try:
        return int(name)
    except:
        return 9999999

def generate_html(videos):
    dirs_js = json.dumps(sorted(videos.keys(), key=lambda x: x.lower()))
    videos_js = json.dumps(videos)

    html = f"""<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LMS Video Player</title>

  <!-- Bootstrap 5 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- Google Material Symbols -->
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />

  <!-- Inter Font -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">

  <style>
    body {{
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
      overflow: hidden;
      height: 100vh;
      display: flex;
      background-color: #121212;
      color: #e0e0e0;
    }}
    #sidebar {{
      width: 250px;
      background-color: #1f1f1f;
      overflow-y: auto;
      border-right: 1px solid #333;
    }}
    #sidebar .list-group-item {{
      cursor: pointer;
      border: none;
      background: #1f1f1f;
      color: #e0e0e0;
    }}
    #sidebar .list-group-item:hover {{
      background-color: #2a2a2a;
    }}
    #sidebar .list-group-item.active {{
      background-color: #0d6efd;
      color: white;
    }}
    #main {{
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      padding: 20px;
      overflow-y: auto;
    }}
    video {{
      width: 100%;
      max-height: 65vh;
      background: black;
    }}
    .material-symbols-outlined {{
      vertical-align: middle;
    }}
    .btn-outline-primary {{
      color: #0d6efd;
      border-color: #0d6efd;
    }}
    .btn-outline-primary:hover {{
      background-color: #0d6efd;
      color: white;
    }}
    select.form-select {{
      background-color: #1f1f1f;
      color: #e0e0e0;
      border-color: #333;
    }}
    h5#videoTitle {{
      color: #ffffff;
    }}
  </style>
</head>
<body>

  <div id="sidebar">
    <div class="list-group list-group-flush" id="dirList"></div>
  </div>

  <div id="main">
    <h5 id="videoTitle" class="mb-3">Select a directory</h5>
    <video id="videoPlayer" controls class="mb-3" style="display: none;"></video>

    <div id="controls" class="mb-3" style="display: none;">
      <button class="btn btn-outline-primary me-2" id="prevBtn">
        <span class="material-symbols-outlined">navigate_before</span> Previous
      </button>
      <button class="btn btn-outline-primary" id="nextBtn">
        Next <span class="material-symbols-outlined">navigate_next</span>
      </button>
    </div>

    <div id="speedControl" class="mb-3" style="display: none;">
      <label for="speedSelect" class="form-label">Playback Speed</label>
      <select id="speedSelect" class="form-select" style="width: auto;">
        <option value="0.25">0.25x</option>
        <option value="0.5">0.5x</option>
        <option value="0.75">0.75x</option>
        <option value="1" selected>1x (Normal)</option>
        <option value="1.25">1.25x</option>
        <option value="1.5">1.5x</option>
        <option value="2">2x</option>
      </select>
    </div>
  </div>

  <script>
    const dirs = {dirs_js};
    const videos = {videos_js};

    const dirListEl = document.getElementById('dirList');
    const videoPlayer = document.getElementById('videoPlayer');
    const videoTitle = document.getElementById('videoTitle');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const controls = document.getElementById('controls');
    const speedControl = document.getElementById('speedControl');
    const speedSelect = document.getElementById('speedSelect');

    let currentDir = null;
    let currentIndex = 0;

    function clearActive() {{
      document.querySelectorAll('#dirList .list-group-item').forEach(el => el.classList.remove('active'));
    }}

    function loadDirectory(dir) {{
      currentDir = dir;
      currentIndex = 0;
      clearActive();
      const activeItem = document.querySelector(`#dirList .list-group-item[data-dir="${dir}"]`);
      if (activeItem) activeItem.classList.add('active');

      if (!videos[dir] || videos[dir].length === 0) {{
        videoTitle.textContent = 'No videos in this directory.';
        videoPlayer.style.display = 'none';
        controls.style.display = 'none';
        speedControl.style.display = 'none';
        return;
      }}

      videoPlayer.style.display = 'block';
      controls.style.display = 'flex';
      speedControl.style.display = 'block';
      playVideo(currentIndex);
    }}

    function playVideo(index) {{
      const videoFiles = videos[currentDir];
      if (!videoFiles || videoFiles.length === 0) return;
      if (index < 0 || index >= videoFiles.length) return;
      currentIndex = index;

      const src = currentDir ? (currentDir + '/' + videoFiles[index]) : videoFiles[index];
      videoPlayer.src = src;
      videoPlayer.playbackRate = parseFloat(speedSelect.value);
      videoTitle.textContent = (currentDir || 'Root') + ' / ' + videoFiles[index];
      videoPlayer.play();
    }}

    prevBtn.onclick = () => {{
      if (currentIndex > 0) playVideo(currentIndex - 1);
    }};

    nextBtn.onclick = () => {{
      if (currentIndex < videos[currentDir].length - 1) playVideo(currentIndex + 1);
    }};

    videoPlayer.onended = () => {{
      if (currentIndex < videos[currentDir].length - 1) playVideo(currentIndex + 1);
    }};

    speedSelect.onchange = () => {{
      videoPlayer.playbackRate = parseFloat(speedSelect.value);
    }};

    dirs.forEach(dir => {{
      const item = document.createElement('button');
      item.className = 'list-group-item list-group-item-action';
      item.textContent = dir || '(root)';
      item.dataset.dir = dir;
      item.onclick = () => loadDirectory(dir);
      dirListEl.appendChild(item);
    }});
  </script>

</body>
</html>
"""
    return html

if __name__ == "__main__":
    base_dir = os.getcwd()
    videos = scan_videos(base_dir)
    html = generate_html(videos)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html generated successfully (dark mode).")
