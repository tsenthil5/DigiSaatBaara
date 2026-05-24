"""
main.py
-------
DigiSaatBaara — Flask web application for crop prediction and rainfall analysis.

Reads pre-processed rainfall and crop-production CSV data, builds Plotly charts,
and renders them in the browser via an index.html template.

Usage:
    cd WebApp/
    pip install -r requirements.txt
    python main.py
    # Then open http://localhost:5000 in your browser
"""

import json
import os

import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import Flask, render_template

# ── App configuration ──────────────────────────────────────────
app = Flask(__name__)
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

# ── Data paths (relative to WebApp/ directory) ─────────────────
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(DATA_DIR, "static")


def _load_csv(filename: str, subdir: str = "") -> pd.DataFrame:
    """Load a CSV from the data or static directory."""
    base = STATIC_DIR if subdir == "static" else DATA_DIR
    return pd.read_csv(os.path.join(base, filename))


def _rainfall_traces(df: pd.DataFrame, year_col: pd.Series) -> list[go.BaseTraceType]:
    """Build Actual / Predicted / confidence-band scatter traces for a rainfall dataset."""
    rain_col = "Predicted" if "Predicted" in df.columns else "Prediction"
    return [
        go.Scatter(x=year_col, y=df["Rainfall"], name="Actual", mode="lines"),
        go.Scatter(x=year_col, y=df[rain_col], name="Predicted", mode="lines"),
        go.Scatter(x=year_col, y=df["Lower"], name="Lower",
                   line=dict(color="grey", width=2, dash="dot")),
        go.Scatter(x=year_col, y=df["Upper"], name="Upper", fill="tonexty",
                   line=dict(color="grey", width=2, dash="dot")),
    ]


@app.route("/")
def index():
    """
    Render the main dashboard with rainfall forecasts and crop-production charts.

    Loads four seasonal rainfall datasets (Jan–Feb, JJAS, MAM, Oct–Nov–Sep)
    and three crop datasets (rice, sugarcane, cotton), serialises them as
    Plotly JSON, and injects them into the Jinja2 template.
    """
    # Load datasets
    rain_jf   = _load_csv("rain_jf.csv")
    rain_jjas = _load_csv("rain_jjas.csv")
    rain_mam  = _load_csv("rain_mam.csv")
    rain_ons  = _load_csv("rain_ons.csv")
    produce   = _load_csv("produce_chart.csv", subdir="static")

    year = rain_jf["Year"]

    # Rainfall traces
    traces = {
        "rain_jf":   _rainfall_traces(rain_jf,   year),
        "rain_jjas": _rainfall_traces(rain_jjas,  year),
        "rain_mam":  _rainfall_traces(rain_mam,   year),
        "rain_ons":  _rainfall_traces(rain_ons,   year),
    }

    # Crop-production traces
    crop_traces = {
        "rice":      [go.Scatter(x=produce["Area"], y=produce["Rice"],      name="Rice",      mode="lines")],
        "sugarcane": [go.Scatter(x=produce["Area"], y=produce["Sugarcane"], name="Sugarcane", mode="lines")],
        "cotton":    [go.Scatter(x=produce["Area"], y=produce["Cotton"],    name="Cotton",    mode="lines")],
    }

    encoder = plotly.utils.PlotlyJSONEncoder

    return render_template(
        "index.html",
        json_rain_jf    = json.dumps(traces["rain_jf"],   cls=encoder),
        json_rain_ijas  = json.dumps(traces["rain_jjas"],  cls=encoder),
        json_rain_mam   = json.dumps(traces["rain_mam"],   cls=encoder),
        json_rain_ons   = json.dumps(traces["rain_ons"],   cls=encoder),
        json_produce_rice      = json.dumps(crop_traces["rice"],      cls=encoder),
        json_produce_sugar     = json.dumps(crop_traces["sugarcane"], cls=encoder),
        json_produce_cotton    = json.dumps(crop_traces["cotton"],    cls=encoder),
    )


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=5000)
