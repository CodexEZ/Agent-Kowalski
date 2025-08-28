
import json

def analyze_data(records):
    analysis_results = {}

    numerical_fields = [
        "Age", "BMI", "BloodPressure", "Glucose", "Insulin",
        "Pregnancies", "SkinThickness", "DiabetesPedigreeFunction"
    ]

    # Initialize statistics for numerical fields
    for field in numerical_fields:
        analysis_results[field] = {
            "min": float('inf'),
            "max": float('-inf'),
            "sum": 0,
            "count": 0,
            "zero_count": 0
        }

    outcome_counts = {0: 0, 1: 0}

    for record in records:
        for field in numerical_fields:
            value = record.get(field)
            if value is not None:
                analysis_results[field]["min"] = min(analysis_results[field]["min"], value)
                analysis_results[field]["max"] = max(analysis_results[field]["max"], value)
                analysis_results[field]["sum"] += value
                analysis_results[field]["count"] += 1
                if value == 0:
                    analysis_results[field]["zero_count"] += 1
        
        outcome = record.get("Outcome")
        if outcome is not None:
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1

    # Calculate means and handle fields with no data
    for field in numerical_fields:
        if analysis_results[field]["count"] > 0:
            analysis_results[field]["mean"] = analysis_results[field]["sum"] / analysis_results[field]["count"]
        else:
            analysis_results[field]["mean"] = "N/A"
            analysis_results[field]["min"] = "N/A"
            analysis_results[field]["max"] = "N/A"

    analysis_results["Outcome_Distribution"] = outcome_counts

    return analysis_results

# Assume 'records' is passed as a JSON string from the environment or a file
# For this example, we'll hardcode the input based on the previous tool output
records_data = [{"Age": 50, "BMI": 33.6, "BloodPressure": 72, "DiabetesPedigreeFunction": 0.627, "Glucose": 148, "Insulin": 0, "Outcome": 1, "Pregnancies": 6, "SkinThickness": 35, "_id": "68a6e5e24bfda2aa97652598"}, {"Age": 31, "BMI": 26.6, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.351, "Glucose": 85, "Insulin": 0, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 29, "_id": "68a6e5e24bfda2aa97652599"}, {"Age": 32, "BMI": 23.3, "BloodPressure": 64, "DiabetesPedigreeFunction": 0.672, "Glucose": 183, "Insulin": 0, "Outcome": 1, "Pregnancies": 8, "SkinThickness": 0, "_id": "68a6e5e24bfda2aa9765259a"}, {"Age": 21, "BMI": 28.1, "BloodPressure": 66, "DiabetesPedigreeFunction": 0.167, "Glucose": 89, "Insulin": 94, "Outcome": 0, "Pregnancies": 1, "SkinThickness": 23, "_id": "68a6e5e24bfda2aa9765259b"}, {"Age": 33, "BMI": 43.1, "BloodPressure": 40, "DiabetesPedigreeFunction": 2.288, "Glucose": 137, "Insulin": 168, "Outcome": 1, "Pregnancies": 0, "SkinThickness": 35, "_id": "68a6e5e24bfda2aa9765259c"}, {"Age": 30, "BMI": 25.6, "BloodPressure": 74, "DiabetesPedigreeFunction": 0.201, "Glucose": 116, "Insulin": 0, "Outcome": 0, "Pregnancies": 5, "SkinThickness": 0, "_id": "68a6e5e24bfda2aa9765259d"}, {"Age": 26, "BMI": 31, "BloodPressure": 50, "DiabetesPedigreeFunction": 0.248, "Glucose": 78, "Insulin": 88, "Outcome": 1, "Pregnancies": 3, "SkinThickness": 32, "_id": "68a6e5e24bfda2aa9765259e"}, {"Age": 29, "BMI": 35.3, "BloodPressure": 0, "DiabetesPedigreeFunction": 0.134, "Glucose": 115, "Insulin": 0, "Outcome": 0, "Pregnancies": 10, "SkinThickness": 0, "_id": "68a6e5e24bfda2aa9765259f"}, {"Age": 53, "BMI": 30.5, "BloodPressure": 70, "DiabetesPedigreeFunction": 0.158, "Glucose": 197, "Insulin": 543, "Outcome": 1, "Pregnancies": 2, "SkinThickness": 45, "_id": "68a6e5e24bfda2aa976525a0"}, {"Age": 54, "BMI": 0, "BloodPressure": 96, "DiabetesPedigreeFunction": 0.232, "Glucose": 125, "Insulin": 0, "Outcome": 1, "Pregnancies": 8, "SkinThickness": 0, "_id": "68a6e5e24bfda2aa976525a1"}]

