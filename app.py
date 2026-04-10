from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


@dataclass
class Metric:
    name: str
    total: float
    goal: float | None = None
    progress: float | None = None


SAMPLE_CSV = """2026 YTD SHIPS (+ in progress films),,,,,,,,,,,,last updated: 4/8,,Annual goals,total number,% complete,,,,,,,,,,,,
Written ,,Social,,Testimonial Films,,Brand + Innovation films,,Advocacy campaigns,,Quote banks ,,Ships Grand Total,,Written,50,30%,,,,,,,,,,,,
Zenken (Ent),1,Summits - Testimonial,4,Travelers ,in progress,Brand Campaign,in progress,Codex social-first,1,Frontiers launch ,8,52,,Social,150,20%,,,,,,,,,,,,
Cisco (Ent),1,Codex - Testiminial,4,Uber ,in progress,Fast Campus,in progress,"Customer posts 
(Advent, Target",2,5.4 launch,11,Q1,,Testimonial,5,100%,,,,,,,,,,,,
Trustbank (Ent),1,Raukten,6,US compilation film (Frontiers),in progress,,,,,,,,Q2,,Brand/Inno,3,67%,,,,,,,,,,,,
Taisei (Ent),1,RealPage,1,UK compilation film (Frontiers),in progress,,,,,,,,,,,,,,,,,,,,,,,
VFL Wolfsburg (Ent),1,GitHub,1,LSEG ,in progress,,,,,,,,,,Quarterly goals,total number,Q1 % complete,Q2 % complete,Q3 % complete,Q4 % complete,,,,,,,
Balyasny Asset Management (Ent),1,BCH,1,,,,,,,,,,,,,Written,12.5,112%,8%,0%,0%,,,,,,,
Rakuten (Ent),1,Notion,1,,,,,,,,,,,,,Social,37.5,67%,13%,0%,0%,,,,,,,
Wayfair (Ent),1,Sierra,1,,,,,,,,,,,,,Testimonial,1.25,0%,400%,0%,0%,,,,,,,
Stadler (Ent),1,me&u (Ryan Hendler),1,,,,,,,,,,,,,Brand/Inno,0.75,0%,267%,0%,0%,,,,,,,
Tolan (SU),1,Ramp,1, ,,,,,,,,,,,,,,,,,,,,,,,
Datadog (SU),1,Retail summit recap,1,,,,,,,,,,,,,,,,,,,,,,,,
Higgsfield (SU),1,Braintrust,1, ,,,,,,,,,,,,,,,,,,,,,,,
Praktika (SU),1,Customer post (Target),1,,,,,,,,,,,,,,,,,,,,,,,,
Descript (SU),1,Customer post (Advent Health),1,,,,,,,,,,,,,,,,,,,,,,,,
Gradient Labs (SU),1,"LGU+
",1,,,,,,,,,,,,,,,,,,,,,,,,
,,Stadler,1, ,,,,,,,,,,,,,,,,,,,,,,,
,,PAYG Codex Blog ,1, ,,,,,,,,,,,,,,,,,,,,,,,
,,Gradient Labs ,1,,,,,,,,,,,,,,,,,,,,,,,,
,,Codex Super Edit  ,1,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Total,15,Total,30,Total,5,Total,2,Total ,3,Total,19,,,,,,,,,,,,,,,,,
"""


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value).replace("\n", " ").strip()


def parse_number(value: Any) -> float | None:
    text = clean_text(value).replace(",", "")
    if not text:
        return None
    if text.endswith("%"):
        text = text[:-1]
    try:
        return float(text)
    except ValueError:
        return None


