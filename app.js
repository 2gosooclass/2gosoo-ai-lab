document.addEventListener('DOMContentLoaded', () => {
    const youtubeInput = document.getElementById('youtube-url');
    const captureBtn = document.getElementById('capture-btn');
    const clipsGrid = document.getElementById('clips-grid');
    const resultChamber = document.getElementById('result-chamber');
    
    // Main Logic
    captureBtn.onclick = async () => {
        const url = youtubeInput.value.trim();
        if (!url) return alert('유튜브 URL을 입력해 주세요, 대표님!');

        setStep(1);
        captureBtn.disabled = true;
        captureBtn.innerHTML = '⚡ CAPTURING...';

        try {
            // 1. Fetching Metadata & Analysis from Mac Mini Backend
            setStep(2);
            const analysis = await analyzeVideo(url);
            
            if (analysis) {
                window.currentClips = analysis;
                renderClips(analysis);
                setStep(3);
                resultChamber.style.display = 'block';
            }
        } catch (e) {
            console.error('Analysis error:', e);
            alert('🚨 Error: ' + e.message);
        } finally {
            captureBtn.disabled = false;
            captureBtn.innerHTML = 'CAPTURE SHORTS 💎';
        }
    };

    function setStep(stepNum) {
        document.querySelectorAll('.step').forEach((s, idx) => {
            if (idx + 1 <= stepNum) s.classList.add('active');
            else s.classList.remove('active');
        });
    }

    async function analyzeVideo(url) {
        try {
            const response = await fetch(`/analyze?url=${encodeURIComponent(url)}`);
            const data = await response.json();
            if (data.status === 'error') throw new Error(data.message);
            
            return data.clips;
        } catch (e) {
            console.error(e);
            throw e;
        }
    }

    function renderClips(clips) {
        clipsGrid.innerHTML = '';
        
        // Read global values to initialize clip-specific checkboxes!
        const globalFullScreen = document.getElementById('opt-fullscreen').checked ? 'checked' : '';
        const globalHideBranding = document.getElementById('opt-hidebranding').checked ? 'checked' : '';
        const globalHideTitle = document.getElementById('opt-hidetitle').checked ? 'checked' : '';

        clips.forEach((clip, idx) => {
            const title = clip.title || clip.Title || clip.clip_title || clip.hook || "Untitled Clip";
            const reason = clip.reason || clip.Reason || clip.description || clip.explanation || "Analysis complete.";
            const score = clip.score || clip.Score || clip.virality || 100;
            const start = clip.start || clip.startTime || clip.Start || "00:00";
            const end = clip.end || clip.endTime || clip.End || "00:00";

            const card = document.createElement('div');
            card.className = 'clip-card';
            card.innerHTML = `
                <div style="padding: 20px;">
                    <div style="display:flex; justify-content: space-between; align-items:center; margin-bottom: 15px;">
                        <span style="color: #facc15; font-weight: 800; font-size: 12px;">CLIP #${idx + 1}</span>
                        <span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; font-size: 10px; padding: 2px 8px; border-radius: 5px;">SCORE: ${score}%</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label style="display:block; font-size: 10px; color: #64748b; margin-bottom: 5px;">EDIT IMPERIAL SUBTITLE (TOP)</label>
                        <textarea class="subtitle-edit-top" style="width: 100%; background: rgba(0,0,0,0.5); border: 1px solid #334155; color: white; border-radius: 5px; padding: 10px; font-size: 14px; height: 60px; resize: none;">${title}</textarea>
                    </div>
                    
                    <!-- INDEPENDENT CLIP CONFIG OPTIONS (INITIALIZED BY GLOBAL VALUES) -->
                    <div class="clip-options" style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; padding: 12px; background: rgba(255,255,255,0.02); border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                        <label style="display: flex; align-items: center; gap: 8px; color: #cbd5e1; font-size: 12.5px; cursor: pointer; font-weight: 600;">
                            <input type="checkbox" class="opt-fullscreen" ${globalFullScreen} style="accent-color: #facc15; width: 15px; height: 15px; cursor: pointer;"> 9:16 전체 화면 📺
                        </label>
                        <label style="display: flex; align-items: center; gap: 8px; color: #cbd5e1; font-size: 12.5px; cursor: pointer; font-weight: 600;">
                            <input type="checkbox" class="opt-hidebranding" ${globalHideBranding} style="accent-color: #facc15; width: 15px; height: 15px; cursor: pointer;"> 하단 문구 삭제 ❌
                        </label>
                        <label style="display: flex; align-items: center; gap: 8px; color: #cbd5e1; font-size: 12.5px; cursor: pointer; font-weight: 600;">
                            <input type="checkbox" class="opt-hidetitle" ${globalHideTitle} style="accent-color: #facc15; width: 15px; height: 15px; cursor: pointer;"> 상단 타이틀 삭제 🚫
                        </label>
                    </div>
                    
                    <button class="imperial-btn" style="width: 100%; padding: 12px;" onclick="window.generateShorts(this, ${idx})">
                        GENERATE IMPERIAL SHORTS 🎬
                    </button>
                </div>
            `;
            clipsGrid.appendChild(card);
        });
    }

    window.generateShorts = async (btn, idx) => {
        const cards = document.querySelectorAll('.clip-card');
        const targetCard = cards[idx];
        const editedTitle = targetCard.querySelector('.subtitle-edit-top').value;
        const clip = window.currentClips[idx];
        
        // Read active options locally from the specific clip card!
        const fullScreen = targetCard.querySelector('.opt-fullscreen').checked;
        const hideBranding = targetCard.querySelector('.opt-hidebranding').checked;
        const hideTitle = targetCard.querySelector('.opt-hidetitle').checked;
        
        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '⚙️ ENGRAVING SUBTITLES...';
        
        try {
            const url = youtubeInput.value.trim();
            const response = await fetch('/render', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    url: url,
                    ...clip,
                    title: editedTitle, // Send the edited title
                    fullScreen: fullScreen,
                    hideBranding: hideBranding,
                    hideTitle: hideTitle
                })
            });
            const data = await response.json();
            if (data.status === 'error') throw new Error(data.message);
            
            alert('🚀 자막 각인 명령 하달 완료! 수정한 자막 그대로 사출됩니다.');
            btn.innerHTML = '✅ RENDER STARTED';
        } catch (e) {
            alert('🚨 Render Error: ' + e.message);
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    };
});
