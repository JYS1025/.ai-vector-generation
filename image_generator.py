# image_generator.py
import os
import requests  # URL에서 이미지를 다운로드하기 위해 추가
from dotenv import load_dotenv
from together import Together

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수에서 API 키를 가져옵니다.
API_KEY = os.getenv("TOGETHER_API_KEY")

class ApiTokenError(Exception):
    "API 토큰이 없을 때 발생하는 사용자 정의 예외입니다."
    pass

def generate_image_api(prompt: str, output_path: str):
    '''
    Together AI API를 사용하여 이미지를 생성하고, 반환된 URL에서 이미지를 다운로드하여 저장합니다.
    '''
    if not API_KEY:
        raise ApiTokenError("Together AI API key not found. Please set the TOGETHER_API_KEY in your .env file.")

    try:
        client = Together(api_key=API_KEY)
        
        # 공식 문서에 따라 API를 호출합니다.
        response = client.images.generate(
            model="black-forest-labs/FLUX.1-schnell-Free", # 무료 모델 사용
            prompt=prompt,
            steps=4
        )

        # 문서에 명시된 대로, 응답 객체의 data 리스트에 있는 첫 번째 아이템의 url 속성을 확인합니다.
        if response.data and response.data[0].url:
            image_url = response.data[0].url
            
            # 반환된 URL에서 이미지 데이터를 다운로드합니다.
            image_response = requests.get(image_url)
            image_response.raise_for_status()  # HTTP 오류가 발생하면 예외를 일으킵니다.
            
            # 다운로드한 이미지 데이터를 파일로 저장합니다.
            with open(output_path, "wb") as f:
                f.write(image_response.content)
        else:
            raise Exception("API 응답에 이미지 URL이 포함되어 있지 않습니다.")

    except Exception as e:
        # 모든 오류를 포괄적으로 처리합니다.
        raise Exception(f"An error occurred: {e}")