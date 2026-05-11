import os
# Inject Homebrew path for macOS Apple Silicon environment to resolve yt-dlp/ffmpeg dependencies
os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", "")

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
from fastapi.staticfiles import StaticFiles
import requests
import re
import threading

from fastapi.responses import RedirectResponse

app = FastAPI(title="GOSOO SHORTS SNIPER API")

@app.get("/")
async def root():
    return RedirectResponse(url="/sniper/")

# Dynamically load the correct active Gemini API Key
try:
    from dotenv import load_dotenv
    load_dotenv()  # Try local directory first
    load_dotenv("/Users/2gosoo/Documents/2GOSOO_AI_LAB/.env")  # Fallback to main workspace env
except ImportError:
    pass

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in the environment or .env file.")

GEMINI_MODEL = "gemini-2.5-flash" # High-speed model for 2026 lab
REMOTION_DIR = "/Users/2gosoo/Documents/2GOSOO_AI_LAB/01_APP_BUILD/02_REMOTION"
OUTPUT_DIR = "/Users/2gosoo/Documents/2GOSOO_AI_LAB/01_APP_BUILD/09_SNIPER/output"

# Helper to mount static directories only if they exist to prevent RuntimeError on startup
def safe_mount_static(path, mount_name, directory_path):
    if os.path.exists(directory_path):
        app.mount(path, StaticFiles(directory=directory_path, html=True), name=mount_name)
        print(f"[+] Successfully mounted {path} -> {directory_path}")
    else:
        print(f"[-] Warning: Directory '{directory_path}' does not exist. Skipping mount for {path}")

