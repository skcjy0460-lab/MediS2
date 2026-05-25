import streamlit as st
import sys
import os
from datetime import datetime

# ── 경로 설정: modules 폴더를 sys.path에 추가 ──────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediClaim Pro | 청구심사 전문 시스템",
    page_icon="⚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600&family=Playfair+Display:wght@700&display=swap');

:root {
    --navy:     #0D1B2A;
    --navy2:    #1B2E44;
    --teal:     #00A896;
    --teal2:    #02C39A;
    --gold:     #F4AC45;
    --red:      #E63946;
    --light:    #F0F4F8;
    --muted:    #8A9BB0;
    --white:    #FFFFFF;
    --card-bg:  #162035;
    --border:   rgba(0,168,150,0.25);
    --font-main:'Noto Sans KR', sans-serif;
    --font-mono:'JetBrains Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font-main) !important;
    background-color: var(--navy) !important;
    color: var(--light) !important;
}
.stApp { background: var(--navy); }
section[data-testid="stSidebar"] {
    background: var(--navy2) !important;
    border-right: 1px solid var(--border);
}

.sidebar-logo { text-align:center; padding:1.5rem 0 1rem; border-bottom:1px solid var(--border); margin-bottom:1.2rem; }
.sidebar-logo .logo-icon { font-size:2.6rem; }
.sidebar-logo .logo-title { font-family:'Playfair Display',serif; font-size:1.35rem; color:var(--teal2); letter-spacing:0.03em; margin-top:0.2rem; }
.sidebar-logo .logo-sub { font-size:0.72rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; }

