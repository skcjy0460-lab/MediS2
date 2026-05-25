# ⚕ MediClaim Pro — 병원 청구심사 전문 시스템

## 📁 프로젝트 구조

```
hospital_claim/
├── app.py                    # 메인 진입점
├── requirements.txt
├── pages/
│   ├── dashboard.py          # 대시보드
│   ├── prescription_search.py # 처방코드 검색
│   ├── criteria.py           # 심사기준 조회
│   ├── notice_guide.py       # 특정내역 알림 가이드
│   ├── ai_diagnosis.py       # AI 청구 진단
│   ├── case_search.py        # 사례 검색
│   └── admin_panel.py        # 관리자 패널
└── data/
    ├── prescriptions.json    # 처방코드 DB
    ├── notices.json          # 특정내역 코드 DB
    └── cases.json            # 사례 DB
```

## 🚀 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 실행
streamlit run app.py
```

## 🔑 로그인 정보 (초기 설정)

| 계정 | 아이디 | 비밀번호 |
|------|--------|----------|
| 관리자 | admin | admin1234 |
| 일반 사용자 | 아무 아이디 | 아무 비밀번호 |

> ⚠️ 실제 운영 시 app.py 내 로그인 로직을 DB 연동 방식으로 교체하세요.

## 🤖 AI 엔진 설정

AI 청구 진단 메뉴에서 아래 API 키를 입력하세요:

| 엔진 | API 키 발급처 |
|------|--------------|
| Claude (Anthropic) | https://console.anthropic.com |
| GPT-4o (OpenAI) | https://platform.openai.com |
| Gemini (Google) | https://makersuite.google.com |

## 📋 주요 기능

1. **처방코드 검색**: 코드·품목명·태그 검색 → 관련코드·심사기준·알림 통합 표시
2. **심사기준 조회**: 심평원 고시 기준 조회 및 원문 링크 제공
3. **특정내역 알림**: GJ/MT 코드 기재 방법·형식·예시 안내
4. **AI 청구 진단**: Claude+GPT+Gemini 다중 AI 삭감 위험 분석
5. **사례 검색**: 삭감·조정·환수 사례 DB 검색
6. **관리자 패널**: 처방코드·특정내역·사례 CRUD + JSON 일괄 업로드/백업

## 🗃 데이터 관리

- `data/prescriptions.json`: 처방코드 추가 시 배열에 항목 추가
- 관리자 패널 > 처방코드 DB 탭에서 UI로 등록 가능
- JSON 파일 일괄 업로드 지원

## ⚠️ 주의사항

- 이 프로그램은 청구심사 **가이드 도구**입니다. 최종 판단은 전문가가 해야 합니다.
- 심평원 기준은 수시로 변경되므로 정기적 업데이트가 필요합니다.
- AI 진단 결과는 참고용이며 법적 책임을 지지 않습니다.
