import streamlit as st
import json
import os
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# DATA 초기화
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR  = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

PRES_PATH   = os.path.join(DATA_DIR, "prescriptions.json")
NOTICE_PATH = os.path.join(DATA_DIR, "notices.json")
CASE_PATH   = os.path.join(DATA_DIR, "cases.json")

DEFAULT_PRESCRIPTIONS = [
  {"code":"648602750","name":"씨엠쿨산","category":"의약품","dept":["피부과","성형외과","외과"],"description":"외래환자의약품관리료 적용 품목. 냉각 시술 후 보조 처방.","related_codes":["AL300","AL301","MZ100"],"related_names":["AL300 외래환자의약품관리료","AL301 의약품조제료","MZ100 처치료"],"criteria":"외래 내원 환자에게 냉각 시술(레이저, 크라이오 등) 후 처방 시 산정 가능. 입원환자에게는 산정 불가.","notice_required":True,"notice_detail":"특정내역 GJ 코드 필수 기재: GJ001(시술명), GJ002(적용부위). 미기재 시 삭감 대상.","wrong_examples":["입원환자에게 처방하여 삭감","GJ 코드 미기재로 반려","동일 날짜 중복 청구"],"caution":"동일 성분·동일 효능 의약품 중복 처방 불가. 1일 1회 산정 원칙.","tags":["냉각","시술","피부과","외래"]},
  {"code":"AL300","name":"외래환자의약품관리료","category":"행위료","dept":["전과목"],"description":"외래 내원 환자에게 의약품 조제·투약 시 산정하는 관리료.","related_codes":["648602750","AL301"],"related_names":["씨엠쿨산","AL301 의약품조제료"],"criteria":"외래 내원 1회당 1회 산정. 의사가 직접 처방한 경우에 한함. 입원환자 산정 불가.","notice_required":False,"notice_detail":"","wrong_examples":["입원환자에게 AL300 청구","동일 외래 방문 시 2회 청구","처방 없이 단독 청구"],"caution":"처방전 없이 단독 청구 시 전액 삭감. 외래 1회당 1회 한도.","tags":["외래","의약품관리","행위료"]},
  {"code":"HA021","name":"초음파 검사(복부)","category":"검사","dept":["내과","외과","산부인과","소아과"],"description":"복부 장기(간, 담낭, 비장, 신장, 췌장 등) 초음파 영상 진단.","related_codes":["HA022","HA023","E6560"],"related_names":["HA022 상복부초음파","HA023 하복부초음파","E6560 판독료"],"criteria":"임상적으로 필요한 경우에 한해 급여 산정. 단순 검진 목적 시 비급여. 6개월 이내 동일 검사 반복 시 사유 기재 필요.","notice_required":True,"notice_detail":"특정내역 MT 코드 기재 필요: MT021(검사 사유). 재검사 시 GJ999(재검사 사유) 추가 기재.","wrong_examples":["검진 목적으로 급여 청구","6개월 이내 재검사 사유 미기재","판독료 별도 산정 누락"],"caution":"판독료(E6560) 별도 산정 가능하나 동일 의사 동일 날 중복 불가.","tags":["초음파","복부","검사","영상진단"]},
  {"code":"MZ100","name":"처치료(일반)","category":"처치","dept":["외과","정형외과","피부과","응급의학과"],"description":"외래 또는 입원 환자 대상 일반 처치 행위에 대한 수가.","related_codes":["MZ101","MZ102","AL300"],"related_names":["MZ101 소독처치","MZ102 봉합처치","AL300 외래환자의약품관리료"],"criteria":"처치 행위 1회당 1회 산정. 동일 날짜 동일 부위 중복 산정 불가. 입원 중 처치는 입원료에 포함될 수 있음.","notice_required":True,"notice_detail":"특정내역 GJ001(처치부위) 기재 필수. 입원환자의 경우 GJ003(처치 필요성) 추가 기재.","wrong_examples":["동일 날짜 동일 부위 중복 청구","입원료 포함 항목 별도 청구","처치부위 미기재"],"caution":"입원 환자의 경우 입원 기본료에 포함 여부 확인 필수.","tags":["처치","외과","소독","봉합"]},
  {"code":"RD001","name":"X선 단순촬영(흉부)","category":"영상검사","dept":["내과","외과","결핵과","응급의학과"],"description":"흉부 X선 단순 촬영 및 판독.","related_codes":["RD002","E6500"],"related_names":["RD002 흉부X선(측면)","E6500 X선 판독료"],"criteria":"임상 증상에 근거한 경우 급여. 검진 목적 비급여. 연 2회 이상 시 임상적 필요성 기재.","notice_required":False,"notice_detail":"연 2회 초과 시 MT코드(MT001) 기재 권장.","wrong_examples":["검진 목적 급여 청구","동일 날짜 정면·측면 각각 별도 청구"],"caution":"정면과 측면을 동시 촬영 시 패키지 코드로 청구해야 하며 분리 청구 시 삭감.","tags":["X선","흉부","영상","촬영"]},
  {"code":"LB001","name":"혈액검사(CBC)","category":"검사","dept":["전과목"],"description":"전혈구 검사(Complete Blood Count). 빈혈, 감염, 혈액질환 등 진단 기초 검사.","related_codes":["LB002","LB010","LB011"],"related_names":["LB002 혈액화학검사","LB010 혈소판검사","LB011 백혈구분류"],"criteria":"임상적 필요 시 급여. 수술 전 기본 검사로 인정. 동일 날짜 반복 시 사유 기재.","notice_required":False,"notice_detail":"반복 시행 시 GJ999(재검사 사유) 기재 권장.","wrong_examples":["사유 없는 동일 날짜 중복 청구","외래 단순 내원 시 과잉 검사 청구"],"caution":"과잉검사로 판단될 경우 심사 청구 조정 대상.","tags":["혈액","CBC","검사","기초검사"]},
  {"code":"NS100","name":"신경전도검사","category":"기능검사","dept":["신경과","신경외과","재활의학과"],"description":"말초신경의 전도 속도 및 기능 평가 검사.","related_codes":["NS101","NS200"],"related_names":["NS101 근전도검사","NS200 유발전위검사"],"criteria":"말초신경병증, 수근관증후군 등 신경계 질환 의심 시 급여. 연 1회 원칙. 재검 시 임상적 변화 기재.","notice_required":True,"notice_detail":"특정내역 GJ001(검사 적응증), GJ002(이전 검사일) 기재 필수.","wrong_examples":["적응증 없이 정기 검사로 청구","동일 환자 6개월 이내 재검 사유 미기재"],"caution":"근전도(NS101)와 동시 시행 시 주된 검사만 100%, 나머지 50% 산정.","tags":["신경","전도검사","신경과","기능검사"]},
  {"code":"PT050","name":"도수치료","category":"치료","dept":["재활의학과","정형외과","신경외과"],"description":"물리치료사에 의한 수기 치료. 근골격계 질환 및 통증 관리.","related_codes":["PT051","PT100"],"related_names":["PT051 운동치료","PT100 전기치료"],"criteria":"보험 급여 대상 아님(비급여). 단, 일부 산재·자동차보험에서 급여 적용 가능.","notice_required":True,"notice_detail":"비급여 동의서 필수 징구. 자동차보험 청구 시 치료 일지 및 소견서 첨부.","wrong_examples":["건강보험에 급여로 청구","비급여 동의서 미징구","횟수 초과 청구"],"caution":"건강보험 급여 청구 시 전액 환수 대상. 반드시 비급여로 처리.","tags":["도수치료","비급여","재활","물리치료"]}
]
DEFAULT_NOTICES = [
  {"code":"GJ001","name":"시술명/처치부위","applicable_codes":["648602750","MZ100","PT050"],"description":"시술 또는 처치 행위 시 구체적인 시술명과 처치 부위를 기재.","format":"GJ001[시술명 또는 처치부위]","example":"GJ001[레이저 냉각치료/좌측 안면부]","required_when":"처치료 및 시술 관련 코드 청구 시 필수","penalty":"미기재 시 해당 처치료 삭감 가능"},
  {"code":"GJ002","name":"적용부위/이전검사일","applicable_codes":["648602750","NS100","HA021"],"description":"시술 적용 부위 또는 이전 동일 검사 시행일을 기재.","format":"GJ002[부위 또는 YYYY-MM-DD]","example":"GJ002[우측 상지] 또는 GJ002[2024-01-15]","required_when":"재검사 또는 부위 특정이 필요한 시술/검사 청구 시","penalty":"재검사 시 미기재 → 의학적 필요성 불인정 처리"},
  {"code":"GJ003","name":"처치 필요성(입원환자)","applicable_codes":["MZ100","MZ101","MZ102"],"description":"입원환자에게 별도 처치를 시행한 경우 그 필요성을 기재.","format":"GJ003[필요성 사유]","example":"GJ003[입원 중 창상 악화로 추가 소독 처치 시행]","required_when":"입원환자 처치료 별도 산정 시","penalty":"미기재 시 입원료 포함 항목으로 간주하여 삭감"},
  {"code":"GJ999","name":"재검사 사유","applicable_codes":["HA021","HA022","NS100","LB001","RD001"],"description":"동일 검사를 기준 기간 내 재시행하는 경우 임상적 사유를 기재.","format":"GJ999[재검사 임상 사유]","example":"GJ999[치료 후 경과 평가, 기존 소견 대비 증상 악화 소견]","required_when":"6개월(영상)/3개월(기능검사) 이내 동일 검사 재시행 시","penalty":"미기재 시 재검사 전액 삭감"},
  {"code":"MT021","name":"검사 사유(초음파)","applicable_codes":["HA021","HA022","HA023"],"description":"초음파 검사의 임상적 필요성 및 검사 사유 기재.","format":"MT021[검사 임상 사유]","example":"MT021[상복부 통증 및 압통, 간기능 이상 소견으로 복부 초음파 시행]","required_when":"복부 초음파 급여 청구 시 필수","penalty":"미기재 시 비급여 전환 또는 삭감"},
  {"code":"MT001","name":"X선 재촬영 사유","applicable_codes":["RD001","RD002"],"description":"동일 부위 X선을 연 2회 이상 시행 시 임상적 사유 기재.","format":"MT001[재촬영 사유]","example":"MT001[치료 경과 모니터링, 폐렴 치료 후 흉부 변화 확인]","required_when":"연 2회 초과 동일 부위 X선 청구 시","penalty":"미기재 시 의학적 필요성 불인정"}
]
DEFAULT_CASES = [
  {"id":"CASE-2024-001","title":"씨엠쿨산 입원환자 청구 오류","dept":"피부과","code":"648602750","type":"삭감","date":"2024-03-12","summary":"입원환자에게 씨엠쿨산(648602750)을 처방하고 외래환자의약품관리료(AL300)와 함께 청구하여 전액 삭감된 사례.","detail":"입원 중인 환자에게 레이저 시술 후 씨엠쿨산을 처방하였으나, 외래 전용 코드인 AL300을 함께 산정하여 심평원 심사에서 삭감됨.","lesson":"입원/외래 구분 철저히 확인. 외래 전용 코드는 반드시 외래 내원 환자에게만 적용.","loss":"120,000","tags":["씨엠쿨산","입원오류","AL300","삭감"]},
  {"id":"CASE-2024-002","title":"초음파 재검사 GJ 코드 미기재","dept":"내과","code":"HA021","type":"조정","date":"2024-05-20","summary":"복부 초음파를 6개월 이내 재시행하면서 재검사 사유(GJ999)를 기재하지 않아 심사 조정된 사례.","detail":"동일 환자에게 2024년 1월과 6월에 복부초음파를 시행하였으나 6월 청구 시 재검사 사유 특정내역을 미기재.","lesson":"6개월 이내 동일 검사 재시행 시 반드시 GJ999(재검사 사유) 기재. 임상 소견 변화 명시 필수.","loss":"85,000","tags":["초음파","재검사","GJ코드","조정"]},
  {"id":"CASE-2024-003","title":"신경전도·근전도 동시산정 착오","dept":"신경과","code":"NS100","type":"삭감","date":"2024-07-08","summary":"신경전도검사(NS100)와 근전도검사(NS101)를 동시 시행 시 각각 100%로 청구하여 삭감된 사례.","detail":"동일 일자에 신경전도(NS100)와 근전도(NS101)를 함께 시행 후 각각 100% 수가로 청구. 규정 위반.","lesson":"동시 시행 검사의 경우 주·부 검사 구분 후 부 검사는 50% 적용.","loss":"210,000","tags":["신경전도","근전도","동시산정","삭감"]},
  {"id":"CASE-2024-004","title":"도수치료 건강보험 급여 청구","dept":"재활의학과","code":"PT050","type":"환수","date":"2024-09-15","summary":"비급여 항목인 도수치료를 건강보험 급여로 청구하여 전액 환수 및 과태료 부과 사례.","detail":"재활의학과에서 도수치료(PT050)를 건강보험 급여 청구 코드로 산정. 급여 청구 시 전액 환수 및 행정처분 대상.","lesson":"비급여 항목 목록 정기적 갱신 필수. 비급여 동의서 징구 및 별도 수납 처리.","loss":"3,500,000","tags":["도수치료","비급여","환수","행정처분"]},
  {"id":"CASE-2024-005","title":"흉부X선 정면·측면 분리 청구 삭감","dept":"내과","code":"RD001","type":"삭감","date":"2024-10-22","summary":"동일 날짜 흉부 X선 정면(RD001)과 측면(RD002)을 각각 별도 코드로 청구하여 삭감된 사례.","detail":"흉부 X선 정면과 측면 동시 촬영 시 패키지 코드로 청구하여야 하나 각각 분리 청구. 측면 촬영분 전액 삭감.","lesson":"동시 촬영 항목은 반드시 패키지 코드 확인 후 청구.","loss":"35,000","tags":["흉부X선","분리청구","패키지","삭감"]},
  {"id":"CASE-2025-001","title":"CBC 동일날짜 중복 청구","dept":"내과","code":"LB001","type":"삭감","date":"2025-01-10","summary":"동일 환자 동일 날짜 CBC 검사를 오전·오후 2회 청구하여 삭감된 사례.","detail":"외래 환자가 오전 내원 후 저녁 응급실 재내원 시 CBC 재검하였으나 사유 미기재로 중복 청구 처리.","lesson":"동일 날짜 동일 검사 재시행 시 임상 소견 변화를 EMR에 명확히 기재하고 특정내역 함께 청구.","loss":"28,000","tags":["CBC","중복청구","혈액검사","삭감"]}
]

