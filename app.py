import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from notifypy import Notify
import requests

notification = Notify()


def download_file(url, progress_bar, status_label, btn):
  try:
    status_label.config(text="Connecting...", fg="blue")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    filename = url.split("/")[-1].split("?")[0]
    if not filename or "." not in filename:
      filename = "downloaded_file.bin"

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    save_path = os.path.join(downloads_path, filename)

    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    with open(save_path, "wb") as f:
      for chunk in response.iter_content(chunk_size=8192):
        if chunk:
          f.write(chunk)
          downloaded += len(chunk)
          if total_size > 0:
            percent = (downloaded / total_size) * 100
            progress_bar["value"] = percent
            status_label.config(
                text=f"Downloading: {int(percent)}%", fg="green"
            )

    status_label.config(text="Success! File Saved.", fg="darkgreen")

    notification.title = "Download Complete! 🎉"
    notification.message = f"File saved as: {filename}\nCheck your Downloads folder."
    notification.send()

    messagebox.showinfo(
        "Success", f"File successfully downloaded!\nSaved as: {filename}"
    )

  except Exception as e:
    status_label.config(text="Download Failed!", fg="red")
    notification.title = "Download Failed ❌"
    notification.message = "Could not download the file. Check the link."
    notification.send()
    messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

  finally:
    btn.config(state=tk.NORMAL)
    progress_bar["value"] = 0


def start_download_thread(url_entry, progress_bar, status_label, btn):
  url = url_entry.get().strip()
  if not url:
    messagebox.showwarning("Warning", "Please enter a valid link!")
    return

  btn.config(state=tk.DISABLED)
  threading.Thread(
      target=download_file,
      args=(url, progress_bar, status_label, btn),
      daemon=True,
  ).start()


root = tk.Tk()
root.title("Link Downloader with Notify")
root.geometry("450x230")
root.resizable(False, False)

title_lbl = tk.Label(
    root, text="Link Downloader + Notify", font=("Arial", 14, "bold")
)
title_lbl.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

lbl = tk.Label(frame, text="Paste Direct File Link:", font=("Arial", 10))
lbl.pack(anchor="w")

url_entry = tk.Entry(frame, width=50, font=("Arial", 11))
url_entry.pack(pady=5)

progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=380, mode="determinate"
)
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="Ready", font=("Arial", 9), fg="gray")
status_label.pack()

download_btn = tk.Button(
    root,
    text="Download & Notify",
    font=("Arial", 10, "bold"),
    bg="#2196F3",
    fg="white",
    width=20,
    command=lambda: start_download_thread(
        url_entry, progress_bar, status_label, download_btn
    ),
)
download_btn.pack(pady=10)

root.mainloop()
