import streamlit as st
import json
import os
from datetime import datetime

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

/* ── Root Variables ── */
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

/* ── Global ── */
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

/* ── Sidebar header ── */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}
.sidebar-logo .logo-icon { font-size: 2.6rem; }
.sidebar-logo .logo-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    color: var(--teal2);
    letter-spacing: 0.03em;
    margin-top: 0.2rem;
}
.sidebar-logo .logo-sub {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── Nav items ── */
div[data-testid="stSidebarNav"] a {
    border-radius: 8px;
    margin: 2px 0;
    transition: all 0.2s;
}
div[data-testid="stSidebarNav"] a:hover { background: rgba(0,168,150,0.15); }

/* ── Page title banner ── */
.page-banner {
    background: linear-gradient(135deg, var(--navy2) 0%, #1a3050 100%);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.8rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
}
.page-banner .banner-icon { font-size: 2.4rem; }
.page-banner .banner-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--white);
}
.page-banner .banner-desc { font-size: 0.88rem; color: var(--muted); margin-top: 2px; }

/* ── KPI Cards ── */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.kpi-card {
    flex: 1;
    min-width: 160px;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content:'';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.teal::before { background: var(--teal2); }
.kpi-card.gold::before { background: var(--gold); }
.kpi-card.red::before  { background: var(--red); }
.kpi-card.blue::before { background: #4A90D9; }
.kpi-label { font-size: 0.75rem; color: var(--muted); letter-spacing: 0.08em; text-transform: uppercase; }
.kpi-value { font-size: 1.7rem; font-weight: 900; margin: 0.2rem 0; }
.kpi-card.teal .kpi-value { color: var(--teal2); }
.kpi-card.gold .kpi-value { color: var(--gold); }
.kpi-card.red  .kpi-value { color: var(--red); }
.kpi-card.blue .kpi-value { color: #4A90D9; }
.kpi-sub { font-size: 0.72rem; color: var(--muted); }

/* ── Search box ── */
.search-container {
    background: var(--card-bg);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
}
.search-label {
    font-size: 0.78rem;
    color: var(--teal2);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Result cards ── */
.result-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: var(--teal2); }
.result-card .rc-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.9rem;
}
.rc-code {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    background: rgba(0,168,150,0.15);
    color: var(--teal2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
}
.rc-name { font-size: 1.05rem; font-weight: 700; color: var(--white); }
.rc-dept {
    margin-left: auto;
    font-size: 0.72rem;
    background: rgba(244,172,69,0.15);
    color: var(--gold);
    border: 1px solid rgba(244,172,69,0.3);
    border-radius: 20px;
    padding: 0.15rem 0.7rem;
}
.rc-section { margin-bottom: 0.7rem; }
.rc-section-title {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.rc-section-body { font-size: 0.9rem; line-height: 1.65; }

/* ── Alert / Notice box ── */
.alert-box {
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
    font-size: 0.9rem;
    line-height: 1.6;
}
.alert-box.warning {
    background: rgba(244,172,69,0.1);
    border: 1px solid rgba(244,172,69,0.35);
}
.alert-box.danger {
    background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.35);
}
.alert-box.info {
    background: rgba(0,168,150,0.1);
    border: 1px solid rgba(0,168,150,0.35);
}
.alert-box .alert-icon { font-size: 1.2rem; margin-top: 1px; }
.alert-box.warning .alert-text { color: var(--gold); }
.alert-box.danger  .alert-text { color: #ff8a8a; }
.alert-box.info    .alert-text { color: var(--teal2); }

/* ── Criteria section ── */
.criteria-block {
    background: rgba(13,27,42,0.7);
    border-left: 3px solid var(--teal2);
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    line-height: 1.7;
}

/* ── AI Diagnosis card ── */
.ai-card {
    background: linear-gradient(135deg, #162035 0%, #1a2d48 100%);
    border: 1px solid rgba(74,144,217,0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
}
.ai-card .ai-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
    font-size: 0.78rem;
    color: #4A90D9;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.ai-card .ai-engine-badge {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    background: rgba(74,144,217,0.2);
    color: #7ab3e8;
    border: 1px solid rgba(74,144,217,0.3);
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    margin-left: auto;
}
.ai-response { font-size: 0.92rem; line-height: 1.75; color: var(--light); }

/* ── Table ── */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.87rem;
}
.styled-table th {
    background: rgba(0,168,150,0.15);
    color: var(--teal2);
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.7rem 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}
.styled-table td {
    padding: 0.65rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    vertical-align: top;
}
.styled-table tr:hover td { background: rgba(255,255,255,0.03); }
.tag-pass {
    display: inline-block;
    font-size: 0.7rem;
    background: rgba(2,195,154,0.15);
    color: var(--teal2);
    border-radius: 20px;
    padding: 0.1rem 0.55rem;
    border: 1px solid rgba(2,195,154,0.3);
}
.tag-fail {
    display: inline-block;
    font-size: 0.7rem;
    background: rgba(230,57,70,0.15);
    color: #ff8a8a;
    border-radius: 20px;
    padding: 0.1rem 0.55rem;
    border: 1px solid rgba(230,57,70,0.3);
}
.tag-warn {
    display: inline-block;
    font-size: 0.7rem;
    background: rgba(244,172,69,0.15);
    color: var(--gold);
    border-radius: 20px;
    padding: 0.1rem 0.55rem;
    border: 1px solid rgba(244,172,69,0.3);
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #0f1e30 !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--light) !important;
    font-family: var(--font-main) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--teal2) !important;
    box-shadow: 0 0 0 2px rgba(2,195,154,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--teal) 0%, var(--teal2) 100%) !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.03em;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,168,150,0.4) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid var(--border);
    gap: 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    border-radius: 8px 8px 0 0;
    font-size: 0.88rem;
    padding: 0.5rem 1.1rem;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,168,150,0.15) !important;
    color: var(--teal2) !important;
    border-bottom: 2px solid var(--teal2) !important;
}
.stExpander {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
.stExpander summary { color: var(--light) !important; }
div[data-testid="stMetric"] {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.8rem 1rem;
}
div[data-testid="stMetricValue"] { color: var(--teal2) !important; font-weight: 900 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--teal); border-radius: 99px; }

