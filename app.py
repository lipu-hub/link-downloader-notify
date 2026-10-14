import os
import tempfile
import streamlit as st
from yt_dlp import YoutubeDL

st.set_page_config(page_title="Video & File Downloader", page_icon="📥")

st.title("📥 HD Video & Link Downloader")
st.write(
    "Kisi bhi website ka link yahan paste karo, MP4 format mein download"
    " hoga!"
)

url = st.text_input("Paste Video Link Here:")

if st.button("Download Video", type="primary"):
  if not url:
    st.warning("Pehle link toh dalo!")
  else:
    try:
      with st.spinner("Downloading video in MP4... ⏳"):
        with tempfile.TemporaryDirectory() as tmpdirname:
          ydl_opts = {
              "format": "best[ext=mp4]/best",
              "outtmpl": os.path.join(tmpdirname, "%(title)s.%(ext)s"),
              "noplaylist": True,
              "merge_output_format": "mp4",
          }

          with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Agar extension .mp4 nahi hai toh ensure karein ki mp4 me convert ho ya file wahi uthe
            base, ext = os.path.splitext(filename)
            if ext.lower() != ".mp4":
              new_filename = base + ".mp4"
              if os.path.exists(filename):
                os.rename(filename, new_filename)
                filename = new_filename

          with open(filename, "rb") as f:
            file_bytes = f.read()

          base_filename = os.path.basename(filename)

      st.success(f"Video Ready: **{base_filename}** 🎉")

      st.download_button(
          label="💾 Click here to Save MP4 Video to PC",
          data=file_bytes,
          file_name=base_filename,
          mime="video/mp4",
      )

    except Exception as e:
      st.error(f"Download fail ho gaya! Error: {e}")
