from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os, base64
from datetime import datetime
from io import BytesIO

class CarbonFootprintReport:
    def __init__(self, user, report_data):
        self.user = user
        self.data = report_data
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            fontSize=24,
            spaceAfter=30,
            name='CustomTitle',
            fontName='Helvetica-bold'
        )
        self.report_folder = self._create_report_folders()


    def generate_report(self):
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')        
        filename = os.path.join(self.report_folder, f'carbon_report_{timestamp}.pdf')

        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        elements = []

        # Use self.title_style
        elements.append(Paragraph("Carbon Footprint Report", self.title_style))
        elements.append(Spacer(1, 12))

        elements.extend(self._add_user_info())
        elements.append(Spacer(1, 12))

        elements.extend(self._add_emission_summary())
        elements.append(Spacer(1, 12))

        # Only add visualization if graph data exists
        if self.data.get('graph'):
            elements.extend(self._add_visualization())
            elements.append(Spacer(1, 12))

        elements.extend(self._add_recommendations())

        doc.build(elements)
        return filename
    

    def _create_report_folders(self):

        base_path = os.path.abspath(os.path.dirname(__file__))
        reports_dir = os.path.join(base_path, 'reports')

        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        

        user_folder = os.path.join(reports_dir, f'user_{self.user.user_id}')
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        return user_folder

def generate_report(self):

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')        
    filename = os.path.join(self.report_folder, f'carbon_report_{timestamp}.pdf')

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottokmMargin=72
    )

    elements = []

    elements.append(Paragraph("Carbon Foorprint Report", self.tittle_style))
    elements.append(Spacer(1, 12))

    elements.extend(self._add_user_info())
    elements.append(Spacer(1, 12))

    elements.extend(self._add_emission_summary())
    elements.append(Spacer(1, 12))

    elements.extend(self._add_detailed_breakdown())
    elements.append(Spacer(1, 12))


    if self.data.get('graph'):
        elements.extend(self._add_visualization())
        elements.append(Spacer(1, 12))

    
    elements.extend(self._add_recommendations())


    doc.build(elements)
    return filename

def _add_user_info(self):
    
    elements = []

    user_type = "Institution" if self.user.user_type == "INSTITUTE" else "Individual"
    user_info = [
        ["Report Date:", datetime.now().strftime('%Y-%m-%d')],
        ["User type:", user_type],
        ["Name:", f"{self.user.first_name} {self.user.last_name}"]
    ]

    if self.user.user_type == "INSTITUTE":
        user_info.extend([
            ["Company:", self.user.company_name],
            ["Position:", self.user.postion],
            ["Employees:", str(self.user.no_employees)]
        ])

    
    table = Table(user_info, colWidths=[100, 300])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(Paragraph("User Information1", self.styles['Heading2']))
    elements.append(table)
    return elements

def _add_emission_summary(self):

    elements = []

    total_emissions = (
        self.data['total_carbon_emission_by_energy'] +
        self.data['total_carbon_emission_by_waste'] +
        self.data['total_carbon_emission_by_business']
    )

    if total_emissions == 0:
        percentage_energy = percentage_waste = percentage_business = 0
    else:
        percentage_energy = (self.data['total_carbon_emission_by_energy']/total_emissions*100)
        percentage_waste = (self.data['total_carbon_emission_by_waste']/total_emissions*100)
        percentage_business = (self.data['total_carbon_emission_by_business']/total_emissions*100)


    summary_data = [
        ["Category", "Emissions (kgCO2)", "Percentage"],
        ["Energy", f"{self.data['total_carbon_emissiom_by_energy']:.2f}",
         f"{(self.data['total_carbon_emission_by_energy']/total_emissions*100):.1f}%"],
        ["waste", f"{self.data['total_carbon_emission_by_waste']:.2f}",
         f"{(self.data['total_carbon_emission_by_waste']/total_emissions*100):.1f}%"],
        ["Business Travel", f"{self.data['total_carbon_emission_by_business']:.2f}",
         f"{(self.data['total_carbon_emission_by_business']/total_emissions*100):.1f}%"],
         ["Total", f"{total_emissions:.2f}", "100%"]
    ]

    table = Table(summary_data, colWidths=[150, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(Paragraph("Emission Summary", self.styles['Heading2']))
    elements.append(table)
    return elements

def _add_visualization(self):

    elements = []

    if self.data.get('graph'):
        img_data = base64.b64decode(self.data['graph'])
        img = Image(BytesIO(img_data))
        img.drawHeight = 4*ich
        img.drawWidth = 6*inch
        elements.append(Paragraph("Emission Distribution", self.styles['Heading2']))
        elements.append(img)
    
    return elements


def _add_recommendations(self):

    elements = []
    elements.append(Paragraph("Recommendations", self.styles['Heading2']))

    recommendations = []

    if self.data['total_carbon_emission_by_energy'] > 0:
        recommendations.append(
            "• Consider investing in energy-efficient appliances and lighting")
        recommendations.append(
            "• Implement a building management system to optimize energy usage")
        

    if self.data['total_carbon_emission_by_waste'] > 0:
        recommendations.append(
            "• Increase recycling efforts and implement waste segregation")
        recommendations.append(
            "• Consider composting organic waste to reduce landfill emissions")


    if self.data['total_carbon_emission_by_business'] > 0:
        recommendations.append(
            "• IPromote virtual meetings to reduce unnecessary business travel")
        recommendations.append(
            "• Consider hybrid or elctric vehicles fro company transportation")

    
    for rec in recommendations:
        elements.append(Paragraph(rec, self.styles['Normal']))
        elements.append(Spacer(1, 6))

    return elements
