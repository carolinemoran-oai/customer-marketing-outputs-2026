const snapshot = {
  lastUpdated: "4/8",
  shipsGrandTotal: 52,
  annualGoalTotal: 208,
  annualCategories: [
    { name: "Written", total: 15, goal: 50, progress: 30 },
    { name: "Social", total: 30, goal: 150, progress: 20 },
    { name: "Testimonial", total: 5, goal: 5, progress: 100 },
    { name: "Brand/Inno", total: 2, goal: 3, progress: 67 }
  ],
  supportingCategories: [
    { name: "Advocacy campaigns", total: 3 },
    { name: "Quote banks", total: 19 }
  ],
  quarterlyCategories: [
    { name: "Written", goal: 12.5, q1: 112, q2: 8, q3: 0, q4: 0, q1Total: 14, q2Total: 1, q3Total: 0, q4Total: 0 },
    { name: "Social", goal: 37.5, q1: 67, q2: 13, q3: 0, q4: 0, q1Total: 25, q2Total: 5, q3Total: 0, q4Total: 0 },
    { name: "Testimonial", goal: 1.25, q1: 0, q2: 400, q3: 0, q4: 0, q1Total: 0, q2Total: 5, q3Total: 0, q4Total: 0 },
    { name: "Brand/Inno", goal: 0.75, q1: 0, q2: 267, q3: 0, q4: 0, q1Total: 0, q2Total: 2, q3Total: 0, q4Total: 0 }
  ],
  pipeline: {
    Written: [
      "Zenken (Ent)",
      "Cisco (Ent)",
      "Trustbank (Ent)",
      "Taisei (Ent)",
      "VFL Wolfsburg (Ent)",
      "Balyasny Asset Management (Ent)"
    ],
    Social: [
      "Summits - Testimonial",
      "Codex - Testiminial",
      "Raukten",
      "RealPage",
      "GitHub",
      "BCH"
    ],
    "Testimonial Films": [
      "Travelers",
      "Uber",
      "US compilation film (Frontiers)",
      "UK compilation film (Frontiers)",
      "LSEG"
    ],
    "Brand + Innovation": [
      "Brand Campaign",
      "Fast Campus"
    ],
    "Advocacy campaigns": [
      "Codex social-first",
      "Customer posts (Advent, Target)"
    ],
    "Quote banks": [
      "Frontiers launch",
      "5.4 launch",
      "Codex Super Edit"
    ]
  }
};

const modeConfig = {
  ships: {
    title: "Ships by content type",
    breakdownTitle: "Shipped volume by lane",
    tableTitle: "Annual goal snapshot",
    activityTitle: "Representative items from the tab",
    badge: "6 content lanes tracked",
    chart: [
      { label: "Written", value: 15 },
      { label: "Social", value: 30 },
      { label: "Testimonial", value: 5 },
      { label: "Brand/Inno", value: 2 },
      { label: "Advocacy", value: 3 },
      { label: "Quote banks", value: 19 }
    ],
    bars: [
      { label: "Social", value: 30, display: "30", note: "largest shipped lane" },
      { label: "Quote banks", value: 19, display: "19", note: "high supporting output" },
      { label: "Written", value: 15, display: "15", note: "30% of annual target" },
      { label: "Testimonial", value: 5, display: "5", note: "already at annual goal" },
      { label: "Advocacy", value: 3, display: "3", note: "supporting campaign work" },
      { label: "Brand/Inno", value: 2, display: "2", note: "67% of annual target" }
    ],
    insights: [
      {
        kicker: "Concentration",
        text: "Social drives the biggest share of shipped work, with 30 completed items already on the board."
      },
      {
        kicker: "Overperformer",
        text: "Testimonial work has already reached 100% of the annual goal, making it the clearest ahead-of-plan category."
      },
      {
        kicker: "Hidden volume",
        text: "Quote banks add 19 extra deliverables beyond the 52-goal-based ship total, so the broader workload is larger than the goal view suggests."
      }
    ]
  },
  annual: {
    title: "Annual goals by category",
    breakdownTitle: "Progress against annual goal",
    tableTitle: "Annual goal detail",
    activityTitle: "Representative items in goal-tracked lanes",
    badge: "208 total annual goal units",
    chart: snapshot.annualCategories.map((item) => ({
      label: item.name,
      value: item.goal
    })),
    bars: snapshot.annualCategories
      .map((item) => ({
        label: item.name,
        value: item.progress,
        display: `${item.progress}%`,
        note: `${item.total} of ${item.goal} complete`
      }))
      .sort((a, b) => b.value - a.value),
    insights: [
      {
        kicker: "Ahead",
        text: "Testimonial is fully complete for the year, while Brand/Inno is also well ahead at 67%."
      },
      {
        kicker: "Gap",
        text: "Social has the biggest remaining lift: 120 units still needed to hit the annual target of 150."
      },
      {
        kicker: "Overall",
        text: "Across the annual-goal categories, 52 of 208 planned units are complete, which puts the tracked goal view at 25%."
      }
    ]
  },
  quarterly: {
    title: "Quarterly shipped output",
    breakdownTitle: "Quarter completion by category",
    tableTitle: "Quarterly goal detail",
    activityTitle: "Representative items feeding quarterly goals",
    badge: "Q1 and Q2 are the active quarters",
    chart: [
      { label: "Q1", value: 39 },
      { label: "Q2", value: 13 },
      { label: "Q3", value: 0 },
      { label: "Q4", value: 0 }
    ],
    bars: [
      { label: "Testimonial Q2", value: 400, display: "400%", note: "5 against a 1.25 goal" },
      { label: "Brand/Inno Q2", value: 267, display: "267%", note: "2 against a 0.75 goal" },
      { label: "Written Q1", value: 112, display: "112%", note: "14 against a 12.5 goal" },
      { label: "Social Q1", value: 67, display: "67%", note: "25 against a 37.5 goal" },
      { label: "Social Q2", value: 13, display: "13%", note: "5 against a 37.5 goal" },
      { label: "Written Q2", value: 8, display: "8%", note: "1 against a 12.5 goal" }
    ],
    insights: [
      {
        kicker: "Peak quarter",
        text: "Q1 produced roughly 39 shipped units across the quarterly-goal categories, about triple the current Q2 total."
      },
      {
        kicker: "Spike",
        text: "Testimonial and Brand/Inno both outperform in Q2 percentage terms because their quarterly goals are small and current output is above plan."
      },
      {
        kicker: "Watchout",
        text: "Q3 and Q4 have no visible progress yet in the tab snapshot, which may be fine now but leaves no forward buffer."
      }
    ]
  }
};

