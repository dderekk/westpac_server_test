from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import QA_Training as qa
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
import wave

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Make sure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

latest_filename = None
latest_mimetype = None
latest_text = None


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload_file():
    global latest_filename, latest_mimetype, latest_text
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        latest_filename = filename
        latest_mimetype = file.mimetype

        # 将上传的音频文件转为文本
        recognizer = sr.Recognizer()
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                print("Transcribed Text: ", text)

                # 获取 ChatGPT 的回答
                client = qa.get_client()
                model_id = "ft:gpt-3.5-turbo-0125:personal::9dbmYZT5"  # Replace with your fine-tuned model ID
                response = qa.chat_with_yx_model(client, model_id, text)
                answer = qa.extract_message(response)
                print("ChatGPT Answer: ", answer)

                # 将 ChatGPT 的回答转换为语音并保存为 WAV 文件
                tts = gTTS(text=answer, lang='en')
                chatgpt_response_audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'chatgpt_response.wav')
                tts.save("chatgpt_response.mp3")

                response_audio = AudioSegment.from_mp3("chatgpt_response.mp3")
                response_audio.export(chatgpt_response_audio_file, format="wav")

                latest_text = answer
                latest_filename = 'chatgpt_response.wav'
                latest_mimetype = 'audio/wav'

                return jsonify(
                    {'message': 'File processed and ChatGPT response generated', 'filename': latest_filename}), 201

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio")
                return jsonify({'message': 'Speech recognition failed'}), 500
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return jsonify({'message': 'Speech recognition request error'}), 500
    return jsonify({'message': 'File upload failed'}), 500


@app.route('/latest_media', methods=['GET'])
def get_latest_media():
    global latest_filename, latest_mimetype, latest_text
    if latest_filename and latest_text:
        return jsonify({
            'filename': latest_filename,
            'text': latest_text,
            'file_url': f'/uploads/{latest_filename}'
        })
    else:
        return jsonify({'message': 'No media available'}), 404


@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'message': 'No question provided'}), 400

    client = qa.get_client()
    model_id = "ft:gpt-3.5-turbo-0125:personal::9dbmYZT5"  # Replace with your fine-tuned model ID
    response = qa.chat_with_yx_model(client, model_id, question)
    answer = qa.extract_message(response)

    if answer:
        return jsonify({'answer': answer}), 200
    else:
        return jsonify({'message': 'Error processing request'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
