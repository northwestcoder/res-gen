from faker import Faker
from datetime import datetime, timedelta
import random
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import argparse
from job_entries import JOB_ENTRIES

# Available fonts and sizes
FONTS = ['Helvetica', 'Times-Roman', 'Courier', 'Helvetica-Bold', 'Times-Bold', 'Courier-Bold']
FONT_SIZES = [10, 11, 12]

class ResumeGenerator:
    def __init__(self):
        self.fake = Faker()
        self.resume = {
            'personal_info': {},
            'experience': [],
            'education': [],
            'skills': [],
            'certifications': []
        }
        # Randomly select font and size for this resume
        self.font = random.choice(FONTS)
        self.font_size = random.choice(FONT_SIZES)
        
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontName=self.font,
            fontSize=self.font_size + 4,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontName=self.font,
            fontSize=self.font_size + 2,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontName=self.font,
            fontSize=self.font_size,
            spaceAfter=6
        ))
    
    def generate_personal_info(self):
        """Generate realistic personal information"""
        self.resume['personal_info'] = {
            'name': self.fake.name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'linkedin': f"linkedin.com/in/{self.fake.user_name()}",
            'summary': self.generate_personalized_summary()
        }
    
    def generate_personalized_summary(self):
        """Generate a personalized summary based on job history and skills"""
        # Get unique industries from experience
        industries = list(set(job['industry'] for job in self.resume['experience']))
        
        # Get years of experience
        years = len(self.resume['experience'])
        
        # Get key skills
        technical_skills = self.resume['skills']['technical']
        soft_skills = self.resume['skills']['soft']
        
        # Generate summary based on experience and skills
        summary_parts = []
        
        # Opening statement
        summary_parts.append(f"Experienced professional with {years} years of experience in {', '.join(industries)}.")
        
        # Add key skills and expertise
        if technical_skills:
            summary_parts.append(f"Proficient in {', '.join(technical_skills[:3])}.")
        
        # Add soft skills
        if soft_skills:
            summary_parts.append(f"Demonstrated strengths in {', '.join(soft_skills)}.")
        
        # Add career focus
        if len(industries) == 1:
            summary_parts.append(f"Committed to excellence in {industries[0]} with a track record of delivering results.")
        else:
            summary_parts.append("Versatile professional with experience across multiple industries.")
        
        # Add value proposition
        summary_parts.append("Seeking opportunities to leverage expertise and drive organizational success.")
        
        return ' '.join(summary_parts)
    
    def generate_experience(self, num_jobs=3):
        """Generate work experience entries using the job entries database"""
        for _ in range(num_jobs):
            job_entry = random.choice(JOB_ENTRIES)
            start_date = self.fake.date_between(start_date='-10y', end_date='-1y')
            end_date = start_date + timedelta(days=random.randint(365, 2000))
            
            job = {
                'company': self.fake.company(),
                'position': job_entry['title'],
                'industry': job_entry['industry'],
                'start_date': start_date.strftime('%B %Y'),
                'end_date': end_date.strftime('%B %Y'),
                'location': self.fake.city(),
                'description': job_entry['description']
            }
            self.resume['experience'].append(job)
    
    def generate_education(self):
        """Generate education history"""
        degrees = ['Bachelor of Science', 'Master of Business Administration', 'Bachelor of Arts']
        majors = ['Computer Science', 'Business Administration', 'Engineering', 'Marketing',
                 'Nursing', 'Education', 'Finance', 'Psychology', 'Biology', 'Chemistry']
        
        for _ in range(2):
            education = {
                'degree': random.choice(degrees),
                'major': random.choice(majors),
                'school': self.fake.company() + ' University',
                'graduation_year': self.fake.year(),
                'gpa': round(random.uniform(3.0, 4.0), 2)
            }
            self.resume['education'].append(education)
    
    def generate_skills(self):
        """Generate relevant skills based on job industry"""
        # Get unique industries from experience
        industries = list(set(job['industry'] for job in self.resume['experience']))
        
        # Define industry-specific skills
        industry_skills = {
            'Healthcare': ['Patient Care', 'Medical Terminology', 'HIPAA Compliance', 'Clinical Documentation', 'Emergency Response'],
            'Finance': ['Financial Analysis', 'Risk Management', 'Investment Strategies', 'Financial Modeling', 'Regulatory Compliance'],
            'Education': ['Curriculum Development', 'Classroom Management', 'Student Assessment', 'Educational Technology', 'Special Education'],
            'Marketing': ['Digital Marketing', 'Social Media Management', 'Content Strategy', 'Market Research', 'Brand Management'],
            'Engineering': ['CAD Design', 'Project Management', 'Technical Documentation', 'Quality Control', 'Systems Analysis'],
            'Legal': ['Legal Research', 'Case Management', 'Contract Law', 'Litigation Support', 'Regulatory Compliance'],
            'Technology': ['Programming', 'System Administration', 'Network Security', 'Cloud Computing', 'Database Management'],
            'Sales': ['Customer Relationship Management', 'Negotiation', 'Market Analysis', 'Sales Strategy', 'Account Management'],
            'Human Resources': ['Recruitment', 'Employee Relations', 'Performance Management', 'Training Development', 'HR Policies'],
            'Hospitality': ['Customer Service', 'Event Planning', 'Inventory Management', 'Quality Assurance', 'Revenue Management'],
            'Manufacturing': ['Production Planning', 'Quality Control', 'Supply Chain Management', 'Process Improvement', 'Safety Compliance'],
            'Media': ['Content Creation', 'Social Media Management', 'Public Relations', 'Media Planning', 'Crisis Communication'],
            'Non-Profit': ['Grant Writing', 'Volunteer Management', 'Fundraising', 'Program Development', 'Community Outreach'],
            'Government': ['Policy Analysis', 'Public Administration', 'Regulatory Compliance', 'Budget Management', 'Stakeholder Engagement']
        }
        
        # Get industry-specific skills
        technical_skills = []
        for industry in industries:
            if industry in industry_skills:
                technical_skills.extend(industry_skills[industry])
        
        # Add some general skills
        soft_skills = [
            'Leadership', 'Communication', 'Project Management',
            'Team Collaboration', 'Problem Solving', 'Time Management',
            'Critical Thinking', 'Adaptability', 'Conflict Resolution'
        ]
        
        self.resume['skills'] = {
            'technical': list(set(technical_skills))[:5],  # Limit to 5 unique technical skills
            'soft': random.sample(soft_skills, 3)
        }
    
    def generate_certifications(self):
        """Generate professional certifications based on industry"""
        # Get unique industries from experience
        industries = list(set(job['industry'] for job in self.resume['experience']))
        
        # Define industry-specific certifications
        industry_certs = {
            'Healthcare': ['Registered Nurse (RN)', 'Certified Medical Assistant (CMA)', 'Basic Life Support (BLS)'],
            'Finance': ['Chartered Financial Analyst (CFA)', 'Certified Public Accountant (CPA)', 'Financial Risk Manager (FRM)'],
            'Education': ['Teaching Certification', 'Special Education Certification', 'Educational Leadership Certification'],
            'Marketing': ['Digital Marketing Certification', 'Google Analytics Certification', 'HubSpot Content Marketing'],
            'Engineering': ['Professional Engineer (PE)', 'Project Management Professional (PMP)', 'Six Sigma Certification'],
            'Legal': ['Bar Certification', 'Certified Legal Manager (CLM)', 'Paralegal Certification'],
            'Technology': ['AWS Certified Solutions Architect', 'Cisco Certified Network Associate', 'Microsoft Certified Professional'],
            'Sales': ['Certified Sales Professional (CSP)', 'Salesforce Certification', 'Professional Sales Certification'],
            'Human Resources': ['Professional in Human Resources (PHR)', 'SHRM Certified Professional', 'Talent Management Certification'],
            'Hospitality': ['Certified Hotel Administrator (CHA)', 'Food Safety Certification', 'Event Planning Certification'],
            'Manufacturing': ['Lean Six Sigma Certification', 'Quality Management Certification', 'Production Planning Certification'],
            'Media': ['Google Analytics Certification', 'Content Marketing Certification', 'Social Media Marketing Certification'],
            'Non-Profit': ['Certified Fund Raising Executive (CFRE)', 'Nonprofit Management Certification', 'Grant Writing Certification'],
            'Government': ['Public Administration Certification', 'Policy Analysis Certification', 'Government Management Certification']
        }
        
        # Get certifications based on industries
        certs = []
        for industry in industries:
            if industry in industry_certs:
                certs.extend(industry_certs[industry])
        
        # Select 2-3 certifications
        num_certs = random.randint(2, 3)
        selected_certs = random.sample(certs, min(num_certs, len(certs)))
        
        for cert_name in selected_certs:
            cert = {
                'name': cert_name,
                'issuer': self.fake.company(),
                'year': self.fake.year()
            }
            self.resume['certifications'].append(cert)
    
    def generate_resume(self):
        """Generate complete resume"""
        self.generate_experience()
        self.generate_education()
        self.generate_skills()
        self.generate_certifications()
        self.generate_personal_info()  # Generate personal info last to use experience and skills
        return self.resume
    
    def save_as_pdf(self, filename='resume.pdf'):
        """Save resume as PDF file"""
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        
        # Add personal information
        story.append(Paragraph(self.resume['personal_info']['name'], self.styles['CustomTitle']))
        story.append(Paragraph(self.resume['personal_info']['email'], self.styles['CustomBody']))
        story.append(Paragraph(self.resume['personal_info']['phone'], self.styles['CustomBody']))
        story.append(Paragraph(self.resume['personal_info']['address'], self.styles['CustomBody']))
        story.append(Paragraph(self.resume['personal_info']['linkedin'], self.styles['CustomBody']))
        story.append(Spacer(1, 12))
        
        # Add summary
        story.append(Paragraph('Professional Summary', self.styles['CustomHeading']))
        story.append(Paragraph(self.resume['personal_info']['summary'], self.styles['CustomBody']))
        story.append(Spacer(1, 12))
        
        # Add experience
        story.append(Paragraph('Professional Experience', self.styles['CustomHeading']))
        for job in self.resume['experience']:
            story.append(Paragraph(f"{job['position']} at {job['company']}", self.styles['CustomBody']))
            story.append(Paragraph(f"{job['start_date']} - {job['end_date']} | {job['location']}", self.styles['CustomBody']))
            story.append(Paragraph(job['description'], self.styles['CustomBody']))
            story.append(Spacer(1, 6))
        
        # Add education
        story.append(Paragraph('Education', self.styles['CustomHeading']))
        for edu in self.resume['education']:
            story.append(Paragraph(f"{edu['degree']} in {edu['major']}", self.styles['CustomBody']))
            story.append(Paragraph(f"{edu['school']} | Graduated: {edu['graduation_year']} | GPA: {edu['gpa']}", self.styles['CustomBody']))
            story.append(Spacer(1, 6))
        
        # Add skills
        story.append(Paragraph('Skills', self.styles['CustomHeading']))
        story.append(Paragraph('Technical: ' + ', '.join(self.resume['skills']['technical']), self.styles['CustomBody']))
        story.append(Paragraph('Soft Skills: ' + ', '.join(self.resume['skills']['soft']), self.styles['CustomBody']))
        story.append(Spacer(1, 12))
        
        # Add certifications
        story.append(Paragraph('Certifications', self.styles['CustomHeading']))
        for cert in self.resume['certifications']:
            story.append(Paragraph(f"{cert['name']} | {cert['issuer']} | {cert['year']}", self.styles['CustomBody']))
        
        # Build the PDF
        doc.build(story)
        return filename

def generate_multiple_resumes(num_resumes=1, output_dir='resumes'):
    """Generate multiple resumes"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(num_resumes):
        generator = ResumeGenerator()
        generator.generate_resume()
        pdf_filename = os.path.join(output_dir, f'resume_{i+1}.pdf')
        generator.save_as_pdf(pdf_filename)
        print(f"Generated resume {i+1} of {num_resumes}: {pdf_filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate realistic resumes')
    parser.add_argument('-n', '--number', type=int, default=1,
                      help='Number of resumes to generate (default: 1)')
    parser.add_argument('-o', '--output', type=str, default='resumes',
                      help='Output directory for generated resumes (default: resumes)')
    
    args = parser.parse_args()
    generate_multiple_resumes(args.number, args.output)

if __name__ == "__main__":
    main() 