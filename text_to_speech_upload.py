from gtts import gTTS
from pydub import AudioSegment
import requests


def text_to_speech_and_upload(text, upload_url):
    chatgpt_response_audio_file = "chatgpt_response.wav"

    # 将文本转换为语音并保存为 MP3 文件
    tts = gTTS(text=text, lang='en')
    tts.save("chatgpt_response.mp3")

    # 将 MP3 文件转换为 WAV 文件
    response_audio = AudioSegment.from_mp3("chatgpt_response.mp3")
    response_audio.export(chatgpt_response_audio_file, format="wav")

    # 上传音频文件和文本到服务器
    def upload_audio(url, audio_path, text):
        with open(audio_path, 'rb') as f:
            files = {'file': (audio_path, f, 'audio/wav')}
            data = {'text': text}
            response = requests.post(url, files=files, data=data)
            return response.json()

    print("Uploading audio and text...")
    response = upload_audio(upload_url, chatgpt_response_audio_file, text)
    print("Server response:", response)
    return response


if __name__ == "__main__":
    sample_text = "Hello, this is a test."
    upload_url = 'http://10.128.219.59:5000/upload'  # 替换为您的服务器地址
    text_to_speech_and_upload(sample_text, upload_url)
