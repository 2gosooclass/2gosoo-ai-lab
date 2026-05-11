# 💎 GOSOO SHORTS SNIPER - IMPERIAL EDITION v1.0

> **Capture the Moment, Rule the Algorithm.**  
> 유튜브 영상 URL 단 하나로 제국의 쇼츠 군단을 무한 사출하십시오.

본 프로젝트는 **FastAPI(Python Backend)**와 **Remotion(React-based Video Render Engine)**을 융합하여, AI가 스스로 영상의 최고 바이럴 구간을 분석 및 도출하고 고품질 9:16 규격의 쇼츠 영상을 자동 자막과 함께 실시간 물리 사출하는 최고존엄 알고리즘 지배 도구입니다.

---

## ⚡ 핵심 기능 (Key Features)

*   **🧠 Gemini AI 바이럴 분석 예측 엔진**: 동영상의 제목과 컨텍스트를 분석하여, 조회수를 최대화할 수 있는 후킹 바이럴 세그먼트 3개 및 가상 virality 스코어 자동 계산.
*   **🎬 Remotion 기반 실시간 영상 합성**: React 기반 비디오 제작 프레임워크인 Remotion을 내재하여 자막, 워터마크, 템플릿 효과를 헤드리스 크로미움(Headless Chromium) 환경에서 동적 오버레이 및 인코딩.
*   **⚙️ 하이브리드 미디어 파이프라인**: `yt-dlp`를 통한 영상의 핵심 키프레임 무손실 분할 다운로드 및 `FFmpeg` 720p 30fps 초고속 트랜스코딩 연동 최적화.
*   **💎 Imperial Cyberpunk UI**: 미래지향적 다크 테마 글래스모피즘(Glassmorphism) 및 골드 네온 임페리얼 무드의 환상적인 웹 인터페이스 제공.

---

## 🛠️ 기술 스택 (Tech Stack)

*   **Backend:** FastAPI (Python 3.10+), Uvicorn, Requests
*   **Frontend:** Vanilla JS, CSS3 (Glassmorphism design, CSS Variables)
*   **Video Engine:** Remotion (React, Node.js), yt-dlp, FFmpeg
*   **AI Model:** Google Gemini 2.5 Flash API

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1. 전제 조건 설치
프로젝트 구동을 위해 다음 네이티브 도구들이 설치되어 있어야 합니다 (macOS Apple Silicon 권장):
```bash
# Homebrew를 통한 yt-dlp 및 FFmpeg 설치
brew install yt-dlp ffmpeg
```

### 2. 가상환경 설정 및 패키지 설치
```bash
# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 종속 패키지 설치
pip install fastapi uvicorn requests python-dotenv
```

### 3. API 키 설정
프로젝트 루트 폴더 혹은 실행 폴더에 `.env` 파일을 생성하고 아래 자격을 입력합니다.
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. 로컬 서버 가동
```bash
# 백엔드 서버 가동 (analyzer.py)
python3 analyzer.py
```
서버 가동 후 브라우저에서 `http://localhost:8000/sniper/`로 접속하여 임페리얼 스나이퍼 관제 패널을 제어합니다.

---

## 🛡️ 보안 및 안전 주의사항
*   본 오픈소스 리포지토리는 API 키 노출 방지를 위한 완벽한 `.gitignore`가 사전 설계되어 안전합니다.
*   실행 시 반드시 로컬 `.env` 혹은 시스템 환경변수를 구성해 주십시오.

---

## ⚖️ License
본 프로젝트는 **2GOSOO AI LAB - Imperial Automation Division**의 소유이며, 상업적 무단 도용을 지양하고 오픈소스 개발 문화의 발전과 잘난 척을 목적으로 자유로운 포크(Fork) 및 학습을 환영합니다.

---
**© 2026 2GOSOO AI LAB. Directed by 2GOSOO.**
