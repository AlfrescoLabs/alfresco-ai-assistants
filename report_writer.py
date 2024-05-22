from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle, PageTemplate, Frame)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color

class ReportWriter:
    def write_report(self, document_title, document_text):
        colors = [Color((32/255), (203/255), (96/255), 1),
                Color((72/255), (227/255), (187/255), 1),
                Color((92/255), (241/255), (233/255), 1),
                Color((47/255), (181/255), (248/255), 1),
                Color((51/255), (68/255), (227/255), 1)]

        doc = SimpleDocTemplate(f"{document_title}.pdf")
        doc.pagesize = portrait(A4)

        elements = []

        spacer = Spacer(10, 30)
        elements.append(spacer)

        d = Drawing(500, 1)
        line = Line(-15, 0, 300, 0)
        line.strokeColor = colors[4]
        line.strokeWidth = 2
        d.add(line)
        elements.append(d)

        spacer = Spacer(10, 1)
        elements.append(spacer)

        d = Drawing(500, 1)
        line = Line(-15, 0, 300, 0)
        line.strokeColor = colors[4]
        line.strokeWidth = 0.5
        d.add(line)
        elements.append(d)

        spacer = Spacer(10, 1)
        elements.append(spacer)

        psHeaderText = ParagraphStyle('Hed0', fontSize=32, alignment=TA_LEFT, borderWidth=3, textColor=colors[4])
        paragraphReportHeader = Paragraph(document_title, psHeaderText)
        elements.append(paragraphReportHeader)

        spacer = Spacer(10, 40)
        elements.append(spacer)

        d = Drawing(500, 1)
        line = Line(-15, 0, 300, 0)
        line.strokeColor = colors[4]
        line.strokeWidth = 2
        d.add(line)
        elements.append(d)

        spacer = Spacer(10, 1)
        elements.append(spacer)

        d = Drawing(500, 1)
        line = Line(-15, 0, 300, 0)
        line.strokeColor = colors[4]
        line.strokeWidth = 0.5
        d.add(line)
        elements.append(d)

        spacer = Spacer(10, 20)
        elements.append(spacer)

        # Add text content.

        for paragraph in document_text.split("\n"):
            psBodyText = ParagraphStyle('BodyText', fontSize=12, alignment=TA_LEFT, borderWidth=0.5)
            paragraphBodyText = Paragraph(paragraph, psBodyText)
            elements.append(paragraphBodyText)
            
            spacer = Spacer(10, 5)
            elements.append(spacer)

        # Draw footer.
        spacer = Spacer(10, 40)
        elements.append(spacer)
        for i in range(5):
            spacer = Spacer(10, 1)
            elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 300, 0)
            line.strokeColor = colors[4-i]
            line.strokeWidth = 2
            d.add(line)
            elements.append(d)

        spacer = Spacer(10, 22)
        elements.append(spacer)

        def drawImage(canvas, doc):
            canvas.drawImage("static/jp_logo.png", 0.5 * inch, doc.height + 0.1 * inch,
                            width=2 * inch, height=2 * inch, preserveAspectRatio=True, mask='auto')
            canvas.drawImage("static/alf_logo.png", doc.width - 0.2 * inch, doc.height + 0.3 * inch,
                            width=1.5 * inch, height=1.5 * inch, preserveAspectRatio=True, mask='auto')
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        pageTemplate = PageTemplate(frames=frame, onPage=drawImage)
        doc.addPageTemplates([pageTemplate])

        doc.build(elements)
