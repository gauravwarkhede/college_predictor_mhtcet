"""
10 switchable color themes + shared footer/credits, used by every page.

Usage in each page file:
    from theme import render_theme_selector, render_footer
    render_theme_selector()   # call near the top, before other UI
    ...page content...
    render_footer()           # call at the very bottom
"""

import streamlit as st

THEMES = {
    "Ocean Blue": {
        "bg": "#0b1120", "sidebar": "#0f172a", "card": "#161f36",
        "primary": "#3b82f6", "primary_dark": "#2563eb", "text": "#f1f5f9",
        "subtext": "#94a3b8", "border": "#243049", "accent": "#38bdf8",
    },
    "Midnight": {
        "bg": "#0a0a12", "sidebar": "#0f0f1a", "card": "#17172a",
        "primary": "#8b5cf6", "primary_dark": "#7c3aed", "text": "#f5f3ff",
        "subtext": "#a1a1c2", "border": "#26264a", "accent": "#c4b5fd",
    },
    "Sunset Orange": {
        "bg": "#1a1006", "sidebar": "#20140a", "card": "#2b1c0f",
        "primary": "#f97316", "primary_dark": "#ea580c", "text": "#fff7ed",
        "subtext": "#d6b590", "border": "#3d2914", "accent": "#fb923c",
    },
    "Forest Green": {
        "bg": "#081310", "sidebar": "#0c1a15", "card": "#122620",
        "primary": "#22c55e", "primary_dark": "#16a34a", "text": "#f0fdf4",
        "subtext": "#9cb8ab", "border": "#1f3a30", "accent": "#4ade80",
    },
    "Royal Purple": {
        "bg": "#120a1f", "sidebar": "#170d26", "card": "#221436",
        "primary": "#a855f7", "primary_dark": "#9333ea", "text": "#faf5ff",
        "subtext": "#bfa3d9", "border": "#33204f", "accent": "#d8b4fe",
    },
    "Rose Pink": {
        "bg": "#1c0a12", "sidebar": "#230d17", "card": "#331523",
        "primary": "#ec4899", "primary_dark": "#db2777", "text": "#fdf2f8",
        "subtext": "#d9a3bf", "border": "#4a1f34", "accent": "#f472b6",
    },
    "Slate Gray": {
        "bg": "#0f1115", "sidebar": "#14171c", "card": "#1c2027",
        "primary": "#64748b", "primary_dark": "#475569", "text": "#f8fafc",
        "subtext": "#9aa4b2", "border": "#2a2f38", "accent": "#94a3b8",
    },
    "Golden Amber": {
        "bg": "#180f04", "sidebar": "#1f1406", "card": "#2c1e0b",
        "primary": "#f59e0b", "primary_dark": "#d97706", "text": "#fffbeb",
        "subtext": "#d9bd8a", "border": "#3d2b0f", "accent": "#fbbf24",
    },
    "Cyber Teal": {
        "bg": "#04120f", "sidebar": "#061815", "card": "#0b241f",
        "primary": "#14b8a6", "primary_dark": "#0d9488", "text": "#f0fdfa",
        "subtext": "#8fc4bb", "border": "#123a33", "accent": "#2dd4bf",
    },
    "Classic Light": {
        "bg": "#f8fafc", "sidebar": "#ffffff", "card": "#ffffff",
        "primary": "#1e3a8a", "primary_dark": "#1c3175", "text": "#0f172a",
        "subtext": "#64748b", "border": "#e2e8f0", "accent": "#2563eb",
    },
}

DEFAULT_THEME = "Ocean Blue"


def _inject_css(t):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {t['bg']};
            color: {t['text']};
        }}
        [data-testid="stSidebar"] {{
            background-color: {t['sidebar']};
            border-right: 1px solid {t['border']};
        }}
        h1, h2, h3, h4, p, span, label, .stMarkdown {{
            color: {t['text']};
        }}
        [data-testid="stCaptionContainer"] {{
            color: {t['subtext']} !important;
        }}
        .stButton>button, .stFormSubmitButton>button {{
            background-color: {t['primary']};
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            transition: background-color 0.15s ease-in-out;
        }}
        .stButton>button:hover, .stFormSubmitButton>button:hover {{
            background-color: {t['primary_dark']};
            color: #ffffff;
        }}
        div[data-baseweb="select"] > div, .stNumberInput input, .stTextInput input {{
            background-color: {t['card']};
            color: {t['text']};
            border: 1px solid {t['border']};
            border-radius: 8px;
        }}
        [data-testid="stForm"] {{
            background-color: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 14px;
            padding: 1.6rem;
        }}
        .pred-card {{
            background-color: {t['card']};
            border: 1px solid {t['border']};
            border-left: 4px solid {t['primary']};
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.6rem;
        }}
        .pred-rank {{
            display: inline-block;
            background-color: {t['primary']};
            color: #ffffff;
            font-weight: 700;
            font-size: 0.75rem;
            border-radius: 999px;
            padding: 0.15rem 0.55rem;
            margin-right: 0.5rem;
        }}
        .pred-name {{
            font-weight: 600;
            font-size: 1.02rem;
            color: {t['text']};
        }}
        .pred-prob {{
            float: right;
            font-weight: 700;
            color: {t['accent']};
        }}
        .stProgress > div > div > div > div {{
            background-color: {t['primary']};
        }}
        .app-hero {{
            background: linear-gradient(135deg, {t['card']} 0%, {t['bg']} 100%);
            border: 1px solid {t['border']};
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.2rem;
        }}
        .nav-card {{
            background-color: {t['card']};
            border: 1px solid {t['border']};
            border-radius: 14px;
            padding: 1.4rem;
            text-align: center;
            height: 100%;
        }}
        .app-footer {{
            margin-top: 3rem;
            padding-top: 1.2rem;
            border-top: 1px solid {t['border']};
            text-align: center;
            color: {t['subtext']};
            font-size: 0.85rem;
        }}
        .app-footer b {{
            color: {t['accent']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_theme_selector():
    """Call near the top of every page. Persists the choice via session_state
    so it stays consistent as the user navigates between pages."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = DEFAULT_THEME

    with st.sidebar:
        st.markdown("### 🎨 Theme")
        chosen = st.selectbox(
            "Choose a color theme",
            list(THEMES.keys()),
            index=list(THEMES.keys()).index(st.session_state["theme"]),
            label_visibility="collapsed",
        )
        st.session_state["theme"] = chosen

    _inject_css(THEMES[st.session_state["theme"]])


def render_footer():
    st.markdown(
        """
        <div class="app-footer">
            🎓 College Predictor &nbsp;|&nbsp; Made with ❤️ by <b>Gaurav</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
