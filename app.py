import streamlit as st
from pydub import AudioSegment
import tempfile
import threading
import time
import pygame

st.set_page_config(page_title="ディズニー風フェードBGMアプリ", page_icon="🎵", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fff6e5, #ffe2cc);
    color: #5a3921;
}
.stButton>button {
    background-color: #f7cda9;
    color: #5a3921;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}
.stButton>button:hover {
    background-color: #f9b97f;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🏰 ディズニー風フェードBGMアプリ")

if "bg_path" not in st.session_state:
    st.session_state.bg_path = None
if "se_path" not in st.session_state:
    st.session_state.se_path = None
if "is_playing_bg" not in st.session_state:
    st.session_state.is_playing_bg = False

pygame.mixer.init()

# === ファイルアップロード ===
bg_file = st.file_uploader("🎵 BGMファイルを選択（mp3 / wav）", type=["mp3", "wav"])
se_file = st.file_uploader("✨ 効果音ファイルを選択（mp3 / wav）", type=["mp3", "wav"])

if bg_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(bg_file.read())
        st.session_state.bg_path = tmp.name
    st.success("BGMを読み込みました！")

if se_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(se_file.read())
        st.session_state.se_path = tmp.name
    st.success("効果音を読み込みました！")

# === 再生関数 ===
def play_bgm_loop():
    pygame.mixer.music.load(st.session_state.bg_path)
    pygame.mixer.music.play(-1, fade_ms=2000)

def play_effect_and_resume():
    if st.session_state.is_playing_bg:
        pygame.mixer.music.fadeout(2000)
        st.session_state.is_playing_bg = False
        time.sleep(2)
    se = pygame.mixer.Sound(st.session_state.se_path)
    se.play()
    time.sleep(se.get_length() + 2)
    play_bgm_loop()
    st.session_state.is_playing_bg = True

# === ボタン操作 ===
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ BGM再生 / 停止"):
        if not st.session_state.bg_path:
            st.warning("BGMを先にアップロードしてね！")
        else:
            if not st.session_state.is_playing_bg:
                st.session_state.is_playing_bg = True
                threading.Thread(target=play_bgm_loop, daemon=True).start()
                st.success("BGM再生を開始しました！")
            else:
                pygame.mixer.music.fadeout(2000)
                st.session_state.is_playing_bg = False
                st.info("BGMを停止しました。")

with col2:
    if st.button("💫 効果音を再生"):
        if not st.session_state.se_path:
            st.warning("効果音をアップロードしてね！")
        else:
            threading.Thread(target=play_effect_and_resume, daemon=True).start()
            st.success("効果音を再生しました！")

st.markdown("---")
st.caption("© 2025 Disney風フェードBGMアプリ 🎶")
