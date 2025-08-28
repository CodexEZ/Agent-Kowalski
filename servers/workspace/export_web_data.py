
import json

# Read data from the specified collection and database using the directly available function
response = read_records(database="auth-demo", collection="web-data")

if response and response.get("status") == "success":
    records = response.get("records", [])
    
    # Convert the list of records to a JSON string
    json_output = json.dumps(records, indent=4)
    
    # Define the filename for the JSON output
    filename = "web_data.json"
    
    # Write the JSON string to the file in the workspace
    with open(filename, "w") as f:
        f.write(json_output)
    
    print(f"Data successfully written to {filename}")
else:
    print("Failed to read records from the database.")
    print(response) # Print response for debugging
