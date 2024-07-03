import requests
import wave
import pyaudio


def download_audio(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    else:
        print(f"Failed to download file: {response.status_code}")
        return None


def play_audio(file_path):
    # Define stream chunk
    chunk = 1024

    # Open a .wav format music
    f = wave.open(file_path, "rb")

    # Instantiate PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)

    # Read data
    data = f.readframes(chunk)

    # Play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # Stop stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()


if __name__ == "__main__":
    media_info_url = 'http://10.128.219.59:5000/latest_media'  # 替换为您的服务器地址
    audio_base_url = 'http://10.128.219.59:5000/uploads/'  # 替换为您的服务器地址
    audio_path = 'downloaded_audio.wav'

    # 获取最新的媒体信息
    response = requests.get(media_info_url)
    if response.status_code == 200:
        data = response.json()
        text = data.get('text')
        filename = data.get('filename')

        print("Received Text: ", text)

        # 下载音频文件
        audio_url = audio_base_url + filename
        downloaded_file = download_audio(audio_url, audio_path)
        if downloaded_file:
            print("Playing audio...")
            play_audio(downloaded_file)
    else:
        print(f"Failed to retrieve media: {response.status_code}")
