import requests
import streamlit as st

st.set_page_config(page_title="Web Link Downloader", page_icon="📥")

st.title("📥 Web Link Downloader")
st.write(
    "Kisi bhi direct file ka link yahan paste karo aur seedha download karo!"
)

url = st.text_input("Paste Direct Link Here:")

if st.button("Download File", type="primary"):
  if not url:
    st.warning("Pehle koi valid link toh dalo!")
  else:
    try:
      with st.spinner("Downloading... ⏳"):
        response = requests.get(url, stream=True)
        response.raise_for_status()

        filename = url.split("/")[-1].split("?")[0]
        if not filename or "." not in filename:
          filename = "downloaded_file.bin"

        file_bytes = response.content

      st.success(f"File Ready: **{filename}** 🎉")

      st.download_button(
          label="💾 Click here to Save to PC",
          data=file_bytes,
          file_name=filename,
          mime="application/octet-stream",
      )

    except Exception as e:
      st.error(f"Download fail ho gaya! Error: {e}")
      
