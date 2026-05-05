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

The shared dashboard can read either the Google Sheet directly or a published CSV snapshot from this repo. CSV upload inside the Streamlit sidebar is only for a one-session local preview; it does not publish data to Streamlit Cloud.

If your Google Workspace allows service accounts, keep the shared URL current this way:

1. Configure the deployed Streamlit app's Secrets with the `[connections.gsheets]` service account block below.
2. Share the Google Sheet with the service account email address as a viewer.
3. Update the `Master total_for Dane` tab in Google Sheets.
4. Use the dashboard's `Refresh source` button when you want to force a rerun.

If Google Cloud or public Sheet sharing is blocked, publish the latest CSV snapshot instead:

```bash
python publish_snapshot.py --push
```

By default, the script picks the newest matching CSV from Desktop or Downloads. You can also pass a specific export:

```bash
python publish_snapshot.py ~/Downloads/my-export.csv --push
```

The shared app reads `data/latest_snapshot.csv` when Google Sheets access is unavailable.

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
