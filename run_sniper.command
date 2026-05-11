#!/bin/bash

# 1. 2GOSOO SHORTS SNIPER 실행 스크립트
# 스크립트가 위치한 디렉토리로 이동
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "========================================="
echo "💎 GOSOO SHORTS SNIPER - IMPERIAL STARTING..."
echo "========================================="

# 2. 가상환경 활성화 (존재하는 경우)
if [ -f "../../.venv/bin/activate" ]; then
    echo "[+] Activating Virtual Environment..."
    source "../../.venv/bin/activate"
else
    echo "[-] Warning: Virtual environment not found at ../../.venv"
fi

# 3. 브라우저에서 서비스 페이지 자동 열기
echo "[+] Opening Browser to http://localhost:8000..."
open "http://localhost:8000"

# 4. FastAPI 백엔드 서버 가동
echo "[+] Starting FastAPI backend server..."
python3 analyzer.py