safe_mount_static("/sniper", "sniper", "/Users/2gosoo/Documents/2GOSOO_AI_LAB/01_APP_BUILD/09_SNIPER")
safe_mount_static("/vision", "vision", "/Users/2gosoo/Documents/2GOSOO_AI_LAB/01_APP_BUILD/08_VISION")
safe_mount_static("/suno", "suno", "/Users/2gosoo/Documents/2GOSOO_AI_LAB/03_Platform_WEB/suno_prompt_generator")
safe_mount_static("/global-suno", "global-suno", "/Users/2gosoo/Documents/2GOSOO_AI_LAB/03_Platform_WEB/suno_global_composer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze")
async def analyze_video(url: str):
    """Gemini AI를 사용하여 영상의 바이럴 구간 분석"""
    try:
        # 영상 제목 추출 (간단히)
        cmd = ["/opt/homebrew/bin/yt-dlp", "--print", "%(title)s", "--skip-download", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        title = result.stdout.strip()
        
        print(f"Analyzing video: {title}")

        prompt = f"""
        You are a YouTube Shorts expert. Analyze the following video title and suggest 3 viral clips for YouTube Shorts.
        Video Title: {title}
        URL: {url}

        Instructions:
        1. Suggest 3 distinct segments (start and end times).
        2. Create a "Hooking Title" for each segment in Korean.
        3. Make titles EXTREMELY viral and clickable (using emojis and strong words).
        4. Return ONLY a valid JSON array of objects with keys: "start", "end", "title", "reason", "score".
        5. Do not use generic titles like "Key Insight" or "Closing Impact". Be specific to the content.

        Example Format:
        [
            {{"start": "00:10", "end": "01:00", "title": "핵심 요약 ㄷㄷ", "reason": "...", "score": 95}},
            ...
        ]
        """

        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(api_url, json=payload, timeout=30)
        print(f"Gemini Status: {response.status_code}")
        
        clips = []
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Gemini Response: {text}")
                # JSON 파싱 (마크다운 코드 블록 제거)
                json_str = text.replace("```json", "").replace("```", "").strip()
                clips = json.loads(json_str)

        if not clips or len(clips) < 3:
            print("Fallback to semi-intelligent generic clips due to AI failure")
            clips = [
                {"start": "00:05", "end": "00:55", "title": f"Viral Hook: {title[:20]}...", "reason": "Opening segment", "score": 95},
                {"start": "01:30", "end": "02:15", "title": f"Secret Insight: {title[:20]}...", "reason": "Core value", "score": 88},
                {"start": "03:00", "end": "03:50", "title": f"Must Watch: {title[:20]}...", "reason": "Final summary", "score": 92}
            ]

        return {"title": title, "clips": clips}
    except Exception as e:
        print(f"Analysis error: {e}")
        return {"title": "Error", "clips": []}

@app.post("/render")
async def render_shorts(clip_data: dict):
    print(f"🎬 Rendering Imperial Shorts via Remotion: {clip_data.get('title', 'Unknown')}")
    try:
        url = clip_data.get('url')
        start = clip_data.get('start')
        end = clip_data.get('end')
        title = clip_data.get('title')
        full_screen = clip_data.get('fullScreen', False)
        hide_branding = clip_data.get('hideBranding', False)
        hide_title = clip_data.get('hideTitle', False)
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        final_output_path = os.path.join(OUTPUT_DIR, f"imperial_{safe_title}.mp4")
        
        # 1. We'll use a unique simple temp video path to avoid Remotion/Chromium encoding issues
        import time
        temp_id = int(time.time())
        temp_video_name = f"raw_{temp_id}.mp4"
        temp_video_path = os.path.join(REMOTION_DIR, "public", temp_video_name)
        
        def job():
            try:
                # Step A: Download the raw segment
                print(f"📥 Downloading raw segment: {start}-{end}")
                raw_download_path = temp_video_path + ".raw.mp4"
                subprocess.run(["yt-dlp", "--download-sections", f"*{start}-{end}", "--force-keyframes-at-cuts", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "-o", raw_download_path, url], check=True)
                
                # Transcode to optimized 720p 30fps for headless Chromium performance
                print(f"⚡ Optimizing video for Remotion rendering (720p, 30fps)...")
                subprocess.run([
                    "ffmpeg", "-y", "-i", raw_download_path,
                    "-vf", "scale=-2:720", "-r", "30",
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
                    "-c:a", "aac", "-ar", "44100",
                    temp_video_path
                ], check=True)
                
                if os.path.exists(raw_download_path): os.remove(raw_download_path)
                
                # Step B: Trigger Remotion Render
                print(f"⚙️ Remotion Firing: {final_output_path}")
                props = {
                    "videoSrc": temp_video_name,
                    "title": title,
                    "startFrame": 0,
                    "fullScreen": full_screen,
                    "hideBranding": hide_branding,
                    "hideTitle": hide_title
                }
                props_json = json.dumps(props)
                
                cmd_remotion = [
                    "npx", "remotion", "render", "Imperial-Shorts",
                    final_output_path,
                    "--props", props_json,
                    "--overwrite",
                    "--puppeteer-timeout", "120000"
                ]
                
                subprocess.run(cmd_remotion, cwd=REMOTION_DIR, check=True)
                
                # Step C: Cleanup
                if os.path.exists(temp_video_path): os.remove(temp_video_path)
                print(f"✅ Imperial Shorts Production Complete: {final_output_path}")
                
                # Step D: Auto-copy to MacBook SMB volume if mounted
                macbook_out_dir = "/Volumes/2gosoo/2GOSOO_AI_LAB/09_SHORTS_SNIPER/output"
                if os.path.exists("/Volumes/2gosoo/2GOSOO_AI_LAB"):
                    print(f"📤 Auto-copying rendered video to MacBook SMB: {macbook_out_dir}")
                    os.makedirs(macbook_out_dir, exist_ok=True)
                    import shutil
                    shutil.copy(final_output_path, os.path.join(macbook_out_dir, os.path.basename(final_output_path)))
                    print("✅ MacBook SMB Auto-copy Successful!")
            except Exception as e:
                print(f"❌ Production fail: {e}")

        threading.Thread(target=job).start()
        return {"status": "success", "message": "Cinematic Production started."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
