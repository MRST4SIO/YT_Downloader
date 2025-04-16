import yt_dlp
import os
import platform
import sys

def get_ffmpeg_path():
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # katalog tymczasowy używany przez PyInstaller
    else:
        base_path = os.path.abspath(".")

    if platform.system() == "Windows":
        return os.path.join(base_path, "ffmpeg", "bin", "ffmpeg.exe")
    else:
        return os.path.join(base_path, "ffmpeg", "bin", "ffmpeg")

def download():
    url = input("Podaj link do filmu: ").strip()

    info_options = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(info_options) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

    print("\nDostępne formaty wideo:")
    for f in formats:
        if f.get('vcodec') != 'none':
            print_video_format(f)

    video_id = input("\nPodaj ID formatu wideo do pobrania (Enter = bez wideo): ").strip()

    print("\nDostępne formaty audio: ")
    audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') not in (None, 'none')]
    for f in audio_formats:
        print_audio_format(f)

    audio_id = input("\nPodaj ID formatu audio (Enter = bez audio): ").strip()

    if video_id and audio_id:
        combined_format = f"{video_id}+{audio_id}"
        format_ext = 'mp4'
        print(f"\nWybrano format: {combined_format} (wideo + audio)")
    elif video_id:
        combined_format = video_id
        format_ext = 'mp4'
        print(f"\nWybrano format: {combined_format} (tylko wideo)")
    elif audio_id:
        combined_format = audio_id
        format_ext = 'm4a'
        print(f"\nWybrano format: {combined_format} (tylko audio)")
    else:
        print("Nie wybrano żadnych formatów.")
        return

    ffmpeg_path = get_ffmpeg_path()
    title = input("Podaj nazwę pliku: ").strip()

    download_options = {
        'format': combined_format,
        'outtmpl': f"{title}.%(ext)s",
        'merge_output_format': format_ext,
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': []
    }

    with yt_dlp.YoutubeDL(download_options) as ydl:
        ydl.download([url])

def print_video_format(f):
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

def print_audio_format(f):
    id = f.get('format_id', '?')
    ext = f.get("ext", "?")
    acodec = f.get("acodec", "?")
    tbr = f.get("tbr")
    size = f.get("filesize")
    size_mb = f"{round(size / 1024 / 1024, 2)} MB" if size else "?"

    print(
        f"{id:>10} | {ext:>4} | {acodec:>20} | "
        f"{str(round(tbr)) + ' kbps' if tbr else '–':>10} | {size_mb:>10}"
    )

if __name__ == "__main__":
    download()
