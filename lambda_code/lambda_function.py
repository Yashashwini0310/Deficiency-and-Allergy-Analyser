import json

# Define symptom-condition mappings with medical history considerations
SYMPTOM_CONDITIONS = {
    "fever": ["Flu", "Viral Infection"],
    "headache": ["Migraine", "Tension Headache"],
    "chest pain": ["Heart Disease", "Anxiety"],
    "sneezing": ["Dust Allergy", "Pollen Allergy"],
    "itchy skin": ["Eczema", "Food Allergy"],
    "fatigue": ["Iron Deficiency", "Vitamin B12 Deficiency"],
    "hives": ["Insect Allergy", "Food Allergy"],
    "nausea": ["Lactose Intolerance", "Food Sensitivity"],
    "shortness of breath": ["Asthma", "Pollen Allergy"],
    "skin rash" : ["skin allergy", "Dust Allergy"],
    "itching": ["Pollen Allergy", "Dust Allergy"],
}

MEDICAL_HISTORY_IMPACT = {
    "diabetes": ["Fatigue", "Slow Healing"],
    "asthma": ["Breathing Issues", "Chest Pain"],
    "hypertension": ["Headache", "Dizziness"],
}

RECOMMENDATIONS = {
    "Flu": "Drink plenty of fluids and rest.",
    "Migraine": "Avoid bright lights and get sufficient sleep.",
    "Anemia": "Increase iron intake through diet or supplements.",
    "Heart Disease": "Seek medical attention immediately.",
}

def analyze_symptoms(symptoms, medical_history):
    possible_conditions = set()
    recommendations = set()

    # eck symptom-based conditions
    for symptom in symptoms:
        conditions = SYMPTOM_CONDITIONS.get(symptom, [])
        possible_conditions.update(conditions)
    
    # check medical history impact
    for condition, affected_symptoms in MEDICAL_HISTORY_IMPACT.items():
        if condition in medical_history:
            for symptom in affected_symptoms:
                if symptom in symptoms:
                    possible_conditions.add(condition)

    #Assign recommendations
    for condition in possible_conditions:
        if condition in RECOMMENDATIONS:
            recommendations.add(RECOMMENDATIONS[condition])

    return {
        "conditions": list(possible_conditions) if possible_conditions else ["Unknown Condition"],
        "recommendation": list(recommendations) if recommendations else ["Consult a doctor if symptoms persist."]
    }

def lambda_handler(event, context):
    try:
        # parse the JSON body correctly
        body = json.loads(event.get("body", "{}"))  
        symptoms = body.get("symptoms", [])
        medical_history = body.get("medical_history", [])

        if not symptoms:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No symptoms provided"})
            }
        
        # Perform analysis
        result = analyze_symptoms(symptoms, medical_history)

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
