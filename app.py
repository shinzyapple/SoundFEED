import streamlit as st
import time

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

# --- 状態変数 ---
if "bg_audio" not in st.session_state:
    st.session_state.bg_audio = None
if "se_audio" not in st.session_state:
    st.session_state.se_audio = None
if "bg_playing" not in st.session_state:
    st.session_state.bg_playing = False

# --- ファイルアップロード ---
bg_file = st.file_uploader("🎵 BGMファイルを選択（mp3 / wav）", type=["mp3", "wav"])
se_file = st.file_uploader("✨ 効果音ファイルを選択（mp3 / wav）", type=["mp3", "wav"])

if bg_file:
    st.session_state.bg_audio = bg_file
    st.success("BGMを読み込みました！")

if se_file:
    st.session_state.se_audio = se_file
    st.success("効果音を読み込みました！")

# --- UI設定 ---
fade_time = st.slider("🎚 フェード時間（秒）", 0.5, 5.0, 2.0, 0.5)
wait_time = st.slider("⏳ 待機時間（秒）", 0.5, 5.0, 2.0, 0.5)

# --- 再生エリア ---
st.markdown("## 🎧 再生コントロール")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ BGM再生"):
        if st.session_state.bg_audio:
            st.audio(st.session_state.bg_audio, format="audio/mp3", start_time=0)
            st.session_state.bg_playing = True
            st.success("BGMを再生中 🎶")
        else:
            st.warning("BGMをアップロードしてね！")

with col2:
    if st.button("💫 効果音を再生"):
        if st.session_state.se_audio:
            with st.spinner(f"効果音準備中… {wait_time}秒後に再生"):
                time.sleep(wait_time)
            st.audio(st.session_state.se_audio, format="audio/mp3")
            st.success("💥 効果音を再生しました！")
            st.info(f"{wait_time}秒後にBGMをフェードインします…")
            time.sleep(wait_time)
            if st.session_state.bg_audio:
                st.audio(st.session_state.bg_audio, format="audio/mp3")
        else:
            st.warning("効果音をアップロードしてね！")

st.markdown("---")
st.caption("© 2025 Disney風フェードBGMアプリ 🎵 by Streamlit Cloud")
