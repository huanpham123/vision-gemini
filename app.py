from flask import Flask, render_template, request, jsonify
import requests
import cv2
import base64
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    image_data = request.form['image']
    # Giải mã dữ liệu hình ảnh
    header, encoded = image_data.split(',', 1)
    decoded_image = base64.b64decode(encoded)
    
    # Lưu hình ảnh vào file tạm thời
    with open('temp_image.jpg', 'wb') as f:
        f.write(decoded_image)
    
    # Gửi hình ảnh đến API
    api_url = 'https://deku-rest-api.gleeze.com/gemini?prompt=describe%20this%20photo&url=https://i.imgur.com/SmVaQ8D.jpeg'
    files = {'file': open('temp_image.jpg', 'rb')}
    
    try:
        response = requests.post(api_url, files=files)
        result = response.json()
        
        if 'result' in result and 'data' in result['result']:
            chatbot_response = result['result']['data']
        else:
            chatbot_response = 'Không có phản hồi phù hợp từ API.'
    except Exception as e:
        chatbot_response = 'Có lỗi xảy ra khi kết nối API.'
    
    return jsonify({'response': chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)
