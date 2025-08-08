import os
import json

VIDEO_EXTS = {'.mp4', '.webm', '.ogg'}

def scan_videos(base_dir):
    """
    Scan base_dir recursively and build a dict:
    {
      "dir_relative_path": [list of video file names sorted],
      ...
    }
    """
    videos = {}
    for root, _, files in os.walk(base_dir):
        rel_dir = os.path.relpath(root, base_dir)
        if rel_dir == '.':
            rel_dir = ''  # root dir as empty string
        vids = [f for f in files if os.path.splitext(f)[1].lower() in VIDEO_EXTS]
        if vids:
            vids.sort(key=lambda x: (try_int(x), x))
            videos[rel_dir] = vids
    return videos

def try_int(filename):
    """Try to extract an integer from filename start for sorting, fallback to large number"""
    name = os.path.splitext(filename)[0]
    try:
        return int(name)
    except:
        return 9999999

def generate_html(videos):
    dirs = sorted(videos.keys(), key=lambda x: x.lower())

    # Escape JS strings (simple)
    def js_escape(s):
        return s.replace('\\','\\\\').replace('"','\\"').replace("'", "\\'")

    # Build directory list JS array
    dirs_js = json.dumps(dirs)
    videos_js = json.dumps(videos)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>LMS Video Player</title>
<style>
  body {{ margin:0; font-family: Arial, sans-serif; display:flex; height:100vh; }}
  #sidebar {{ width: 250px; background: #f0f0f0; overflow-y: auto; border-right: 1px solid #ccc; }}
  #sidebar ul {{ list-style:none; padding:0; margin:0; }}
  #sidebar li {{ padding: 10px; cursor: pointer; border-bottom: 1px solid #ddd; }}
  #sidebar li:hover, #sidebar li.active {{ background: #ddd; }}
  #player {{ flex-grow: 1; padding: 20px; display:flex; flex-direction: column; }}
  #videoTitle {{ margin-bottom: 10px; font-weight: bold; font-size: 18px; }}
  video {{ width: 100%; max-height: 70vh; background: black; }}
  #controls {{ margin-top: 10px; }}
  button {{ padding: 8px 16px; margin-right: 10px; font-size: 16px; cursor: pointer; }}
</style>
</head>
<body>
  <div id="sidebar">
    <ul id="dirList"></ul>
  </div>
  <div id="player">
    <div id="videoTitle">Select a directory</div>
    <video id="videoPlayer" controls></video>
    <div id="controls" style="display:none;">
      <button id="prevBtn">Previous</button>
      <button id="nextBtn">Next</button>
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

  let currentDir = null;
  let currentIndex = 0;

  function clearActive() {{
    [...dirListEl.children].forEach(li => li.classList.remove('active'));
  }}

  function loadDirectory(dir) {{
    currentDir = dir;
    currentIndex = 0;
    clearActive();
    for(let li of dirListEl.children) {{
      if(li.dataset.dir === dir) {{
        li.classList.add('active');
        break;
      }}
    }}
    if (!videos[dir] || videos[dir].length === 0) {{
      videoTitle.textContent = 'No videos in this directory.';
      videoPlayer.style.display = 'none';
      controls.style.display = 'none';
      return;
    }}
    videoPlayer.style.display = 'block';
    controls.style.display = 'block';
    playVideo(currentIndex);
  }}

  function playVideo(index) {{
    const videoFiles = videos[currentDir];
    if (!videoFiles || videoFiles.length === 0) return;
    if(index < 0 || index >= videoFiles.length) return;
    currentIndex = index;
    const src = currentDir ? (currentDir + '/' + videoFiles[index]) : videoFiles[index];
    videoPlayer.src = src;
    videoTitle.textContent = (currentDir || 'Root') + ' / ' + videoFiles[index];
    videoPlayer.play();
  }}

  prevBtn.onclick = () => {{
    if (currentIndex > 0) {{
      playVideo(currentIndex - 1);
    }}
  }};

  nextBtn.onclick = () => {{
    if (currentIndex < videos[currentDir].length - 1) {{
      playVideo(currentIndex + 1);
    }}
  }};

  videoPlayer.onended = () => {{
    if (currentIndex < videos[currentDir].length - 1) {{
      playVideo(currentIndex + 1);
    }}
  }};

  // Build directory list UI
  dirs.forEach(dir => {{
    const li = document.createElement('li');
    li.textContent = dir || '(root)';
    li.dataset.dir = dir;
    li.onclick = () => loadDirectory(dir);
    dirListEl.appendChild(li);
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
    print("index.html generated successfully.")
