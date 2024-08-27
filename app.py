import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to send email
def send_email(name, email, message):
    sender_email = os.getenv("SENDER_EMAIL")  # Fetch email from environment variable
    receiver_email = "nandan.pabolu808@gmail.com"  # Replace with your email
    password = os.getenv("EMAIL_PASSWORD")  # Fetch password from environment variable
    
    if sender_email and password:
        st.write("Environment variables loaded successfully.")
        st.write(f"Sender Email: {sender_email}")  # Optional, for debugging
    else:
        st.error("Error: Environment variables are not loaded properly.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Create the plain-text version of your message
    text = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    part1 = MIMEText(text, "plain")
    msg.attach(part1)

    # SMTP server configuration for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # Use 587 for TLS if you prefer

    # Send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Streamlit App
st.title("Contact Me")

st.write("Fill out the form below to contact me:")

# Contact Form
with st.form("contact_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    submit_button = st.form_submit_button("Send")

    if submit_button:
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        else:
            success = send_email(name, email, message)
            if success:
                st.success("Your message has been sent!")
            else:
                st.error("There was an error sending your message. Please try again.")
