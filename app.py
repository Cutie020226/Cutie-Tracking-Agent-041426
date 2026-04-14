from __future__ import annotations

import os
import io
import time
import uuid
import random
import zipfile
import datetime
import traceback
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

# Soft imports with user feedback
try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    px = None
    go = None
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


# -----------------------------------------------------------------------------
# Constants, Default Data & i18n
# -----------------------------------------------------------------------------

APP_TITLE_EN = "WOW Regulatory Command Center"
APP_TITLE_ZH = "WOW 智能法規與數據指揮中心"

DEFAULT_DATASET_CSV = """SupplierID,Deliverdate,CustomerID,LicenseNo,Category,UDID,DeviceNAME,LotNO,SerNo,Model,Number
B00079,20251107,C05278,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,波士頓科技英吉尼心臟節律器,890057,,L111,1
B00079,20251106,C06030,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,波士頓科技英吉尼心臟節律器,872177,,L111,1
B00079,20251106,C00123,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,波士頓科技英吉尼心臟節律器,889490,,L111,1
B00079,20251105,C06034,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,波士頓科技英吉尼心臟節律器,889253,,L111,1
B00079,20251103,C05363,衛部醫器輸字第029100號,E.3610植入式心律器之脈搏產生器,00802526576461,波士頓科技艾科雷心臟節律器,869531,,L311,1
B00079,20251103,C06034,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,波士頓科技英吉尼心臟節律器,889230,,L111,1
B00079,20251103,C05278,衛部醫器輸字第029100號,E.3610植入式心律器之脈搏產生器,00802526576485,波士頓科技艾科雷心臟節律器,182310,,L331,1
B00051,20251030,C02822,衛部醫器輸字第028560號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,08437007606478,尼奧麥迪克舒兒莉芙特骨盆懸吊系統,CC250520,19,CPS02,1
B00079,20251030,C00123,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576324,波士頓科技英吉尼心臟節律器,915900,,L110,1
B00051,20251030,C02822,衛部醫器輸字第028560號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,08437007606478,尼奧麥迪克舒兒莉芙特骨盆懸吊系統,CC250520,20,CPS02,1
B00051,20251029,C02082,衛部醫器輸字第028560號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,08437007606478,尼奧麥迪克舒兒莉芙特骨盆懸吊系統,CC250326,4,CPS02,1
B00209,20251028,C03210,衛部醫器輸字第026988號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,07798121803473,博美敦凱莉星脫垂修補系統,,00012150,Calistar S,1
B00051,20251028,C01774,衛部醫器輸字第030820號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,08437007606515,尼奧麥迪克蜜普思微創骨盆懸吊系統,MB241203,140,KITMIPS02,1
B00209,20251028,C03210,衛部醫器輸字第026988號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,07798121803473,博美敦凱莉星脫垂修補系統,,00012154,Calistar S,1
B00051,20251028,C01773,衛部醫器輸字第028560號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,08437007606478,尼奧麥迪克舒兒莉芙特骨盆懸吊系統,CC241128,85,CPS02,1
"""

UI_TEXT = {
    "en": {
        "nav_dashboard": "Dashboard",
        "nav_dataset": "Dataset Studio",
        "nav_infograph": "Infograph Lab",
        "nav_report": "Report Generator",
        "nav_pdf": "PDF Ops Room",
        "nav_agents": "Agent Studio",
        "nav_notes": "NoteKeeper",
        "nav_skill": "Skill Builder",
        "nav_settings": "Settings & Keys",
        "status_ok": "Ready",
        "missing_key": "Missing",
        "run_health": "Run LLM Check",
        "generate": "Generate",
    },
    "zh-TW": {
        "nav_dashboard": "儀表板",
        "nav_dataset": "數據工作室",
        "nav_infograph": "視覺化圖表實驗室",
        "nav_report": "報告生成器",
        "nav_pdf": "PDF 文件處理室",
        "nav_agents": "代理工作區",
        "nav_notes": "AI 筆記管家",
        "nav_skill": "技能生成器",
        "nav_settings": "設定與 API 金鑰",
        "status_ok": "已就緒",
        "missing_key": "未設定",
        "run_health": "執行 LLM 檢查",
        "generate": "生成",
    },
}

