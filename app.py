import os
import tempfile
import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="Video Downloader", page_icon="🎬", layout="centered"
)
st.title("🎬 Multi-Platform Video Downloader")
st.caption("YouTube aur other platforms downloader (Bot Bypass)")

url = st.text_input(
    "Video ka link paste karein",
    placeholder="https://www.youtube.com/watch?v=...",
)

FORMAT_SELECTOR = (
    "best[ext=mp4][vcodec!=none][acodec!=none]/best[vcodec!=none][acodec!=none]/best"
)


def download_video(link: str, target_dir: str) -> str:
  ydl_opts = {
      "format": FORMAT_SELECTOR,
      "outtmpl": os.path.join(target_dir, "%(title).80s.%(ext)s"),
      "noplaylist": True,
      "quiet": True,
      "no_warnings": True,
      "restrictfilenames": True,
      "http_headers": {
          "User-Agent": (
              "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)"
              " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6"
              " Mobile/15E148 Safari/604.1"
          ),
      },
      # Bot sign-in check bypass karne ke liye ios aur web client
      "extractor_args": {
          "youtube": {
              "player_client": ["ios", "web"],
          }
      },
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(link, download=True)
    file_path = ydl.prepare_filename(info)

    if not os.path.exists(file_path):
      files = os.listdir(target_dir)
      if not files:
        raise FileNotFoundError("Download hui file nahi mili.")
      file_path = os.path.join(target_dir, files[0])
  return file_path


if st.button("Download Video", type="primary"):
  if not url.strip():
    st.warning("Pehle ek valid link daalein.")
  else:
    try:
      with st.spinner("Video download ho rahi hai... ⏳"):
        with tempfile.TemporaryDirectory() as tmp_dir:
          file_path = download_video(url.strip(), tmp_dir)

          with open(file_path, "rb") as f:
            file_bytes = f.read()

          file_name = os.path.basename(file_path)

          st.session_state["file_bytes"] = file_bytes
          st.session_state["file_name"] = file_name
          st.success("Video successfully taiyaar hai! ✅")

    except yt_dlp.utils.DownloadError as e:
      st.session_state.pop("file_bytes", None)
      st.error(f"Download fail ho gaya. Detail: {e}")
    except Exception as e:
      st.session_state.pop("file_bytes", None)
      st.error(f"Kuch unexpected error aa gaya: {e}")

if "file_bytes" in st.session_state:
  st.download_button(
      label="⬇️ File Save Karein",
      data=st.session_state["file_bytes"],
      file_name=st.session_state["file_name"],
      mime="video/mp4",
  )
