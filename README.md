# College Predictor (Streamlit)
app link:https://collegepredictormhtcet-mxhxcpi38gj8pz3ze2n7fe.streamlit.app/Course_Predictor

Two-page Streamlit app:
- **Institute Predictor** — from percentile, category, seat type, gender, course
- **Course Predictor** — from percentile, category, seat type, gender, institute

Streamlit auto-generates the sidebar navigation from the `pages/` folder —
no routing code needed.

## Features

- Clean landing page (`app.py`) with nav cards linking to both predictor pages
- Results ranked by probability, shown as styled cards + progress bars,
  with an adjustable "number of colleges/courses to show" slider
- **10 switchable color themes** (sidebar dropdown), persisted across pages
  for the session — see `theme.py`
- Footer credit on every page: "Made with ❤️ by Gaurav"

## ⚠️ Before you deploy — confirm feature order

Same caveat as before: the XGBoost models were pickled without column names,
so I can't verify the exact input order they were trained on. Open
`model_utils.py` and check:

```python
FEATURE_ORDER_INSTITUTE = ["percentile", "category", "seat_type", "gender", "course"]
FEATURE_ORDER_COURSE    = ["percentile", "category", "seat_type", "gender", "institute"]
```

Match these to your training notebook's actual column order. The app runs
fine either way — but wrong order means confidently wrong predictions.

## Project structure

```
.
├── app.py                        # Home / landing page (nav cards)
├── pages/
│   ├── 1_Institute_Predictor.py
│   └── 2_Course_Predictor.py
├── theme.py                      # 10 color themes + CSS injection + footer
├── model_utils.py                # shared loading + prediction logic
├── convert_models.py             # optional: pkl -> lighter native json format
├── requirements.txt
├── .streamlit/config.toml        # minimal base config
└── models/
    ├── institute_model.pkl (or .json after conversion)
    ├── course_model.pkl (or .json after conversion)
    ├── category_encoder.pkl
    ├── course_encoder.pkl
    ├── gender_encoder.pkl
    ├── institute_encoder.pkl
    └── seat_encoder.pkl
```

The app automatically uses `institute_model.json` / `course_model.json` if
present (lighter to load), otherwise falls back to the `.pkl` files — so it
works before *and* after you run `convert_models.py`.

## Run locally

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501 — sidebar has both pages.

(Optional, recommended for memory) convert the models first:
```bash
python convert_models.py
```

---

## Deployment options

### Option A — Streamlit Community Cloud (free)

**Requires a public GitHub repo** (not GitLab — Community Cloud doesn't
support GitLab). If your code currently lives on GitLab, either push a copy
to GitHub too, or mirror it:

```bash
git remote add github https://github.com/<you>/college_predictor.git
git push github main
```

Then:
1. Go to https://share.streamlit.io → sign in with GitHub
2. **New app** → pick the repo, branch, and set **Main file path** to `app.py`
3. Deploy

Free tier gives roughly 1GB RAM and apps sleep after ~12 hours of no
traffic (slow to wake up on the next visit — normal, not a bug).

If your model files are large, use **Git LFS** on GitHub the same way you
did on GitLab (`git lfs track "*.pkl"` and/or `"*.json"`), since GitHub also
has a 100MB per-file limit on regular commits.

### Option B — Hugging Face Spaces (free, usually more RAM headroom)

1. Create a new Space at https://huggingface.co/new-space
2. SDK: **Streamlit**
3. Push your code (Spaces uses git):
   ```bash
   git remote add hf https://huggingface.co/spaces/<you>/college-predictor
   git push hf main
   ```
4. Space builds automatically and serves `app.py`

Large files: Hugging Face has native, generous LFS support — `git lfs track`
the same way, it's built for this.

### Option C — Render, running Streamlit instead of Flask

You can reuse your existing GitLab repo/Render project. Change:

- **Start Command:**
  ```
  streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  ```

Note: this doesn't change Render's 512MB free-tier RAM limit — if that was
the blocker before, switching to Streamlit alone won't fix it. Combine with
`convert_models.py` and/or a paid instance if you stay on Render.

## Notes

- `scikit-learn==1.6.1` and `xgboost==2.1.1` are pinned to match the
  versions your encoders/models were originally saved with. If you retrain
  with different versions, update these pins to match.
- `st.cache_resource` in `model_utils.py` ensures models/encoders load once
  per app process, not on every user interaction.
