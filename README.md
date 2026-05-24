# DigiSaatBaara — Geofencing & Crop Prediction for Farmers

> Civic Tech · AgriTech · IEEE Published · 2021

End-to-end platform that digitises **Saat Baara** land documents (Maharashtra's official land records) to enable GPS-based geofencing of farmland and ML-driven crop prediction. Government admins upload land records; farmers get tailored crop recommendations and cost analysis on a web dashboard.

**📄 IEEE Published**  
👉 [Geofencing and Efficient Crop Prediction Using Government Documents — IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/9708082)

## Highlights
- Parses unstructured government land documents to extract structured soil + crop history data
- Geofences land parcels using GPS coordinates with ±2% area tolerance
- Crop prediction ML model trained on regional soil health card data
- Full stack: Android app (data collection) + Flask web app (analysis + dashboard)

## Architecture
```
Android App (Farmer / Admin)
       │
  GPS Geofencing + Document Upload
       │
  Flask Backend (Python)
       │
  ┌────┴──────────────────┐
  │                       │
Crop Prediction        Rainfall Analysis
(scikit-learn)         (historical CSV data)
  │                       │
  └────────┬──────────────┘
           │
    Plotly Dashboard       ← interactive charts for farmers
```

---

## Setup & Running

### Web App (Flask)

#### 1. Clone & Install
```bash
git clone https://github.com/tsenthil5/DigiSaatBaara
cd DigiSaatBaara/WebApp
pip install -r requirements.txt
```

> Requires Python 3.8+.

#### 2. Run the Server
```bash
python main.py
```

Open your browser at: **http://localhost:5000**

The server will start and show:
```
* Running on http://127.0.0.1:5000/
```

> To enable debug mode: `FLASK_DEBUG=true python main.py`

#### 3. What you'll see
- Crop prediction form — enter soil/land details to get crop recommendations
- Rainfall analysis charts — seasonal rainfall trends by region
- Cost analysis per predicted crop

---

### Android App

The Android app was built for data collection in the field (GPS geofencing + document upload). APK and source are in the `Android_App/` folder. Open in Android Studio to build.

---

## Data Files Included

All CSV data files are included in the repo — no external downloads required:

| File | Contents |
|---|---|
| `crop_prediction.xlsx` | Training data for crop prediction model |
| `rainfall_dataset.csv` | Full rainfall dataset |
| `rain_jf.csv` | Jan–Feb seasonal rainfall |
| `rain_jjas.csv` | Jun–Sep (monsoon) rainfall |
| `rain_mam.csv` | Mar–May seasonal rainfall |
| `rain_ons.csv` | Oct–Nov seasonal rainfall |

---

## Tech Stack
`Python` `Flask` `scikit-learn` `Plotly` `Pandas` `NumPy` `Android` `Google Maps SDK`

## Citation
```
S. Thanneermalai, et al.,
"Geofencing and Efficient Crop Prediction Using Government Documents,"
IEEE ICACC 2021. https://ieeexplore.ieee.org/abstract/document/9708082
```