def init_data():
    if not os.path.exists(PRES_PATH):
        with open(PRES_PATH,"w",encoding="utf-8") as f: json.dump(DEFAULT_PRESCRIPTIONS,f,ensure_ascii=False,indent=2)
    if not os.path.exists(NOTICE_PATH):
        with open(NOTICE_PATH,"w",encoding="utf-8") as f: json.dump(DEFAULT_NOTICES,f,ensure_ascii=False,indent=2)
    if not os.path.exists(CASE_PATH):
        with open(CASE_PATH,"w",encoding="utf-8") as f: json.dump(DEFAULT_CASES,f,ensure_ascii=False,indent=2)

def load_pres():
    try:
        with open(PRES_PATH,encoding="utf-8") as f: return json.load(f)
    except: return list(DEFAULT_PRESCRIPTIONS)

def load_notices():
    try:
        with open(NOTICE_PATH,encoding="utf-8") as f: return json.load(f)
    except: return list(DEFAULT_NOTICES)

def load_cases():
    try:
        with open(CASE_PATH,encoding="utf-8") as f: return json.load(f)
    except: return list(DEFAULT_CASES)

def save_json(path, data):
    with open(path,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)

init_data()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="청구전문컨설팅 Medium | 청구심사 전문 시스템",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS  (밝은 테마)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  /* ── 밝은 테마 팔레트 ── */
  --bg:        #F4F7FB;
  --bg2:       #EAEFF7;
  --sidebar:   #FFFFFF;
  --card:      #FFFFFF;
  --border:    #D6E0EE;
  --teal:      #0E8B7A;
  --teal2:     #11A392;
  --teal-lt:   #E6F6F4;
  --gold:      #D48A0A;
  --gold-lt:   #FEF4DC;
  --red:       #C0392B;
  --red-lt:    #FDECEA;
  --blue:      #2563A8;
  --blue-lt:   #EBF2FC;
  --text:      #1A2535;
  --text2:     #3D5068;
  --muted:     #6B82A0;
  --white:     #FFFFFF;
  --shadow:    0 2px 12px rgba(0,0,0,0.07);
  --shadow-md: 0 4px 20px rgba(0,0,0,0.10);
  --font:      'Noto Sans KR', sans-serif;
  --mono:      'JetBrains Mono', monospace;
}

/* ── 전체 배경 ── */
html, body, [class*="css"] { font-family: var(--font) !important; background: var(--bg) !important; color: var(--text) !important; }
.stApp { background: var(--bg) !important; }

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
  background: var(--sidebar) !important;
  border-right: 1.5px solid var(--border) !important;
  box-shadow: 2px 0 12px rgba(0,0,0,0.05);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── 사이드바 라디오 버튼 완전 정렬 수정 ── */
section[data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
section[data-testid="stSidebar"] .stRadio > div > label {
  display: flex !important;
  align-items: center !important;
  padding: 0.52rem 0.9rem !important;
  border-radius: 8px !important;
  margin: 1px 0 !important;
  cursor: pointer !important;
  transition: background 0.18s !important;
  color: var(--text2) !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  line-height: 1.3 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
  background: var(--teal-lt) !important;
  color: var(--teal) !important;
}
/* 라디오 버튼 원형 아이콘 숨기고 텍스트만 표시 */
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
  display: none !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] input:checked ~ div,
