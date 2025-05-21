# Flask 주소록 애플리케이션

간단한 Flask 기반 주소록 웹 애플리케이션입니다. 이 앱을 통해 연락처를 추가, 편집, 삭제하고 검색할 수 있습니다.

## 기능
<img src="https://github.com/gomtam/image/blob/main/250521/KakaoTalk_20250521_150511614.png" width="300" height="300"><img src="https://github.com/gomtam/image/blob/main/250521/KakaoTalk_20250521_150532524.png" width="300" height="300"><img src="https://github.com/gomtam/image/blob/main/250521/KakaoTalk_20250521_150540006.png" width="300" height="300">
- 연락처 추가, 편집, 삭제
- 연락처 검색
- 반응형 디자인 (모바일 및 데스크톱 지원)

## 설치 방법

1. 저장소를 복제합니다:
```bash
git clone https://github.com/gomtam/flaskjuso.git
cd flaskjuso
```

2. 가상 환경을 생성하고 활성화합니다:
```bash
conda create -n ( 가상 환경 이름 ) python=( 버전 )
shift + ctrl + p -> python: select interpreter -> 가상 환경 선택
```

3. 필요한 패키지를 설치합니다:
```bash
pip install -r requirements.txt
```

## 실행 방법

1. 애플리케이션을 실행합니다:
```bash
python jusoApp.py
```

2. 웹 브라우저에서 `http://127.0.0.1:5000`으로 접속합니다.

## 기술 스택

- Python 3.x
- Flask
- SQLAlchemy (SQLite 데이터베이스)
- HTML/CSS

## 라이센스

MIT 라이센스에 따라 사용할 수 있습니다. 