const elements = {
  reportingDate: document.querySelector("#reportingDate"),
  focusHeadline: document.querySelector("#focusHeadline"),
  heroHeadline: document.querySelector("#heroHeadline"),
  revenueValue: document.querySelector("#revenueValue"),
  revenueDelta: document.querySelector("#revenueDelta"),
  revenueNarrative: document.querySelector("#revenueNarrative"),
  leadsValue: document.querySelector("#leadsValue"),
  leadsDelta: document.querySelector("#leadsDelta"),
  conversionValue: document.querySelector("#conversionValue"),
  conversionDelta: document.querySelector("#conversionDelta"),
  retentionValue: document.querySelector("#retentionValue"),
  retentionDelta: document.querySelector("#retentionDelta"),
  trendTitleText: document.querySelector("#trendTitleText"),
  breakdownTitle: document.querySelector("#breakdownTitle"),
  tableTitle: document.querySelector("#tableTitle"),
  activityTitle: document.querySelector("#activityTitle"),
  trendSummary: document.querySelector("#trendSummary"),
  trendArea: document.querySelector("#trendArea"),
  trendLine: document.querySelector("#trendLine"),
  trendDots: document.querySelector("#trendDots"),
  trendLabels: document.querySelector("#trendLabels"),
  channelBars: document.querySelector("#channelBars"),
  insightList: document.querySelector("#insightList"),
  regionTable: document.querySelector("#regionTable"),
  activityList: document.querySelector("#activityList"),
  segments: document.querySelectorAll(".segment")
};

function formatPercent(value) {
  return `${Math.round(value)}%`;
}

function setMetricCards() {
  const trackedPercent = (snapshot.shipsGrandTotal / snapshot.annualGoalTotal) * 100;
  const extendedOutput = snapshot.supportingCategories.reduce((sum, item) => sum + item.total, 0);
  const topAnnual = snapshot.annualCategories.reduce((top, item) => {
    return item.progress > top.progress ? item : top;
  });

  elements.reportingDate.textContent = `Source: Master total_for Dane • updated ${snapshot.lastUpdated}`;
  elements.revenueValue.textContent = `${snapshot.shipsGrandTotal}`;
  elements.revenueDelta.textContent = formatPercent(trackedPercent);
  elements.revenueNarrative.textContent = "of annual goal complete";

  elements.leadsValue.textContent = `${snapshot.annualCategories[0].total + snapshot.annualCategories[1].total}`;
  elements.leadsDelta.textContent = formatPercent(
    ((snapshot.annualCategories[0].total + snapshot.annualCategories[1].total) / snapshot.shipsGrandTotal) * 100
  );

  elements.conversionValue.textContent = `${snapshot.annualCategories.length + snapshot.supportingCategories.length}`;
  elements.conversionDelta.textContent = `${snapshot.supportingCategories.length} support`;

  elements.retentionValue.textContent = formatPercent(topAnnual.progress);
  elements.retentionDelta.textContent = topAnnual.name;

  elements.focusHeadline.textContent = `${topAnnual.name} is furthest ahead, while Social still carries the largest absolute target gap.`;
  elements.heroHeadline.textContent =
    `The goal-tracked ship total is ${snapshot.shipsGrandTotal}, with ${extendedOutput} additional deliverables sitting in advocacy and quote banks.`;
}