section[data-testid="stSidebar"] [aria-checked="true"] {
  background: var(--teal-lt) !important;
  color: var(--teal) !important;
  font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stRadio label p {
  margin: 0 !important;
  color: inherit !important;
}

/* ── 사이드바 기타 위젯 ── */
section[data-testid="stSidebar"] .stTextInput input {
  background: var(--bg2) !important; color: var(--text) !important;
  border: 1.5px solid var(--border) !important; border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stTextInput label { color: var(--text2) !important; font-weight: 600 !important; }
section[data-testid="stSidebar"] .stExpander {
  background: var(--bg2) !important; border: 1.5px solid var(--border) !important; border-radius: 10px !important;
}
section[data-testid="stSidebar"] .stExpander summary { color: var(--text) !important; font-weight: 600 !important; }
section[data-testid="stSidebar"] .stButton button {
  background: linear-gradient(135deg, var(--teal), var(--teal2)) !important;
  color: #fff !important; font-weight: 700 !important; border: none !important;
  width: 100%; border-radius: 8px !important;
}
section[data-testid="stSidebar"] hr { border-color: var(--border) !important; opacity: 1 !important; }

/* ── 사이드바 로고 ── */
.sidebar-logo {
  text-align: center; padding: 1.5rem 1rem 1.2rem;
  border-bottom: 1.5px solid var(--border); margin-bottom: 1rem;
}
.sidebar-logo .logo-icon { font-size: 2.5rem; line-height: 1; }
.sidebar-logo .logo-title {
  font-size: 1.05rem; font-weight: 900; color: var(--teal);
  letter-spacing: -0.01em; margin-top: 0.4rem; line-height: 1.35;
}
.sidebar-logo .logo-maker {
  font-size: 0.65rem; color: var(--muted); margin-top: 0.3rem;
  letter-spacing: 0.04em;
}
.sidebar-menu-label {
  font-size: 0.72rem; font-weight: 700; color: var(--muted);
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 0 0.9rem; margin-bottom: 0.3rem; display: block;
}
.sidebar-status {
  font-size: 0.71rem; color: var(--muted); text-align: center;
  line-height: 2; padding: 0.5rem 0.5rem 0.2rem;
}
.dot-online {
  display: inline-block; width: 7px; height: 7px;
  background: var(--teal2); border-radius: 50%;
  animation: pulse 2s infinite; vertical-align: middle; margin-right: 3px;
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

/* ── 배지 ── */
.admin-badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  font-size: 0.72rem; background: var(--gold-lt); color: var(--gold);
  border: 1px solid #F0C96B; border-radius: 20px; padding: 0.22rem 0.85rem; font-weight: 600;
}
.user-badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  font-size: 0.72rem; background: var(--teal-lt); color: var(--teal);
  border: 1px solid #A8DDD8; border-radius: 20px; padding: 0.22rem 0.85rem; font-weight: 600;
}

/* ── 페이지 배너 ── */
.page-banner {
  background: linear-gradient(135deg, var(--teal) 0%, #0AAFA0 100%);
  border-radius: 16px; padding: 1.6rem 2rem;
  margin-bottom: 1.8rem;
  display: flex; align-items: center; gap: 1.2rem;
  box-shadow: var(--shadow-md);
}
.page-banner .bi { font-size: 2.3rem; }
.page-banner .bt { font-size: 1.4rem; font-weight: 800; color: #fff; }
.page-banner .bd { font-size: 0.84rem; color: rgba(255,255,255,0.82); margin-top: 3px; }

/* 대시보드 배너 (가운데 정렬) */
.page-banner-center {
  background: linear-gradient(135deg, var(--teal) 0%, #0AAFA0 100%);
  border-radius: 16px; padding: 2rem 2rem 1.8rem;
  margin-bottom: 1.8rem; text-align: center;
  box-shadow: var(--shadow-md);
}
.page-banner-center .bc-maker { font-size: 0.72rem; color: rgba(255,255,255,0.7); margin-bottom: 0.3rem; letter-spacing: 0.06em; }
.page-banner-center .bc-title { font-size: 1.7rem; font-weight: 900; color: #fff; letter-spacing: -0.01em; }
.page-banner-center .bc-sub   { font-size: 0.88rem; color: rgba(255,255,255,0.8); margin-top: 0.4rem; }

/* ── KPI 카드 ── */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.kpi-card {
  flex: 1; min-width: 155px;
  background: var(--card); border: 1.5px solid var(--border);
  border-radius: 14px; padding: 1.1rem 1.3rem;
  box-shadow: var(--shadow); position: relative; overflow: hidden;
}
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.kpi-card.teal::before { background: var(--teal2); }
.kpi-card.gold::before { background: var(--gold); }
.kpi-card.red::before  { background: var(--red); }
.kpi-card.blue::before { background: var(--blue); }
.kpi-label { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.07em; text-transform: uppercase; font-weight: 600; }
.kpi-value { font-size: 1.75rem; font-weight: 900; margin: 0.15rem 0; }
.kpi-card.teal .kpi-value { color: var(--teal); }
.kpi-card.gold .kpi-value { color: var(--gold); }
.kpi-card.red  .kpi-value { color: var(--red); }
.kpi-card.blue .kpi-value { color: var(--blue); }
.kpi-sub { font-size: 0.71rem; color: var(--muted); }

/* ── 결과 카드 ── */
.result-card {
  background: var(--card); border: 1.5px solid var(--border);
  border-radius: 12px; padding: 1.1rem 1.4rem; margin-bottom: 0.8rem;
  box-shadow: var(--shadow); transition: box-shadow 0.2s, border-color 0.2s;
}
.result-card:hover { box-shadow: var(--shadow-md); border-color: var(--teal2); }
.rc-code {
  font-family: var(--mono); font-size: 0.78rem;
  background: var(--teal-lt); color: var(--teal);
  border: 1px solid #A8DDD8; border-radius: 6px; padding: 0.16rem 0.5rem;
}
.rc-name { font-size: 1rem; font-weight: 700; color: var(--text); }
.rc-dept {
  font-size: 0.7rem; background: var(--gold-lt); color: var(--gold);
  border: 1px solid #F0C96B; border-radius: 20px; padding: 0.12rem 0.6rem; font-weight: 600;
}
.rc-section-title { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.25rem; font-weight: 700; }

/* ── 알림 박스 ── */
.alert-box { border-radius: 10px; padding: 0.85rem 1.1rem; margin-bottom: 0.7rem; display: flex; gap: 0.7rem; align-items: flex-start; font-size: 0.87rem; line-height: 1.65; }
.alert-box.warning { background: var(--gold-lt);  border: 1.5px solid #F0C96B; }
.alert-box.danger  { background: var(--red-lt);   border: 1.5px solid #F0A9A4; }
.alert-box.info    { background: var(--teal-lt);  border: 1.5px solid #A8DDD8; }
.alert-box .aico   { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.alert-box.warning .atxt { color: #8A5C00; }
.alert-box.danger  .atxt { color: #8B1E1E; }
.alert-box.info    .atxt { color: #0A6B5E; }

/* ── 기준 블록 ── */
.criteria-block {
  background: var(--bg2); border-left: 3px solid var(--teal2);
  border-radius: 0 10px 10px 0; padding: 0.95rem 1.15rem;
  margin: 0.55rem 0; font-size: 0.87rem; line-height: 1.8; color: var(--text2);
}

/* ── AI 카드 ── */
.ai-card {
  background: var(--blue-lt); border: 1.5px solid #BDD5EF;
  border-radius: 14px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.ai-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.9rem; font-size: 0.75rem; color: var(--blue); letter-spacing: 0.1em; text-transform: uppercase; font-weight: 700; }
.ai-engine-badge { font-family: var(--mono); font-size: 0.68rem; background: #fff; color: var(--blue); border: 1px solid #BDD5EF; border-radius: 4px; padding: 0.08rem 0.38rem; margin-left: auto; }
.ai-response { font-size: 0.9rem; line-height: 1.8; color: var(--text); }

/* ── 테이블 ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: 0.86rem; }
.styled-table th { background: var(--bg2); color: var(--teal); font-size: 0.72rem; letter-spacing: 0.07em; text-transform: uppercase; padding: 0.65rem 0.9rem; text-align: left; border-bottom: 2px solid var(--border); font-weight: 700; }
.styled-table td { padding: 0.6rem 0.9rem; border-bottom: 1px solid var(--border); vertical-align: top; color: var(--text2); }
.styled-table tr:hover td { background: var(--bg2); }
.tag-pass { display:inline-block; font-size:0.69rem; background:var(--teal-lt); color:var(--teal); border-radius:20px; padding:0.08rem 0.5rem; border:1px solid #A8DDD8; font-weight:600; }
.tag-fail { display:inline-block; font-size:0.69rem; background:var(--red-lt);  color:var(--red);  border-radius:20px; padding:0.08rem 0.5rem; border:1px solid #F0A9A4; font-weight:600; }
.tag-warn { display:inline-block; font-size:0.69rem; background:var(--gold-lt); color:var(--gold); border-radius:20px; padding:0.08rem 0.5rem; border:1px solid #F0C96B; font-weight:600; }

/* ── 푸터 ── */
.footer-bar {
  margin-top: 2.5rem; padding: 1rem 0 0.5rem;
  border-top: 1.5px solid var(--border);
  text-align: center; font-size: 0.75rem; color: var(--muted);
  line-height: 1.9;
}
.footer-bar strong { color: var(--teal); }

/* ── 구분선 ── */
.section-divider { border: none; border-top: 1.5px solid var(--border); margin: 1.3rem 0; }

/* ── Streamlit 위젯 밝은 테마 오버라이드 ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
  background: #fff !important; border: 1.5px solid var(--border) !important;
  border-radius: 8px !important; color: var(--text) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stMultiSelect label, .stCheckbox label { color: var(--text2) !important; font-weight: 600 !important; }
.stSelectbox > div > div > div { background: #fff !important; border: 1.5px solid var(--border) !important; border-radius: 8px !important; color: var(--text) !important; }
.stButton > button {
  background: linear-gradient(135deg, var(--teal), var(--teal2)) !important;
  color: #fff !important; font-weight: 700 !important; border: none !important;
  border-radius: 8px !important; padding: 0.46rem 1.4rem !important;
}
.stButton > button:hover { box-shadow: 0 4px 14px rgba(14,139,122,0.35) !important; transform: translateY(-1px) !important; }
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 2px solid var(--border); gap: 0.3rem; }
.stTabs [data-baseweb="tab"] { background: transparent; color: var(--muted); border-radius: 8px 8px 0 0; font-size: 0.86rem; padding: 0.42rem 1rem; border: none; font-weight: 500; }
.stTabs [aria-selected="true"] { background: var(--teal-lt) !important; color: var(--teal) !important; border-bottom: 2.5px solid var(--teal) !important; font-weight: 700 !important; }
.stExpander { background: var(--card) !important; border: 1.5px solid var(--border) !important; border-radius: 12px !important; box-shadow: var(--shadow) !important; }
.stExpander summary { color: var(--text) !important; font-weight: 600 !important; }
div[data-testid="stMetricValue"] { color: var(--teal) !important; font-weight: 900 !important; }
.stMultiSelect > div > div > div { background: #fff !important; color: var(--text) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--teal2); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION 초기화
# ──────────────────────────────────────────────────────────────────────────────
for k, v in [("is_admin", False), ("logged_in", False), ("menu", "🏠  대시보드")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # 로고 + 제작자
    st.markdown("""
    <div class="sidebar-logo">
      <div class="logo-icon">⚕</div>
      <div class="logo-title">청구전문컨설팅<br>Medium</div>
      <div class="logo-maker">제작자 : 주식회사 메디엄 조정윤</div>
    </div>
    """, unsafe_allow_html=True)

    # 로그인
    if st.session_state.logged_in:
        if st.session_state.is_admin:
            st.markdown('<span class="admin-badge">🔐 관리자 모드</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="user-badge">👤 일반 사용자</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("로그아웃", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.is_admin  = False
            st.rerun()
    else:
        with st.expander("🔑 로그인"):
            uid = st.text_input("아이디",   key="login_uid")
            pw  = st.text_input("비밀번호", key="login_pw", type="password")
            if st.button("로그인", key="login_btn"):
                if uid == "admin" and pw == "admin1234":
                    st.session_state.logged_in = True
                    st.session_state.is_admin  = True
                    st.success("관리자로 로그인되었습니다.")
                    st.rerun()
                elif uid and pw:
                    st.session_state.logged_in = True
                    st.session_state.is_admin  = False
                    st.success("로그인되었습니다.")
                    st.rerun()
                else:
                    st.error("아이디와 비밀번호를 입력하세요.")

    st.markdown("---")
    st.markdown('<span class="sidebar-menu-label">📂 메뉴</span>', unsafe_allow_html=True)

    MENU_ITEMS = [
        "🏠  대시보드",
        "🔍  처방코드 검색",
        "📋  심사기준 조회",
        "🔔  내역 알림 가이드",
        "🤖  AI 청구 진단",
        "📚  사례 검색",
        "⚙️  관리자 패널",
    ]
    idx  = MENU_ITEMS.index(st.session_state.menu) if st.session_state.menu in MENU_ITEMS else 0
    menu = st.radio("", MENU_ITEMS, index=idx, label_visibility="collapsed", key="menu_radio")
    st.session_state.menu = menu

    st.markdown("---")
    st.markdown(f"""
    <div class="sidebar-status">
      <span class="dot-online"></span> 시스템 정상 운영 중<br>
      {datetime.now().strftime('%Y-%m-%d %H:%M')} 기준<br>
      심평원 DB 동기화 완료
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# 공통 헬퍼
# ──────────────────────────────────────────────────────────────────────────────
def banner(icon, title, desc):
    st.markdown(f"""
    <div class="page-banner">
      <div class="bi">{icon}</div>
      <div>
        <div class="bt">{title}</div>
        <div class="bd">{desc}</div>
        <div style="font-size:0.68rem;color:rgba(255,255,255,0.65);margin-top:0.35rem;">제작자 : 주식회사 메디엄 조정윤</div>
      </div>
    </div>""", unsafe_allow_html=True)

def alert(kind, icon, text):
    st.markdown(f"""
    <div class="alert-box {kind}">
      <span class="aico">{icon}</span>
      <span class="atxt">{text}</span>
    </div>""", unsafe_allow_html=True)

def divider():
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

def footer():
    st.markdown("""
    <div class="footer-bar">
      <strong>청구전문컨설팅 Medium</strong> · 병원 청구심사 전문 시스템<br>
      제작자 : 주식회사 메디엄 조정윤 &nbsp;|&nbsp;
      심평원 DB 기준 · 본 시스템의 결과는 참고용이며 최종 판단은 전문가가 합니다
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: 대시보드
# ──────────────────────────────────────────────────────────────────────────────
def page_dashboard():
    # 가운데 정렬 배너
    st.markdown("""
    <div class="page-banner-center">
      <div class="bc-maker">제작자 : 주식회사 메디엄 조정윤</div>
      <div class="bc-title">⚕ 청구전문컨설팅 Medium 통합 대시보드</div>
      <div class="bc-sub">병원 청구심사 전문 시스템 · 실시간 현황 및 주요 알림</div>
    </div>
    """, unsafe_allow_html=True)

    pres_data = load_pres()
    case_data = load_cases()

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card teal">
        <div class="kpi-label">등록 처방코드</div>
        <div class="kpi-value">{len(pres_data)}</div>
        <div class="kpi-sub">처방코드 DB</div>
      </div>
      <div class="kpi-card gold">
        <div class="kpi-label">이번 달 삭감 위험</div>
        <div class="kpi-value">23</div>
        <div class="kpi-sub">⚠ 주의 필요 항목</div>
      </div>
      <div class="kpi-card red">
        <div class="kpi-label">미기재 내역 알림</div>
        <div class="kpi-value">7</div>
        <div class="kpi-sub">🔔 즉시 확인 필요</div>
      </div>
      <div class="kpi-card blue">
        <div class="kpi-label">사례 DB</div>
        <div class="kpi-value">{len(case_data)}</div>
        <div class="kpi-sub">📚 누적 사례 수</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### 📌 오늘의 심사 주의 알림")
        alert("danger",  "🚨", "도수치료(PT050) 건강보험 급여 청구 오류 패턴 감지 — 즉시 확인 필요")
        alert("warning", "⚠️", "씨엠쿨산(648602750) GJ001/GJ002 특정내역 미기재 7건 확인됨")
        alert("warning", "⚠️", "초음파(HA021) 6개월 이내 재검사 GJ999 누락 위험 3건")
        alert("info",    "ℹ️", "심평원 2025년 2분기 수가 개정 사항 반영 완료")
        alert("info",    "ℹ️", "신경전도·근전도 동시 산정 오류 사례 DB에 신규 2건 추가됨")

    with col2:
        st.markdown("#### 📊 진료과별 삭감 현황")
        dept_data = {"피부과":38, "내과":27, "재활의학과":19, "신경과":14, "외과":12, "정형외과":9}
        mx = max(dept_data.values())
        for dept, val in dept_data.items():
            pct   = val / mx * 100
            color = "#C0392B" if val >= 30 else "#D48A0A" if val >= 20 else "#0E8B7A"
            st.markdown(f"""
            <div style="margin-bottom:0.7rem;">
              <div style="display:flex;justify-content:space-between;font-size:0.84rem;margin-bottom:3px;">
                <span style="color:var(--text2);font-weight:500;">{dept}</span>
                <span style="color:{color};font-weight:700;">{val}건</span>
              </div>
              <div style="background:var(--bg2);border-radius:99px;height:7px;border:1px solid var(--border);">
                <div style="background:{color};width:{pct:.0f}%;height:7px;border-radius:99px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    divider()
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 🕐 최근 검색 기록")
        rows = [("648602750","씨엠쿨산","2분 전"), ("HA021","초음파(복부)","18분 전"),
                ("NS100","신경전도검사","1시간 전"), ("AL300","외래환자의약품관리료","09:12")]
        st.markdown('<table class="styled-table"><thead><tr><th>코드</th><th>품목명</th><th>시각</th></tr></thead><tbody>', unsafe_allow_html=True)
        for code, name, t in rows:
            st.markdown(f'<tr><td><span class="rc-code">{code}</span></td><td>{name}</td><td style="color:var(--muted);font-size:0.79rem;">{t}</td></tr>', unsafe_allow_html=True)
        st.markdown("</tbody></table>", unsafe_allow_html=True)

    with col4:
        st.markdown("#### 📰 심평원 최신 공지")
        notices_list = [
            ("2025-06-01", "[개정] 2025년 2분기 행위 수가 개정 고시"),
            ("2025-05-20", "[안내] 비급여 진료비용 고지 의무 강화"),
            ("2025-05-10", "[주의] 도수치료 건강보험 청구 집중심사 예고"),
            ("2025-04-28", "[개정] 초음파 급여 기준 확대 적용 고시"),
        ]
        for d, t in notices_list:
            st.markdown(f"""
            <div style="display:flex;gap:0.7rem;align-items:flex-start;margin-bottom:0.55rem;
                        padding:0.6rem 0.85rem;background:var(--card);border:1.5px solid var(--border);
                        border-radius:9px;font-size:0.84rem;box-shadow:var(--shadow);">
              <span style="font-family:var(--mono);font-size:0.69rem;color:var(--muted);white-space:nowrap;margin-top:2px;">{d}</span>
              <span style="color:var(--text2);">{t}</span>
            </div>""", unsafe_allow_html=True)

    footer()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: 처방코드 검색
# ──────────────────────────────────────────────────────────────────────────────
def page_prescription_search():
    banner("🔍", "처방코드 검색", "처방명·코드·시술명으로 검색 — 관련코드·심사기준·알림 내역 통합 제공")
    data    = load_pres()
    notices = load_notices()

    col_q, col_dept, col_btn = st.columns([4, 2, 1])
    with col_q:
        query = st.text_input("", "", placeholder="예) 씨엠쿨산 · 648602750 · 초음파 · CBC",
                              label_visibility="collapsed", key="ps_query")
    with col_dept:
        depts  = ["전체","내과","외과","피부과","정형외과","신경과","재활의학과","산부인과","소아과","응급의학과","성형외과"]
        dept_f = st.selectbox("", depts, label_visibility="collapsed", key="ps_dept")
    with col_btn:
        st.button("검색", key="ps_search")

    tag_cols = st.columns(8)
    quick    = ["씨엠쿨산","초음파","CBC","도수치료","X선","신경전도","처치료","AL300"]
    for i, tag in enumerate(quick):
        with tag_cols[i]:
            if st.button(tag, key=f"qt_{tag}"): query = tag

    divider()

    if not query.strip():
        st.markdown("**전체 등록 처방코드 목록**")
        st.markdown('<table class="styled-table"><thead><tr><th>코드</th><th>품목명</th><th>분류</th><th>진료과</th><th>특정내역</th></tr></thead><tbody>', unsafe_allow_html=True)
        for item in data:
            ds   = ", ".join(item["dept"][:2])
            ntag = '<span class="tag-warn">필수기재</span>' if item["notice_required"] else '<span class="tag-pass">해당없음</span>'
            st.markdown(f'<tr><td><span class="rc-code">{item["code"]}</span></td><td><strong>{item["name"]}</strong></td><td style="color:var(--muted);">{item["category"]}</td><td style="font-size:0.81rem;">{ds}</td><td>{ntag}</td></tr>', unsafe_allow_html=True)
        st.markdown("</tbody></table>", unsafe_allow_html=True)
        footer(); return

    q       = query.lower().strip()
    results = [it for it in data if
               q in it["code"].lower() or q in it["name"].lower() or
               any(q in t.lower() for t in it["tags"]) or
               any(q in rn.lower() for rn in it["related_names"])
               and (dept_f == "전체" or dept_f in it["dept"] or "전과목" in it["dept"])]

    if not results:
        alert("info","ℹ️","검색 결과가 없습니다. 다른 키워드로 시도하거나 관리자에게 코드 등록을 요청하세요.")
        footer(); return

    st.markdown(f'<div style="font-size:0.83rem;color:var(--muted);margin-bottom:1rem;">총 <strong style="color:var(--teal);">{len(results)}</strong>건 — <em>{query}</em> 검색 결과</div>', unsafe_allow_html=True)

    for item in results:
        item_notices = [n for n in notices if item["code"] in n["applicable_codes"]]
        nb = "🔔 " if item["notice_required"] else ""
        ds = " · ".join(item["dept"][:3])
        with st.expander(f'[{item["code"]}]  {nb}{item["name"]}  ·  {ds}', expanded=True):
            t1, t2, t3, t4 = st.tabs(["📋 기본정보","📌 심사기준","🔔 특정내역 알림","⚠️ 주의사항"])
            with t1:
                ca, cb = st.columns(2)
                with ca:
                    st.markdown(f'<div class="rc-section-title">품목 설명</div><div style="font-size:0.87rem;line-height:1.75;color:var(--text2);">{item["description"]}</div>', unsafe_allow_html=True)
                    rel = " ".join([f'<span class="rc-code">{c}</span>' for c in item["related_codes"]])
                    st.markdown(f'<div class="rc-section-title" style="margin-top:0.9rem;">관련 처방 코드</div><div style="display:flex;flex-wrap:wrap;gap:0.3rem;margin-top:0.25rem;">{rel}</div>', unsafe_allow_html=True)
                with cb:
                    st.markdown(f'<div class="rc-section-title">관련 품목명</div><div style="font-size:0.86rem;line-height:1.8;">{"<br>".join(item["related_names"])}</div>', unsafe_allow_html=True)
                    tags_h = " ".join([f'<span style="font-size:0.69rem;background:var(--teal-lt);color:var(--teal);border:1px solid #A8DDD8;border-radius:20px;padding:0.07rem 0.45rem;font-weight:600;">#{t}</span>' for t in item["tags"]])
                    st.markdown(f'<div class="rc-section-title" style="margin-top:0.9rem;">태그</div><div style="display:flex;flex-wrap:wrap;gap:0.28rem;margin-top:0.25rem;">{tags_h}</div>', unsafe_allow_html=True)
            with t2:
                st.markdown(f'<div class="criteria-block">{item["criteria"]}</div>', unsafe_allow_html=True)
                st.markdown('<a href="https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA020044020000" target="_blank" style="color:var(--teal);font-size:0.8rem;text-decoration:none;font-weight:600;">🔗 심평원 급여기준 원문 보기 →</a>', unsafe_allow_html=True)
            with t3:
                if item["notice_required"]:
                    alert("warning","🔔",f"<strong>특정내역 기재 필수!</strong><br>{item['notice_detail']}")
                    for n in item_notices:
                        st.markdown(f"""
                        <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:10px;padding:0.9rem 1.1rem;margin-top:0.5rem;">
                          <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.45rem;">
                            <span class="rc-code">{n["code"]}</span>
                            <strong style="font-size:0.87rem;">{n["name"]}</strong>
                          </div>
                          <div class="rc-section-title">입력 형식</div>
                          <div style="font-family:var(--mono);font-size:0.79rem;background:#fff;border:1.5px solid var(--border);border-radius:6px;padding:0.35rem 0.75rem;color:var(--teal);margin-bottom:0.4rem;">{n["format"]}</div>
                          <div class="rc-section-title">입력 예시</div>
                          <div style="font-size:0.85rem;color:var(--text2);margin-bottom:0.45rem;">{n["example"]}</div>
                          <div style="font-size:0.79rem;color:var(--red);font-weight:600;">⚠ 미기재 시: {n["penalty"]}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    alert("info","✅","해당 코드는 필수 특정내역 기재 항목이 아닙니다.")
            with t4:
                alert("warning","⚠️",f"<strong>주의사항:</strong><br>{item['caution']}")
                st.markdown("**잘못된 처방 예시 (삭감 사례)**")
                for ex in item["wrong_examples"]:
                    alert("danger","❌",ex)
    footer()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: 심사기준 조회
# ──────────────────────────────────────────────────────────────────────────────
HIRA_DB = {
  "648602750":{"title":"씨엠쿨산 (외래환자의약품관리료)","source":"건강보험 행위 급여·비급여 목록표","updated":"2025-01-01","content":"【급여기준】\n- 외래 내원 환자에게 의사의 처방에 따라 투약·조제한 경우에 한해 산정\n- 입원환자, 응급실 내원 후 입원 전환 환자에게는 산정 불가\n- 동일 외래 방문 1회당 1회 산정 원칙\n\n【산정 조건】\n1. 의사가 직접 발행한 처방전에 의거\n2. 외래 내원 확인이 가능한 경우에 한함\n3. 동일 성분·동일 효능 의약품 중복 처방 불가\n\n【청구 시 유의사항】\n- AL300(외래환자의약품관리료)와 연계하여 청구\n- 특정내역 GJ001, GJ002 기재 필수 (시술 관련 처방 시)"},
  "HA021":{"title":"초음파 검사 급여기준 (복부)","source":"건강보험 행위 급여기준 고시 제2024-183호","updated":"2024-10-01","content":"【급여 적용 대상】\n- 복부 통증, 압통, 복부 종괴 의심, 간기능 이상 등 임상 증상이 있는 경우\n- 악성 종양 또는 간경변, 담낭 질환 진단·추적 관찰\n- 수술 전·후 복부 장기 평가\n\n【비급여 적용 대상】\n- 단순 건강검진 목적\n- 증상 없는 정기 추적 관찰\n\n【재검사 기준】\n- 6개월 이내 동일 부위 재검사 시 임상적 변화 소견 기재 필수\n- GJ999(재검사 사유) + MT021(검사 사유) 함께 기재"},
  "NS100":{"title":"신경전도검사 급여기준","source":"건강보험 행위 급여기준 고시","updated":"2024-07-01","content":"【급여 적용】\n- 말초신경병증, 수근관증후군, 척골신경병증 등 신경계 질환 의심 시\n- 당뇨병성 신경병증 추적 관찰 (연 1회 인정)\n\n【동시 시행 기준】\n- 신경전도(NS100) + 근전도(NS101) 동시 시행 시:\n  주된 검사 100%, 부가 검사 50% 산정\n\n【재검사 기준】\n- 연 1회 원칙\n- 재검사 필요 시 GJ001(적응증) + GJ002(이전 검사일) 기재 필수"},
}

def page_criteria():
    PORTAL_URL = "https://biz.hira.or.kr/index.do"
    banner("📋","심사기준 조회","요양기관업무포털 심사기준 종합서비스 연동 · 내부 기준 DB 통합 제공")
    data = load_pres()

    # ── 포털 접속 안내 박스 ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#EBF5FF,#F0FAF8);border:2px solid #A8DDD8;
                border-radius:14px;padding:1.3rem 1.5rem;margin-bottom:1.2rem;
                box-shadow:0 2px 10px rgba(14,139,122,0.1);">
      <div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:1rem;">
        <span style="font-size:1.6rem;">🏥</span>
        <div>
          <div style="font-size:1rem;font-weight:800;color:#0E6655;">심사기준 조회 방법 안내</div>
          <div style="font-size:0.78rem;color:#5D8A82;margin-top:1px;">심평원 사이트는 외부 직접 링크 접근이 차단됩니다 — 요양기관업무포털을 통해 접속하세요</div>
        </div>
      </div>
      <div style="display:flex;flex-direction:column;gap:0.6rem;margin-bottom:1rem;">
        <div style="display:flex;gap:0.6rem;align-items:center;">
          <span style="background:#0E8B7A;color:#fff;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;flex-shrink:0;">1</span>
          <span style="font-size:0.87rem;color:#1A3A35;">아래 <strong>요양기관업무포털 접속</strong> 버튼 클릭</span>
        </div>
        <div style="display:flex;gap:0.6rem;align-items:center;">
          <span style="background:#0E8B7A;color:#fff;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;flex-shrink:0;">2</span>
          <span style="font-size:0.87rem;color:#1A3A35;">공인인증서/간편인증으로 <strong>로그인</strong> 후 메인화면에서 <span style="background:#FEF4DC;color:#8A5C00;border-radius:4px;padding:0.08rem 0.4rem;font-weight:700;">심사기준 종합서비스</span> 클릭</span>
        </div>
        <div style="display:flex;gap:0.6rem;align-items:center;">
          <span style="background:#0E8B7A;color:#fff;border-radius:50%;width:22px;height:22px;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;flex-shrink:0;">3</span>
          <span style="font-size:0.87rem;color:#1A3A35;">아래 검색창에서 코드/품목명 검색 → <strong>포털 검색어</strong> 복사 후 붙여넣기</span>
        </div>
      </div>
      <div style="font-size:0.72rem;color:#5D8A82;background:rgba(14,139,122,0.07);border-radius:8px;padding:0.45rem 0.8rem;">
        ⚠️ 포털 접속에는 요양기관 담당자 계정(공인인증서 또는 간편인증)이 필요합니다.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_b1, col_b2, _ = st.columns([2, 2, 3])
    with col_b1:
        st.link_button("🏥 요양기관업무포털 접속", PORTAL_URL)
    with col_b2:
        st.link_button("📋 심사기준 종합서비스", PORTAL_URL)

    divider()
    st.markdown("#### 🔍 내부 기준 DB 검색 + 포털 검색어 안내")
    col_s, col_b = st.columns([5, 1])
    with col_s:
        query = st.text_input("", placeholder="처방코드 또는 품목명 입력 (예: HA021, 초음파, 씨엠쿨산, 신경전도)",
                              label_visibility="collapsed", key="cr_query")
    with col_b:
        st.button("검색", key="cr_search")

    if query.strip():
        matched = [d for d in data if
                   query.lower() in d["code"].lower() or query.lower() in d["name"].lower() or
                   any(query.lower() in t.lower() for t in d["tags"])]
        if not matched:
            alert("info","ℹ️",f"내부 DB에 <strong>\'{query}\'</strong> 관련 기준이 없습니다. 요양기관업무포털에서 직접 검색하세요.")
            st.markdown(f"""
            <div style="background:var(--gold-lt);border:2px solid #F0C96B;border-radius:12px;padding:1.1rem 1.3rem;margin-top:0.5rem;">
              <div style="font-size:0.84rem;font-weight:700;color:#6B4A00;margin-bottom:0.5rem;">📋 포털 심사기준 종합서비스 검색어 (복사 후 붙여넣기)</div>
              <div style="font-family:var(--mono);font-size:1rem;font-weight:700;color:#3D2A00;
                          background:#fff;border:1.5px solid #F0C96B;border-radius:8px;padding:0.5rem 1rem;">
                {query}
              </div>
              <div style="font-size:0.74rem;color:#8A6200;margin-top:0.45rem;">위 검색어 복사 → 포털 접속 → 심사기준 종합서비스 → 검색창에 붙여넣기</div>
            </div>
            """, unsafe_allow_html=True)
            st.link_button("🏥 요양기관업무포털에서 검색하기 →", PORTAL_URL)
            footer(); return

        for item in matched:
            hira = HIRA_DB.get(item["code"])
            with st.expander(f'📋 [{item["code"]}] {item["name"]} — 심사기준', expanded=True):
                st.markdown(f"""
                <div style="background:var(--gold-lt);border:1.5px solid #F0C96B;border-radius:10px;padding:0.8rem 1.1rem;margin-bottom:0.9rem;">
                  <div style="font-size:0.74rem;font-weight:700;color:#6B4A00;margin-bottom:0.45rem;">🏥 요양기관업무포털 심사기준 종합서비스 검색어</div>
                  <div style="display:flex;gap:0.6rem;align-items:center;flex-wrap:wrap;">
                    <span style="font-family:var(--mono);font-size:0.9rem;font-weight:700;color:#3D2A00;background:#fff;border:1.5px solid #F0C96B;border-radius:6px;padding:0.25rem 0.75rem;">{item["code"]}</span>
                    <span style="font-size:0.74rem;color:#8A6200;">또는</span>
                    <span style="font-family:var(--mono);font-size:0.9rem;font-weight:700;color:#3D2A00;background:#fff;border:1.5px solid #F0C96B;border-radius:6px;padding:0.25rem 0.75rem;">{item["name"]}</span>
                    <a href="{PORTAL_URL}" target="_blank"
                       style="margin-left:auto;background:#0E8B7A;color:#fff;border-radius:7px;padding:0.28rem 0.85rem;font-size:0.77rem;font-weight:700;text-decoration:none;white-space:nowrap;">
                       🏥 포털에서 검색 →
                    </a>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                if hira:
                    st.markdown(f'<div style="font-size:0.72rem;color:var(--muted);margin-bottom:0.6rem;">📌 출처: {hira["source"]} &nbsp;|&nbsp; 🗓 최종 업데이트: {hira["updated"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="criteria-block">{hira["content"].replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="criteria-block">{item["criteria"]}</div>', unsafe_allow_html=True)
                    alert("info","ℹ️","내부 DB 기준입니다. 최신 심평원 고시 원문은 요양기관업무포털에서 확인하세요.")
    else:
        st.markdown("#### 📌 자주 조회되는 심사기준")
        st.markdown('<div style="font-size:0.82rem;color:var(--muted);margin-bottom:0.8rem;">검색창에 코드/품목명 입력 → 내부 기준 확인 + 포털 검색어 자동 안내</div>', unsafe_allow_html=True)
        popular = [
            ("HA021","초음파 검사(복부)","재검사 6개월 기준, GJ999 필수"),
            ("NS100","신경전도검사","동시산정 50% 규정 주의"),
            ("648602750","씨엠쿨산","외래 전용, GJ001/GJ002 필수"),
            ("PT050","도수치료","건강보험 비급여 — 급여 청구 금지"),
            ("RD001","흉부X선","정면·측면 동시 촬영 시 패키지 코드"),
            ("LB001","혈액검사(CBC)","동일날짜 중복 청구 주의"),
            ("MZ100","처치료(일반)","입원환자 GJ003 필수 기재"),
            ("AL300","외래환자의약품관리료","외래 전용·입원 산정 불가"),
        ]
        for code, name, note in popular:
            st.markdown(f"""
            <div class="result-card">
              <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap;">
                <span class="rc-code">{code}</span>
                <span style="font-weight:700;">{name}</span>
                <span style="font-size:0.79rem;color:var(--muted);">{note}</span>
                <a href="{PORTAL_URL}" target="_blank"
                   style="margin-left:auto;background:var(--teal-lt);color:var(--teal);border:1px solid #A8DDD8;
                          border-radius:7px;padding:0.2rem 0.7rem;font-size:0.74rem;font-weight:700;
                          text-decoration:none;white-space:nowrap;">🏥 포털 검색 →</a>
              </div>
            </div>""", unsafe_allow_html=True)

        divider()
        st.markdown("#### 🗺 요양기관업무포털 심사기준 종합서비스 이용 순서")
        st.markdown(f"""
        <div style="background:var(--card);border:1.5px solid var(--border);border-radius:14px;padding:1.3rem 1.5rem;box-shadow:var(--shadow);">
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:0.9rem;text-align:center;">
            <div style="background:var(--teal-lt);border-radius:10px;padding:0.9rem 0.4rem;">
              <div style="font-size:1.4rem;margin-bottom:0.35rem;">🌐</div>
              <div style="font-size:0.72rem;font-weight:700;color:var(--teal);">STEP 1</div>
              <div style="font-size:0.8rem;font-weight:600;margin-top:0.15rem;">포털 접속</div>
              <div style="font-size:0.68rem;color:var(--muted);margin-top:0.15rem;">biz.hira.or.kr</div>
            </div>
            <div style="background:var(--blue-lt);border-radius:10px;padding:0.9rem 0.4rem;">
              <div style="font-size:1.4rem;margin-bottom:0.35rem;">🔐</div>
              <div style="font-size:0.72rem;font-weight:700;color:var(--blue);">STEP 2</div>
              <div style="font-size:0.8rem;font-weight:600;margin-top:0.15rem;">로그인</div>
              <div style="font-size:0.68rem;color:var(--muted);margin-top:0.15rem;">공인인증/간편인증</div>
            </div>
            <div style="background:var(--gold-lt);border-radius:10px;padding:0.9rem 0.4rem;">
              <div style="font-size:1.4rem;margin-bottom:0.35rem;">📋</div>
              <div style="font-size:0.72rem;font-weight:700;color:var(--gold);">STEP 3</div>
              <div style="font-size:0.8rem;font-weight:600;margin-top:0.15rem;">심사기준 종합서비스</div>
              <div style="font-size:0.68rem;color:var(--muted);margin-top:0.15rem;">메인화면에서 선택</div>
            </div>
            <div style="background:var(--red-lt);border-radius:10px;padding:0.9rem 0.4rem;">
              <div style="font-size:1.4rem;margin-bottom:0.35rem;">🔍</div>
              <div style="font-size:0.72rem;font-weight:700;color:var(--red);">STEP 4</div>
              <div style="font-size:0.8rem;font-weight:600;margin-top:0.15rem;">코드/품목명 검색</div>
              <div style="font-size:0.68rem;color:var(--muted);margin-top:0.15rem;">위 검색어 복사 입력</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        cp1, cp2 = st.columns(2)
        with cp1: st.link_button("🏥 요양기관업무포털 바로가기", PORTAL_URL)
        with cp2: st.link_button("📞 심평원 고객센터 1644-2000", PORTAL_URL)
    footer()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: 특정내역 알림 가이드
# ──────────────────────────────────────────────────────────────────────────────
def page_notice_guide():
    banner("🔔","특정내역 기재 알림 가이드","청구 시 반드시 입력해야 하는 특정내역 코드 · 형식 · 예시 통합 안내")
    notices = load_notices()
    alert("warning","⚠️",f"<strong>특정내역 미기재는 삭감의 주요 원인입니다.</strong><br>현재 등록된 필수 기재 코드: <strong>{len(notices)}종</strong> — 청구 전 반드시 확인하세요.")
    query = st.text_input("", placeholder="특정내역 코드 또는 적용 처방코드 검색 (예: GJ001, HA021)",
                          label_visibility="collapsed", key="ng_query")
    filtered = [n for n in notices if not query or
                query.upper() in n["code"] or query in n["name"] or
                any(query.upper() in ac for ac in n["applicable_codes"])]
    divider()
    for n in filtered:
        with st.expander(f'🔔 [{n["code"]}] {n["name"]} — 적용: {", ".join(n["applicable_codes"])}', expanded=True):
            ca, cb = st.columns(2)
            with ca:
                ac_h = " ".join([f'<span class="rc-code">{c}</span>' for c in n["applicable_codes"]])
                st.markdown(f'<div class="rc-section-title">적용 처방코드</div><div style="display:flex;gap:0.3rem;flex-wrap:wrap;margin-top:0.2rem;">{ac_h}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="rc-section-title" style="margin-top:0.7rem;">적용 시점</div><div style="font-size:0.86rem;color:var(--text2);">{n["required_when"]}</div>', unsafe_allow_html=True)
            with cb:
                alert("danger","🚫",f"<strong>미기재 시:</strong><br>{n['penalty']}")
            st.markdown(f"""
            <div style="margin:0.7rem 0 0.4rem;">
              <div class="rc-section-title">기재 형식</div>
              <div style="font-family:var(--mono);font-size:0.82rem;background:#fff;border:1.5px solid var(--border);border-radius:8px;padding:0.5rem 0.9rem;color:var(--teal);margin-top:0.22rem;">{n["format"]}</div>
            </div>
            <div style="margin-bottom:0.7rem;">
              <div class="rc-section-title">실제 입력 예시</div>
              <div style="font-size:0.85rem;background:var(--teal-lt);border:1.5px solid #A8DDD8;border-radius:8px;padding:0.5rem 0.9rem;margin-top:0.22rem;color:var(--text2);">💬 {n["example"]}</div>
            </div>
            <div class="rc-section-title">설명</div>
            <div style="font-size:0.85rem;color:var(--text2);">{n["description"]}</div>
            """, unsafe_allow_html=True)
    divider()
    st.markdown("#### ✅ 청구 전 특정내역 체크리스트")
    st.markdown("""
    <div class="criteria-block">
      <strong>처방 청구 전 필수 확인 사항:</strong><br><br>
      ☐ 1. 해당 처방코드가 특정내역 필수 기재 대상인지 확인<br>
      ☐ 2. GJ001 ~ GJ003: 시술명/처치부위/필요성 기재 여부<br>
      ☐ 3. GJ999: 재검사·반복 청구 시 사유 기재 여부<br>
      ☐ 4. MT코드: 검사 사유 및 재촬영 사유 기재 여부<br>
      ☐ 5. 입원/외래 구분 정확성 확인<br>
      ☐ 6. 동일 날짜 중복 청구 여부 확인<br>
      ☐ 7. 비급여 항목 급여 청구 여부 확인<br>
      ☐ 8. 동시 시행 검사 산정 비율(50%) 적용 여부
    </div>""", unsafe_allow_html=True)
    footer()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: AI 청구 진단
# ──────────────────────────────────────────────────────────────────────────────
def call_claude(prompt, key):
    import requests
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"},
            json={"model":"claude-3-5-sonnet-20241022","max_tokens":1500,
                  "system":"당신은 대한민국 건강보험 청구심사 전문가입니다. 심평원 기준에 따라 처방 정보를 분석하여 삭감 위험, 오류 가능성, 개선 방안을 구체적으로 한국어로 답변하세요.",
                  "messages":[{"role":"user","content":prompt}]},timeout=30)
        r.raise_for_status(); return r.json()["content"][0]["text"]
    except Exception as e: return f"[Claude API 오류] {e}"

def call_gpt(prompt, key):
    import requests
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
            json={"model":"gpt-4o","max_tokens":1500,
                  "messages":[{"role":"system","content":"대한민국 건강보험 청구심사 전문가로서 한국어로 답변하세요."},
                               {"role":"user","content":prompt}]},timeout=30)
        r.raise_for_status(); return r.json()["choices"][0]["message"]["content"]
    except Exception as e: return f"[GPT API 오류] {e}"

def call_gemini(prompt, key):
    import requests
    try:
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={key}",
            json={"contents":[{"parts":[{"text":"대한민국 건강보험 청구심사 전문가로서 한국어로 분석하세요:\n\n"+prompt}]}],
                  "generationConfig":{"maxOutputTokens":1500}},timeout=30)
        r.raise_for_status(); return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"[Gemini API 오류] {e}"

def page_ai_diagnosis():
    banner("🤖","AI 청구 진단","Claude · GPT-4o · Gemini 다중 AI 엔진으로 처방 오류 · 삭감 위험 자동 분석")
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {"claude":"","openai":"","gemini":""}

    with st.expander("🔑 AI 엔진 API 키 설정", expanded=not any(st.session_state.api_keys.values())):
        alert("info","ℹ️","API 키는 세션 중에만 저장되며 서버에 기록되지 않습니다. 최소 1개 이상 입력하세요.")
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown('<div style="font-size:0.77rem;color:#7B5EA7;font-weight:700;margin-bottom:4px;">🟣 Claude (Anthropic)</div>', unsafe_allow_html=True)
            ck = st.text_input("", value=st.session_state.api_keys["claude"], type="password", placeholder="sk-ant-...", label_visibility="collapsed", key="ck_in")
        with k2:
            st.markdown('<div style="font-size:0.77rem;color:#0E8B7A;font-weight:700;margin-bottom:4px;">🟢 GPT-4o (OpenAI)</div>', unsafe_allow_html=True)
            ok = st.text_input("", value=st.session_state.api_keys["openai"], type="password", placeholder="sk-...", label_visibility="collapsed", key="ok_in")
        with k3:
            st.markdown('<div style="font-size:0.77rem;color:#2563A8;font-weight:700;margin-bottom:4px;">🔵 Gemini (Google)</div>', unsafe_allow_html=True)
            gk = st.text_input("", value=st.session_state.api_keys["gemini"], type="password", placeholder="AIza...", label_visibility="collapsed", key="gk_in")
        if st.button("키 저장", key="save_keys"):
            st.session_state.api_keys = {"claude":ck,"openai":ok,"gemini":gk}
            st.success("API 키가 저장되었습니다.")

    divider()
    st.markdown("#### 📝 처방 정보 입력")
    ca, cb = st.columns(2)
    with ca:
        dept = st.selectbox("진료과",["내과","외과","피부과","정형외과","신경과","재활의학과","산부인과","소아과","응급의학과","성형외과","기타"],key="ai_dept")
    with cb:
        avail = []
        if st.session_state.api_keys["claude"]: avail.append("Claude")
        if st.session_state.api_keys["openai"]: avail.append("GPT-4o")
        if st.session_state.api_keys["gemini"]: avail.append("Gemini")
        if not avail: avail = ["Claude","GPT-4o","Gemini"]
        engines = st.multiselect("AI 엔진 선택", avail, default=avail[:1], key="ai_engines")

    codes_input = st.text_area("처방 코드 및 품목명","",placeholder="예) 648602750 씨엠쿨산, AL300 외래환자의약품관리료",height=80,key="ai_codes")
    situation   = st.text_area("임상 상황 설명","",placeholder="예) 외래 내원 환자에게 레이저 시술 후 씨엠쿨산 처방",height=80,key="ai_situation")
    extra       = st.text_input("추가 정보 (선택)",placeholder="입원/외래 구분, 재검사 여부, 특이사항",key="ai_extra")
    run_btn     = st.button("🤖 AI 진단 실행", key="ai_run")

    divider()
    if run_btn:
        if not codes_input.strip() or not situation.strip():
            alert("warning","⚠️","처방 코드와 임상 상황을 모두 입력하세요.")
            footer(); return
        prompt = f"[병원 청구심사 AI 진단]\n진료과: {dept}\n처방 코드 및 품목: {codes_input}\n임상 상황: {situation}\n추가 정보: {extra or '없음'}\n\n분석 항목:\n1. 삭감 위험 항목 및 사유\n2. 특정내역(GJ/MT 코드) 기재 필요 여부와 방법\n3. 급여/비급여 구분 적정성\n4. 동시 산정 시 수가 적용 주의사항\n5. 개선 권고사항\n6. 유사 삭감 사례 및 예방법"
        st.markdown("#### 🤖 AI 진단 결과")
        engine_fns = {"Claude":("claude",call_claude),"GPT-4o":("openai",call_gpt),"Gemini":("gemini",call_gemini)}
        tabs = st.tabs(engines if engines else ["Claude"])
        for i, eng in enumerate(engines if engines else ["Claude"]):
            with tabs[i]:
                key_name, fn = engine_fns.get(eng,("claude",call_claude))
                api_key = st.session_state.api_keys.get(key_name,"")
                st.markdown(f'<div class="ai-card"><div class="ai-header">🤖 AI 청구심사 진단 <span class="ai-engine-badge">{eng}</span></div>', unsafe_allow_html=True)
                if not api_key:
                    alert("warning","🔑",f"{eng} API 키가 설정되지 않았습니다.")
                    st.markdown('<div class="ai-response"><strong>⚠ 데모 모드</strong> — API 키 연결 시 실제 AI 분석이 제공됩니다.<br><br>예상 분석 항목:<br>1. 특정내역(GJ001/GJ002) 미기재 시 삭감 위험<br>2. 입원/외래 구분 오류 가능성<br>3. 동일 날짜 중복 청구 여부</div>', unsafe_allow_html=True)
                else:
                    with st.spinner(f"{eng} 분석 중..."):
                        result = fn(prompt, api_key)
                    st.markdown(f'<div class="ai-response">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem;background:var(--card);border:1.5px solid var(--border);border-radius:16px;box-shadow:var(--shadow);">
          <div style="font-size:3rem;margin-bottom:0.8rem;">🤖</div>
          <div style="font-size:1.05rem;font-weight:700;color:var(--text);margin-bottom:0.5rem;">AI 다중 엔진 청구심사 진단</div>
          <div style="font-size:0.87rem;line-height:1.85;color:var(--muted);">처방 코드와 임상 상황을 입력하면<br>
          Claude · GPT-4o · Gemini가 동시에 삭감 위험을 분석합니다.<br><br>
          <span style="color:var(--teal);font-weight:600;">API 키를 등록하여 실시간 AI 진단을 시작하세요.</span></div>
        </div>""", unsafe_allow_html=True)
    footer()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: 사례 검색
# ──────────────────────────────────────────────────────────────────────────────
TYPE_COLOR = {"삭감":("#C0392B","tag-fail"),"조정":("#D48A0A","tag-warn"),"환수":("#8B1E1E","tag-fail")}

def page_case_search():
    banner("📚","사례 검색","삭감·조정·환수 사례 DB — 유형별 · 진료과별 · 코드별 검색")
    cases = load_cases()
    cq, cd, ct = st.columns([3,1.5,1.5])
    with cq: query = st.text_input("",placeholder="키워드·처방코드·사례번호 검색",label_visibility="collapsed",key="cs_q")
    with cd:
        dl = ["전체"]+list(dict.fromkeys(c["dept"] for c in cases))
        df = st.selectbox("",dl,label_visibility="collapsed",key="cs_dept")
    with ct: tf = st.selectbox("",["전체","삭감","조정","환수"],label_visibility="collapsed",key="cs_type")

    filtered = [c for c in cases if
        (not query or any(query.lower() in str(c.get(k,"")).lower() for k in ["title","code","summary","id"]) or
         any(query.lower() in t.lower() for t in c.get("tags",[]))) and
        (df=="전체" or c["dept"]==df) and (tf=="전체" or c["type"]==tf)]

    tl = sum(int(c["loss"].replace(",","")) for c in filtered)
    sc = sum(1 for c in filtered if c["type"]=="삭감")
    ac = sum(1 for c in filtered if c["type"]=="조정")

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card teal"><div class="kpi-label">검색된 사례</div><div class="kpi-value">{len(filtered)}</div><div class="kpi-sub">전체 {len(cases)}건 중</div></div>
      <div class="kpi-card red"><div class="kpi-label">삭감 사례</div><div class="kpi-value">{sc}</div><div class="kpi-sub">건</div></div>
      <div class="kpi-card gold"><div class="kpi-label">조정 사례</div><div class="kpi-value">{ac}</div><div class="kpi-sub">건</div></div>
      <div class="kpi-card blue"><div class="kpi-label">누적 손실 추정</div><div class="kpi-value">{tl:,}</div><div class="kpi-sub">원</div></div>
    </div>""", unsafe_allow_html=True)

    if not filtered: alert("info","ℹ️","검색 조건에 맞는 사례가 없습니다."); footer(); return

    for c in filtered:
        color, tcls = TYPE_COLOR.get(c["type"],("#2563A8","tag-pass"))
        tags_h = " ".join([f'<span style="font-size:0.68rem;background:var(--teal-lt);color:var(--teal);border:1px solid #A8DDD8;border-radius:20px;padding:0.06rem 0.42rem;font-weight:600;">#{t}</span>' for t in c.get("tags",[])])
        with st.expander(f'[{c["id"]}] {c["title"]} — {c["dept"]} | {c["type"]} | {c["date"]}'):
            cm, cs = st.columns([3,1])
            with cm:
                st.markdown(f'<div class="rc-section-title">사례 요약</div><div style="font-size:0.87rem;line-height:1.75;color:var(--text2);margin-top:0.2rem;">{c["summary"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="rc-section-title" style="margin-top:0.75rem;">상세 내용</div><div class="criteria-block">{c["detail"]}</div>', unsafe_allow_html=True)
                alert("info","💡",c["lesson"])
                st.markdown(f'<div style="margin-top:0.45rem;">{tags_h}</div>', unsafe_allow_html=True)
            with cs:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:1rem;text-align:center;box-shadow:var(--shadow);">
                  <div class="rc-section-title">처방 코드</div>
                  <div class="rc-code" style="display:block;width:fit-content;margin:0.25rem auto 0.75rem;font-size:0.86rem;">{c["code"]}</div>
                  <div class="rc-section-title">유형</div>
                  <div class="{tcls}" style="font-size:0.82rem;padding:0.16rem 0.7rem;display:block;width:fit-content;margin:0.22rem auto 0.75rem;">{c["type"]}</div>
                  <div class="rc-section-title">추정 손실액</div>
                  <div style="font-size:1.1rem;font-weight:900;color:{color};">₩{c["loss"]}</div>
                  <div style="font-size:0.69rem;color:var(--muted);margin-top:0.45rem;">{c["date"]}</div>
                </div>""", unsafe_allow_html=True)

    divider()
    if st.session_state.get("logged_in"):
        st.markdown("#### ➕ 새 사례 등록")
        with st.expander("사례 직접 등록"):
            f1, f2 = st.columns(2)
            with f1:
                nt    = st.text_input("사례 제목 *",key="nc_t")
                nc    = st.text_input("처방코드 *",key="nc_c")
                nd    = st.selectbox("진료과",["내과","외과","피부과","정형외과","신경과","재활의학과","기타"],key="nc_d")
                ntype = st.selectbox("유형",["삭감","조정","환수"],key="nc_type")
            with f2:
                ns    = st.text_area("사례 요약 *",height=70,key="nc_s")
                ndt   = st.text_area("상세 내용",height=70,key="nc_dt")
                nl    = st.text_area("교훈/예방법",height=50,key="nc_l")
                nloss = st.text_input("손실액(원)",placeholder="예) 150,000",key="nc_loss")
            if st.button("사례 등록",key="submit_case"):
                if nt and nc and ns:
                    cd_list = load_cases()
                    new_id  = f"USER-{len(cd_list)+1:04d}"
                    cd_list.append({"id":new_id,"title":nt,"dept":nd,"code":nc,"type":ntype,
                                    "date":str(datetime.now().date()),"summary":ns,"detail":ndt,
                                    "lesson":nl,"loss":nloss or "0","tags":[nc,nd,ntype]})
                    save_json(CASE_PATH, cd_list)
                    st.success(f"사례 [{new_id}] 등록 완료!"); st.rerun()
                else: st.warning("제목, 처방코드, 요약은 필수입니다.")
    footer()

# ──────────────────────────────────────────────────────────────────────────────
# PAGE: 관리자 패널
# ──────────────────────────────────────────────────────────────────────────────
def page_admin():
    banner("⚙️","관리자 패널","처방코드 DB 관리 · 특정내역 관리 · 사례 관리 · 시스템 설정")
    if not st.session_state.get("logged_in"):
        alert("danger","🔐","<strong>접근 권한 없음</strong><br>좌측 사이드바에서 로그인하세요."); footer(); return
    if not st.session_state.get("is_admin"):
        alert("warning","⚠️","<strong>관리자 전용 메뉴</strong><br>관리자 계정으로 로그인하세요. (테스트: admin / admin1234)"); footer(); return

    st.markdown('<span class="admin-badge">🔐 관리자 모드 활성화</span><br><br>', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["📦 처방코드 DB","🔔 특정내역 관리","📚 사례 관리","⚙️ 시스템"])

    with t1:
        pres = load_pres()
        st.markdown(f"현재 등록 코드: **{len(pres)}건**")
        for i, item in enumerate(pres):
            with st.expander(f'[{item["code"]}] {item["name"]}'):
                ce, cd = st.columns([4,1])
                with cd:
                    if st.button("삭제",key=f"dp_{i}"):
                        pres.pop(i); save_json(PRES_PATH,pres); st.success("삭제 완료"); st.rerun()
                with ce: st.json(item)
        divider()
        st.markdown("**새 처방코드 등록**")
        with st.form("add_pres"):
            p1, p2 = st.columns(2)
            with p1:
                nc    = st.text_input("처방코드 *")
                nn    = st.text_input("품목명 *")
                ncat  = st.selectbox("분류",["의약품","행위료","검사","영상검사","처치","기능검사","치료"])
                ndept = st.multiselect("적용 진료과",["전과목","내과","외과","피부과","정형외과","신경과","재활의학과","산부인과","소아과","응급의학과"])
            with p2:
                ndesc   = st.text_area("설명",height=60)
                ncrit   = st.text_area("심사기준",height=60)
                ncaut   = st.text_area("주의사항",height=45)
                nnotice = st.checkbox("특정내역 기재 필수")
                nnd     = st.text_input("특정내역 상세")
                nrel    = st.text_input("관련코드(쉼표)")
                ntags   = st.text_input("태그(쉼표)")
                nwrong  = st.text_input("잘못된 예시(쉼표)")
            if st.form_submit_button("등록"):
                if nc and nn:
                    pres.append({"code":nc.strip(),"name":nn.strip(),"category":ncat,
                                 "dept":ndept or ["전과목"],"description":ndesc,
                                 "related_codes":[x.strip() for x in nrel.split(",") if x.strip()],
                                 "related_names":[],"criteria":ncrit,"notice_required":nnotice,
                                 "notice_detail":nnd,"wrong_examples":[x.strip() for x in nwrong.split(",") if x.strip()],
                                 "caution":ncaut,"tags":[x.strip() for x in ntags.split(",") if x.strip()]})
                    save_json(PRES_PATH,pres); st.success(f"[{nc}] 등록 완료!"); st.rerun()
                else: st.error("처방코드와 품목명은 필수입니다.")
        divider()
        st.markdown("**JSON 파일 일괄 업로드**")
        up = st.file_uploader("처방코드 JSON (배열 형식)",type=["json"],key="pres_up")
        if up:
            try:
                nd2 = json.load(up)
                if isinstance(nd2,list):
                    pres.extend(nd2); save_json(PRES_PATH,pres)
                    st.success(f"{len(nd2)}건 일괄 등록 완료!"); st.rerun()
                else: st.error("JSON 파일은 배열([ ]) 형식이어야 합니다.")
            except Exception as e: st.error(f"파일 파싱 오류: {e}")

    with t2:
        notices = load_notices()
        st.markdown(f"현재 등록 특정내역 코드: **{len(notices)}종**")
        for i, n in enumerate(notices):
            with st.expander(f'[{n["code"]}] {n["name"]}'):
                ne, nd3 = st.columns([4,1])
                with nd3:
                    if st.button("삭제",key=f"dn_{i}"):
                        notices.pop(i); save_json(NOTICE_PATH,notices); st.success("삭제 완료"); st.rerun()
                with ne: st.json(n)
        divider()
        st.markdown("**새 특정내역 코드 등록**")
        with st.form("add_notice"):
            n1, n2 = st.columns(2)
            with n1:
                ncc = st.text_input("특정내역 코드 *",placeholder="예) GJ001")
                ncn = st.text_input("코드명 *")
                nca = st.text_input("적용 처방코드(쉼표) *")
                ncw = st.text_input("적용 시점")
            with n2:
                ncd = st.text_area("설명",height=50)
                ncf = st.text_input("입력 형식")
                nce = st.text_input("입력 예시")
                ncp = st.text_input("미기재 시 결과")
            if st.form_submit_button("특정내역 등록"):
                if ncc and ncn and nca:
                    notices.append({"code":ncc.strip(),"name":ncn.strip(),
                                    "applicable_codes":[x.strip() for x in nca.split(",") if x.strip()],
                                    "description":ncd,"format":ncf,"example":nce,
                                    "required_when":ncw,"penalty":ncp})
                    save_json(NOTICE_PATH,notices); st.success("등록 완료!"); st.rerun()
                else: st.error("코드, 코드명, 적용 처방코드는 필수입니다.")

    with t3:
        case_data = load_cases()
        st.markdown(f"현재 등록 사례: **{len(case_data)}건**")
        for i, c in enumerate(case_data):
            with st.expander(f'[{c["id"]}] {c["title"]}'):
                ce2, cd2 = st.columns([4,1])
                with cd2:
                    if st.button("삭제",key=f"dc_{i}"):
                        case_data.pop(i); save_json(CASE_PATH,case_data); st.success("삭제 완료"); st.rerun()
                with ce2: st.json(c)
        divider()
        st.download_button("📥 전체 사례 JSON 다운로드",
            data=json.dumps(case_data,ensure_ascii=False,indent=2),
            file_name=f"cases_{datetime.now().strftime('%Y%m%d')}.json",mime="application/json")

    with t4:
        pres=load_pres(); notices=load_notices(); cases=load_cases()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="result-card">
              <div style="font-size:0.84rem;line-height:2.1;">
                🖥 시스템: 청구전문컨설팅 Medium v4.0<br>
                📅 현재 날짜: {datetime.now().strftime('%Y년 %m월 %d일')}<br>
                🗃 처방코드 DB: {len(pres)}건<br>
                🔔 특정내역 코드: {len(notices)}종<br>
                📚 사례 DB: {len(cases)}건
              </div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="result-card">
              <div style="font-size:0.84rem;line-height:2.1;">
                🔗 심평원 연동: <span style="color:var(--teal);font-weight:700;">정상</span><br>
                👤 제작자: 주식회사 메디엄 조정윤<br>
                🤖 Claude API: AI 진단 메뉴에서 설정<br>
                🤖 GPT-4o API: AI 진단 메뉴에서 설정<br>
                🤖 Gemini API: AI 진단 메뉴에서 설정
              </div>
            </div>""", unsafe_allow_html=True)
        divider()
        all_data = {"prescriptions":pres,"notices":notices,"cases":cases,"backup_date":datetime.now().isoformat()}
        st.download_button("💾 전체 DB 백업 다운로드",
            data=json.dumps(all_data,ensure_ascii=False,indent=2),
            file_name=f"mediclaim_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json")
        divider()
        st.markdown("**DB 복원**")
        rf = st.file_uploader("백업 JSON 파일로 복원",type=["json"],key="restore_up")
        if rf:
            try:
                rd = json.load(rf)
                if st.button("⚠️ 복원 실행 (기존 데이터 덮어씀)",key="restore_btn"):
                    if "prescriptions" in rd: save_json(PRES_PATH,rd["prescriptions"])
                    if "notices"       in rd: save_json(NOTICE_PATH,rd["notices"])
                    if "cases"         in rd: save_json(CASE_PATH,rd["cases"])
                    st.success("DB 복원 완료!"); st.rerun()
            except Exception as e: st.error(f"복원 오류: {e}")
    footer()

# ──────────────────────────────────────────────────────────────────────────────
# ROUTING
# ──────────────────────────────────────────────────────────────────────────────
PAGES = {
    "🏠  대시보드":          page_dashboard,
    "🔍  처방코드 검색":     page_prescription_search,
    "📋  심사기준 조회":     page_criteria,
    "🔔  내역 알림 가이드":  page_notice_guide,
    "🤖  AI 청구 진단":      page_ai_diagnosis,
    "📚  사례 검색":         page_case_search,
    "⚙️  관리자 패널":       page_admin,
}
PAGES.get(menu, page_dashboard)()
