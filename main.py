import yt_dlp
import os

url = input("Podaj link do filmu: ")


info_options = {
    'quiet': True,
    'skip_download': True,
}

with yt_dlp.YoutubeDL(info_options) as ydl:
    info = ydl.extract_info(url, download=False)
    formats = info.get('formats', [])

# ---------------------------------------------------------------

print("\nDostępne formaty wideo:")
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
            f"{str(fps) + 'fps' if fps else '–':>7} | "
            f"{str(round(tbr)) + ' kbps' if tbr else '–':>11} | "
            f"{size_mb:>10} | {vcodec:>30} | {acodec:>10} | {format_note}"
        )



video_id = input("\nPodaj ID formatu wideo do pobrania (Enter = bez wideo): ").strip()

print("\nDostępne formaty audio: ")
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
            f"{id:>10} | {ext:>4} | {acodec:>20} | "
            f"{str(round(tbr)) + ' kbps' if tbr else '–':>10} | {size_mb:>10}"
        )

audio_id = input("\nPodaj ID formatu audio (Enter = bez audio): ").strip()

if audio_id and video_id:
    combined_format = f"{video_id}+{audio_id}"
    print(f"\nWybrano format: {combined_format} (video + audio)")
    format = 'mp4'
else:
    if video_id and not(audio_id):
        combined_format = video_id
        print(f"\nWybrano format: {combined_format} (tylko video, bez audio)")
        format = 'mp4'
    else: 
        if audio_id:
            combined_format = audio_id
            print(f"\nWybrano format: {combined_format} (tylko audio, bez wideo)")
            format = 'm4a'
        else:
            print("Nie wybrano żadnych formatów")
            exit()


ffmpeg_path = os.path.abspath('./ffmpeg/bin/ffmpeg.exe')

title = input("Podaj nazwę pliku: ").strip()



download_options = {
    'format': combined_format,
    'outtmpl': f"{title}.%(ext)s",
    'merge_output_format': format,
    'ffmpeg_location': ffmpeg_path,
    'postprocessors': []
}

with yt_dlp.YoutubeDL(download_options) as ydl:
    ydl.download([url])
