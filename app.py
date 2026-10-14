import os
import tempfile
import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="Video Downloader", page_icon="🎬", layout="centered"
)
st.title("🎬 Multi-Platform Video Downloader")
st.caption(
    "YouTube, Instagram aur anya restricted platforms ke liye (Enhanced Anti-Bot"
    " Bypass)"
)

url = st.text_input(
    "Video ka link paste karein",
    placeholder="https://www.youtube.com/watch?v=... ya Instagram link",
)

# Best progressive stream selector jo bina ffmpeg ke HD/SD video de sake
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
      # Anti-bot aur restrictions bypass karne ke liye headers aur user-agent
      "http_headers": {
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
          ),
          "Accept": (
              "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
          ),
          "Accept-Language": "en-US,en;q=0.5",
      },
      "extractor_args": {
          "youtube": {
              "player_client": ["android", "web"],
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
      with st.spinner(
          "Video fetch ho raha hai... restrictions bypass ki ja rahi hain ⏳"
      ):
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
      st.error(
          "Download fail ho gaya. Yeh link restricted, private ya invalid ho"
          f" sakta hai.\n\nDetail: {e}"
      )
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