.page-banner { background:linear-gradient(135deg,var(--navy2) 0%,#1a3050 100%); border:1px solid var(--border); border-radius:14px; padding:1.6rem 2rem; margin-bottom:1.8rem; display:flex; align-items:center; gap:1.2rem; }
.page-banner .banner-icon { font-size:2.4rem; }
.page-banner .banner-title { font-size:1.5rem; font-weight:700; color:var(--white); }
.page-banner .banner-desc { font-size:0.88rem; color:var(--muted); margin-top:2px; }

.kpi-row { display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.kpi-card { flex:1; min-width:160px; background:var(--card-bg); border:1px solid var(--border); border-radius:12px; padding:1.1rem 1.3rem; position:relative; overflow:hidden; }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.kpi-card.teal::before { background:var(--teal2); }
.kpi-card.gold::before { background:var(--gold); }
.kpi-card.red::before  { background:var(--red); }
.kpi-card.blue::before { background:#4A90D9; }
.kpi-label { font-size:0.75rem; color:var(--muted); letter-spacing:0.08em; text-transform:uppercase; }
.kpi-value { font-size:1.7rem; font-weight:900; margin:0.2rem 0; }
.kpi-card.teal .kpi-value { color:var(--teal2); }
.kpi-card.gold .kpi-value { color:var(--gold); }
.kpi-card.red  .kpi-value { color:var(--red); }
.kpi-card.blue .kpi-value { color:#4A90D9; }
.kpi-sub { font-size:0.72rem; color:var(--muted); }

.result-card { background:var(--card-bg); border:1px solid var(--border); border-radius:12px; padding:1.3rem 1.5rem; margin-bottom:1rem; transition:border-color 0.2s; }
.result-card:hover { border-color:var(--teal2); }
.result-card .rc-header { display:flex; align-items:center; gap:0.8rem; margin-bottom:0.9rem; }
.rc-code { font-family:var(--font-mono); font-size:0.82rem; background:rgba(0,168,150,0.15); color:var(--teal2); border:1px solid var(--border); border-radius:6px; padding:0.2rem 0.6rem; }
.rc-name { font-size:1.05rem; font-weight:700; color:var(--white); }
.rc-dept { margin-left:auto; font-size:0.72rem; background:rgba(244,172,69,0.15); color:var(--gold); border:1px solid rgba(244,172,69,0.3); border-radius:20px; padding:0.15rem 0.7rem; }
.rc-section { margin-bottom:0.7rem; }
.rc-section-title { font-size:0.72rem; color:var(--muted); letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.3rem; }
.rc-section-body { font-size:0.9rem; line-height:1.65; }

.alert-box { border-radius:10px; padding:1rem 1.2rem; margin-bottom:0.8rem; display:flex; gap:0.8rem; align-items:flex-start; font-size:0.9rem; line-height:1.6; }
.alert-box.warning { background:rgba(244,172,69,0.1); border:1px solid rgba(244,172,69,0.35); }
.alert-box.danger  { background:rgba(230,57,70,0.1);  border:1px solid rgba(230,57,70,0.35); }
.alert-box.info    { background:rgba(0,168,150,0.1);  border:1px solid rgba(0,168,150,0.35); }
.alert-box .alert-icon { font-size:1.2rem; margin-top:1px; }
.alert-box.warning .alert-text { color:var(--gold); }
.alert-box.danger  .alert-text { color:#ff8a8a; }
.alert-box.info    .alert-text { color:var(--teal2); }

.criteria-block { background:rgba(13,27,42,0.7); border-left:3px solid var(--teal2); border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin:0.6rem 0; font-size:0.88rem; line-height:1.7; }

.ai-card { background:linear-gradient(135deg,#162035 0%,#1a2d48 100%); border:1px solid rgba(74,144,217,0.35); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:1.2rem; }
.ai-card .ai-header { display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem; font-size:0.78rem; color:#4A90D9; letter-spacing:0.1em; text-transform:uppercase; }
.ai-card .ai-engine-badge { font-family:var(--font-mono); font-size:0.7rem; background:rgba(74,144,217,0.2); color:#7ab3e8; border:1px solid rgba(74,144,217,0.3); border-radius:4px; padding:0.1rem 0.4rem; margin-left:auto; }
.ai-response { font-size:0.92rem; line-height:1.75; color:var(--light); }

.styled-table { width:100%; border-collapse:collapse; font-size:0.87rem; }
.styled-table th { background:rgba(0,168,150,0.15); color:var(--teal2); font-size:0.75rem; letter-spacing:0.08em; text-transform:uppercase; padding:0.7rem 1rem; text-align:left; border-bottom:1px solid var(--border); }
.styled-table td { padding:0.65rem 1rem; border-bottom:1px solid rgba(255,255,255,0.05); vertical-align:top; }
.styled-table tr:hover td { background:rgba(255,255,255,0.03); }
.tag-pass { display:inline-block; font-size:0.7rem; background:rgba(2,195,154,0.15); color:var(--teal2); border-radius:20px; padding:0.1rem 0.55rem; border:1px solid rgba(2,195,154,0.3); }
.tag-fail { display:inline-block; font-size:0.7rem; background:rgba(230,57,70,0.15); color:#ff8a8a; border-radius:20px; padding:0.1rem 0.55rem; border:1px solid rgba(230,57,70,0.3); }
.tag-warn { display:inline-block; font-size:0.7rem; background:rgba(244,172,69,0.15); color:var(--gold); border-radius:20px; padding:0.1rem 0.55rem; border:1px solid rgba(244,172,69,0.3); }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background:#0f1e30 !important; border:1.5px solid var(--border) !important;
    border-radius:8px !important; color:var(--light) !important; font-family:var(--font-main) !important;
}
.stButton > button {
    background:linear-gradient(135deg,var(--teal) 0%,var(--teal2) 100%) !important;
    color:var(--navy) !important; font-weight:700 !important; border:none !important;
    border-radius:8px !important; padding:0.5rem 1.5rem !important; transition:all 0.2s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 4px 16px rgba(0,168,150,0.4) !important; }
.stTabs [data-baseweb="tab-list"] { background:transparent; border-bottom:1px solid var(--border); gap:0.5rem; }
.stTabs [data-baseweb="tab"] { background:transparent; color:var(--muted); border-radius:8px 8px 0 0; font-size:0.88rem; padding:0.5rem 1.1rem; border:none; }
.stTabs [aria-selected="true"] { background:rgba(0,168,150,0.15) !important; color:var(--teal2) !important; border-bottom:2px solid var(--teal2) !important; }
.stExpander { background:var(--card-bg) !important; border:1px solid var(--border) !important; border-radius:10px !important; }
div[data-testid="stMetric"] { background:var(--card-bg); border:1px solid var(--border); border-radius:10px; padding:0.8rem 1rem; }
div[data-testid="stMetricValue"] { color:var(--teal2) !important; font-weight:900 !important; }

::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--navy); }
::-webkit-scrollbar-thumb { background:var(--teal); border-radius:99px; }

.admin-badge { display:inline-flex; align-items:center; gap:0.4rem; font-size:0.72rem; background:rgba(244,172,69,0.15); color:var(--gold); border:1px solid rgba(244,172,69,0.3); border-radius:20px; padding:0.2rem 0.8rem; }
.section-divider { border:none; border-top:1px solid var(--border); margin:1.5rem 0; }
.dot-online { display:inline-block; width:8px; height:8px; background:var(--teal2); border-radius:50%; animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;}50%{opacity:0.4;} }
</style>
""", unsafe_allow_html=True)

# ─── Session 초기화 ──────────────────────────────────────────────────────────
if "is_admin"  not in st.session_state: st.session_state.is_admin  = False
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "menu"      not in st.session_state: st.session_state.menu      = "🏠  대시보드"

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">⚕</div>
        <div class="logo-title">MediClaim Pro</div>
        <div class="logo-sub">Hospital Claim Audit System</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        badge_style = "background:rgba(244,172,69,0.1);color:var(--gold);" if st.session_state.is_admin \
                      else "background:rgba(0,168,150,0.1);color:var(--teal2);border-color:rgba(0,168,150,0.3);"
        label = "🔐 관리자 모드" if st.session_state.is_admin else "👤 일반 사용자"
        st.markdown(f'<span class="admin-badge" style="{badge_style}">{label}</span>', unsafe_allow_html=True)
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
    st.markdown("**📂 메뉴**")

    menu_items = [
        "🏠  대시보드",
        "🔍  처방코드 검색",
        "📋  심사기준 조회",
        "🔔  내역 알림 가이드",
        "🤖  AI 청구 진단",
        "📚  사례 검색",
        "⚙️  관리자 패널",
    ]
    menu = st.radio("", menu_items, label_visibility="collapsed",
                    index=menu_items.index(st.session_state.menu)
                          if st.session_state.menu in menu_items else 0,
                    key="menu_radio")
    st.session_state.menu = menu

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.72rem;color:var(--muted);text-align:center;line-height:1.8;">
        <span class="dot-online"></span> 시스템 정상 운영 중<br>
        {datetime.now().strftime('%Y-%m-%d %H:%M')} 기준<br>
        심평원 DB 동기화 완료
    </div>
    """, unsafe_allow_html=True)

# ─── 페이지 라우팅 (importlib 사용으로 경로 문제 완전 해결) ──────────────────
import importlib.util

def load_module(name: str):
    """modules/ 폴더에서 직접 파일을 로드하여 경로 충돌 방지"""
    path = os.path.join(MODULES_DIR, f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ROUTE = {
    "🏠  대시보드":       "dashboard",
    "🔍  처방코드 검색":  "prescription_search",
    "📋  심사기준 조회":  "criteria",
    "🔔  내역 알림 가이드": "notice_guide",
    "🤖  AI 청구 진단":   "ai_diagnosis",
    "📚  사례 검색":      "case_search",
    "⚙️  관리자 패널":    "admin_panel",
}

module_name = ROUTE.get(menu, "dashboard")
try:
    page = load_module(module_name)
    page.show()
except Exception as e:
    st.error(f"페이지 로딩 오류: {e}")
    import traceback
    st.code(traceback.format_exc())
