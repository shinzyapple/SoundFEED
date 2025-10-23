import streamlit as st
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import threading
import time

st.set_page_config(page_title="ディズニー風フェードBGMアプリ", page_icon="🎵", layout="centered")

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

st.title("🏰 ディズニー風フェードBGMアプリ")

# セッション状態で音データを保持
if "bg_audio" not in st.session_state:
    st.session_state.bg_audio = None
if "se_audio" not in st.session_state:
    st.session_state.se_audio = None
if "is_playing_bg" not in st.session_state:
    st.session_state.is_playing_bg = False

# === ファイルアップロード ===
bg_file = st.file_uploader("🎵 BGMファイルを選択（mp3 / wav）", type=["mp3", "wav"])
se_file = st.file_uploader("✨ 効果音ファイルを選択（mp3 / wav）", type=["mp3", "wav"])

if bg_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(bg_file.read())
        st.session_state.bg_audio = AudioSegment.from_file(tmp.name)
    st.success("BGMを読み込みました！")

if se_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(se_file.read())
        st.session_state.se_audio = AudioSegment.from_file(tmp.name)
    st.success("効果音を読み込みました！")

# === 再生関数 ===
def play_bgm_loop():
    fade_in_time = 2000
    fade_out_time = 2000
    bg = st.session_state.bg_audio
    while st.session_state.is_playing_bg:
        play(bg.fade_in(fade_in_time).fade_out(fade_out_time))
        time.sleep(2)

def play_effect_and_resume():
    if st.session_state.is_playing_bg:
        st.session_state.is_playing_bg = False
        time.sleep(0.5)
    play(st.session_state.se_audio)
    time.sleep(2)
    st.session_state.is_playing_bg = True
    threading.Thread(target=play_bgm_loop, daemon=True).start()

# === ボタン操作 ===
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ BGM再生 / 停止"):
        if not st.session_state.bg_audio:
            st.warning("BGMを先にアップロードしてね！")
        else:
            if not st.session_state.is_playing_bg:
                st.session_state.is_playing_bg = True
                threading.Thread(target=play_bgm_loop, daemon=True).start()
                st.success("BGM再生を開始しました！")
            else:
                st.session_state.is_playing_bg = False
                st.info("BGMを停止しました。")

with col2:
    if st.button("💫 効果音を再生"):
        if not st.session_state.se_audio:
            st.warning("効果音をアップロードしてね！")
        else:
            threading.Thread(target=play_effect_and_resume, daemon=True).start()
            st.success("効果音を再生しました！")

st.markdown("---")
st.caption("© 2025 Disney風オーディオ体験アプリ（pydub + Streamlit）")
