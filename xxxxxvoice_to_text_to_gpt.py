from pydub import AudioSegment
import speech_recognition as sr
import os
from FAQ_server import get_answer
from gtts import gTTS
import requests
import wave

# 定义音频文件路径和目标WAV文件路径
input_audio_file = "recorded_audio.wav"  # what you get from frontend
output_wav_file = "output.wav"
chatgpt_response_audio_file = "chatgpt_response.wav"
upload_url = 'http://127.0.0.1:5000/upload'  # 替换为您的服务器地址

# 检查文件格式并转换为 WAV 格式（如果不是 WAV 格式）
if not input_audio_file.lower().endswith(".wav"):
    audio = AudioSegment.from_file(input_audio_file)
    audio.export(output_wav_file, format="wav")
else:
    output_wav_file = input_audio_file

# 创建一个识别器对象
recognizer = sr.Recognizer()

# 读取 WAV 音频文件
with sr.AudioFile(output_wav_file) as source:
    audio_data = recognizer.record(source)

# 进行语音识别
try:
    text = recognizer.recognize_google(audio_data, language="en-US")
    print("Transcribed Text: ", text)

    # 获取 ChatGPT 的回答
    answer = get_answer(text)
    print("ChatGPT Answer: ", answer)

    # 将 ChatGPT 的回答转换为语音并保存为 WAV 文件
    tts = gTTS(text=answer, lang='en')
    tts.save("chatgpt_response.mp3")
    response_audio = AudioSegment.from_mp3("chatgpt_response.mp3")
    response_audio.export(chatgpt_response_audio_file, format="wav")


    # 上传音频文件到服务器
    def upload_audio(url, audio_path):
        with open(audio_path, 'rb') as f:
            files = {'file': (audio_path, f, 'audio/wav')}
            response = requests.post(url, files=files)
            return response.json()


    print("Uploading audio...")
    response = upload_audio(upload_url, chatgpt_response_audio_file)
    print("Server response:", response)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
