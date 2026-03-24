import yt_dlp
import os
import streamlit as st

def main():
    st.title("K.I.T.T. 全能媒體擷取系統")
    
    # 1. 任務配置區
    url = st.text_input("輸入網址 (影片或清單):", placeholder="https://www.youtube.com/playlist?list=...")
    save_path = st.text_input("儲存路徑:", value="./downloads")
    
    # 新增：任務模式選擇
    mode = st.radio("任務模式：", ["僅下載當前影片", "下載整個播放清單"], horizontal=True)
    is_playlist = (mode == "下載整個播放清單")

    # 2. 啟動按鈕
    if st.button("啟動任務"):
        if not url:
            st.warning("Brett，請先鎖定目標網址。")
            return
            
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            
        execute_download(url, save_path, is_playlist)

def execute_download(url, save_path, is_playlist):
    # 配置偽裝與下載參數
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(save_path, '%(playlist_index)s-%(title)s.%(ext)s' if is_playlist else '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,  # 關鍵設定：是否抓取清單
        'quiet': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'ignoreerrors': True, # 遇到清單中某個影片掛掉時，繼續下載下一個
    }

    try:
        with st.spinner(f"正在執行{'清單' if is_playlist else '單片'}擷取任務..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        st.success("任務達成：所有掃描目標已處理完畢。")
    except Exception as e:
        st.error(f"系統異常：{str(e)}")

if __name__ == "__main__":
    main()
