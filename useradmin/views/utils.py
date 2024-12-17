from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def generate_receipt(sale):
    # Create a BytesIO buffer
    buffer = BytesIO()

    # Create a PDF canvas
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw Header (Company Name or Logo)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "Cider Cellar")

    # Draw Receipt Title
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2, height - 100, "SALES RECEIPT")

    # Draw Item Table
    items = [
        ["Qty", "Item Description", "Price"],
        ["1x", "Bulmers Original Bottle", "£4.00"],
        ["", "*** Price Override: Manager Override", "-£2.00"],
        ["1x", "Bulmers Pear Bottle", "£4.00"],
        ["", "*** Line Discount: Wrongly Advertised", "-£1.00"],
    ]
    
    # Add totals
    items += [
        ["", "2x Items Sold", ""],
        ["", "Sub Total:", "£8.00"],
        ["", "Line Discount:", "-£3.00"],
        ["", "Transaction Discount:", "-£0.50"],
        ["", "Discount Total:", "-£3.50"],
        ["", "Total:", "£4.50"],
        ["", "Cash:", "£5.00"],
        ["", "Tendered Total:", "£5.00"],
        ["", "Change:", "£0.50"],
    ]

    # Create a table
    table = Table(items, colWidths=[50, 300, 100])
    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ])
    )

    # Draw the table
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, height - 350)

    # Draw footer
    p.setFont("Helvetica", 10)
    p.drawString(50, 100, "Thank you for your purchase!")
    p.drawString(50, 85, "Receipt ID: 22285")
    p.drawString(50, 70, "Date: 24/09/2018")
    p.drawString(50, 55, "Time: 14:30")
    p.drawString(50, 40, "Admin")

    # Finish the PDF
    p.save()

    # Save the PDF file
    buffer.seek(0)
    receipt_name = f"sale_receipt_{sale.id}.pdf"
    return ContentFile(buffer.read(), name=receipt_name)
