import os
from datetime import datetime
from jinja2 import Template
import markdown

def format_analysis_for_html(analysis_text):
    """Convert markdown-style analysis to HTML"""
    # Convert markdown to HTML
    html = markdown.markdown(analysis_text)
    return html

def generate_html_report(report_data):
    """Generate HTML report from data"""
    
    # Read template
    template_path = os.path.join('templates', 'daily_report.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Format timestamp
    timestamp = report_data['timestamp']
    date_str = timestamp.strftime('%B %d, %Y')
    time_str = timestamp.strftime('%I:%M %p')
    
    # Convert analysis to HTML
    analysis_html = format_analysis_for_html(report_data['analysis'])
    
    # Render template
    html = template.render(
        date=date_str,
        time=time_str,
        tradfi=report_data['tradfi'],
        crypto=report_data['crypto'],
        onchain=report_data['onchain'],
        news=report_data['news'],
        analysis_html=analysis_html
    )
    
    # Save to reports/ with correct filename format
    filename = timestamp.strftime('report_%Y%m%d.html')  # ← Changed format
    filepath = os.path.join('reports', filename)         # ← Changed directory
    
    # Ensure directory exists
    os.makedirs('reports', exist_ok=True)                # ← Changed directory
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Report saved to: {filepath}")
    
    return filepath

if __name__ == "__main__":
    print("Reporter module - use from main.py")