def parse_snapshot(df: pd.DataFrame) -> dict[str, Any]:
    df = df.fillna("")

    last_updated = ""
    annual_metrics: list[Metric] = []
    quarterly_metrics: list[dict[str, Any]] = []
    def cell(row_index: int, col_index: int) -> str:
        if row_index >= len(df.index) or col_index >= len(df.columns):
            return ""
        return clean_text(df.iat[row_index, col_index])

    title_row = [clean_text(value) for value in df.iloc[0].tolist()] if len(df.index) else []
    for value in title_row:
        if value.lower().startswith("last updated:"):
            last_updated = value.split(":", 1)[1].strip()

    annual_rows = [
        ("Written", 1),
        ("Social", 2),
        ("Testimonial", 3),
        ("Brand/Inno", 4),
    ]
    for expected_name, row_index in annual_rows:
        category = cell(row_index, 14) or expected_name
        goal = parse_number(cell(row_index, 15))
        progress = parse_number(cell(row_index, 16))
        if goal is not None:
            annual_metrics.append(
                Metric(name=category, goal=goal, progress=progress, total=0)
            )

    quarterly_rows = [
        ("Written", 7),
        ("Social", 8),
        ("Testimonial", 9),
        ("Brand/Inno", 10),
    ]
    for expected_name, row_index in quarterly_rows:
        category = cell(row_index, 14) or expected_name
        if not category:
            continue
        quarterly_metrics.append(
            {
                "name": category,
                "goal": parse_number(cell(row_index, 15)) or 0,
                "q1": parse_number(cell(row_index, 16)) or 0,
                "q2": parse_number(cell(row_index, 17)) or 0,
                "q3": parse_number(cell(row_index, 18)) or 0,
                "q4": parse_number(cell(row_index, 19)) or 0,
            }
        )

    category_pairs = [
        ("Written", 0, 1),
        ("Social", 2, 3),
        ("Testimonial", 4, 5),
        ("Brand/Inno", 6, 7),
        ("Advocacy campaigns", 8, 9),
        ("Quote banks", 10, 11),
    ]

    pipeline: dict[str, list[dict[str, Any]]] = {name: [] for name, _, _ in category_pairs}
    totals: dict[str, float] = {}
    ships_grand_total = parse_number(cell(2, 12)) or 0.0

    for row_index in range(2, len(df)):
        row_values = [clean_text(value) for value in df.iloc[row_index].tolist()]
        if any(value == "Total" for value in row_values[:12]):
            for name, label_col, value_col in category_pairs:
                totals[name] = parse_number(df.iat[row_index, value_col]) or 0
            break

        for name, label_col, value_col in category_pairs:
            item = clean_text(df.iat[row_index, label_col]) if label_col < len(df.columns) else ""
            measure = clean_text(df.iat[row_index, value_col]) if value_col < len(df.columns) else ""
            if item:
                pipeline[name].append({"item": item, "measure": measure})

    annual_by_name = {metric.name: metric for metric in annual_metrics}
    for name in ["Written", "Social", "Testimonial", "Brand/Inno"]:
        if name in annual_by_name:
            annual_by_name[name].total = totals.get(name, 0)

    annual_goal_total = sum(metric.goal or 0 for metric in annual_metrics)

    return {
        "last_updated": last_updated,
        "ships_grand_total": ships_grand_total,
        "annual_goal_total": annual_goal_total,
        "annual_metrics": annual_metrics,
        "supporting_metrics": [
            Metric(name="Advocacy campaigns", total=totals.get("Advocacy campaigns", 0)),
            Metric(name="Quote banks", total=totals.get("Quote banks", 0)),
        ],
        "quarterly_metrics": quarterly_metrics,
        "pipeline": pipeline,
    }


def find_recent_csv() -> Path | None:
    downloads = Path.home() / "Downloads"
    if not downloads.exists():
        return None

    candidates = []
    priority_terms = (
        "dane",
        "master",
        "customer marketing",
        "goal tracking",
        "output",
    )

    for path in downloads.glob("*.csv"):
        name = path.name.lower()
        score = sum(term in name for term in priority_terms)
        candidates.append((score, path.stat().st_mtime, path))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    best_score, _, best_path = candidates[0]
    if best_score == 0:
        return None
    return best_path


def load_snapshot(uploaded_file: Any) -> tuple[dict[str, Any], str]:
    if uploaded_file is not None:
        return parse_snapshot(
            pd.read_csv(uploaded_file, header=None, engine="python", on_bad_lines="skip")
        ), "Uploaded CSV"

    recent_csv = find_recent_csv()
    if recent_csv is not None:
        return parse_snapshot(
            pd.read_csv(recent_csv, header=None, engine="python", on_bad_lines="skip")
        ), f"Auto-loaded from Downloads: {recent_csv.name}"

    return parse_snapshot(
        pd.read_csv(io.StringIO(SAMPLE_CSV), header=None, engine="python", on_bad_lines="skip")
    ), "Built-in sample snapshot"


def progress_color(progress: float) -> str:
    if progress >= 100:
        return "#2ec4a6"
    if progress >= 60:
        return "#72b3ff"
    if progress >= 30:
        return "#f6bd60"
    return "#f28482"