/* ── Admin badge ── */
.admin-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    background: rgba(244,172,69,0.15);
    color: var(--gold);
    border: 1px solid rgba(244,172,69,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
}
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.5rem 0;
}

/* ── Status dot ── */
.dot-online { display:inline-block; width:8px; height:8px; background:var(--teal2); border-radius:50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-icon">⚕</div>
        <div class="logo-title">MediClaim Pro</div>
        <div class="logo-sub">Hospital Claim Audit System</div>
    </div>
    """, unsafe_allow_html=True)

    # 사용자 상태
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # 로그인 상태 표시
    if st.session_state.logged_in:
        if st.session_state.is_admin:
            st.markdown('<span class="admin-badge">🔐 관리자 모드</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="admin-badge" style="background:rgba(0,168,150,0.1);color:var(--teal2);border-color:rgba(0,168,150,0.3);">👤 일반 사용자</span>', unsafe_allow_html=True)
        if st.button("로그아웃", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.rerun()
    else:
        with st.expander("🔑 로그인"):
            uid = st.text_input("아이디", key="login_uid")
            pw  = st.text_input("비밀번호", type="password", key="login_pw")
            if st.button("로그인", key="login_btn"):
                if uid == "admin" and pw == "admin1234":
                    st.session_state.logged_in = True
                    st.session_state.is_admin = True
                    st.success("관리자로 로그인되었습니다.")
                    st.rerun()
                elif uid and pw:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = False
                    st.success("로그인되었습니다.")
                    st.rerun()
                else:
                    st.error("아이디와 비밀번호를 입력하세요.")

    st.markdown("---")
    st.markdown("**📂 메뉴**")

    menu = st.radio(
        "",
        ["🏠  대시보드", "🔍  처방코드 검색", "📋  심사기준 조회",
         "🔔  내역 알림 가이드", "🤖  AI 청구 진단", "📚  사례 검색",
         "⚙️  관리자 패널"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.72rem;color:var(--muted);text-align:center;line-height:1.8;">
        <span class="dot-online"></span> 시스템 정상 운영 중<br>
        {datetime.now().strftime('%Y-%m-%d %H:%M')} 기준<br>
        심평원 DB 동기화 완료
    </div>
    """, unsafe_allow_html=True)

# ─── Store menu in session ───────────────────────────────────────────────────
st.session_state["menu"] = menu

# ─── Route to pages ─────────────────────────────────────────────────────────
if   menu == "🏠  대시보드":
    import pages.dashboard as p;  p.show()
elif menu == "🔍  처방코드 검색":
    import pages.prescription_search as p; p.show()
elif menu == "📋  심사기준 조회":
    import pages.criteria as p; p.show()
elif menu == "🔔  내역 알림 가이드":
    import pages.notice_guide as p; p.show()
elif menu == "🤖  AI 청구 진단":
    import pages.ai_diagnosis as p; p.show()
elif menu == "📚  사례 검색":
    import pages.case_search as p; p.show()
elif menu == "⚙️  관리자 패널":
    import pages.admin_panel as p; p.show()
