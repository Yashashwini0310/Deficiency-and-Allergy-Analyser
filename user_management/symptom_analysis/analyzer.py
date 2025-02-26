from .data import symptom_to_condition

def analyze_symptoms(user_symptoms, medical_history):
    # Normalize user input
    print("symptom_to_condition contents:", symptom_to_condition)
    user_symptoms = [symptom.strip().lower() for symptom in user_symptoms]
    print(f"User Symptoms: {user_symptoms}")  # Debug

    matched_conditions = []

    # Iterate through known symptoms
    for symptom, conditions in symptom_to_condition.items():
        print(f"Checking: {symptom} - {conditions}")  # Debug
        if symptom in user_symptoms:
            for condition in conditions:
                severity = determine_severity(condition)  # Get severity for this condition
                matched_conditions.append({"condition": condition, "severity": severity})

    if not matched_conditions:
        return [{"condition": "No matching allergy or deficiency found.", "severity": "N/A"}]

    return matched_conditions

def determine_severity(condition):
    # Define severity levels based on conditions
    severity_map = {
        "Pollen Allergy": "Mild",
        "Iron Deficiency": "Moderate",
        "Dust Allergy": "Mild",
        "Migraine": "Severe",
        "Vitamin D Deficiency": "Moderate",
        "Sinus Allergy": "Mild",
    }
    return severity_map.get(condition, "Mild")  # Default severity if condition not found