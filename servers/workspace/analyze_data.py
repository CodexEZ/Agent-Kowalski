
import json

def analyze_data(records):
    numerical_fields = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
    
    analysis_results = {
        "summary_statistics": {},
        "outcome_distribution": {}
    }

    # Initialize statistics for numerical fields
    for field in numerical_fields:
        analysis_results["summary_statistics"][field] = {
            "sum": 0,
            "count": 0,
            "min": float('inf'),
            "max": float('-inf'),
            "zeros_count": 0
        }

    outcome_counts = {0: 0, 1: 0}
    total_records = len(records)

    for record in records:
        for field in numerical_fields:
            value = record.get(field)
            if value is not None:
                if value == 0:
                    analysis_results["summary_statistics"][field]["zeros_count"] += 1
                
                # Only include non-zero values for mean/min calculation for certain fields
                if field in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
                    if value != 0:
                        analysis_results["summary_statistics"][field]["sum"] += value
                        analysis_results["summary_statistics"][field]["count"] += 1
                        analysis_results["summary_statistics"][field]["min"] = min(analysis_results["summary_statistics"][field]["min"], value)
                        analysis_results["summary_statistics"][field]["max"] = max(analysis_results["summary_statistics"][field]["max"], value)
                else: # For Pregnancies, DiabetesPedigreeFunction, Age, 0 is a valid value
                    analysis_results["summary_statistics"][field]["sum"] += value
                    analysis_results["summary_statistics"][field]["count"] += 1
                    analysis_results["summary_statistics"][field]["min"] = min(analysis_results["summary_statistics"][field]["min"], value)
                    analysis_results["summary_statistics"][field]["max"] = max(analysis_results["summary_statistics"][field]["max"], value)

        outcome = record.get("Outcome")
        if outcome is not None:
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1

    # Calculate means and clean up min/max for fields with no non-zero values
    for field in numerical_fields:
        stats = analysis_results["summary_statistics"][field]
        if stats["count"] > 0:
            stats["mean"] = round(stats["sum"] / stats["count"], 2)
        else:
            stats["mean"] = "N/A"
        
        if stats["min"] == float('inf'):
            stats["min"] = "N/A"
        if stats["max"] == float('-inf'):
            stats["max"] = "N/A"
        
        del stats["sum"] # Remove sum as it's no longer needed for output
        del stats["count"] # Remove count as it's implicitly total_records or non-zero count

    # Calculate outcome percentages
    for outcome, count in outcome_counts.items():
        analysis_results["outcome_distribution"][outcome] = {
            "count": count,
            "percentage": round((count / total_records) * 100, 1) if total_records > 0 else 0.0
        }
    
    return analysis_results

# Assume 'records' variable is populated from the read_records tool output
# For the purpose of running this script via the tool, we expect 'records' to be available in the global scope
# This is a placeholder for how the records would be passed in a real execution environment
# For direct execution, you'd replace this with the actual data from the previous step.

# Example usage (replace with actual data from read_records output):
# records_from_db = [...] 
# For the current execution context, we need to access the records from the previous tool output.
# Given the previous tool output, the records are available under `read_records_response['records']`

# Since the previous tool call output is available in the current context, 
# we can directly use the 'read_records_response' variable.
if 'read_records_response' in locals() and 'records' in read_records_response:
    analysis = analyze_data(read_records_response['records'])
    
    # Format the output for readability
    output_str = "Summary Statistics:\n"
    output_str += "| Field | Count | Mean (excluding 0s) | Min (excluding 0s) | Max | Zeros Count |\n"
    output_str += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    # Sort fields for consistent output
    sorted_fields = sorted(analysis['summary_statistics'].keys())
    
    for field in sorted_fields:
        stats = analysis['summary_statistics'][field]
        output_str += f"| **{field}** | {len(read_records_response['records'])} | {stats['mean']} | {stats['min']} | {stats['max']} | {stats['zeros_count']} |\n"

    output_str += "\nOutcome Distribution:\n"
    for outcome, data in analysis['outcome_distribution'].items():
        output_str += f"*   **Outcome {outcome} ({'No Diabetes' if outcome == 0 else 'Diabetes'}):** {data['count']} records ({data['percentage']}%)"
        if outcome == 0:
            output_str += "\n"
    
    print(output_str)

