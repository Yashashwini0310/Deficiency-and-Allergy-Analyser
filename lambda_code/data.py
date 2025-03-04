

# Mapping of symptoms to conditions, severity, and recommendations
SYMPTOM_CONDITION_MAPPING = {
    "fever": {
        "condition": "Flu",
        "severity": "Moderate",
        "recommendation": "Stay hydrated, rest, and monitor temperature."
    },
    "headache": {
        "condition": "Migraine",
        "severity": "Severe",
        "recommendation": "Avoid bright lights, stay hydrated, and rest."
    },
    "fatigue": {
        "condition": "Anemia",
        "severity": "Moderate",
        "recommendation": "Increase iron intake through diet or supplements."
    },
    "chest pain": {
        "condition": "Heart Disease",
        "severity": "Severe",
        "recommendation": "Seek immediate medical attention."
    },
}
# Medical history impact on symptoms
MEDICAL_HISTORY_IMPACT = {
    "diabetes": {
        "fatigue": {
            "condition": "Diabetic Fatigue",
            "severity": "Severe",
            "recommendation": "Monitor blood sugar levels and consult a doctor."
        },
        "wound healing issues": {
            "condition": "Delayed Wound Healing",
            "severity": "Moderate",
            "recommendation": "Keep wounds clean and monitor blood sugar levels."
        }
    },
    "hypertension": {
        "chest pain": {
            "condition": "Hypertension Complication",
            "severity": "Severe",
            "recommendation": "Seek immediate medical attention."
        },
        "headache": {
            "condition": "Hypertensive Headache",
            "severity": "Moderate",
            "recommendation": "Monitor blood pressure and avoid stress."
        }
    }
}

# Default response if symptom is unknown
DEFAULT_RESPONSE = {
    "condition": "Unknown Condition",
    "severity": "Mild",
    "recommendation": "Consult a doctor for further diagnosis."
}
