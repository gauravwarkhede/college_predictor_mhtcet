import streamlit as st

from model_utils import (
    FEATURE_ORDER_COURSE,
    TOP_N,
    build_feature_vector,
    load_encoders,
    load_models,
    predict_top_n,
)

st.set_page_config(page_title="Predict Course", page_icon="📚")
st.title("📚 Predict Your Course")
st.caption("Enter your details to see the most likely courses.")

encoders = load_encoders()
models = load_models()

with st.form("course_form"):
    percentile = st.number_input(
        "Percentile", min_value=0.0, max_value=100.0, step=0.0001, format="%.4f"
    )
    category = st.selectbox("Category", sorted(encoders["category"].classes_.tolist()))
    seat_type = st.selectbox("Seat Type", sorted(encoders["seat_type"].classes_.tolist()))
    gender = st.selectbox("Gender", sorted(encoders["gender"].classes_.tolist()))
    institute = st.selectbox("Institute", sorted(encoders["institute"].classes_.tolist()))
    submitted = st.form_submit_button("Predict Course", use_container_width=True)

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
        results = predict_top_n(models["course"], encoders["course"], X, n=TOP_N)

        st.subheader(f"Top {len(results)} Predicted Courses")
        for i, (label, prob) in enumerate(results, start=1):
            st.write(f"**{i}. {label}**  —  {prob * 100:.2f}%")
            st.progress(min(max(prob, 0.0), 1.0))
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Prediction failed: {e}")