def percent(value: float, digits: int = 0) -> str:
    return f"{value:.{digits}f}%"


def whole_number(value: float) -> str:
    return f"{int(round(value))}"


st.set_page_config(
    page_title="Customer Marketing outputs 2026",
    page_icon=":bar_chart:",
    layout="wide",
)

st.markdown(
    """
    <style>
      [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8, 15, 24, 0.96), rgba(9, 25, 39, 0.96));
        border-right: 1px solid rgba(186, 230, 253, 0.08);
      }
      [data-testid="stSidebar"] .st-emotion-cache-16txtl3,
      [data-testid="stSidebar"] .st-emotion-cache-1r6slb0 {
        padding-top: 1.4rem;
      }
      .stApp {
        background:
          radial-gradient(circle at top left, rgba(37, 99, 235, 0.14), transparent 26%),
          radial-gradient(circle at 90% 8%, rgba(16, 185, 129, 0.16), transparent 20%),
          linear-gradient(160deg, #07111a 0%, #0f2231 45%, #09151f 100%);
        color: #eff6ff;
      }
      .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
      }
      h1, h2, h3 {
        letter-spacing: -0.03em;
      }
      .glass {
        background: rgba(8, 20, 31, 0.78);
        border: 1px solid rgba(186, 230, 253, 0.12);
        border-radius: 24px;
        padding: 1.25rem 1.35rem;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
      }
      .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.5fr) minmax(280px, 0.8fr);
        gap: 1rem;
        margin-bottom: 1rem;
      }
      .hero {
        padding: 1.6rem 1.7rem;
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(8, 47, 73, 0.7));
        border: 1px solid rgba(125, 211, 252, 0.16);
      }
      .hero-stat {
        background: linear-gradient(180deg, rgba(7, 22, 35, 0.88), rgba(9, 35, 46, 0.72));
        border: 1px solid rgba(125, 211, 252, 0.14);
        border-radius: 28px;
        padding: 1.4rem 1.35rem;
      }
      .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #67e8f9;
        font-size: 0.76rem;
        font-weight: 700;
      }
      .hero h1 {
        margin: 0.2rem 0 0.4rem 0;
        font-size: 3rem;
      }
      .hero p {
        margin: 0;
        color: #cbd5e1;
        max-width: 52rem;
      }
      .metric {
        background: rgba(8, 20, 31, 0.78);
        border: 1px solid rgba(186, 230, 253, 0.12);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        min-height: 8.6rem;
      }
      .metric-label {
        color: #94a3b8;
        font-size: 0.86rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }
      .metric-value {
        font-size: 2.6rem;
        line-height: 1.05;
        font-weight: 800;
        margin: 0.45rem 0;
      }
      .metric-note {
        color: #cbd5e1;
        font-size: 0.95rem;
      }
      .subtle {
        color: #94a3b8;
      }
      .section-title {
        margin: 1.4rem 0 0.6rem 0;
        font-size: 1.3rem;
        font-weight: 700;
      }
      .insight-stack {
        display: grid;
        gap: 0.8rem;
      }
      .insight {
        padding: 1rem 1.05rem;
        border-radius: 20px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.12);
      }
      .insight strong {
        display: block;
        color: #f8fafc;
        margin-bottom: 0.3rem;
      }
      .goal-strip {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        gap: 0.6rem;
      }
      .upload-tip {
        padding: 1rem 1.05rem;
        border-radius: 18px;
        background: rgba(14, 33, 49, 0.85);
        border: 1px solid rgba(103, 232, 249, 0.12);
        margin: 0.75rem 0 1rem 0;
      }
      .pill {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.65rem;
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.12);
        border: 1px solid rgba(45, 212, 191, 0.18);
        color: #b6fff3;
        font-size: 0.82rem;
        font-weight: 600;
      }
      @media (max-width: 980px) {
        .hero-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.header("Data Source")
st.sidebar.markdown(
    """
    <div class="upload-tip">
      <div class="eyebrow">Refresh Flow</div>
      Download the active Google Sheet tab as a CSV. This app will now try to auto-load the newest matching CSV from Downloads.
    </div>
    """,
    unsafe_allow_html=True,
)
if st.sidebar.button("Refresh from latest CSV"):
    st.rerun()
uploaded_file = st.sidebar.file_uploader(
    "Or upload CSV export of `Master total_for Dane`",
    type=["csv"],
    help="In Google Sheets: File -> Download -> Comma-separated values (.csv) for the active tab.",
)

snapshot, source_label = load_snapshot(uploaded_file)
annual_metrics = snapshot["annual_metrics"]
supporting_metrics = snapshot["supporting_metrics"]
quarterly_metrics = snapshot["quarterly_metrics"]
pipeline = snapshot["pipeline"]

st.sidebar.caption(f"Current source: {source_label}")

overall_progress = (
    (snapshot["ships_grand_total"] / snapshot["annual_goal_total"]) * 100
    if snapshot["annual_goal_total"]
    else 0
)
top_metric = max(annual_metrics, key=lambda item: item.progress or 0) if annual_metrics else None
top_shipped = max(
    annual_metrics + supporting_metrics,
    key=lambda item: item.total,
) if annual_metrics or supporting_metrics else None

social = next((item for item in annual_metrics if item.name == "Social"), None)
testimonial = next((item for item in annual_metrics if item.name == "Testimonial"), None)
quote_banks = next((item for item in supporting_metrics if item.name == "Quote banks"), None)
advocacy = next((item for item in supporting_metrics if item.name == "Advocacy campaigns"), None)

st.markdown(
    f"""
    <div class="hero-grid">
      <div class="hero">
        <div class="eyebrow">Master total_for Dane</div>
        <h1>Customer Marketing outputs 2026</h1>
        <p>
          A local planning view for shipped volume, goal pacing, and pipeline mix.
          {source_label}
        </p>
      </div>
      <div class="hero-stat">
        <div class="eyebrow">Status</div>
        <p style="font-size:2rem;font-weight:800;margin:0.25rem 0 0.35rem 0;">{percent(overall_progress)}</p>
        <p style="margin:0;color:#cbd5e1;">Overall progress toward the annual tracked goal.</p>
        <div style="margin-top:0.95rem;">
          <span class="pill">{f"Updated {snapshot['last_updated']}" if snapshot["last_updated"] else "Awaiting live upload"}</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    st.markdown(
        f"""
        <div class="metric">
          <div class="metric-label">Ships Grand Total</div>
          <div class="metric-value">{int(snapshot["ships_grand_total"])}</div>
          <div class="metric-note">{percent(overall_progress)} of annual goal complete</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_cols[1]:
    annual_total = sum(metric.total for metric in annual_metrics)
    st.markdown(
        f"""
        <div class="metric">
          <div class="metric-label">Goal-Tracked Output</div>
          <div class="metric-value">{int(annual_total)}</div>
          <div class="metric-note">Across written, social, testimonial, and brand/inno</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_cols[2]:
    st.markdown(
        f"""
        <div class="metric">
          <div class="metric-label">Top Volume Lane</div>
          <div class="metric-value">{top_shipped.name if top_shipped else "N/A"}</div>
          <div class="metric-note">{int(top_shipped.total) if top_shipped else 0} total items</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with metric_cols[3]:
    st.markdown(
        f"""
        <div class="metric">
          <div class="metric-label">Best Goal Progress</div>
          <div class="metric-value">{percent(top_metric.progress or 0) if top_metric else "0%"}</div>
          <div class="metric-note">{top_metric.name if top_metric else "No annual goal data"}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

left, right = st.columns([1.3, 1], gap="large")

with left:
    st.subheader("Category Mix")
    category_df = pd.DataFrame(
        [
            {"Category": metric.name, "Total": metric.total}
            for metric in annual_metrics + supporting_metrics
        ]
    ).sort_values("Total", ascending=False)
    st.bar_chart(category_df.set_index("Category"))

    st.subheader("Annual Goal Progress")
    annual_df = pd.DataFrame(
        [
            {
                "Category": metric.name,
                "Shipped": metric.total,
                "Goal": metric.goal,
                "Progress %": metric.progress,
                "Remaining": max((metric.goal or 0) - metric.total, 0),
            }
            for metric in annual_metrics
        ]
    )
    if not annual_df.empty:
        st.dataframe(
            annual_df.style.format(
                {
                    "Shipped": "{:.0f}",
                    "Goal": "{:.2f}",
                    "Progress %": "{:.0f}%",
                    "Remaining": "{:.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

with right:
    st.subheader("Signals")
    if annual_metrics:
        st.markdown(
            f"""
            <div class="insight-stack">
              <div class="insight">
                <strong>{top_shipped.name if top_shipped else "Top lane"}</strong>
                {whole_number(top_shipped.total) if top_shipped else "0"} items make this the biggest visible output lane right now.
              </div>
              <div class="insight">
                <strong>{testimonial.name if testimonial else "Testimonial"} pacing</strong>
                {percent(testimonial.progress or 0)} puts this lane furthest ahead on annual progress.
              </div>
              <div class="insight">
                <strong>{social.name if social else "Social"} gap</strong>
                {whole_number(max((social.goal or 0) - social.total, 0)) if social else "0"} items still remain to hit the annual target.
              </div>
              <div class="insight">
                <strong>Support work</strong>
                {whole_number(quote_banks.total) if quote_banks else "0"} quote-bank items and {whole_number(advocacy.total) if advocacy else "0"} advocacy items sit outside the main goal-tracked total.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Quarterly View")
    if quarterly_metrics:
        quarterly_df = pd.DataFrame(quarterly_metrics)
        quarterly_long = quarterly_df.melt(
            id_vars=["name", "goal"],
            value_vars=["q1", "q2", "q3", "q4"],
            var_name="Quarter",
            value_name="Progress %",
        )
        st.dataframe(
            quarterly_long.rename(columns={"name": "Category", "goal": "Quarterly Goal"}).style.format(
                {"Quarterly Goal": "{:.2f}", "Progress %": "{:.0f}%"}
            ),
            use_container_width=True,
            hide_index=True,
        )

st.markdown('<div class="section-title">Goal Cards</div>', unsafe_allow_html=True)
goal_cols = st.columns(len(annual_metrics) or 1)
for col, metric in zip(goal_cols, annual_metrics):
    remaining = max((metric.goal or 0) - metric.total, 0)
    progress = metric.progress or 0
    color = progress_color(progress)
    with col:
        st.markdown(
            f"""
            <div class="glass">
              <div class="goal-strip">
                <div class="metric-label">{metric.name}</div>
                <div style="color:{color};font-weight:700;">{percent(progress)}</div>
              </div>
              <div class="metric-value" style="font-size:2rem;">{whole_number(metric.total)}</div>
              <div class="subtle">Goal {metric.goal:g} • Remaining {remaining:g}</div>
              <div style="margin-top:0.9rem;background:rgba(148,163,184,0.18);border-radius:999px;height:12px;">
                <div style="width:{min(progress, 100)}%;background:{color};height:12px;border-radius:999px;"></div>
              </div>
              <div style="margin-top:0.75rem;color:#e2e8f0;">{whole_number(metric.total)} shipped so far</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

pipeline_left, pipeline_right = st.columns([1.15, 0.85], gap="large")
with pipeline_left:
    st.markdown('<div class="section-title">Pipeline Snapshot</div>', unsafe_allow_html=True)
    selected_lane = st.selectbox("Choose a content lane", list(pipeline.keys()))
    lane_items = pipeline[selected_lane]
    lane_df = pd.DataFrame(lane_items).rename(columns={"item": "Item", "measure": "Count / Status"})
    st.dataframe(lane_df, use_container_width=True, hide_index=True)

with pipeline_right:
    st.markdown('<div class="section-title">Quick Read</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="glass">
          <div class="metric-label">Selected Lane</div>
          <div class="metric-value" style="font-size:2rem;">{selected_lane}</div>
          <div class="metric-note">{len(lane_items)} visible line items in this CSV snapshot.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if lane_items:
        preview_items = ", ".join(item["item"] for item in lane_items[:3])
        st.markdown(
            f"""
            <div class="glass" style="margin-top:0.8rem;">
              <div class="metric-label">Preview</div>
              <div class="metric-note" style="margin-top:0.55rem;">{preview_items}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander("How to use your real sheet export"):
    st.markdown(
        """
        1. Open the `Master total_for Dane` tab in Google Sheets.
        2. Use `File -> Download -> Comma-separated values (.csv)` while that tab is active.
        3. Upload the CSV in the sidebar.
        4. The dashboard will swap from the sample snapshot to your exported data.
        """
    )

if snapshot["last_updated"]:
    st.caption(f"Source note from sheet: last updated {snapshot['last_updated']}")
