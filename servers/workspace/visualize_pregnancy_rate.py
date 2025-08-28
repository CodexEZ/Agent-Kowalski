
from collections import defaultdict
import json

# Read the records (assuming this data would be passed or fetched within the script)
# For demonstration, I will use a placeholder for the data fetched from the database
# In a real scenario, this script would be called with the data as an argument or fetch it directly.

# Placeholder for data that would be read from the database
# This would typically come from a default_api.read_records call
records_raw = default_api.read_records(database="auth-demo", collection="data", projection=["Age", "Pregnancies"])

if records_raw and records_raw.get("status") == "success":
    records = records_raw.get("records", [])

    age_pregnancies = defaultdict(lambda: {"sum_pregnancies": 0, "count": 0})

    for record in records:
        age = record.get("Age")
        pregnancies = record.get("Pregnancies")
        if age is not None and pregnancies is not None:
            age_pregnancies[age]["sum_pregnancies"] += pregnancies
            age_pregnancies[age]["count"] += 1

    chart_data = []
    for age, data in sorted(age_pregnancies.items()):
        if data["count"] > 0:
            average_pregnancies = round(data["sum_pregnancies"] / data["count"], 2)
            chart_data.append({"Age": age, "AveragePregnancies": average_pregnancies})

    print(json.dumps(chart_data, indent=2))
else:
    print(json.dumps({"error": "Failed to retrieve data from the database."}))
