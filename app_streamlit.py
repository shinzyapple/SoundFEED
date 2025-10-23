import streamlit as st
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import time
import threading
import tempfile

# ===== ページ設定 =====
st.set_page_config(
    page_title="🌸 フェード付きBGM＆効果音コントローラー 🎶",
    layout="centered"
)

# ===== ディズニー風スタイル =====
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

# ===== セッション変数 =====
if "bg_audio" not in st.session_state:
    st.session_state.bg_audio = None
if "bg_play_obj" not in st.session_state:
    st.session_state.bg_play_obj = None
if "status" not in st.session_state:
    st.session_state.status = "待機中"

# ===== ファイルアップロード =====
bg_file = st.file_uploader("🎧 BGMファイルを選んでね", type=["mp3", "wav"])
se_file = st.file_uploader("🔔 効果音ファイルを選んでね", type=["mp3", "wav"])

# ===== パラメータ =====
fade_time = st.slider("🌈 フェード時間（秒）", 0.5, 5.0, 2.0, 0.1)
wait_time = st.slider("⏳ 効果音後の待機時間（秒）", 0.0, 5.0, 2.0, 0.1)

# ===== 関数 =====
def play_bgm():
    if not bg_file:
        st.warning("BGMファイルを選んでね！")
        return
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(bg_file.read())
    tmp.close()
    st.session_state.bg_audio = AudioSegment.from_file(tmp.name)
    st.session_state.bg_thread = threading.Thread(target=loop_bgm)
    st.session_state.bg_thread.start()
    st.session_state.status = "BGM再生中 🎵"

def loop_bgm():
    while True:
        if st.session_state.bg_audio is None:
            break
        st.session_state.bg_play_obj = _play_with_simpleaudio(st.session_state.bg_audio)
        st.session_state.bg_play_obj.wait_done()

def stop_bgm():
    if st.session_state.bg_play_obj:
        st.session_state.bg_play_obj.stop()
    st.session_state.bg_audio = None
    st.session_state.status = "停止中 💤"

def play_effect():
    if not se_file:
        st.warning("効果音ファイルを選んでね！")
        return
    threading.Thread(target=_play_effect_thread).start()

def _play_effect_thread():
    st.session_state.status = "フェードアウト中..."
    if st.session_state.bg_audio and st.session_state.bg_play_obj:
        fade_out_audio = st.session_state.bg_audio.fade_out(int(fade_time * 1000))
        st.session_state.bg_play_obj.stop()
        _play_with_simpleaudio(fade_out_audio)
        time.sleep(fade_time)

    time.sleep(wait_time)  # 待機してから効果音再生
    st.session_state.status = "効果音再生中 🔊"

    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(se_file.read())
    tmp.close()
    se_audio = AudioSegment.from_file(tmp.name)
    se_play_obj = _play_with_simpleaudio(se_audio)
    se_play_obj.wait_done()

    st.session_state.status = "効果音終了、待機中..."
    time.sleep(wait_time)

    # BGMフェードイン再開
    if st.session_state.bg_audio:
        st.session_state.status = "BGMフェードイン中 🌸"
        fade_in_audio = st.session_state.bg_audio.fade_in(int(fade_time * 1000))
        st.session_state.bg_play_obj = _play_with_simpleaudio(fade_in_audio)

    st.session_state.status = "準備完了"

# ===== ボタン配置 =====
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ BGM再生", type="primary"):
        play_bgm()
with col2:
    if st.button("🔔 効果音再生", type="primary"):
        play_effect()
with col3:
    if st.button("⏹ 停止", type="primary"):
        stop_bgm()

# ===== ステータス表示 =====
st.markdown(f"### 📡 現在の状態：**{st.session_state.status}**")
