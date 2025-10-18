# 세금 데이터 분석 시스템 💰

VBA 예제를 Streamlit 웹 서비스로 구현한 프로젝트입니다.

## 🚀 Streamlit Cloud 배포 방법

### 1단계: GitHub 저장소 생성
1. [GitHub](https://github.com)에 로그인
2. 새 저장소(Repository) 생성
   - 이름: `tax-analysis-app` (원하는 이름)
   - Public으로 설정
3. 다음 파일들을 업로드:
   - `tax_app.py`
   - `requirements.txt`
   - `README.md` (선택사항)

### 2단계: Streamlit Cloud 배포
1. [Streamlit Cloud](https://share.streamlit.io)에 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 저장소 선택:
   - Repository: `your-username/tax-analysis-app`
   - Branch: `main`
   - Main file path: `tax_app.py`
5. "Deploy!" 클릭

### 3단계: 완료!
몇 분 후 앱이 배포되고 공개 URL을 받게 됩니다:
- 예: `https://your-app-name.streamlit.app`
- 이 URL을 누구에게나 공유 가능!

## 📋 기능

1. ✅ 데이터 보기
2. ✅ 세율 자동 계산
3. ✅ 조건부 서식
4. ✅ 통계 분석
5. ✅ 새 데이터 추가
6. ✅ 인터랙티브 차트
7. ✅ CSV/Excel 업로드/다운로드

## 🛠️ 로컬 실행 방법

```bash
# 라이브러리 설치
pip install -r requirements.txt

# 앱 실행
streamlit run tax_app.py
```

## 💡 참고사항

- 데이터는 세션에만 저장됩니다 (새로고침 시 초기화)
- 영구 저장이 필요한 경우 데이터베이스 연결 필요
- 무료 Streamlit Cloud는 월 1GB 트래픽 제공

## 📞 문의

GitHub Issues를 통해 문의해주세요!
