class ChatEngine:
    def __init__(self):
        self.knowledge_base = {
            "blood pressure": "According to AHA guidelines, Normal BP is <120/80. Stage 1 Hypertension is 130-139/80-89. Persistent high BP can lead to hypertensive heart disease.",
            "cholesterol": "High cholesterol (Hyperlipidemia) increases the risk of plaque buildup in arteries. Total cholesterol should ideally be below 200 mg/dL.",
            "chest pain": "Chest pain (Angina) can be stable or unstable. If you experience sudden, severe chest pain radiating to the left arm or jaw, seek emergency care immediately.",
            "exercise": "The ACC recommends at least 150 minutes of moderate-intensity aerobic activity per week for optimal cardiovascular health.",
            "diet": "A heart-healthy diet includes high fiber, lean proteins (like fish), and healthy fats (Omega-3), while limiting saturated fats and sodium (<2,300mg/day).",
            "smoking": "Smoking is a primary risk factor for atherosclerosis. Quitting smoking can reduce your risk of heart disease by 50% within one year.",
            "diabetes": "High blood sugar (Fasting > 126 mg/dL) can damage blood vessels and the nerves that control your heart.",
            "prediction": "I analyze 13 clinical parameters including your ECG results, age, and vitals to predict your risk using a Random Forest model with 91.6% accuracy."
        }

    def get_response(self, query: str):
        query = query.lower()
        
        # Check for keywords in query
        for key in self.knowledge_base:
            if key in query:
                return self.knowledge_base[key]
        
        return "I am specialized in cardiovascular health. You can ask me about blood pressure, cholesterol, diet, exercise, or how my AI prediction model works."

chat_engine = ChatEngine()