def t(key: str) -> str:
    lang = st.session_state.get("ui_lang", "zh-TW")
    return UI_TEXT.get(lang, UI_TEXT["en"]).get(key, key)


# -----------------------------------------------------------------------------
# WOW Theme & Visual System
# -----------------------------------------------------------------------------
PAINTER_STYLES = [
    {"id": "monet", "name": "Claude Monet Mist", "bg": "#F2F7FB", "fg": "#15202B", "accent": "#6EA8C7"},
    {"id": "van-gogh", "name": "Van Gogh Starfield", "bg": "#081A3A", "fg": "#F9F3C2", "accent": "#F6C445"},
    {"id": "picasso", "name": "Picasso Cubist Grid", "bg": "#F9F7F2", "fg": "#111111", "accent": "#D7263D"},
    {"id": "klimt", "name": "Klimt Gilded Panel", "bg": "#111111", "fg": "#F5E6B3", "accent": "#D4AF37"},
    {"id": "hopper", "name": "Edward Hopper", "bg": "#0B1F2A", "fg": "#F5F5F5", "accent": "#F59E0B"},
    {"id": "matisse", "name": "Henri Matisse", "bg": "#FFF7ED", "fg": "#111827", "accent": "#EF4444"},
]

def apply_wow_css():
    style_id = st.session_state.get("style_id", "monet")
    style = next((s for s in PAINTER_STYLES if s["id"] == style_id), PAINTER_STYLES[0])
    bg = style["bg"]
    fg = style["fg"]
    accent = style["accent"]

    theme = st.session_state.get("theme", "dark")
    if theme == "dark":
        page_bg, card_bg, border, muted, text = "#0B0F14", "rgba(255,255,255,0.04)", "rgba(255,255,255,0.1)", "rgba(255,255,255,0.6)", "#F8FAFC"
    else:
        page_bg, card_bg, border, muted, text = bg, "rgba(0,0,0,0.03)", "rgba(0,0,0,0.1)", "rgba(0,0,0,0.6)", fg

    css = f"""
    <style>
      .stApp {{ background: {page_bg}; color: {text}; }}
      .wow-card {{ background: {card_bg}; border: 1px solid {border}; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
      .wow-kpi {{ font-size: 28px; font-weight: bold; color: {accent}; }}
      .wow-sub {{ font-size: 14px; color: {muted}; }}
      .stButton>button {{ border-radius: 8px; border: 1px solid {accent}; color: {accent}; }}
      .stButton>button:hover {{ background: {accent}; color: #fff; }}
      h1, h2, h3, a {{ color: {accent} !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def trigger_wow_effect(msg="LLM Task Completed!"):
    effects = [st.balloons, st.snow]
    random.choice(effects)()
    st.toast(f"🌟 WOW! {msg}", icon="✨")

# -----------------------------------------------------------------------------
# Session Initialization
# -----------------------------------------------------------------------------
def ss_init():
    defaults = {
        "ui_lang": "zh-TW", "output_lang": "zh-TW", "theme": "dark", "style_id": "monet",
        "session_secrets": {}, "live_log": [], "run_state": "idle",
        "dataset_raw": None, "dataset_filtered": None, "filter_query": "",
        "pdf_files": [], "pdf_summaries": {}, "master_toc": "",
        "report_draft": "", "notes_input": "", "notes_output": "", "skill_md": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Initialize Default Dataset if pandas is available and data is missing
    if pd is not None and st.session_state.dataset_raw is None:
        try:
            df = pd.read_csv(io.StringIO(DEFAULT_DATASET_CSV.strip()))
            df['Deliverdate'] = pd.to_datetime(df['Deliverdate'], format='%Y%m%d', errors='coerce')
            st.session_state.dataset_raw = df
            st.session_state.dataset_filtered = df
        except Exception as e:
            st.error(f"Failed to load default dataset: {e}")

def log_event(msg: str, level="INFO"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.live_log.insert(0, f"[{ts}] [{level}] {msg}")

# -----------------------------------------------------------------------------
# LLM Providers & Call wrapper
# -----------------------------------------------------------------------------
def get_provider_key(provider: str) -> Optional[str]:
    provider = provider.lower()
    env_map = {"openai": "OPENAI_API_KEY", "gemini": "GEMINI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "grok": "GROK_API_KEY"}
    env_name = env_map.get(provider)
    if env_name and os.environ.get(env_name): return os.environ[env_name]
    try:
        if env_name and env_name in st.secrets: return st.secrets[env_name]
    except: pass
    if provider == "grok" and os.environ.get("XAI_API_KEY"): return os.environ["XAI_API_KEY"]
    return st.session_state.session_secrets.get(provider)

MODEL_REGISTRY = [
    {"provider": "openai", "id": "gpt-4o-mini", "label": "OpenAI — gpt-4o-mini"},
    {"provider": "gemini", "id": "gemini-2.5-flash", "label": "Gemini — 2.5 Flash"},
    {"provider": "anthropic", "id": "claude-3-5-sonnet-latest", "label": "Anthropic — Claude 3.5 Sonnet"},
    {"provider": "grok", "id": "grok-4-fast-reasoning", "label": "Grok — grok-4-fast"},
]

def llm_call(model_label: str, sys_prompt: str, user_prompt: str, max_tokens=2500) -> str:
    m = next(x for x in MODEL_REGISTRY if x["label"] == model_label)
    provider, model_id = m["provider"], m["id"]
    key = get_provider_key(provider)
    if not key:
        raise ValueError(f"Missing API Key for {provider}")

    start = time.time()
    try:
        if provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=key)
            resp = client.chat.completions.create(
                model=model_id, max_tokens=max_tokens,
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}]
            )
            res = resp.choices[0].message.content
        elif provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel(model_name=model_id, system_instruction=sys_prompt)
            resp = model.generate_content(user_prompt)
            res = resp.text
        elif provider == "anthropic":
            import anthropic
            client = anthropic.Anthropic(api_key=key)
            msg = client.messages.create(
                model=model_id, max_tokens=max_tokens, system=sys_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            res = "\n".join([b.text for b in msg.content if b.type == 'text'])
        elif provider == "grok":
            from openai import OpenAI
            client = OpenAI(api_key=key, base_url="https://api.x.ai/v1")
            resp = client.chat.completions.create(
                model=model_id, max_tokens=max_tokens,
                messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}]
            )
            res = resp.choices[0].message.content
        else:
            raise ValueError("Unknown provider")
        
        log_event(f"LLM Call [{model_id}] success. {round(time.time()-start, 2)}s")
        return res
    except Exception as e:
        log_event(f"LLM Error: {str(e)}", "ERROR")
        raise e

# -----------------------------------------------------------------------------
# Module: Dashboard
# -----------------------------------------------------------------------------
def module_dashboard():
    st.markdown(f"### {t('nav_dashboard')}")
    df = st.session_state.dataset_filtered
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='wow-card'><div class='wow-kpi'>{len(df) if df is not None else 0}</div><div class='wow-sub'>Records Analyzed</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='wow-card'><div class='wow-kpi'>{df['SupplierID'].nunique() if df is not None else 0}</div><div class='wow-sub'>Unique Suppliers</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='wow-card'><div class='wow-kpi'>{df['CustomerID'].nunique() if df is not None else 0}</div><div class='wow-sub'>Unique Customers</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='wow-card'><div class='wow-kpi'>{len(st.session_state.pdf_files)}</div><div class='wow-sub'>PDFs Indexed</div></div>", unsafe_allow_html=True)

    with st.expander("System Live Log", expanded=True):
        st.code("\n".join(st.session_state.live_log[:15]), language="bash")

# -----------------------------------------------------------------------------
# Module: Dataset Studio
# -----------------------------------------------------------------------------
def module_dataset():
    st.markdown(f"### {t('nav_dataset')}")
    if pd is None:
        st.error("Pandas is required for Dataset Studio. Install with `pip install pandas`.")
        return

    df = st.session_state.dataset_raw
    if df is not None:
        st.markdown("#### Dynamic Filters")
        c1, c2, c3 = st.columns(3)
        sel_sup = c1.multiselect("SupplierID", df['SupplierID'].dropna().unique())
        sel_cus = c2.multiselect("CustomerID", df['CustomerID'].dropna().unique())
        sel_lic = c3.multiselect("LicenseNo", df['LicenseNo'].dropna().unique())
        
        f_df = df.copy()
        if sel_sup: f_df = f_df[f_df['SupplierID'].isin(sel_sup)]
        if sel_cus: f_df = f_df[f_df['CustomerID'].isin(sel_cus)]
        if sel_lic: f_df = f_df[f_df['LicenseNo'].isin(sel_lic)]
        
        st.session_state.dataset_filtered = f_df
        st.session_state.filter_query = f"Suppliers: {sel_sup or 'All'}, Customers: {sel_cus or 'All'}, Licenses: {sel_lic or 'All'}"
        
        st.dataframe(f_df.head(50), use_container_width=True)

# -----------------------------------------------------------------------------
# Module: Infograph Lab
# -----------------------------------------------------------------------------
def module_infograph():
    st.markdown(f"### {t('nav_infograph')}")
    if px is None or go is None or pd is None:
        st.error("Plotly and Pandas are required for Infographs.")
        return
    
    df = st.session_state.dataset_filtered
    if df is None or df.empty:
        st.warning("No data available.")
        return

    st.info("Interactive WOW Infographs dynamically generated from filtered dataset.")

    tab1, tab2, tab3 = st.tabs(["Supply Chain Network", "Time Series & Heatmap", "Distributions"])

    with tab1:
        st.markdown("**Chart 1: Supply Chain Network Graph (Supplier → License → Model → Customer)**")
        try:
            # Build Sankey mapping
            nodes = []
            links = {"source": [], "target": [], "value": []}
            
            # Helper to get index
            def get_node(name):
                if name not in nodes: nodes.append(name)
                return nodes.index(name)
            
            for _, row in df.iterrows():
                s = get_node(f"Sup: {row['SupplierID']}")
                l = get_node(f"Lic: {row['LicenseNo']}")
                m = get_node(f"Mod: {row['Model']}")
                c = get_node(f"Cus: {row['CustomerID']}")
                qty = row['Number'] if pd.notna(row['Number']) else 1
                
                # S->L
                links["source"].append(s); links["target"].append(l); links["value"].append(qty)
                # L->M
                links["source"].append(l); links["target"].append(m); links["value"].append(qty)
                # M->C
                links["source"].append(m); links["target"].append(c); links["value"].append(qty)

            fig = go.Figure(data=[go.Sankey(
                node = dict(pad = 15, thickness = 20, line = dict(color = "black", width = 0.5), label = nodes),
                link = dict(source = links["source"], target = links["target"], value = links["value"])
            )])
            fig.update_layout(height=600, margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Sankey failed: {e}")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Chart 2: Time Series Flow**")
            ts_df = df.groupby('Deliverdate')['Number'].sum().reset_index()
            fig2 = px.line(ts_df, x='Deliverdate', y='Number', markers=True)
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            st.markdown("**Chart 3: Supplier vs Customer Heatmap**")
            hm_df = df.groupby(['SupplierID', 'CustomerID'])['Number'].sum().reset_index()
            fig3 = px.density_heatmap(hm_df, x='CustomerID', y='SupplierID', z='Number', text_auto=True)
            st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Chart 4: License & Category Distribution**")
            fig4 = px.pie(df, names='Category', values='Number', hole=0.3)
            st.plotly_chart(fig4, use_container_width=True)
        with c2:
            st.markdown("**Chart 5: Portfolio Treemap**")
            df['Category_str'] = df['Category'].astype(str)
            df['Model_str'] = df['Model'].astype(str)
            fig5 = px.treemap(df, path=['Category_str', 'Model_str'], values='Number')
            st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------------------------------------------------
# Module: Report Generator
# -----------------------------------------------------------------------------
def module_report():
    st.markdown(f"### {t('nav_report')}")
    df = st.session_state.dataset_filtered
    
    model = st.selectbox("LLM Provider", [m["label"] for m in MODEL_REGISTRY], key="report_model")
    
    if st.button("Generate Comprehensive Report (3000-4000 words + 5 Tables + 20 Entities)"):
        with st.spinner("Compiling insights and drafting..."):
            try:
                # Prepare JSON summary for LLM context to save tokens
                stats = {
                    "total_records": len(df),
                    "filters": st.session_state.filter_query,
                    "top_suppliers": df['SupplierID'].value_counts().head(5).to_dict(),
                    "top_customers": df['CustomerID'].value_counts().head(5).to_dict(),
                    "top_licenses": df['LicenseNo'].value_counts().head(5).to_dict(),
                    "missing_serial": int(df['SerNo'].isna().sum()),
                }
                
                lang = "Traditional Chinese" if st.session_state.output_lang == "zh-TW" else "English"
                sys_prompt = f"You are a Senior Regulatory Intelligence Analyst. Output strictly in {lang}."
                user_prompt = f"""
                Write a highly detailed, comprehensive regulatory and supply chain report (target 3000-4000 words).
                You MUST include:
                1. 5 well-formatted Markdown Tables covering dataset summary, top suppliers, top customers, license cross-matrix, and data quality.
                2. Explicitly list 20 extracted key entities (Suppliers, Customers, Models, etc.) and analyze them.
                3. Detailed sections: Exec Summary, Dataset Overview, Entity Relationships, Temporal Patterns, Quality Traceability, Risks, and Recommendations.
                
                Context Data (Aggregated): {str(stats)}
                Filters Applied: {st.session_state.filter_query}
                """
                
                res = llm_call(model, sys_prompt, user_prompt, max_tokens=4000)
                st.session_state.report_draft = res
                trigger_wow_effect("Comprehensive Report Masterpiece Generated!")
            except Exception as e:
                st.error(f"Failed: {e}")

    if st.session_state.report_draft:
        st.markdown("#### Draft Report")
        st.session_state.report_draft = st.text_area("Edit Report Markdown", st.session_state.report_draft, height=500, key="report_edit_area")
        st.download_button("Download Report (.md)", data=st.session_state.report_draft, file_name="WOW_Report.md")

# -----------------------------------------------------------------------------
# Module: AI NoteKeeper & NEW WOW Features
# -----------------------------------------------------------------------------
def module_notekeeper():
    st.markdown(f"### {t('nav_notes')}")
    model = st.selectbox("LLM Provider", [m["label"] for m in MODEL_REGISTRY], key="note_model")
    st.session_state.notes_input = st.text_area("Paste Notes / Meeting Minutes here:", st.session_state.notes_input, height=150)
    
    if st.button("Organize to Markdown"):
        with st.spinner("Structuring..."):
            sys = "You are a precise note organizer."
            user = f"Organize the following unstructured notes into clean Markdown. Highlight important keywords by wrapping them in HTML coral color like <span style='color:#FF7F50;'>keyword</span>.\n\n{st.session_state.notes_input}"
            try:
                out = llm_call(model, sys, user)
                st.session_state.notes_output = out
                trigger_wow_effect("Notes neatly structured!")
            except Exception as e:
                st.error(e)

    if st.session_state.notes_output:
        st.markdown(st.session_state.notes_output, unsafe_allow_html=True)
        st.divider()
        st.markdown("#### WOW AI Magics")
        
        c1, c2, c3 = st.columns(3)
        magic_choice = st.selectbox("Select Magic Tool", [
            "Structure Wizard", "Risk Lens", "Action Extractor", 
            "★ Adverse Event Predictor (NEW)", 
            "★ Predicate Gap Synthesizer (NEW)", 
            "★ Supply Chain Resiliency Scorer (NEW)"
        ])
        
        if st.button("Apply Magic"):
            with st.spinner(f"Applying {magic_choice}..."):
                try:
                    sys = "You are an expert Medical Device Regulatory AI."
                    user = f"Apply the tool '{magic_choice}' to the following text. If it's a prediction tool, extrapolate plausible regulatory insights based on standard medical device domain knowledge.\n\nText:\n{st.session_state.notes_output}"
                    new_out = llm_call(model, sys, user, max_tokens=1500)
                    st.session_state.notes_output = new_out
                    trigger_wow_effect(f"Magic '{magic_choice}' Applied Brilliantly!")
                except Exception as e:
                    st.error(e)

# -----------------------------------------------------------------------------
# Module: Skill Builder
# -----------------------------------------------------------------------------
def module_skill():
    st.markdown(f"### {t('nav_skill')}")
    st.info("Generates an automated `skill.md` capturing the methodology used in this session to replicate workflows consistently.")
    model = st.selectbox("LLM Provider", [m["label"] for m in MODEL_REGISTRY], key="skill_model")
    
    if st.button("Generate skill.md"):
        with st.spinner("Synthesizing skill..."):
            try:
                sys = "You are an Expert AI Operations Architect."
                user = """
                Based on the capabilities of the 'WOW Regulatory Command Center', generate a `skill.md` playbook.
                It must detail:
                1. The 'Skill Creator Methodology' (Triggers, Inputs, Step-by-step workflow).
                2. Instructions for using the 6 Infographs and compiling the 5 Tables.
                3. Include guides on utilizing the 3 NEW WOW AI Features:
                   - Adverse Event Predictor
                   - Predicate Gap Synthesizer
                   - Supply Chain Resiliency Scorer.
                Output fully formatted Markdown.
                """
                out = llm_call(model, sys, user)
                st.session_state.skill_md = out
                trigger_wow_effect("Skill methodology captured!")
            except Exception as e:
                st.error(e)
                
    if st.session_state.skill_md:
        st.text_area("skill.md output", st.session_state.skill_md, height=400, key="skill_edit")
        st.download_button("Download skill.md", data=st.session_state.skill_md, file_name="skill.md")

# -----------------------------------------------------------------------------
# Main Application Layout
# -----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="WOW Command Center", layout="wide")
    ss_init()
    apply_wow_css()
    
    # Header / Settings Sidebar
    st.sidebar.title(t('nav_settings'))
    st.session_state.ui_lang = st.sidebar.selectbox("Language", ["zh-TW", "en"], index=0)
    st.session_state.theme = st.sidebar.selectbox("Theme", ["dark", "light"], index=0)
    st.session_state.style_id = st.sidebar.selectbox("Painter Style", [s["id"] for s in PAINTER_STYLES])
    if st.sidebar.button("Jackslot Random Style"):
        st.session_state.style_id = random.choice([s["id"] for s in PAINTER_STYLES])
        st.rerun()
    
    st.sidebar.divider()
    st.sidebar.markdown("**Session API Keys** (Overrides Env)")
    for p in ["openai", "gemini", "anthropic", "grok"]:
        v = st.sidebar.text_input(p.capitalize() + " Key", type="password", key=f"key_{p}")
        if v: st.session_state.session_secrets[p] = v
        
    # Main Tabs
    st.title("🌟 " + (APP_TITLE_ZH if st.session_state.ui_lang=="zh-TW" else APP_TITLE_EN))
    
    tab_dash, tab_data, tab_info, tab_rep, tab_notes, tab_skill = st.tabs([
        t('nav_dashboard'), t('nav_dataset'), t('nav_infograph'), 
        t('nav_report'), t('nav_notes'), t('nav_skill')
    ])
    
    with tab_dash: module_dashboard()
    with tab_data: module_dataset()
    with tab_info: module_infograph()
    with tab_rep: module_report()
    with tab_notes: module_notekeeper()
    with tab_skill: module_skill()

if __name__ == "__main__":
    main()
