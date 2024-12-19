import streamlit as st
import yt_dlp
import os

# Function to check and validate FFmpeg path
def check_ffmpeg_path():
    # Default ffmpeg path assumption
    current_directory = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(current_directory, 'ffmpeg', 'bin', 'ffmpeg.exe')

    if not os.path.isfile(ffmpeg_path):
        st.error("FFmpeg not found! Please ensure it is installed and the path is correctly set.")
        st.stop()
    return ffmpeg_path

# Callback function to show download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        st.session_state.progress = f"Downloading {d['filename']} - {d['_percent_str']} complete"
    elif d['status'] == 'finished':
        st.session_state.progress = f"Finished downloading {d['filename']}"

# Function to download YouTube playlist
def download_youtube_playlist(playlist_url, output_directory, video_quality):
    # Get the FFmpeg path
    ffmpeg_path = check_ffmpeg_path()

    # Configuration options for yt-dlp
    ydl_opts = {
        'format': f'bestvideo[height<={video_quality}]+bestaudio/best/best',
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
        'noplaylist': False,  # Allow playlist download
        'progress_hooks': [progress_hook],
        'merge_output_format': 'mp4',
        'ffmpeg_location': ffmpeg_path,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'noprogress': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        st.success("Playlist download completed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI
def main():
    # Page title
    st.title("YouTube Playlist Downloader")
    st.write("Download entire playlists from YouTube with custom video quality.")

    # Input fields
    playlist_url = st.text_input("Enter the YouTube playlist URL:", placeholder="Paste the playlist URL here")
    output_directory = st.text_input("Enter output directory (optional):", placeholder="Leave blank for current directory")
    video_quality = st.selectbox("Select desired video quality:", ["2160", "1440", "1080", "720", "480", "360", "240", "144"], index=2)

    # Default output directory
    if not output_directory:
        output_directory = os.path.dirname(os.path.abspath(__file__))

    # Display progress
    if "progress" not in st.session_state:
        st.session_state.progress = ""
    st.write(st.session_state.progress)

    # Download button
    if st.button("Download Playlist"):
        if not playlist_url:
            st.warning("Please enter a valid playlist URL.")
        else:
            download_youtube_playlist(playlist_url, output_directory, video_quality)

if __name__ == "__main__":
    main()
