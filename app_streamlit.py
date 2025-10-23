import streamlit as st
import pygame
import time
import threading
import tempfile
import base64

# ===== ページ設定 =====
st.set_page_config(
    page_title="✨フェード付きBGM＆効果音コントローラー🎶",
    layout="centered"
)

# ===== 背景CSS（リーナ・ベルカラー🎀） =====
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ffe6f2 0%, #cce6ff 100%);
    color: #333333;
}
h1 {
    color: #c96fa3;
    text-shadow: 1px 1px 2px #fff;
    text-align: center;
}
button[kind="primary"] {
    background-color: #ffb6c1 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    box-shadow: 0px 3px 5px rgba(0,0,0,0.2);
}
button[kind="primary"]:hover {
    background-color: #ffa0b2 !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===== タイトル =====
st.title("🌸 フェード付きBGM & 効果音コントローラー 🎶")

# ===== pygame 初期化 =====
pygame.mixer.init()

# ===== セッション変数 =====
if "bgm" not in st.session_state:
    st.session_state.bgm = None
if "se" not in st.session_state:
    st.session_state.se = None
if "status" not in st.session_state:
    st.session_state.status = "待機中"

# ===== ファイルアップロード =====
st.session_state.bgm = st.file_uploader("🎧 BGMファイルを選んでね", type=["mp3", "wav"])
st.session_state.se = st.file_uploader("🔔 効果音ファイルを選んでね", type=["mp3", "wav"])

# ===== パラメータ =====
fade_time = st.slider("🌈 フェード時間（ミリ秒）", 500, 5000, 2000, 100)
wait_time = st.slider("⏳ 効果音後の待機時間（ミリ秒）", 0, 5000, 2000, 100)

# ===== BGM 再生関数 =====
def play_bgm():
    if not st.session_state.bgm:
        st.warning("BGMファイルを選んでね！")
        return
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(st.session_state.bgm.read())
        tmp_path = tmp.name
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play(-1)
    st.session_state.status = "BGM再生中 🎵"

# ===== 効果音再生関数 =====
def play_se():
    if not st.session_state.se:
        st.warning("効果音ファイルを選んでね！")
        return
    threading.Thread(target=_play_se_thread).start()

def _play_se_thread():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(st.session_state.se.read())
        se_path = tmp.name

    if pygame.mixer.music.get_busy():
        st.session_state.status = "BGMフェードアウト中..."
        pygame.mixer.music.fadeout(fade_time)
        time.sleep(fade_time / 1000.0)

    st.session_state.status = "効果音再生中 🔊"
    se = pygame.mixer.Sound(se_path)
    se.play()
    while se.get_num_channels() > 0:
        time.sleep(0.1)

    st.session_state.status = "待機中..."
    time.sleep(wait_time / 1000.0)

    if st.session_state.bgm:
        with tempfile.NamedTemporaryFile(delete=False) as tmp2:
            tmp2.write(st.session_state.bgm.read())
            bgm_path = tmp2.name
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.play(-1, fade_ms=fade_time)
        st.session_state.status = "BGMフェードイン中 🌸"

# ===== 停止関数 =====
def stop_all():
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    st.session_state.status = "停止中 💤"

# ===== ボタン配置 =====
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ BGM再生", type="primary"):
        play_bgm()
with col2:
    if st.button("🔔 効果音再生", type="primary"):
        play_se()
with col3:
    if st.button("⏹ 停止", type="primary"):
        stop_all()

# ===== ステータス表示 =====
st.markdown(f"### 📡 現在の状態：**{st.session_state.status}**")
