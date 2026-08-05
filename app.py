import streamlit as st

from theme import render_theme_selector, render_footer

st.set_page_config(
    page_title="College Predictor",
    page_icon="🎓",
    layout="wide",
)

render_theme_selector()

st.markdown(
    """
    <div class="app-hero">
        <h1 style="margin-bottom:0.2rem;">🎓 College Predictor</h1>
        <p style="font-size:1.05rem; margin-bottom:0;">
            Predict your most likely <b>institute</b> or <b>course</b> based on your
            percentile, category, seat type, and gender — ranked by probability.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown(
        """
        <div class="nav-card">
            <div style="font-size:2.2rem;">🏫</div>
            <h3>Institute Predictor</h3>
            <p style="opacity:0.85;">Find the institutes you're most likely to get,
            ranked by probability.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/1_Institute_Predictor.py",
        label="Go to Institute Predictor →",
        icon="🏫",
        use_container_width=True,
    )

with col2:
    st.markdown(
        """
        <div class="nav-card">
            <div style="font-size:2.2rem;">📚</div>
            <h3>Course Predictor</h3>
            <p style="opacity:0.85;">Find the courses you're most likely to get
            at a given institute, ranked by probability.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/2_Course_Predictor.py",
        label="Go to Course Predictor →",
        icon="📚",
        use_container_width=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
st.info("💡 Tip: pick a color theme from the sidebar — 10 themes available.")

render_footer()
