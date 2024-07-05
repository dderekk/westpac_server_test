# westpac_server_test

启动流程:
1. run Server.py
2. 如果有recorded_audio.wav 则执行4 否则 3
3. run xxxxxvideo_Record.py 录音 生成 recorded_audio.wav
4. run voice_to_text_chatgpt.py 上传 chatgpt 的声音内容 至 sever
5. 接收端口 测试 :xxxxxtest_frontend_get_voice_text.py

注:
/upload 是 你上传 你的录音


/latest_media 是你接受 chatgpt 这边生成的 录音


IP 地址我写的是 hard code 需要根据你自己的地址 改动, 要是不知道的话, 当你 成功执行 Server.py 后  命令窗口会告诉你 runing on 什么 IP地址
![image](https://github.com/dderekk/westpac_server_test/assets/101934458/a1e66d38-4127-4ffc-89c3-c8a104040ece)



声音 生成部分有几个 包 要装:
1. pip install gTTS 
2. pip install Flask pyttsx3 
3. pip install pydub 
4. pip install pydub speechrecognition

除此之外还有几个包:
pyaudio
requests
flask
openai
numpy
