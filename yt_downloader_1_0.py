import yt_dlp

url = "https://youtu.be/LXb3EKWsInQ?si=Mz3-K3SjcsHJvols"

ytdlp_info_options = {
    'quiet': True,
    'skip_download': True,
}

with yt_dlp.YoutubeDL(ytdlp_info_options) as ydl:
    info = ydl.extract_info(url, download=False)
    formats = info.get('formats', [])



for f in formats:
    id = f.get('format_id', '?')

    ext = f.get("ext", "?")

    height = f.get("height")

    fps = f.get("fps")
    
    tbr = f.get("tbr")

    size = f.get("filesize")
    size_mb = f"{round(size / 1024 / 1024, 2)} MB" if size else "?"

    vcodec = f.get('vcodec', '?')
    acodec = f.get('acodec', '?')

    format_note = f.get('format_note', '?')

    print(
        f"{id:>5} | {ext:>5} | {str(height):>5}p | {str(fps):>4}fps | "
        f"{str(round(tbr)) + ' kbps' if tbr else '–':>10} | {size_mb:>10} | "
        f"{vcodec:>10} | {acodec:>10} | {format_note}"
    )

video_id = input("\n🎬 Podaj ID formatu wideo do pobrania: ").strip()

preferred_audio = None
for f in formats:
    if f.get('vcodec') == 'none' and f.get('acodec', '').startswith(('mp4a', 'opus')):
        preferred_audio = f['format_id']
        break

if not preferred_audio:
    print("❌ Nie znaleziono odpowiedniego formatu audio.")
    exit()
    

combined_format = f"{video_id}+{preferred_audio}"
print(f"\n✅ Wybrany format: {combined_format} (video+audio)")

ytdlp_download_options = {
    'format': combined_format,
    'outtmpl': '%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'postproccessors': [
        {
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }
    ]
}

with yt_dlp.YoutubeDL(ytdlp_download_options) as ydl:
    ydl.download([url])