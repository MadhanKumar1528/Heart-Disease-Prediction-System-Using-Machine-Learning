from fpdf import FPDF
import datetime
import os

class MedicalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Heart Disease Prediction Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(patient_data, prediction_data):
    pdf = MedicalReport()
    pdf.add_page()
    
    # Patient Details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Patient Details:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 10, f"Name: {patient_data['name']}", 0, 1)
    pdf.cell(0, 10, f"Age: {patient_data['age']}", 0, 1)
    pdf.cell(0, 10, f"Gender: {'Male' if patient_data['gender'] == 1 else 'Female'}", 0, 1)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.ln(5)

    # Prediction Results
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Prediction Analysis:', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 10, f"Disease Risk: {prediction_data['risk_level']}", 0, 1)
    pdf.cell(0, 10, f"Probability: {prediction_data['probability'] * 100:.2f}%", 0, 1)
    pdf.ln(5)

    # Recommendations
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Recommendations:', 0, 1)
    pdf.set_font('Arial', '', 11)
    for rec in prediction_data['recommendations']:
        pdf.cell(0, 10, f"- {rec}", 0, 1)
    pdf.ln(5)

    # Precautions
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Precautions:', 0, 1)
    pdf.set_font('Arial', '', 11)
    for prec in prediction_data['precautions']:
        pdf.cell(0, 10, f"- {prec}", 0, 1)

    # Save PDF
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        
    filename = f"report_{patient_data['id']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(reports_dir, filename)
    pdf.output(file_path)
    
    return file_path
