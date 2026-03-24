import yt_dlp
import os
import streamlit as st
import threading

# 內容分析：移除不相容的 tkinter 並改用 Streamlit 原生組件
def main():
    st.title("K.I.T.T. 媒體擷取系統")
    st.info("任務說明：請輸入影片網址並指定儲存路徑。")

    # 1. 介面輸入區：取代原本的視窗輸入
    url = st.text_input("影片網址 (URL):", placeholder="https://www.youtube.com/watch?v=...")
    
    # 在雲端環境中，建議預設存放在相對路徑 './downloads'
    save_path = st.text_input("儲存路徑:", value="./downloads")

    # 2. 功能執行區
    if st.button("啟動擷取任務"):
        if not url:
            st.warning("Brett，請先提供有效的網址。")
            return

        # 確保資料夾存在
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            st.write(f"系統訊息：已建立路徑 {save_path}")

        # 執行下載
        download_video(url, save_path)

def download_video(url, save_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
    }

    try:
        with st.spinner("掃描中，請稍候..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        st.success("任務達成：影片已成功儲存在伺服器路徑中。")
    except Exception as e:
        st.error(f"警告：系統遭遇未知錯誤。詳細資訊：{str(e)}")

if __name__ == "__main__":
    main()
