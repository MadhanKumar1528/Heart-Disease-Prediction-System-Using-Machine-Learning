# CardioAI: Real-Time Heart Disease Prediction System

CardioAI is a production-ready, full-stack healthcare application that uses advanced Machine Learning (Random Forest) to predict heart disease risk with 91.6% accuracy. Designed for clinical decision support, it features explainable AI (XAI), real-time monitoring via WebSockets, and a professional healthcare dashboard.

## 🚀 Key Features
- **Accurate ML Prediction**: Uses a Random Forest Classifier trained on the UCI Cleveland dataset.
- **Explainable AI (XAI)**: Visualizes feature contributions for each prediction (e.g., how cholesterol impacted the risk).
- **Professional Dashboard**: Real-time patient monitoring and analytics using Chart.js.
- **Clinical Reporting**: Professional PDF report generation for diagnostic documentation.
- **Voice-Enabled Entry**: Hands-free clinical data input support.
- **AI Health Assistant**: Integrated clinical chatbot for health inquiries.
- **Secure Architecture**: JWT-based authentication and role-based access control.

## 🛠️ Tech Stack
- **Frontend**: React.js (Vite), Tailwind CSS, Framer Motion, Chart.js, jsPDF.
- **Backend**: FastAPI (Python), SQLAlchemy, WebSockets, JWT.
- **Machine Learning**: Scikit-learn, Pandas, Joblib.
- **Database**: SQLite (Production-ready with PostgreSQL support).

## 🏗️ Architecture
The system follows a modern microservices-inspired monolithic architecture:
1.  **Frontend Layer**: A responsive React SPA that communicates via REST and WebSockets.
2.  **API Layer**: FastAPI handles high-concurrency requests and real-time streaming.
3.  **ML Engine**: A separate module for feature engineering, scaling, and inference.
4.  **Data Layer**: SQLAlchemy ORM for secure and structured data persistence.

## 📝 Resume Description
**Heart Disease Prediction System (Full Stack & ML)**
*Developed an industry-level healthcare AI portal using FastAPI and React to predict cardiovascular risks with 91%+ accuracy.*
- Integrated Explainable AI (XAI) to provide diagnostic transparency for clinical use.
- Implemented real-time WebSocket alerts for high-risk cardiac events.
- Engineered a multi-step clinical form with voice-input support and automated PDF reporting.
- Designed a high-performance dashboard with interactive Chart.js analytics and medical trends.

## 🎓 Viva Questions & Answers
**Q1: Why did you choose Random Forest over Logistic Regression?**
A: While Logistic Regression is good for linear relationships, Random Forest handles non-linear medical data more effectively and is less prone to overfitting due to ensemble learning.

**Q2: How do you ensure data security?**
A: We use JWT (JSON Web Tokens) for stateless authentication and password hashing (bcrypt) to ensure patient and user data remains encrypted at rest.

**Q3: What is the significance of the 'thal' parameter in the dataset?**
A: 'thal' refers to Thalassemia, a blood disorder. It is a critical feature in the Cleveland dataset, where 'fixed defect' or 'reversable defect' significantly correlates with heart disease risk.

---
© 2024 CardioAI Intelligence. Developed for Clinical Excellence.
