from flask import Flask, request, jsonify
from transformers import pipeline
import random

import base64
from PIL import Image
from io import BytesIO

from flasgger import Swagger

# 初始化
image_captioner = pipeline("image-to-text", model="./models/caption")


# 在文件顶部添加
sentiment_analyzer = pipeline("sentiment-analysis", model="./models/sentiment")


app = Flask(__name__)

app.config['SWAGGER'] = {'title': 'AI API Factory'}
Swagger(app)


@app.route('/random', methods=['POST'])
def get_random():
    """
    生成随机数API
    ---
    tags:
      - 实用工具
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - max_value
          properties:
            max_value:
              type: integer
              description: 随机数的最大值
              example: 100
    responses:
      200:
        description: 成功生成随机数
        schema:
          type: object
          properties:
            random_number:
              type: integer
              description: 生成的随机数
      400:
        description: 缺少参数或参数无效
    """
    if not request.json or 'max_value' not in request.json:
        return jsonify({'error': 'Missing max_value parameter'}), 400
    max_val = request.json['max_value']
    return jsonify({'random_number': random.randint(0, max_val)})


# 在/sentiment路由上方添加：

@app.route('/sentiment', methods=['POST'])
def sentiment():
    """
    情绪分析API
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
    responses:
      200:
        description: 分析结果
        schema:
          type: object
          properties:
            sentiment:
              type: string
    """

    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Missing text parameter'}), 400
    text = request.json['text']
    result = sentiment_analyzer(text)[0]
    return jsonify(result)

@app.route('/caption', methods=['POST'])
def caption():
    """
    图像描述生成API
    ---
    tags:
      - AI分析
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - image
          properties:
            image:
              type: string
              format: base64
              description: base64编码的图像数据
              example: "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    responses:
      200:
        description: 图像描述结果
        schema:
          type: object
          properties:
            generated_text:
              type: string
              description: 生成的图像描述
      400:
        description: 缺少图像数据
    """

    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'Missing image data'}), 400
    img_data = base64.b64decode(request.json['image'])
    image = Image.open(BytesIO(img_data))
    result = image_captioner(image)[0]
    return jsonify(result)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)