from pydub import AudioSegment
import speech_recognition as sr
import os
from FAQ_server import get_answer
from text_to_speech_upload import text_to_speech_and_upload

# 定义音频文件路径和目标WAV文件路径
input_audio_file = "recorded_audio.wav"  # what you get from frontend
output_wav_file = "output.wav"
upload_url = 'http://10.128.219.59:5000/upload'  # 替换为您的服务器地址

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

    # 调用 text_to_speech_and_upload 函数
    response = text_to_speech_and_upload(answer, upload_url)
    print("Upload response:", response)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
