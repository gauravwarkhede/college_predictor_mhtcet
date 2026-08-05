import streamlit as st

from model_utils import (
    FEATURE_ORDER_COURSE,
    build_feature_vector,
    load_encoders,
    load_models,
    predict_top_n,
)
from theme import render_theme_selector, render_footer

st.set_page_config(page_title="Course Predictor", page_icon="📚", layout="centered")

render_theme_selector()

st.title("📚 Predict Your Course")
st.caption("Enter your details to see the courses you're most likely to get, ranked by probability.")

encoders = load_encoders()
models = load_models()

with st.form("course_form"):
    c1, c2 = st.columns(2)
    with c1:
        percentile = st.number_input(
            "Percentile", min_value=0.0, max_value=100.0, step=0.0001, format="%.4f"
        )
        seat_type = st.selectbox("Seat Type", sorted(encoders["seat_type"].classes_.tolist()))
    with c2:
        category = st.selectbox("Category", sorted(encoders["category"].classes_.tolist()))
        gender = st.selectbox("Gender", sorted(encoders["gender"].classes_.tolist()))

    institute = st.selectbox("Institute", sorted(encoders["institute"].classes_.tolist()))

    top_n = st.slider("Number of courses to show", min_value=3, max_value=20, value=5)

    submitted = st.form_submit_button("🔮 Predict Course", use_container_width=True)

if submitted:
    values = {
        "percentile": percentile,
        "category": category,
        "seat_type": seat_type,
        "gender": gender,
        "institute": institute,
    }
    try:
        X = build_feature_vector(encoders, values, FEATURE_ORDER_COURSE)
        results = predict_top_n(models["course"], encoders["course"], X, n=top_n)

        st.markdown(f"### Top {len(results)} Predicted Courses")
        for i, (label, prob) in enumerate(results, start=1):
            st.markdown(
                f"""
                <div class="pred-card">
                    <span class="pred-rank">#{i}</span>
                    <span class="pred-name">{label}</span>
                    <span class="pred-prob">{prob * 100:.2f}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(min(max(prob, 0.0), 1.0))

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Prediction failed: {e}")

render_footer()
