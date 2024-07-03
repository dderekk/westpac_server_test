from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import QA_Training as qa

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
    if 'file' not in request.files or 'text' not in request.form:
        return jsonify({'message': 'No file or text part in the request'}), 400
    file = request.files['file']
    text = request.form['text']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        latest_filename = filename
        latest_mimetype = file.mimetype
        latest_text = text
        return jsonify({'message': 'File and text uploaded successfully', 'filename': filename}), 201
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
