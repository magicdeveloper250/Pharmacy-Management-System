from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import qrcode
from PIL import Image
import os


def generate_receipt(request, sale, invoice_link):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        c.setTitle(f"Invoice #{sale.id} - {request.user.pharmacy.pharmacy_name}")
        y_position = height - 40   
        line_spacing = 15   
    
        company_name = request.user.pharmacy.pharmacy_name
        company_address = request.user.pharmacy.address
        company_city = ""
        company_phone = request.user.pharmacy.contact_phone
        c.setFont("Helvetica-Bold", 24)
        c.drawString(40, y_position, company_name)
        y_position -= 25   
        
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, company_address)
        y_position -= line_spacing
        c.drawString(40, y_position, company_city)
        y_position -= line_spacing
        c.drawString(40, y_position, company_phone)
        y_position -= 25   
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y_position, f"Invoice #{sale.id}")
        y_position -= line_spacing
        
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, f"Date: {sale.sale_date.strftime('%B %d, %Y')}")
        y_position -= 25   
        c.drawString(40, y_position, "Bill To:")
        y_position -= line_spacing
        
        c.setFont("Helvetica", 12)
        c.drawString(40, y_position, sale.customer.first_name)
        y_position -= line_spacing
        c.drawString(40, y_position, f"Phone: {sale.customer.phone_number}")
        
        if sale.customer.email:
            y_position -= line_spacing
            c.drawString(40, y_position, f"Email: {sale.customer.email}")
        
        y_position -= 25   
        data = [["Item", "Quantity", "Price", "Total"]]
        for item in sale.cart.cartmedicines_set.all():
            data.append([
                item.medicine.name,
                str(item.quantity),
                f"RWF{item.medicine.price:.2f}",
                f"RWF{(item.quantity * item.medicine.price):.2f}"
            ])
        
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
        
        table.wrapOn(c, width, height)
        table.drawOn(c, 40, y_position - 100)   
        
        y_position = y_position - 140   
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y_position, f"Total: RWF{sale.total_price:.2f}")
        y_position -= 40
 
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
 
        qr.add_data(invoice_link)
        qr.make(fit=True)
   
        qr_img = qr.make_image(fill_color="black", back_color="white")
 
        temp_qr_path = f"temp_qr_{sale.id}.png"
        
        try:
            qr_img.save(temp_qr_path)
            
            qr_code_size = 100   
            x_position_centered = (width - qr_code_size) / 2   
            y_position_qr = y_position - 100   
            
            c.drawImage(temp_qr_path, x_position_centered, y_position_qr, width=qr_code_size, height=qr_code_size)
 
            c.setFont("Helvetica", 10)
            text_width = c.stringWidth("Scan to view digital invoice", "Helvetica", 10)
            c.drawString((width - text_width) / 2, y_position_qr - 20, "Scan to view digital invoice")
        
        finally:
            if os.path.exists(temp_qr_path):
                os.remove(temp_qr_path)
        
        c.setFont("Helvetica", 8)
        c.drawString(40, 30, "Thank you for your business!")
        c.drawString(width - 200, 30, f"Page 1 of 1")
        
        c.save()
        
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        print(f"Error generating receipt: {str(e)}")
        raise
