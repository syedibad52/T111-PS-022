"""Regenerate DesignDocument.pdf: pip install reportlab; python docs/build_design_pdf.py."""
from pathlib import Path
from html import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

ROOT = Path(__file__).resolve().parent
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyTextDemo', fontName='Helvetica', fontSize=10.5,
                         leading=15, spaceAfter=9, textColor=colors.HexColor('#263449')))
styles['Title'].fontSize = 25
styles['Title'].leading = 30
styles['Title'].alignment = TA_LEFT
styles['Title'].textColor = colors.HexColor('#113d65')
styles['Heading2'].textColor = colors.HexColor('#113d65')
styles['Heading3'].textColor = colors.HexColor('#226285')

def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#d4dfe9'))
    canvas.line(48, 43, A4[0]-48, 43)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#52657b'))
    canvas.drawString(48, 29, 'Credit Bureau Score Simulator | Design document')
    canvas.drawRightString(A4[0]-48, 29, str(doc.page))

story=[]
for block in (ROOT/'DesignDocument.md').read_text(encoding='utf-8').split('\n\n'):
    block=block.strip()
    if not block:
        continue
    if block=='<!-- pagebreak -->':
        story.append(PageBreak())
    elif block.startswith('# '):
        story.append(Paragraph(escape(block[2:]), styles['Title']))
    elif block.startswith('## '):
        story.append(Paragraph(escape(block[3:]), styles['Heading2']))
    elif block.startswith('### '):
        story.append(Paragraph(escape(block[4:]), styles['Heading3']))
    elif block.startswith('- '):
        for line in block.splitlines():
            story.append(Paragraph(escape(line[2:]), styles['BodyTextDemo'], bulletText='-'))
    else:
        story.append(Paragraph(escape(block).replace('\n',' '), styles['BodyTextDemo']))

doc=SimpleDocTemplate(str(ROOT/'DesignDocument.pdf'),pagesize=A4,
    rightMargin=48,leftMargin=58,topMargin=45,bottomMargin=58,
    title='Credit Bureau Score Simulator - Design Document',author='Credit Bureau Simulator project')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(ROOT/'DesignDocument.pdf')
