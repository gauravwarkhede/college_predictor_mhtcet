"""
Run this ONCE, locally, in the same environment where your original .pkl
files load correctly (i.e. where `import xgboost` works and matches the
version they were trained with — check with `python -c "import xgboost;
print(xgboost.__version__)"` and pin the same version in requirements.txt).

It converts the heavy sklearn-wrapper pickles into XGBoost's native model
format (institute_model.json / course_model.json), which the app will
automatically prefer over the .pkl files if present (see model_utils.py).
This tends to load lighter in memory at runtime, which matters on
memory-capped free hosting tiers.

Usage:
    python convert_models.py
"""
import os
import pickle

import xgboost as xgb

MODELS_DIR = "models"

for name in ["institute_model", "course_model"]:
    pkl_path = os.path.join(MODELS_DIR, f"{name}.pkl")
    out_path = os.path.join(MODELS_DIR, f"{name}.json")

    with open(pkl_path, "rb") as f:
        clf = pickle.load(f)

    booster = clf.get_booster()
    booster.save_model(out_path)
    print(f"Saved {out_path}")

print("Done. Commit the new .json files (you can keep or remove the old .pkl files).")