analysis_output = analyze_data(records_data)

html_output = """
<div style="
    background-color:#1e293b;
    color:#f1f5f9;
    font-family:'Roboto', sans-serif;
    padding:20px;
    border-radius:8px;
    box-shadow:1px 2px 10px rgba(0,0,0,0.6);
    max-width:600px;
    margin:20px auto;
">
    <h2 style="color:#f1f5f9; font-size:1.5em; margin-bottom:15px;">Data Analysis Report</h2>
    <h3 style="color:#f1f5f9; font-size:1.2em; margin-bottom:10px;">Descriptive Statistics</h3>
    <div style="
        max-height: 300px;
        overflow-x: auto;
        overflow-y: auto;
        border: 1px solid #334155;
        border-radius: 8px;
        margin-bottom: 20px;
    ">
        <table style="
            width:100%;
            border-collapse:collapse;
            text-align:left;
            border-radius:8px;
            overflow:hidden;
        ">
            <thead style="background-color:#334155;">
                <tr>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Field</th>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Count</th>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Mean</th>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Min</th>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Max</th>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Zero Count</th>
                </tr>
            </thead>
            <tbody>
"""

row_counter = 0
for field, stats in analysis_output.items():
    if field != "Outcome_Distribution":
        bg_color = "#1e293b" if row_counter % 2 == 0 else "#2d3a4b"
        html_output += f"""
                <tr style="background-color:{bg_color};">
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{field}</td>
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{stats["count"]}</td>
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{stats["mean"]:.2f}</td>
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{stats["min"]}</td>
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{stats["max"]}</td>
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{stats["zero_count"]}</td>
                </tr>
        """
        row_counter += 1

html_output += """
            </tbody>
        </table>
    </div>

    <h3 style="color:#f1f5f9; font-size:1.2em; margin-bottom:10px;">Outcome Distribution</h3>
    <div style="
        max-height: 100px;
        overflow-x: auto;
        overflow-y: auto;
        border: 1px solid #334155;
        border-radius: 8px;
        margin-bottom: 20px;
    ">
        <table style="
            width:100%;
            border-collapse:collapse;
            text-align:left;
            border-radius:8px;
            overflow:hidden;
        ">
            <thead style="background-color:#334155;">
                <tr>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Outcome (0=No, 1=Yes)</th>
                    <th style="padding:12px 15px; font-weight:500; font-size:1em; color:#f1f5f9;">Count</th>
                </tr>
            </thead>
            <tbody>
"""
row_counter = 0
for outcome, count in analysis_output["Outcome_Distribution"].items():
    bg_color = "#1e293b" if row_counter % 2 == 0 else "#2d3a4b"
    html_output += f"""
                <tr style="background-color:{bg_color};">
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{outcome}</td>
                    <td style="padding:10px 15px; border-bottom:1px solid #334155; color:#cbd5e1;">{count}</td>
                </tr>
    """
    row_counter += 1

html_output += """
            </tbody>
        </table>
    </div>

    <h3 style="color:#f1f5f9; font-size:1.2em; margin-bottom:10px;">Observations & Potential Issues:</h3>
    <ul style="color:#cbd5e1; padding-left:20px;">
"""

anomalies_found = False
for field, stats in analysis_output.items():
    if field != "Outcome_Distribution" and stats["zero_count"] > 0:
        if field in ["BMI", "BloodPressure", "Glucose", "Insulin", "SkinThickness"]:
            html_output += f"""
        <li style="margin-bottom:5px;">
            <strong style="color:#facc15;">Warning:</strong> The '{field}' field has {stats["zero_count"]} zero values out of {stats["count"]} records. In medical datasets, these often represent missing data rather than actual zero measurements, which could skew analysis.
        </li>
            """
            anomalies_found = True

if not anomalies_found:
    html_output += """
        <li style="margin-bottom:5px;">No significant anomalies (like unexpected zero values in critical health metrics) were found in this small sample.</li>
    """

html_output += """
    </ul>
</div>
"""

print(html_output)
