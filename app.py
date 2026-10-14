import os
import tempfile
import streamlit as st
from yt_dlp import YoutubeDL

st.set_page_config(page_title="Video & File Downloader", page_icon="📥")

st.title("📥 HD Video & Link Downloader")
st.write(
    "YouTube ya kisi bhi platform ka link yahan paste karo, full quality mein"
    " download hoga!"
)

url = st.text_input("Paste Video or File Link Here:")

if st.button("Download Video", type="primary"):
  if not url:
    st.warning("Pehle link toh dalo!")
  else:
    try:
      with st.spinner("Downloading video in best quality... ⏳"):
        # Temporary folder mein video download karne ke liye
        with tempfile.TemporaryDirectory() as tmpdirname:
          ydl_opts = {
              "format": (
                  "bestvideo+bestaudio/best"  # Best quality video + audio merge
              ),
              "outtmpl": os.path.join(tmpdirname, "%(title)s.%(ext)s"),
          }

          with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

          # File read karna
          with open(filename, "rb") as f:
            file_bytes = f.read()

          base_filename = os.path.basename(filename)

      st.success(f"Video Ready: **{base_filename}** 🎉")

      # Browser par download button
      st.download_button(
          label="💾 Click here to Save Video to PC",
          data=file_bytes,
          file_name=base_filename,
          mime="video/mp4",
      )

    except Exception as e:
      st.error(
          f"Download fail ho gaya! Ensure link is correct. Error details: {e}"
      )
