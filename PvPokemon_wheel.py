import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="PvP GO 盃賽大轉盤", layout="centered")

st.title("🎡 Pokémon GO 對戰盃賽轉盤")
st.write("點擊轉盤中心，決定你們的對戰規則！")

# 盃賽數據
cup_data = [
    {"name": "超級聯賽", "cp": "1500", "limit": "無限制", "legend": "可", "mega": "不可"},
    {"name": "高級聯賽", "cp": "2500", "limit": "無限制", "legend": "可", "mega": "不可"},
    {"name": "大師聯賽", "cp": "無限", "limit": "無限制", "legend": "可", "mega": "不可"},
    {"name": "小小盃", "cp": "500", "limit": "無其他特殊限制", "legend": "可", "mega": "不可"},
    {"name": "假日盃", "cp": "1500", "limit": "僅限：一般、草、電、冰、飛行、幽靈屬性", "legend": "可", "mega": "不可"},
    {"name": "掛軸盃", "cp": "1500", "limit": "僅限：水、格鬥、惡屬性 (禁西獅海壬)", "legend": "可", "mega": "不可"},
    {"name": "進化盃", "cp": "1500", "limit": "僅限「能進化且尚未進化」的寶可夢", "legend": "不可", "mega": "不可"},
    {"name": "元素盃", "cp": "500", "limit": "僅限 水、火、草 屬性", "legend": "不可", "mega": "不可"},
    {"name": "萬聖節盃", "cp": "1500", "limit": "僅限 毒、幽靈、惡、冰、妖精", "legend": "可", "mega": "不可"},
    {"name": "化石盃", "cp": "1500", "limit": "僅限 水、岩石、鋼", "legend": "可", "mega": "不可"},
    {"name": "大師紀念賽", "cp": "無限", "limit": "禁止傳說與幻之寶可夢", "legend": "不可", "mega": "不可"},
    {"name": "超級紀念賽", "cp": "1500", "limit": "禁止傳說與幻之寶可夢", "legend": "不可", "mega": "不可"},
    {"name": "幻彩盃", "cp": "1500", "limit": "禁止單一屬性寶可夢", "legend": "不可", "mega": "不可"}
]

# 豐富色卡
colors = ["#FF595E", "#FF924C", "#FFCA3A", "#C5CA30", "#8AC926", "#36949D", "#1982C4", "#4267AC", "#6A4C93", "#B5179E", "#94D2BD", "#E9D8A6", "#EE9B00"]

cups_json = json.dumps(cup_data)
colors_json = json.dumps(colors)

wheel_html = f"""
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

<div id="wrapper" style="text-align:center; font-family: 'Microsoft JhengHei', sans-serif;">
    <canvas id="wheel" width="600" height="600" style="cursor:pointer; max-width: 100%; height: auto;"></canvas>
    
    <div id="result-container" style="margin-top: 25px; padding: 20px; border-radius: 20px; background: #ffffff; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: none; max-width: 500px; margin-left: auto; margin-right: auto; border-top: 5px solid #ff4b4b;">
        <h2 id="winner-name" style="color: #333; margin-bottom: 10px; font-size: 32px; font-weight: 800;"></h2>
        <div style="text-align: left; font-size: 18px; line-height: 1.8; color: #444;">
            <div style="background: #f8f9fa; padding: 10px; border-radius: 10px; margin-bottom: 8px;">📏 <b>CP 限制：</b> <span id="res-cp"></span></div>
            <div style="padding: 0 10px;">🚫 <b>特殊限制：</b> <span id="res-limit"></span></div>
            <div style="padding: 0 10px;">🐉 <b>傳說/幻之：</b> <span id="res-legend"></span></div>
            <div style="padding: 0 10px;">💎 <b>Mega 進化：</b> <span id="res-mega"></span></div>
        </div>
    </div>
</div>

<script>
const cups = {cups_json};
const palette = {colors_json};
const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const resultContainer = document.getElementById('result-container');

let startAngle = 0;
const arc = Math.PI / (cups.length / 2);
let isSpinning = false;

function drawWheel() {{
    const centerX = 300, centerY = 300, radius = 280;
    ctx.clearRect(0, 0, 600, 600);
    
    cups.forEach((cup, i) => {{
        const angle = startAngle + i * arc;
        ctx.fillStyle = palette[i % palette.length];
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, angle, angle + arc, false);
        ctx.lineTo(centerX, centerY);
        ctx.fill();
        
        ctx.strokeStyle = "rgba(255,255,255,0.6)";
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // --- 文字佈局優化 ---
        ctx.save();
        ctx.fillStyle = "white";
        ctx.shadowBlur = 5;
        ctx.shadowColor = "rgba(0,0,0,0.6)";
        ctx.font = "bold 20px 'Microsoft JhengHei'"; 
        
        // 將坐標系移到圓周附近 (radius * 0.8)
        const textDist = radius * 0.75; 
        ctx.translate(centerX + Math.cos(angle + arc / 2) * textDist, 
                      centerY + Math.sin(angle + arc / 2) * textDist);
        
        // 旋轉文字使其與扇形方向垂直（放射狀）
        ctx.rotate(angle + arc / 2 + Math.PI / 2);
        
        ctx.fillText(cup.name, -ctx.measureText(cup.name).width / 2, 0);
        ctx.restore();
    }});

    // 中心點
    ctx.beginPath();
    ctx.arc(centerX, centerY, 25, 0, 2 * Math.PI);
    ctx.fillStyle = "#fff";
    ctx.fill();
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 5;
    ctx.stroke();

    // 指針
    ctx.fillStyle = "#333";
    ctx.beginPath();
    ctx.moveTo(centerX - 25, 15);
    ctx.lineTo(centerX + 25, 15);
    ctx.lineTo(centerX, 60);
    ctx.fill();
}}

function spin() {{
    if (isSpinning) return;
    isSpinning = true;
    resultContainer.style.display = 'none';
    const duration = 3000; 
    const start = performance.now();
    const totalRotation = (Math.PI * 16) + (Math.random() * Math.PI * 2); 
    const initialAngle = startAngle;

    function animate(time) {{
        let elapsed = time - start;
        let progress = Math.min(elapsed / duration, 1);
        let curve = 1 - Math.pow(1 - progress, 4); 
        startAngle = initialAngle + (curve * totalRotation);
        drawWheel();
        if (progress < 1) requestAnimationFrame(animate);
        else {{ isSpinning = false; stopRotateWheel(); }}
    }}
    requestAnimationFrame(animate);
}}

function stopRotateWheel() {{
    const degrees = (startAngle * 180 / Math.PI) % 360;
    const arcd = 360 / cups.length;
    const index = Math.floor((360 - (degrees + 90) % 360) / arcd);
    const winner = cups[(index + cups.length) % cups.length];
    
    document.getElementById('winner-name').innerText = winner.name;
    document.getElementById('res-cp').innerText = winner.cp;
    document.getElementById('res-limit').innerText = winner.limit;
    document.getElementById('res-legend').innerText = winner.legend;
    document.getElementById('res-mega').innerText = winner.mega;
    resultContainer.style.display = 'block';

    confetti({{ particleCount: 200, spread: 80, origin: {{ y: 0.6 }} }});
}}

canvas.addEventListener('click', spin);
drawWheel();
</script>
"""

components.html(wheel_html, height=1000)