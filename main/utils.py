# utils.py

from django.core.mail import EmailMessage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.conf import settings

def generate_pdf_receipt(booking):
    """
    Generates a PDF receipt for the booking and returns it as a BytesIO object.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Header (Company Information)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 770, "Your Company Name")
    p.setFont("Helvetica", 10)
    p.drawString(200, 755, "Address: 123 Main Street, City, Country")
    p.drawString(200, 740, "Phone: +1234567890")
    p.drawString(200, 725, "Email: support@yourcompany.com")

    # Receipt Title
    p.setFont("Helvetica-Bold", 12)
    p.drawString(200, 700, "Receipt")

    # Booking Details Section
    p.setFont("Helvetica", 10)
    p.drawString(50, 675, f"Booking ID: {booking.id}")
    p.drawString(50, 660, f"Name: {booking.name}")
    p.drawString(50, 645, f"Email: {booking.email}")
    p.drawString(50, 630, f"Phone: {booking.phone}")
    p.drawString(50, 615, f"Seat Number: {booking.seat.seat_number if booking.seat else 'No seat assigned'}")
    p.drawString(50, 600, f"Identification Number: {booking.identification_number}")

    # Fare Section
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, 570, f"Total Fare: ${booking.fare}")

    # Footer
    p.setFont("Helvetica", 8)
    p.drawString(50, 50, "Thank you for booking with us!")
    p.drawString(50, 40, "Visit us again for more exciting offers.")

    # Draw a line to separate footer
    p.setStrokeColorRGB(0, 0, 0)
    p.setLineWidth(0.5)
    p.line(50, 60, 550, 60)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def send_receipt_email(booking, pdf_buffer):
    """
    Sends an email with the generated PDF receipt as an attachment.
    """
    subject = 'Booking Confirmation - Your Receipt'
    message = f'Hello {booking.name},\n\nThank you for your booking! Please find your receipt attached.'
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # Sender's email address
        [booking.email],  # Recipient's email address
    )
    email.attach('receipt.pdf', pdf_buffer.read(), 'application/pdf')
    email.send()
