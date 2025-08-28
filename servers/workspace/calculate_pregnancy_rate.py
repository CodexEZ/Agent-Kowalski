
from collections import defaultdict
import json

# Assuming default_api is available in the script execution environment
# and read_records can be called directly.

def calculate_pregnancy_rate():
    try:
        # Read all records with 'Age' and 'Pregnancies' fields
        response = default_api.read_records(
            database="auth-demo",
            collection="data",
            projection=["Age", "Pregnancies"]
        )

        if response.get("status") == "success":
            records = response.get("records", [])
            
            age_data = defaultdict(lambda: {"total_pregnancies": 0, "count_individuals": 0})

            for record in records:
                age = record.get("Age")
                pregnancies = record.get("Pregnancies")

                if age is not None and pregnancies is not None:
                    age_data[age]["total_pregnancies"] += pregnancies
                    age_data[age]["count_individuals"] += 1
            
            results = []
            for age, data in sorted(age_data.items()):
                if data["count_individuals"] > 0:
                    average_pregnancies = data["total_pregnancies"] / data["count_individuals"]
                    results.append({"Age": age, "AveragePregnancies": round(average_pregnancies, 2)})
            
            print(json.dumps({"status": "success", "data": results}))
        else:
            print(json.dumps({"status": "error", "message": response.get("message", "Failed to retrieve records")}))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

calculate_pregnancy_rate()
