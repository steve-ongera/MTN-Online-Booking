import os
from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.conf import settings
from PIL import Image

def generate_professional_ticket_pdf(booking):
    """
    Generates a professional, visually appealing PDF ticket with QR code
    """
    # Generate a custom filename
    pdf_filename = f"{booking.booking_order_id}_{booking.name.replace(' ', '_')}_ticket.pdf"

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    styles.add(ParagraphStyle(
        name='CenteredTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        fontSize=16
    ))
    styles.add(ParagraphStyle(
        name='CenteredSubtitle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=12,
        textColor=colors.darkblue
    ))
    styles.add(ParagraphStyle(
        name='CenteredInfo',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.darkgray
    ))

    elements = []

    # Logo Handling
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png')
    if os.path.exists(logo_path):
        try:
            logo = RLImage(logo_path, width=2*inch, height=2*inch)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            
            # Bus Name and Seat Number below logo
            bus_info = Paragraph(
                f"{booking.seat.bus_schedule.bus.name} - {booking.seat.bus_schedule.bus.plate_number}<br/>" +
                f"Seat Number: {booking.seat.seat_number}", 
                styles['CenteredInfo']
            )
            elements.append(bus_info)
            elements.append(Spacer(1, 12))
        except Exception as e:
            print(f"Error loading logo: {e}")

    # Header Section
    header_data = [
        [
            Paragraph("InnovationHub Travel", styles['CenteredTitle']),
            Paragraph("Official Booking Ticket", styles['CenteredSubtitle'])
        ]
    ]
    header_table = Table(header_data, colWidths=[4*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # Booking Details
    ticket_details = [
        ['Booking ID', f"# {booking.booking_order_id}"],
        ['Passenger Name', booking.name],
        ['Bus', f"{booking.seat.bus_schedule.bus.name} - {booking.seat.bus_schedule.bus.plate_number}"],
        ['Travel Route', f"{booking.seat.bus_schedule.boarding_location} → {booking.seat.bus_schedule.destination}"],
        ['Date of Travel', booking.seat.bus_schedule.date_of_travel.strftime('%d %b %Y')],
        ['Departure Time', booking.seat.bus_schedule.departure_time.strftime('%I:%M %p')],
        ['Seat Number', booking.seat.seat_number],
        ['Identification Number', booking.identification_number],
    ]

    ticket_table = Table(ticket_details, colWidths=[2*inch, 4*inch])
    ticket_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(ticket_table)
    elements.append(Spacer(1, 12))

    # QR Code Generation
    qr_code = qr.QrCodeWidget(
        f"Booking:{booking.booking_order_id}|Name:{booking.name}|Route:{booking.seat.bus_schedule.boarding_location}-{booking.seat.bus_schedule.destination}"
    )
    qr_drawing = Drawing(2*inch, 2*inch)
    qr_drawing.add(qr_code)
    elements.append(qr_drawing)
    elements.append(Spacer(1, 12))

    # Fare and Additional Information
    fare_details = [
        ['Total Fare', f"KSH {booking.fare}"],
        ['Payment Status', 'Confirmed'],
    ]
    fare_table = Table(fare_details, colWidths=[2*inch, 4*inch])
    fare_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgreen),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(fare_table)
    elements.append(Spacer(1, 12))

    # Footer
    footer_text = [
        Paragraph("Thank you for choosing InnovationHub Travel", styles['Normal']),
        Paragraph("Terms & Conditions Apply | Non-Transferable", styles['Normal'])
    ]
    elements.extend(footer_text)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer, pdf_filename

def send_professional_ticket_email(booking, pdf_buffer):
    """
    Sends a professional email with the generated ticket PDF
    """
    # Generate PDF with custom filename
    pdf_buffer, pdf_filename = generate_professional_ticket_pdf(booking)

    subject = f'Your Travel Ticket - Booking #{booking.booking_order_id}'
    message = f"""
    Dear {booking.name},

    Thank you for booking with InnovationHub Travel. 
    Please find your official travel ticket attached to this email.

    Booking Details:
    - Booking ID: {booking.booking_order_id}
    - Bus Name: {booking.seat.bus_schedule.bus.name} - {booking.seat.bus_schedule.bus.plate_number}
    - Route: {booking.seat.bus_schedule.boarding_location} to {booking.seat.bus_schedule.destination}
    - Date: {booking.seat.bus_schedule.date_of_travel.strftime('%d %b %Y')}
    - Departure Time: {booking.seat.bus_schedule.departure_time.strftime('%I:%M %p')}
    - Seat Number: {booking.seat.seat_number}

    We wish you a pleasant journey!

    Best regards,
    InnovationHub Travel Team
    """

    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Sender's email
        [booking.email]  # Recipient's email
    )
    email.attach(pdf_filename, pdf_buffer.read(), 'application/pdf')
    email.send()