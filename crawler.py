import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

def download_video_thread():
    dl_btn.config(state="disabled")
    # 建立獨立線程，確保 UI 不凍結
    thread = threading.Thread(target=execute_download, daemon=True)
    thread.start()

def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            percent = (downloaded / total) * 100
            root.after(0, lambda p=percent, s=d.get('_percent_str', '掃描中...'): update_ui(p, s))
        except:
            pass
    elif d['status'] == 'finished':
        root.after(0, lambda: status_label.config(text=">> 數據抓取完成，啟動 FFmpeg 聲波重組 (AAC)...", fg="orange"))

def update_ui(p, s):
    progress_var.set(p)
    status_label.config(text=f">> 正在抓取目標數據... {s}", fg="red")

def execute_download():
    video_url = url_entry.get().strip()
    save_path = path_entry.get().strip()
    mode = download_mode.get()
    
    # === 核心路徑配置：指向您的 FFmpeg 引擎 ===
    FFMPEG_PATH = r"C:\Users\brett\OneDrive\Desktop\AI應用\ffmpeg-2026-03-18-git-106616f13d-essentials_build\ffmpeg-2026-03-18-git-106616f13d-essentials_build\bin"
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [progress_hook],
        'noplaylist': True if mode == "single" else False,
        
        # 強制執行 AAC 轉碼，確保音軌有聲
        'postprocessor_args': [
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k'
        ],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        },
    }

    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        messagebox.showinfo("任務完成", f"OK, Brett. 聲波解鎖成功，目標已安全送達。\n{save_path}")
        root.after(0, lambda: status_label.config(text=">> 系統待命 (音訊鏈路已加固)", fg="#0f0"))
    except Exception as e:
        messagebox.showerror("核心異常", f"任務失敗。原因：{e}")
        root.after(0, lambda: status_label.config(text=">> 鏈路中斷", fg="yellow"))
    finally:
        dl_btn.config(state="normal")

def select_path():
    path = filedialog.askdirectory()
    if path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, path)

# === UI 介面佈署 (已校準所有括號) ===
root = tk.Tk()
root.title("K.I.T.T. 2026 - STABLE V3.2.2")
root.geometry("620x480")
root.configure(bg="#000")

tk.Label(root, text="[ YOUTUBE STRATEGIC CAPTURE ]", font=("Courier New", 14, "bold"), bg="#000", fg="red").pack(pady=20)

mode_frame = tk.LabelFrame(root, text=" 任務模式 (Task Mode) ", bg="#000", fg="red", font=("Courier New", 10))
mode_frame.pack(pady=10, padx=40, fill="x")
download_mode = tk.StringVar(value="single")
tk.Radiobutton(mode_frame, text="單一影片鎖定", variable=download_mode, value="single", bg="#000", fg="#0f0", selectcolor="#222").pack(side="left", padx=20, pady=10)
tk.Radiobutton(mode_frame, text="整份清單下載", variable=download_mode, value="playlist", bg="#000", fg="#0f0", selectcolor="#222").pack(side="left", padx=20, pady=10)

tk.Label(root, text="目標網址 (Target URL):", bg="#000", fg="#0f0").pack(anchor="w", padx=40)
url_entry = tk.Entry(root, width=65, bg="#111", fg="#0f0", insertbackground="#0f0")
url_entry.pack(pady=5, padx=40)
url_entry.insert(0, "https://www.youtube.com/watch?v=y5bUCGzw6tY")

tk.Label(root, text="存放座標 (Storage Path):", bg="#000", fg="#0f0").pack(anchor="w", padx=40)
path_frame = tk.Frame(root, bg="#000")
path_frame.pack(pady=10, padx=40, fill="x")
path_entry = tk.Entry(path_frame, bg="#111", fg="#0f0")
path_entry.pack(side="left", expand=True, fill="x")
path_entry.insert(0, r"C:\Users\brett\OneDrive\Desktop\Downloads")
tk.Button(path_frame, text=" 瀏覽... ", command=select_path, bg="#333", fg="#0f0").pack(side="right", padx=5)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=480)
progress_bar.pack(pady=20)

dl_btn = tk.Button(root, text="啟動聲波解鎖抓取", font=("MS Serif", 12, "bold"), command=download_video_thread, bg="red", fg="white", width=30)
dl_btn.pack(pady=10)

status_label = tk.Label(root, text=">> 系統待命 (AAC 轉碼已就緒)", bg="#000", fg="#0f0", font=("Courier New", 9))
status_label.pack(side="bottom", fill="x")

root.mainloop()