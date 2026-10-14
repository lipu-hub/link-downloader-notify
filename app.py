import os
import tempfile
import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="Video Downloader", page_icon="🎬", layout="centered"
)
st.title("🎬 Video Downloader")
st.caption("YouTube, Instagram aur anya platforms ke liye (bina ffmpeg ke)")

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
      "merge_output_format": None,
      "postprocessors": [],
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


if st.button("Download Video"):
  if not url.strip():
    st.warning("Pehle ek valid link daalein.")
  else:
    try:
      with st.spinner("Download ho raha hai... kripya wait karein"):
        with tempfile.TemporaryDirectory() as tmp_dir:
          file_path = download_video(url.strip(), tmp_dir)

          with open(file_path, "rb") as f:
            file_bytes = f.read()

          file_name = os.path.basename(file_path)

          st.session_state["file_bytes"] = file_bytes
          st.session_state["file_name"] = file_name
          st.success("Video taiyaar hai! ✅")

    except yt_dlp.utils.DownloadError as e:
      st.session_state.pop("file_bytes", None)
      st.error(
          "Download fail hua. Link galat ho sakta hai ya video private/restricted"
          f" hai. \n\n Detail: {e}"
      )
    except Exception as e:
      st.session_state.pop("file_bytes", None)
      st.error(f"Kuch gadbad ho gayi: {e}")

if "file_bytes" in st.session_state:
  st.download_button(
      label="⬇️ File Save Karein",
      data=st.session_state["file_bytes"],
      file_name=st.session_state["file_name"],
      mime="video/mp4",
  )