function renderChart(points, maxValue) {
  const xStart = 70;
  const xEnd = 630;
  const chartHeight = 180;
  const yBase = 216;
  const step = points.length > 1 ? (xEnd - xStart) / (points.length - 1) : 0;

  const coordinates = points.map((point, index) => {
    const x = xStart + step * index;
    const y = yBase - (point.value / Math.max(maxValue, 1)) * chartHeight;
    return { ...point, x, y };
  });

  const linePoints = coordinates.map((point) => `${point.x},${point.y}`).join(" ");
  const areaPoints = [`${xStart},${yBase}`, linePoints, `${coordinates[coordinates.length - 1].x},${yBase}`].join(" ");

  elements.trendLine.setAttribute("points", linePoints);
  elements.trendArea.setAttribute("points", areaPoints);

  elements.trendDots.innerHTML = coordinates
    .map((point) => `<circle class="chart-dot" cx="${point.x}" cy="${point.y}" r="7"></circle>`)
    .join("");

  elements.trendLabels.innerHTML = coordinates
    .map(
      (point) => `
        <text class="chart-label" x="${point.x}" y="244">${point.label}</text>
        <text class="chart-label" x="${point.x}" y="${Math.max(point.y - 14, 24)}">${point.value}</text>
      `
    )
    .join("");
}

function renderBars(items) {
  const maxValue = Math.max(...items.map((item) => item.value), 1);
  elements.channelBars.innerHTML = items
    .map((item) => {
      const width = (item.value / maxValue) * 100;
      return `
        <div class="bar-row">
          <div class="bar-topline">
            <strong>${item.label}</strong>
            <span>${item.display || item.value} <span class="bar-note">${item.note}</span></span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width:${width}%"></div>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderInsights(items) {
  elements.insightList.innerHTML = items
    .map(
      (item) => `
        <li class="insight-item">
          <span class="insight-kicker">${item.kicker}</span>
          <div>${item.text}</div>
        </li>
      `
    )
    .join("");
}

function renderAnnualTable() {
  elements.regionTable.innerHTML = snapshot.annualCategories
    .map((item) => {
      const remaining = Math.max(item.goal - item.total, 0);
      return `
        <tr>
          <td><strong>${item.name}</strong></td>
          <td>${item.total} / ${item.goal}</td>
          <td>${item.progress}%</td>
          <td>${remaining}</td>
        </tr>
      `;
    })
    .join("");
}

function renderQuarterlyTable() {
  elements.regionTable.innerHTML = snapshot.quarterlyCategories
    .map(
      (item) => `
        <tr>
          <td><strong>${item.name}</strong></td>
          <td>${item.goal}</td>
          <td>Q1 ${item.q1}% • Q2 ${item.q2}%</td>
          <td>Q3 ${item.q3}% • Q4 ${item.q4}%</td>
        </tr>
      `
    )
    .join("");
}

function renderShipsTable() {
  const combined = [
    ...snapshot.annualCategories.map((item) => ({
      name: item.name,
      total: item.total,
      progress: `${item.progress}% annual`,
      remaining: Math.max(item.goal - item.total, 0)
    })),
    ...snapshot.supportingCategories.map((item) => ({
      name: item.name,
      total: item.total,
      progress: "No annual goal",
      remaining: "-"
    }))
  ];

  elements.regionTable.innerHTML = combined
    .map(
      (item) => `
        <tr>
          <td><strong>${item.name}</strong></td>
          <td>${item.total}</td>
          <td>${item.progress}</td>
          <td>${item.remaining}</td>
        </tr>
      `
    )
    .join("");
}

function renderActivity(mode) {
  const selectedSets =
    mode === "annual"
      ? ["Written", "Social", "Testimonial Films", "Brand + Innovation"]
      : ["Written", "Social", "Testimonial Films", "Brand + Innovation", "Advocacy campaigns", "Quote banks"];

  elements.activityList.innerHTML = selectedSets
    .flatMap((group) =>
      (snapshot.pipeline[group] || []).slice(0, 3).map((item, index) => ({
        group,
        item,
        time: index === 0 ? "Top listed item" : "Additional tracked item"
      }))
    )
    .slice(0, 9)
    .map(
      (entry) => `
        <div class="activity-item">
          <div class="activity-dot"></div>
          <div>
            <strong>${entry.item}</strong>
            <span>${entry.group}</span>
          </div>
          <div class="activity-time">${entry.time}</div>
        </div>
      `
    )
    .join("");
}

function renderMode(mode) {
  const config = modeConfig[mode];
  const chartMax = Math.max(...config.chart.map((item) => item.value), 1);

  elements.trendTitleText.textContent = config.title;
  elements.breakdownTitle.textContent = config.breakdownTitle;
  elements.tableTitle.textContent = config.tableTitle;
  elements.activityTitle.textContent = config.activityTitle;
  elements.trendSummary.textContent = config.badge;

  renderChart(config.chart, chartMax);
  renderBars(config.bars);
  renderInsights(config.insights);
  renderActivity(mode);

  if (mode === "annual") {
    renderAnnualTable();
  } else if (mode === "quarterly") {
    renderQuarterlyTable();
  } else {
    renderShipsTable();
  }
}

elements.segments.forEach((button) => {
  button.addEventListener("click", () => {
    elements.segments.forEach((segment) => segment.classList.remove("active"));
    button.classList.add("active");
    renderMode(button.dataset.period);
  });
});

setMetricCards();
renderMode("ships");
