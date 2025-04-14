import yt_dlp

url = "https://youtu.be/LXb3EKWsInQ?si=Mz3-K3SjcsHJvols"

info_options = {
    'quiet': True,
    'skip_download': True,
}

with yt_dlp.YoutubeDL(info_options) as ydl:
    info = ydl.extract_info(url, download=False)
    formats = info.get('formats', [])

print("\n🎥 Dostępne formaty wideo:")
for f in formats:
    if f.get('vcodec') != 'none':
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
            f"{id:>5} | {ext:>4} | {str(height) + 'p' if height else '–':>6} | "
            f"{str(fps) + 'fps' if fps else '–':>6} | "
            f"{str(round(tbr)) + ' kbps' if tbr else '–':>10} | "
            f"{size_mb:>10} | {vcodec:>10} | {acodec:>10} | {format_note}"
        )

video_id = input("\n🎬 Podaj ID formatu wideo do pobrania: ").strip()

if not video_id:
    print("❌ Musisz podać format wideo.")
    exit()

print("\n🎧 Dostępne formaty audio:")
audio_formats = []
for f in formats:
    if f.get('vcodec') == 'none' and f.get('acodec') not in (None, 'none'):
        id = f.get('format_id', '?')
        ext = f.get("ext", "?")
        acodec = f.get("acodec", "?")
        tbr = f.get("tbr")
        size = f.get("filesize")
        size_mb = f"{round(size / 1024 / 1024, 2)} MB" if size else "?"

        audio_formats.append((id, ext, acodec, tbr, size_mb))

        print(
            f"{id:>5} | {ext:>4} | {acodec:>10} | "
            f"{str(round(tbr)) + ' kbps' if tbr else '–':>10} | {size_mb:>10}"
        )

audio_id = input("\n🎧 Podaj ID formatu audio (Enter = bez dźwięku): ").strip()

if audio_id:
    combined_format = f"{video_id}+{audio_id}"
    print(f"\n✅ Wybrano format: {combined_format} (video + audio)")
else:
    combined_format = video_id
    print(f"\n✅ Wybrano format: {combined_format} (tylko video, bez dźwięku)")

download_options = {
    'format': combined_format,
    'outtmpl': '%(title)s.%(ext)s',
    'merge_output_format': 'mp4',  # scal bez konwertowania
    # 'postprocessors': []  # NIE dodawaj FFmpegVideoConvertor!
}

with yt_dlp.YoutubeDL(download_options) as ydl:
    ydl.download([url])
