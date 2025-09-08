import pandas as pd
from fpdf import FPDF
import os

# Load CSV data
std_data = pd.read_csv('./studentsPerformance.csv')

# Function to assign letter grades and remarks
def get_grade_and_remark(avg):
    if avg >= 90:
        return "A", "Outstanding! Keep up the excellent work."
    elif avg >= 80:
        return "B", "Very good performance. Aim for the top."
    elif avg >= 70:
        return "C", "Satisfactory effort. Continue improving."
    elif avg >= 60:
        return "D", "Needs improvement in multiple areas."
    else:
        return "F", "Significant improvement required."

# Create 'reports' folder if it doesn't exist
output_dir = 'reports'
os.makedirs(output_dir, exist_ok=True)

# Create the PDF report for each student
for index, row in std_data.iterrows():
    name = row['name']
    math = row['math score']
    reading = row['reading score']
    writing = row['writing score']
    average = round((math + reading + writing) / 3, 2)
    grade, remark = get_grade_and_remark(average)

    # Start PDF
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 70, 140)
    pdf.cell(200, 10, "Student Report Card", ln=True, align='C')

    # Basic Info
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(1)
    pdf.ln(10)
    pdf.cell(200, 10, f"Name: {name}", ln=True)
    pdf.ln(5)

    # Table Headers
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(65, 10, "Subject", 1, 0, 'C', 1)
    pdf.cell(65, 10, "Score", 1, 1, 'C', 1)

    # Table Body
    pdf.set_font("Arial", '', 12)
    pdf.cell(65, 10, "Math", 1, 0, 'C')
    pdf.cell(65, 10, str(math), 1, 1, 'C')

    pdf.cell(65, 10, "Reading", 1, 0, 'C')
    pdf.cell(65, 10, str(reading), 1, 1, 'C')

    pdf.cell(65, 10, "Writing", 1, 0, 'C')
    pdf.cell(65, 10, str(writing), 1, 1, 'C')

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(65, 10, "Average", 1, 0, 'C')
    pdf.cell(65, 10, str(average), 1, 1, 'C')

    pdf.cell(65, 10, "Grade", 1, 0, 'C')
    pdf.cell(65, 10, grade, 1, 1, 'C')

    # Remarks section
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 70, 0)
    pdf.cell(200, 10, "Teacher's Remark", ln=True)

    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(0)
    pdf.multi_cell(0, 10, remark, border=1)

    # Save to reports folder
    filename = f"{name.replace(' ', '_')}_Report.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)

    print(f"Report created for {name}: {filepath}")
