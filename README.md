# Dane Dashboard

Local Streamlit dashboard for the `Master total_for Dane` tab.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Load live data

1. Open the `Master total_for Dane` tab in Google Sheets.
2. Choose `File -> Download -> Comma-separated values (.csv)` while that tab is active.
3. Upload that CSV in the Streamlit sidebar.

If you do not upload a CSV yet, the app uses a built-in sample snapshot based on the sheet structure we inspected.
