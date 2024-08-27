import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_email(name, email, message):
    sender_email = st.secrets["SENDER_EMAIL"]  # Fetch email from Streamlit secrets
    receiver_email = "nandan.pabolu808@gmail.com"  # Replace with your email
    password = st.secrets["EMAIL_PASSWORD"]  # Fetch password from Streamlit secrets
    
    if not sender_email or not password:
        st.error("Email credentials are not configured properly.")
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
st.set_page_config(page_title="Contact Me", page_icon="📬", layout="centered")

st.title("📬 Contact Me")
st.write("If you have any questions, feel free to reach out using the form below.")

st.markdown(
    """
    <style>
        .stTextInput, .stTextArea {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            margin-bottom: 15px;
        }
        .stButton > button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .success-message {
            font-size: 16px;
            color: green;
        }
        .error-message {
            font-size: 16px;
            color: red;
        }
    </style>
    """, unsafe_allow_html=True
)

# Contact Form
with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Name", placeholder="Enter your name")
    email = st.text_input("Email", placeholder="Enter your email address")
    message = st.text_area("Message", placeholder="Enter your message here...")

    submit_button = st.form_submit_button("Send")

    if submit_button:
        if not name or not email or not message:
            st.error("Please fill out all fields.", icon="🚨")
        else:
            success = send_email(name, email, message)
            if success:
                st.success("Your message has been sent! Thank you for reaching out.", icon="✅")
            else:
                st.error("There was an error sending your message. Please try again later.", icon="❌")
