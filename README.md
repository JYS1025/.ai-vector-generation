# AI VectorGen Studio

AI VectorGen Studio는 사용자가 입력한 텍스트 설명(프롬프트)을 기반으로, 편집 가능한 고품질 벡터 그래픽(SVG)을 생성하는 데스크톱 애플리케이션입니다. 아이디어를 즉시 디자인 워크플로우에 통합할 수 있는 벡터 에셋으로 변환하여 창작의 초기 장벽을 낮춥니다.

## 주요 기능

- **텍스트 → 벡터 변환**: 원하는 이미지를 텍스트로 설명하여 벡터 그래픽을 생성합니다.
- **간편한 GUI**: 직관적인 인터페이스를 통해 벡터 파일을 손쉽게 생성하고 저장할 수 있습니다.
- **API 기반 작동**: Hugging Face Inference API를 사용하여 이미지를 생성하므로, 고사양의 로컬 GPU가 필요 없습니다.
- **편집 가능한 결과물**: Adobe Illustrator, Inkscape, Figma 등 모든 벡터 그래픽 소프트웨어에서 편집할 수 있는 표준 SVG 파일을 생성합니다.

## 핵심 기술 스택

- **언어**: Python 3.9+
- **GUI 프레임워크**: PyQt5
- **이미지 생성**: Hugging Face Inference API (`runwayml/stable-diffusion-v1-5`)
- **벡터 변환**: ImageMagick + Potrace

## 설치 및 설정 방법

프로젝트를 로컬 컴퓨터에서 실행하기 위해 다음 단계를 따르세요.

### 1. 사전 요구사항

시스템에 아래 소프트웨어들이 먼저 설치되어 있어야 합니다:

- **Python 3.9 이상**
- **ImageMagick**: 이미지 처리 도구
  - [공식 웹사이트에서 다운로드 및 설치](https://imagemagick.org/script/download.php)
- **Potrace**: 비트맵 트레이싱 도구
  - [공식 웹사이트에서 다운로드 및 설치](http://potrace.sourceforge.net/#downloading)

터미널에서 `magick`과 `potrace` 명령어가 정상적으로 실행되는지 확인하세요.

### 2. Hugging Face API 토큰 발급

이미지 생성을 위해 Hugging Face API 토큰이 필요합니다.

1. [Hugging Face 웹사이트](https://huggingface.co/join)에서 무료 계정을 생성합니다.
2. 로그인 후, **Settings → Access Tokens** 페이지([huggingface.co/settings/tokens](https://huggingface.co/settings/tokens))로 이동합니다.
3. **"New token"** 버튼을 클릭하여 새로운 토큰을 생성합니다. (권한은 `read`로 충분합니다.)
4. 생성된 토큰(`hf_`로 시작)을 복사합니다.

### 3. 프로젝트 설정

1. **프로젝트 파일 다운로드 또는 복제**: 이 프로젝트 파일들을 컴퓨터로 내려받습니다.

2. **Python 의존성 설치**: 프로젝트 디렉토리에서 터미널을 열고 아래 명령어를 실행하여 필요한 라이브러리들을 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

3. **API 토큰 설정**:
    - 프로젝트 디렉토리에 있는 `.env` 파일을 엽니다.
    - `your_token_here` 부분을 2단계에서 복사한 실제 Hugging Face API 토큰으로 교체하고 저장합니다.
    - 파일 내용은 아래와 같은 형식이 됩니다:
      ```
      # Hugging Face API 토큰을 아래에 붙여넣으세요.
      HUGGINGFACE_API_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      ```

## 애플리케이션 실행 방법

모든 설정이 완료되었다면, 프로젝트의 루트 디렉토리에서 아래 명령어를 실행하세요:

```bash
python main_app.py
```

이제 애플리케이션이 `.env` 파일에서 API 토큰을 자동으로 읽어와 실행됩니다.
