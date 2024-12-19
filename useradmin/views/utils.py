from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import qrcode
from PIL import Image
import os


def generate_receipt(sale, invoice_link):
    """
    Generate a PDF receipt for a pharmacy sale.
    Returns a BytesIO object containing the PDF data.
    """
    try:
        # Create a buffer to store the PDF
        buffer = BytesIO()
        
        # Create the PDF object
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.setTitle(f"Invoice #{sale.id} - Your Pharmacy Name")
        
        # Starting y position and spacing
        y_position = height - 40  # Start closer to top
        line_spacing = 15  # Reduced spacing between lines
        
        # Company details
        company_name = "Your Pharmacy Name"
        company_address = "123 Health Street"
        company_city = "Medical City, MC 12345"
        company_phone = "Phone: (555) 123-4567"
        
        # Add company information
        c.setFont("Helvetica-Bold", 24)
        c.drawString(40, y_position, company_name)
        y_position -= 25  # Larger spacing after company name
        
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, company_address)
        y_position -= line_spacing
        c.drawString(40, y_position, company_city)
        y_position -= line_spacing
        c.drawString(40, y_position, company_phone)
        y_position -= 25  # Add some space before invoice details
        
        # Add invoice details
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y_position, f"Invoice #{sale.id}")
        y_position -= line_spacing
        
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, f"Date: {sale.sale_date.strftime('%B %d, %Y')}")
        y_position -= 25  # Add space before customer info
        
        # Add customer information
        c.drawString(40, y_position, "Bill To:")
        y_position -= line_spacing
        
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, sale.customer.first_name)
        y_position -= line_spacing
        c.drawString(40, y_position, f"Phone: {sale.customer.phone_number}")
        
        if sale.customer.email:
            y_position -= line_spacing
            c.drawString(40, y_position, f"Email: {sale.customer.email}")
        
        y_position -= 25  # Space before table
        
        # Create table for items
        data = [["Item", "Quantity", "Price", "Total"]]
        
        # Add items from cart
        for item in sale.cart.cartmedicines_set.all():
            data.append([
                item.medicine.name,
                str(item.quantity),
                f"RWF{item.medicine.price:.2f}",
                f"RWF{(item.quantity * item.medicine.price):.2f}"
            ])
        
        # Calculate table dimensions
        table = Table(data, colWidths=[3*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))
        
        # Draw the table
        table.wrapOn(c, width, height)
        table.drawOn(c, 40, y_position - 100)  # Adjusted position
        
        # Update position for elements after table
        y_position = y_position - 140  # Adjusted spacing after table
        
        # Add total
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y_position, f"Total: RWF{sale.total_price:.2f}")
        y_position -= 40
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add invoice URL to QR code
        qr.add_data(invoice_link)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Create a temporary file name
        temp_qr_path = f"temp_qr_{sale.id}.png"
        
        try:
            # Save QR code temporarily
            qr_img.save(temp_qr_path)
            
            # Center QR code on the page
            qr_code_size = 100  # Width and height of the QR code
            x_position_centered = (width - qr_code_size) / 2  # Center horizontally
            y_position_qr = y_position - 100  # Adjust vertical position
            
            c.drawImage(temp_qr_path, x_position_centered, y_position_qr, width=qr_code_size, height=qr_code_size)
            
            # Add scan message centered below QR code
            c.setFont("Helvetica", 10)
            text_width = c.stringWidth("Scan to view digital invoice", "Helvetica", 10)
            c.drawString((width - text_width) / 2, y_position_qr - 20, "Scan to view digital invoice")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_qr_path):
                os.remove(temp_qr_path)
        
        # Add footer
        c.setFont("Helvetica", 8)
        c.drawString(40, 30, "Thank you for your business!")
        c.drawString(width - 200, 30, f"Page 1 of 1")
        
        # Save the PDF
        c.save()
        
        # Get the PDF data and reset buffer position
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        # Log the error and re-raise
        print(f"Error generating receipt: {str(e)}")
        raise
