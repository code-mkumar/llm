import streamlit as st
import sqlite3
import pyotp
import qrcode
import time  
from streamlit.components.v1 import html 
from io import BytesIO
from datetime import datetime
import os
import google.generativeai as genai
# Configure Google Gemini API key
genai.configure(api_key='AIzaSyD3WqHberJDYyzXkmY1zKaoqd5uCJZDetI')
model = genai.GenerativeModel('gemini-pro')



# SQLite connection
def create_connection():
    return sqlite3.connect("university.db")

# Generate a new TOTP secret for a user
def generate_secret_code(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    secret = pyotp.random_base32()  # Generate a TOTP secret
    cursor.execute("UPDATE user_detail SET secret_code = ? WHERE id = ?", (secret, user_id))
    conn.commit()
    conn.close()
    return secret

# Retrieve the secret code and role for a user
def get_user_details(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT secret_code, role, name FROM user_detail WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None, None)

# Generate a QR code for the TOTP secret
def generate_qr_code(user_id, secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user_id, issuer_name="University Authenticator")
    qr = qrcode.QRCode()
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# Verify the OTP against the secret
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

# Update the multifactor status in the database
def update_multifactor_status(user_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_detail SET multifactor = ? WHERE id = ?", (status, user_id))
    conn.commit()
    conn.close()

# Read file content and save to session
def read_student_files():
    with open("student_role.txt", "r") as role_file:
        role_content = role_file.read()
    with open("student_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def read_default_files():
    with open("default.txt", "r") as role_file:
        role_content = role_file.read()
    with open("default_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def read_staff_files():
    with open("staff_role.txt", "r") as role_file:
        role_content = role_file.read()
    with open("staff_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content

def read_admin_files():
    with open("admin_role.txt", "r") as role_file:
        role_content = role_file.read()
    with open("admin_sql.txt", "r") as sql_file:
        sql_content = sql_file.read()
    return role_content, sql_content
def write_content(data):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = 'result.txt'
    
    # Check if the file exists, if not create it
    if not os.path.exists(file_path):
        # Create the file if it doesn't exist
        with open(file_path, 'w') as file:
            file.write(f'File created on {current_datetime}\n')

    # Append the data to the file
    with open(file_path, 'a') as file:
        file.write(f'{current_datetime} - {data}\n')


def guest_page():
    # Initialize session state for storing Q&A history
    if 'qa_list' not in st.session_state:
        st.session_state.qa_list = []

    if 'last_question' not in st.session_state:
        st.session_state.last_question = ""  # Track the last processed question

    if 'question_input' not in st.session_state:
        st.session_state.question_input = ""  # Initialize the question input

    # Main page content - Top of the page
    st.title("Welcome, Guest!")
    st.subheader("Hi, I'm ANJAC AI ")
    st.write("You can explore the site as a guest, but you'll need to log in for full role-based access.")

    # Function to process and clear text input after processing
    def process_and_clear():
        # Process the question if it's valid
        if st.session_state.question_input.strip() and st.session_state.question_input != st.session_state.last_question:
            with st.spinner("Processing your question..."):
                time.sleep(2)  # Simulate processing delay
                try:
                    question = st.session_state.question_input
                    # Simulate model processing and generate a response
                    default, default_sql = read_default_files()  # Placeholder function for reading default files
                    response = model.generate_content(f"{default_sql}\n\n{question}")
                    raw_query = response.text

                    # Format the SQL query for execution (example)
                    formatted_query = raw_query.replace("sql", "").strip("'''").strip()
                    single_line_query = " ".join(formatted_query.split()).replace("```", "")

                    # Execute the formatted query (simulate)
                    data = read_sql_query(single_line_query)  # Placeholder function for reading SQL query

                    # Generate an answer based on the data and user question
                    answer = model.generate_content(
                        f"{default} Answer this question: {question} with results {str(data)}"
                    )
                    result_text = answer.candidates[0].content.parts[0].text

                    # Append the Q&A to session state for later display
                    st.session_state.qa_list.append({'question': question, 'answer': result_text})

                    # Update last_question to avoid reprocessing the same question
                    st.session_state.last_question = question

                    # Clear the input field after processing
                    st.session_state.question_input = ""  # Clear the input field

                except Exception as e:
                    # Handle errors gracefully
                    st.error(f"An error occurred: {e}")

    # Display the most recent Q&A if it's available
    if st.session_state.qa_list:
        most_recent_qa = st.session_state.qa_list[-1]
        st.markdown("### Question & Answer Q&A")
        st.markdown(f"**Question:** {most_recent_qa['question']}")
        st.markdown(f"**Answer:** {most_recent_qa['answer']}")
        st.markdown("---")

    # Sidebar to display previous questions and answers (optional)
    with st.sidebar:
        st.markdown("""
        <style>
            .login-btn {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                transition: background-color 0.3s ease;
            }
            .login-btn:hover {
                background-color: #45a049;
            }
        </style>
        """, unsafe_allow_html=True)

        if st.button("Go to Login", help="Click to login for full access"):
            st.session_state.page = "login"
            st.rerun()

        st.title("Chat History")
        if st.session_state.qa_list:
            for qa in reversed(st.session_state.qa_list):  # Most recent first
                st.markdown(f"**Question:** {qa['question']}")
                st.markdown(f"**Answer:** {qa['answer']}")
                st.markdown("---")
        else:
            st.info("No previous chats yet.")

    # Input field for the user's question - Fixed at the bottom of the page
    question_input = st.text_area(
        'Input your question:',
        placeholder="Type your question and press Enter",
        key="question_input",
        value=st.session_state.question_input,  # Bind to session state
        on_change=process_and_clear,  # Process and clear on change
        help="Type your question here and it will be processed by ANJAC AI."
    ) 
    # Custom HTML for Icon (can use Font Awesome for a 'Send' icon or similar)
    icon_html = '''
    <style>
        .send-icon {
            font-size: 20px;
            float:right;
            cursor: pointer;
            padding: 10px;
            background-color: #000;
            border: none;
            color: white;
            border-radius: 100px;
            transition: background-color 0.3s, transform 0.2s; /* Smooth transition */
            }
            
        .send-icon:hover {
            background-color: #555; /* Change background color on hover */
            transform: scale(1.1); /* Slightly enlarge the button on hover */
            }
    </style>
    <button class="send-icon" onclick="document.getElementById('submit-button').click()">↑</button>
    '''
    html(icon_html)  # Display icon button using custom HTML


    # Custom CSS Styling
    st.markdown("""
        <style>
            .css-18e3th9 {
                padding: 1rem;
                background-color: #f7f7f7;
                border-radius: 10px;
            }
            .css-1d391kg {
                font-size: 18px;
                color: #2d3748;
            }
            .css-1q7s4c7 {
                font-size: 22px;
                font-weight: bold;
                color: #38a169;
            }
            .css-1h69q0h {
                font-size: 14px;
                color: #7a7a7a;
            }
        </style>
    """, unsafe_allow_html=True)

#login page
# def login_page():
#     st.title("Login")
#     user_id = st.text_input("User ID")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         conn = create_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM user_detail WHERE id = ? AND password = ?", (user_id, password))
#         user = cursor.fetchone()
#         conn.close()

#         if user:
#             st.session_state.authenticated = True
#             st.session_state.user_id = user_id
#             st.session_state.multifactor = user[7]  # Multifactor column
#             st.session_state.secret = user[9]  # Secret code column
#             st.success("Login successful!")
#             if st.session_state.multifactor == 1:
#                 st.session_state.page = "otp_verification"  # Direct to OTP verification if MFA is enabled
#             else:
#                 if st.session_state.secret == "None":
#                     st.session_state.page = "qr_setup"  # If MFA is not enabled, show QR setup
#                 else:
#                     st.session_state.page = "otp_verification"  # Otherwise show OTP verification
#         else:
#             st.error("Invalid credentials.")
#     if st.button("Visit as Guest"):
#         st.session_state.page = "guest"



def login_page():
    st.title("Login")

    # Initialize session state variables if they don't exist
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = ""
    if "password" not in st.session_state:
        st.session_state.password = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Default page

    # Define function to handle authentication
    def authenticate():
        user_id = st.session_state.user_id
        password = st.session_state.password

        # Establish connection to the database
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_detail WHERE id = ? AND password = ?", (user_id, password))
        user = cursor.fetchone()
        conn.close()

        # Check if credentials are correct
        if user:
            # Successful login, set session state variables
            st.session_state.authenticated = True
            st.session_state.user_id = user_id
            st.session_state.multifactor = user[7]  # Assuming MFA column is at index 7
            st.session_state.secret = user[9]  # Assuming secret column is at index 9

            st.success("Login successful!")
            
            # Handle MFA flow
            if st.session_state.multifactor == 1:
                st.session_state.page = "otp_verification"  # Go to OTP verification if MFA is enabled
            else:
                if st.session_state.secret == "None":
                    st.session_state.page = "qr_setup"  # Go to QR setup if MFA is not enabled
                else:
                    st.session_state.page = "otp_verification"  # Go to OTP verification if secret exists
        else:
            st.error("Invalid credentials. Please try again.")

    # Create input fields for User ID and Password
    user_id_input = st.text_input("Enter your User ID", key="user_id")  
    password_input = st.text_input("Enter your Password", type="password", key="password")  

    # Create a Login button that triggers authentication
    if st.button("Login"):
        authenticate()

    # Option for visiting as a guest
    if st.button("Visit as Guest"):
        st.session_state.page = "guest"
        st.rerun()  # Trigger a rerun to load the guest page directly

#qr scanning page
def qr_setup_page():
    st.title("Setup Multifactor Authentication")
    user_id = st.session_state.user_id

    if st.session_state.secret == "None":
        # Generate a new secret
        secret = generate_secret_code(user_id)
        st.session_state.secret = secret
    else:
        secret = st.session_state.secret

    # Display QR Code
    qr_code_stream = generate_qr_code(user_id, secret)
    st.image(qr_code_stream, caption="Scan this QR code with your authenticator app.", use_column_width=False)
    st.write(f"Secret Code: `{secret}` (store this securely!)")

    # Immediate OTP verification
    otp = st.text_input("Enter OTP from Authenticator App", type="password")
    if st.button("Verify OTP"):
        if verify_otp(secret, otp):
            update_multifactor_status(user_id, 1)  # Update MFA status in the database
            st.session_state.multifactor = 1
            _, role, name = get_user_details(user_id)
            st.session_state.id=user_id
            st.session_state.role = role
            st.session_state.name = name
            if role == "student":
                role_content, sql_content = read_student_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
            if role == "staff":
                role_content,sql_content = read_staff_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
            if role == "admin":
                role_content,sql_content = read_admin_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
            st.success("Multifactor authentication is now enabled.")
            st.session_state.page = "welcome"
        else:
            st.error("Invalid OTP. Try again.")

#otp verification page
def otp_verification_page():
    st.title("Verify OTP")
    user_id = st.session_state.user_id
    secret = st.session_state.secret

    otp = st.text_input("Enter OTP", type="password")
    if st.button("Verify"):
        if verify_otp(secret, otp):
            st.success("OTP Verified! Welcome.")
            _, role, name = get_user_details(user_id)
            st.session_state.id=user_id
            st.session_state.role = role
            st.session_state.name = name
            if role == "student":
                role_content, sql_content = read_student_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
            if role == "staff":
                role_content,sql_content = read_staff_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
            if role == "admin":
                role_content,sql_content = read_admin_files()
                st.session_state.role_content = role_content
                st.session_state.sql_content = sql_content
            st.session_state.page = "welcome"
        else:
            st.error("Invalid OTP. Try again.")

#just for combining
def create_combined_prompt(question, sql_prompt):
    return f"{sql_prompt}\n\n{question}\n\n "

# Function to interact with the Google Gemini model
def get_gemini_response(combined_prompt):
    response = model.generate_content(combined_prompt)
    print(response)
    try:
        final = model.generate_content(f"{response.text} if any user_id word found in this statement replace with {st.session_state.id}")
        #final=model.generate_content(response.text)
    except:
        return "please contact to the staff or admin"
    return final.text
    # if not response or 'candidates' not in response:
    #     return "The model could not generate a valid response. Please try again."

    # candidate_content = response.candidates[0].content.parts[0].text
    # return candidate_content if candidate_content else "No valid content returned from the candidate."

# Function to query the SQL database
def read_sql_query(sql):
    try:
        #print(sql)
        conn = create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        #print(sql)
        print(e)
        return f"SQLite error: {e}"


def welcome_page():
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.page = "login"

        st.header("Chat history")
        if st.session_state.qa_list:
            for qa in reversed(st.session_state.qa_list):
                # Display previous questions and answers
                st.markdown(f"**Question:** {qa['question']}")
                st.markdown(f"**Answer:** {qa['answer']}")
                st.markdown("---")
        else:
            st.info("No previous questions yet!")

    st.title("Welcome to the ANJAC AI")
    st.write(f"Hello, {st.session_state.name}!")

    if st.session_state.role:
        # Initialize session state
        if 'qa_list' not in st.session_state:
            st.session_state.qa_list = []
        if 'last_question' not in st.session_state:
            st.session_state.last_question = ""

        role = st.session_state.role
        role_prompt = st.session_state.role_content
        sql_content = st.session_state.sql_content

        # Text input for the question
        question = st.text_input('Input your question:', key='input')

        # Check if question is submitted and handle re-submissions
        if question.strip():
            try:
                st.session_state.last_question = question  # Update last question
                combined_prompt = create_combined_prompt(question, sql_content)
                response = get_gemini_response(combined_prompt)

                # Display the SQL query
                st.write("Generated SQL Query:", response)
                raw_query = response
                formatted_query = raw_query.replace("sql", "").strip("'''").strip()
                single_line_query = " ".join(formatted_query.split()).replace("```", "")

                # Query the database
                data = read_sql_query(single_line_query)

                if isinstance(data, list):
                    # Process data if it's a list
                    st.table(data)
                else:
                    # Process other types of data
                    pass

                # Generate response for the question
                answer = model.generate_content(f"student name :{st.session_state.name} role:{role} prompt:{role_prompt} Answer this question: {question} with results {str(data)}")
                result_text = answer.candidates[0].content.parts[0].text

                # Store the question and answer in session state
                st.session_state.qa_list.append({'question': question, 'answer': result_text})
                write_content({'query': single_line_query, 'data': data, 'question': question, 'answer': result_text})

                # Display the current question and answer
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Answer:** {result_text}")
                st.markdown("---")
            except Exception as e:
                st.error(f"An error occurred: {e}")



# def welcome_page():
#     # Sidebar for logout and chat history
#     with st.sidebar:
#         if st.button("Logout"):
#             st.session_state.authenticated = False
#             st.session_state.page = "login"
#         st.header("Chat history")
#         if st.session_state.qa_list:
#             for qa in reversed(st.session_state.qa_list):
#                 # Display previous questions and answers
#                 st.markdown(f"**Question:** {qa['question']}")
#                 st.markdown(f"**Answer:** {qa['answer']}")
#                 st.markdown("---")
#         else:
#             st.info("No previous questions yet!")

#     # Main content
#     st.title("Welcome to the ANJAC AI")
#     st.write(f"Hello, {st.session_state.name}!")

#     if st.session_state.role:
#         # Initialize session state
#         if 'qa_list' not in st.session_state:
#             st.session_state.qa_list = []
      
#         role = st.session_state.role
#         role_prompt = st.session_state.role_content
#         sql_content = st.session_state.sql_content

#         # Text input for the question
#         question = st.text_input(
#             'Input your question:',
#             key='input'
#         )
#         submit=st.button("Ask question")
    
#         if submit:
#             try:               
#                 # Generate the combined prompt and get a response
#                 combined_prompt = create_combined_prompt(question, st.session_state.sql_content)
#                 response = get_gemini_response(combined_prompt)

#                 # Process the SQL query
#                 formatted_query = response.replace("sql", "").strip("'''").strip()
#                 single_line_query = " ".join(formatted_query.split()).replace("```", "")
#                 data = read_sql_query(single_line_query)

#                 # Generate response for the question
#                 answer = model.generate_content(
#                 f"student name: {st.session_state.name} role: {st.session_state.role} "
#                 f"prompt: {st.session_state.role_content} Answer this question: {question} with results: {str(data)}"
#                 )
#                 result_text = answer.candidates[0].content.parts[0].text

#                 # Store the question and answer in session state
#                 st.session_state.qa_list.append({'question': question, 'answer': result_text})
#                 write_content({'query': single_line_query, 'data': data, 'question': question, 'answer': result_text})

#                 # Display the current question and answer
#                 st.markdown(f"**Question:** {question}")
#                 st.markdown(f"**Answer:** {result_text}")
#                 st.markdown("---")
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")


    

# Main app
def app():
    # Initialize session state attributes
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "page" not in st.session_state:
        st.session_state.page = "guest"
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "multifactor" not in st.session_state:
        st.session_state.multifactor = None
    if "secret" not in st.session_state:
        st.session_state.secret = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "name" not in st.session_state:
        st.session_state.name = None
    if "id" not in st.session_state:
        st.session_state.id = None
    

    # Page navigation
    if st.session_state.page == "guest":
        guest_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "qr_setup":
        qr_setup_page()
    elif st.session_state.page == "otp_verification":
        otp_verification_page()
    elif st.session_state.page == "welcome":
        welcome_page()

# Run the app
if __name__ == "__main__":
    app()
