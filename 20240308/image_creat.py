
import requests
import json
import urllib
import io
#import base64p
from PIL import Image

# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력
REST_API_KEY = '본인들 키 받아서 여기에 넣을 것'

# 이미지 생성하기 요청
def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            'prompt': prompt,
            'negative_prompt': negative_prompt
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

# 프롬프트에 사용할 제시어
#prompt = "A dog with white fur"
prompt = "hyper-detailed flower head with plants, (by loish), queen of the forest, " \
         "trending on artstation hd, long curly hair, highly detailed face"
negative_prompt = "sleeping cat, dog, human, ugly face, cropped"

# 이미지 생성하기 REST API 호출
response = t2i(prompt, negative_prompt)

# 응답의 첫 번째 이미지 생성 결과 출력하기
result = Image.open(urllib.request.urlopen(response.get("images")[0].get("image")))
#result.show()
#result.save('image_create.png','PNG')
result.save('image_create17.png','PNG')


##################################

"""
import requests
import json
import io
import base64
import urllib
from PIL import Image

# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력
REST_API_KEY = '16d543f2e968eedb468da2815185b756'

# 이미지 확대하기
def upscale(images, scale=2):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/upscale',
        json = {
            'images': images,
            'scale': scale
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

# Base64 인코딩
def imageToString(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    return my_encoded_img

# 이미지 파일 불러오기
img = Image.open('image_create.png')

# 이미지를 Base64 인코딩하기
img_base64 = imageToString(img)

# 이미지를 Base64 인코딩한 값의 배열
img_arr = []
img_arr.append(img_base64)

# 이미지 변환하기 REST API 호출
response = upscale(img_arr, 4)

# 응답의 첫 번째 이미지 생성 결과 출력하기
result = Image.open(urllib.request.urlopen(response.get("images")[0]))
#result.show()
result.save('image_scaling.png','PNG')
"""

"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
"""
import openai
openai.api_key = "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"

response = openai.Image.create(
    prompt = "a white siamese cat",
    n=1,
    size = "1024x1024"
)
image_url = response['data'][0]['url']
"""