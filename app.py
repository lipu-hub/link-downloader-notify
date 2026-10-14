import os
import tempfile

import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="Video Downloader",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 Video Downloader")
st.caption("YouTube, Instagram aur anya platforms ke liye (bina ffmpeg ke)")

url = st.text_input("Video ka link paste karein", placeholder="https://www.youtube.com/watch?v=...")

# Single-file formats (video+audio pehle se merged), taaki ffmpeg na lage.
# Pehle mp4 progressive, phir koi bhi single best file, aur last me generic fallback.
FORMAT_SELECTOR = "best[ext=mp4][vcodec!=none][acodec!=none]/best[vcodec!=none][acodec!=none]/best"


def download_video(link: str, target_dir: str) -> str:
    """Video ko target_dir me download karke file ka path return karta hai."""
    ydl_opts = {
        "format": FORMAT_SELECTOR,
        "outtmpl": os.path.join(target_dir, "%(title).80s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,   # safe filenames
        "merge_output_format": None, # merge nahi karna
        "postprocessors": [],        # koi ffmpeg postprocessor nahi
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        file_path = ydl.prepare_filename(info)

    # Kabhi kabhi extension badal jaata hai, isliye fallback check
    if not os.path.exists(file_path):
        files = os.listdir(target_dir)
        if not files:
            raise FileNotFoundError("Download hui file nahi mili.")
        file_path = os.path.join(target_dir, files[0])

    return file_path


if st.button("Download Video"):
    if not url.strip():
        st.warning("Pehle ek valid link daalein.")
    else:
        try:
            with st.spinner("Download ho raha hai... kripya wait karein"):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    file_path = download_video(url.strip(), tmp_dir)

                    # File ko memory me read karna zaroori hai,
                    # kyunki temp directory with-block ke baad delete ho jaati hai.
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                    file_name = os.path.basename(file_path)

            # Session state me rakhte hain taaki rerun par button gayab na ho
            st.session_state["file_bytes"] = file_bytes
