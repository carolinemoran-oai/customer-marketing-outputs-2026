# Dane Dashboard

Local Streamlit dashboard for the `Master total_for Dane` tab.

## Run it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy it

For Appy/Appliku-style hosting, use this web process command:

```bash
bash run.sh
```

Set `SERVER_NAME` to the app domain if your host requires it. `PORT` is usually provided by the host automatically.

## Keep the shared dashboard current

The shared dashboard should read the Google Sheet directly. CSV upload is only for a one-session local preview; it does not publish data to Streamlit Cloud.

To keep the shared URL current:

1. Configure the deployed Streamlit app's Secrets with the `[connections.gsheets]` service account block below.
2. Share the Google Sheet with the service account email address as a viewer.
3. Update the `Master total_for Dane` tab in Google Sheets.
4. Use the dashboard's `Refresh source` button when you want to force a rerun.

## Load live data

1. Open the `Master total_for Dane` tab in Google Sheets.
2. Choose `File -> Download -> Comma-separated values (.csv)` while that tab is active.
3. Upload that CSV in the Streamlit sidebar.

If you do not upload a CSV yet and Google Sheets secrets are unavailable, the app uses a built-in sample snapshot based on the sheet structure we inspected.

## Live Google Sheets

The app can also read directly from the Google Sheet tab when a Google service account is configured in Streamlit secrets.

Create `.streamlit/secrets.toml` with:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/1cF9mfhyVOukIPydhFN9aG7VryWRvvv8UoqlcHoxsUiI/edit?gid=2001564991#gid=2001564991"
type = "service_account"
# Add the remaining service-account JSON fields in this same block.
```

Then share the Google Sheet with the service account email address as a viewer.
When you paste the credential text, keep escaped newline characters exactly as they appear in the downloaded service-account JSON.
