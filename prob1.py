import streamlit as st
import requests
from supabase import create_client, Client
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv('supabase_url')
supabase_key = os.getenv('supabase_key')
supabase: Client = create_client(supabase_url, supabase_key)

# URL for sending emails and posting on LinkedIn
email_url = "http://54.84.189.207/send_email/"
linkedin_url = "http://54.84.189.207/post_linkedin/"

def send_email(receiver_emails, subject, body):
    payload = {
        "receiver_emails": receiver_emails,
        "subject": subject,
        "body": body
    }
    response = requests.post(email_url, json=payload)
    return response.status_code

def post_linkedin(title, image_url, text_content):
    payload = {
        "title": title,
        "image_url": image_url,
        "text_content": text_content
    }
    response = requests.post(linkedin_url, json=payload)
    return response.status_code

def save_employee_info(name, email, age, gender,phone,department):
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "department":department,
        "age": age,
        "gender": gender
    }
    response = supabase.table('employee').insert(data).execute()
    return response

# Streamlit app
st.title("HR Agent - Employee Onboarding")

st.header("Employee Onboarding")

# Collect employee's personal details
with st.form("employee_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=18, max_value=100)
    phone = st.number_input("Phone Number",min_value=1000000000, max_value=9999999999)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    department = st.text_input("Department")
    submit = st.form_submit_button("Onboard Employee")

if submit:
    # Save details in the database
    response = save_employee_info(name, email, age, gender,phone,department)
    
    if response:
        st.success("Employee information saved successfully.")
        
        # Send welcome email with necessary attachments
        subject = "Welcome to the Company"
        #body = f"Dear {name},\n\nWelcome to the company! Here is your Slack invite and employee policy.\n\nBest Regards,\nHR Team"
        body = f"""Dear  {name},\n\n

        Welcome to the company! We are thrilled to have you join our team. Below, you will find your Slack invite link and our employee policy document.

        \n\nSlack Invite
        Please use the following link to join our company's Slack workspace:
        Join Slack

        \n\nEmployee Policy
        Attached is the employee policy document, which outlines important guidelines and information to help you navigate your new role.

        Employee Policy Highlights
        \n\n
        Working Hours:

        Regular working hours are from 9:00 AM to 5:00 PM, Monday through Friday.
        Flexible working arrangements can be discussed with your manager.
        \n\n
        Dress Code:

        Our dress code is business casual. On Fridays, you may dress more casually as part of our "Casual Fridays."
        \n\nLeave Policy:

        Employees are entitled to 15 days of paid leave per year.
        Sick leave is available for up to 10 days per year.
        Public holidays will be observed as per the company calendar.
        \n\nCommunication:

        Slack is our primary communication tool. Please ensure you check it regularly for updates and messages.
        Email should be used for more formal communication.
        \n\nPerformance Reviews:

        Performance reviews will be conducted semi-annually to provide feedback and discuss growth opportunities.
        \n\nProfessional Development:

        The company supports continuous learning and professional development. Employees are encouraged to participate in workshops, courses, and conferences.
        \n\nCode of Conduct:

        All employees are expected to maintain a professional demeanor and respect their colleagues.
        Harassment, discrimination, and any form of misconduct will not be tolerated.
        \n\nHealth and Safety:

        The company is committed to providing a safe and healthy work environment. Please report any hazards or unsafe conditions to HR immediately.
        \n\nData Security:

        Employees must adhere to data security protocols to protect company and client information.
        \n\nFeedback and Suggestions:

        We value your feedback. Please feel free to share any suggestions or concerns with your manager or HR.
        For a comprehensive understanding, please refer to the attached employee policy document.

        We look forward to your contributions and wish you success in your new role. If you have any questions or need further assistance, please do not hesitate to reach out to us.

        Best Regards,\n
        HR Team\n

 """
        email_status = send_email([email], subject, body)
        
        if email_status == 200:
            st.success("Welcome email sent successfully.")
        else:
            st.error("Failed to send welcome email.")
        
        # Notify the department manager
        manager_email = "dharani.e@goml.io"
        subject = "New Employee Onboarding"
        body = f"Dear Manager,\n\nPlease be informed that {name} has joined the {department} department.\n\nBest Regards,\nHR Team"
        email_status = send_email([manager_email], subject, body)
        
        if email_status == 200:
            st.success("Department manager notified successfully.")
        else:
            st.error("Failed to notify department manager.")
        title = "Welcome to our new employee!"
        image_url = "https://i.pinimg.com/originals/cb/37/5e/cb375e56ea17907217a0b970e8eef870.png"
        text_content = f"Join us in welcoming {name} to the company! We are excited to have you on board."
        linkedin_status = post_linkedin(title, image_url, text_content)
        
        if linkedin_status == 200:
            st.success("Social media announcement posted successfully.")
        else:
            st.error("Failed to post social media announcement.")
        
