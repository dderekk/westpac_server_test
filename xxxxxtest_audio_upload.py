import pyaudio
import wave
import time
import requests

def record_audio(duration, output_path):
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    rate = 44100  # Record at 44100 samples per second

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def upload_audio(url, audio_path):
    with open(audio_path, 'rb') as f:
        files = {'file': (audio_path, f, 'audio/wav')}
        response = requests.post(url, files=files)
        return response.json()

if __name__ == "__main__":
    url = 'http://10.128.219.59:5000/upload'  # 替换为您的服务器地址
    audio_path = 'recorded_audio.wav'
    duration = 10  # Record duration in seconds

    print("Recording audio...")
    record_audio(duration, audio_path)
    print("Uploading audio...")
    response = upload_audio(url, audio_path)
    print("Server response:", response)
