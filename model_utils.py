"""
Shared helpers for both Streamlit pages: loading encoders/models once
(cached across reruns and page navigations) and running predictions.

Same feature-order caveat as the Flask version: the XGBoost models were
pickled without column names, so FEATURE_ORDER_INSTITUTE / FEATURE_ORDER_COURSE
below need to match whatever order you used when training. Edit if needed.
"""

import os
import pickle

import numpy as np
import streamlit as st

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

FEATURE_ORDER_INSTITUTE = ["percentile", "category", "seat_type", "gender", "course"]
FEATURE_ORDER_COURSE = ["percentile", "category", "seat_type", "gender", "institute"]

TOP_N = 5


def _load_pickle(filename):
    path = os.path.join(MODELS_DIR, filename)
    with open(path, "rb") as f:
        return pickle.load(f)


@st.cache_resource
def load_encoders():
    """Loaded once per app process and reused across pages/reruns."""
    return {
        "category": _load_pickle("category_encoder.pkl"),
        "seat_type": _load_pickle("seat_encoder.pkl"),
        "gender": _load_pickle("gender_encoder.pkl"),
        "course": _load_pickle("course_encoder.pkl"),
        "institute": _load_pickle("institute_encoder.pkl"),
    }


@st.cache_resource
def load_models():
    """
    Loads institute_model + course_model, once per app process.

    Prefers the lightweight native XGBoost format (institute_model.json /
    course_model.json — see convert_models.py) if present, since it uses
    less memory than unpickling the full sklearn wrapper. Falls back to
    the original .pkl files automatically if you haven't run the
    conversion yet, so the app works either way.
    """
    def _load_one(base_name):
        json_path = os.path.join(MODELS_DIR, f"{base_name}.json")
        pkl_path = os.path.join(MODELS_DIR, f"{base_name}.pkl")
        if os.path.exists(json_path):
            import xgboost as xgb
            booster = xgb.Booster()
            booster.load_model(json_path)
            return booster, "booster"
        clf = _load_pickle(f"{base_name}.pkl")
        return clf, "sklearn"

    return {
        "institute": _load_one("institute_model"),
        "course": _load_one("course_model"),
    }


def encode_value(encoders, field_name, raw_value):
    """Encode a single value with the right LabelEncoder (or float for percentile)."""
    if field_name == "percentile":
        return float(raw_value)

    encoder = encoders[field_name]
    try:
        return int(encoder.transform([raw_value])[0])
    except ValueError:
        raise ValueError(
            f"'{raw_value}' is not a recognized value for '{field_name}'. "
            f"Please pick one of the values from the dropdown."
        )


def build_feature_vector(encoders, values, feature_order):
    """values: dict of {field_name: raw_value}. Returns an ordered (1, n) array."""
    row = []
    for field in feature_order:
        raw_value = values.get(field)
        if raw_value is None or raw_value == "":
            raise ValueError(f"Missing value for '{field}'.")
        row.append(encode_value(encoders, field, raw_value))
    return np.array(row, dtype=float).reshape(1, -1)


def predict_top_n(model_tuple, label_encoder, X, n=TOP_N):
    """model_tuple is (model, kind) from load_models() — kind is 'booster' or 'sklearn'."""
    model, kind = model_tuple
    if kind == "booster":
        import xgboost as xgb
        probs = model.predict(xgb.DMatrix(X))[0]
    else:
        probs = model.predict_proba(X)[0]

    top_idx = np.argsort(probs)[::-1][:n]
    labels = label_encoder.inverse_transform(top_idx)
    return [(str(label), float(probs[i])) for label, i in zip(labels, top_idx)]
