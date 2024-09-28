from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        image_data = request.json['image']
        header, encoded = image_data.split(',', 1)
        decoded_image = base64.b64decode(encoded)

        # Tạo thư mục lưu trữ nếu chưa tồn tại
        os.makedirs('static/images', exist_ok=True)

        # Lưu hình ảnh
        image_path = 'static/images/captured_image.jpg'
        with open(image_path, 'wb') as f:
            f.write(decoded_image)

        # Trả về URL của ảnh
        image_url = f'/{image_path}'
        return jsonify({'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Nhận URL hình ảnh từ client
        image_url = request.json['image_url']

        # Gửi URL đến API phân tích
        api_url = f'https://deku-rest-api.gleeze.com/gemini?prompt=describe%20this%20photo&url={image_url}'

        response = requests.get(api_url)
        result = response.json()

        if 'result' in result and 'data' in result['result']:
            chatbot_response = result['result']['data']
        else:
            chatbot_response = 'Không có phản hồi phù hợp từ API.'
    except Exception as e:
        chatbot_response = f'Có lỗi xảy ra khi kết nối API: {str(e)}'
    
    return jsonify({'response': chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)
