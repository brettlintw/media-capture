def execute_download(url, save_path, is_playlist):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(save_path, '%(playlist_index)s-%(title)s.%(ext)s' if is_playlist else '%(title)s.%(ext)s'),
        'noplaylist': not is_playlist,
        'quiet': False,
        'ignoreerrors': True,
        # --- 深度偽裝強化模組 ---
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
        },
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    try:
        with st.spinner(f"正在執行{'清單' if is_playlist else '單片'}擷取任務..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 這裡改用 extract_info 先抓取資訊再下載，增加成功率
                ydl.download([url])
        st.success("任務達成：掃描目標已全數處理。")
    except Exception as e:
        if "403" in str(e):
            st.error("警告：YouTube 攔截了請求 (403 Forbidden)。")
            st.info("這通常是因為雲端伺服器的 IP 被 YouTube 標記。建議：1. 更換網址測試。 2. 稍後再試。")
        else:
            st.error(f"系統異常：{str(e)}")
