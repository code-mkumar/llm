import streamlit as st
import sqlite3
import google.generativeai as genai
import os
# Configure Google Gemini API key
genai.configure(api_key='AIzaSyAdY8kZFTZvmaDsFE6r4JF4gekpinMpju8')
model = genai.GenerativeModel('gemini-pro')

# Default prompt (always included)
DEFAULT_PROMPT = '''
You are an expert in converting English questions to SQL queries!

The SQL database has the name STUDENT2 and contains the following tables:

1. Graduate
- id: TEXT (PRIMARY KEY)  
- name: TEXT (NOT NULL)

2. Department
- id: TEXT (PRIMARY KEY)
- name: TEXT (NOT NULL)
- phone_no: TEXT (NOT NULL)
- graduate_id: TEXT (NOT NULL, FOREIGN KEY referencing `graduate(id)` ON DELETE CASCADE ON UPDATE CASCADE)

3. Course
- id: TEXT (PRIMARY KEY)
- name: TEXT (NOT NULL, CHECK values: 'Core', 'Allied', 'Elective', 'Non-Major Elective')

4. User Detail
- id: TEXT (PRIMARY KEY)
- name: TEXT (NOT NULL)
- email: TEXT (NOT NULL)
- gender: TEXT
- role: TEXT (NOT NULL, CHECK values: 'student', 'staff', 'admin')
- phone_no: TEXT (NOT NULL) (Do not retrieve this field)
- password: TEXT (NOT NULL)
- department_id: TEXT (FOREIGN KEY referencing `department(id)` ON DELETE SET NULL ON UPDATE CASCADE)

5. Subject
- id: TEXT (PRIMARY KEY)
- department_id: TEXT (NOT NULL, FOREIGN KEY referencing `department(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- staff_id: TEXT (NOT NULL, FOREIGN KEY referencing `user_detail(id)` ON DELETE SET NULL ON UPDATE CASCADE)
- name: TEXT (NOT NULL)
- course_id: TEXT (NOT NULL, FOREIGN KEY referencing `course(id)` ON DELETE CASCADE ON UPDATE CASCADE)

6. Syllabus
- id: TEXT (PRIMARY KEY)
- subject_id: TEXT (NOT NULL, FOREIGN KEY referencing `subject(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- unit_no: INTEGER (NOT NULL, CHECK between 1 and 5)
- unit_name: TEXT (NOT NULL)
- topics: TEXT (NOT NULL)
- book_id: TEXT (FOREIGN KEY referencing `book(id)` ON DELETE SET NULL ON UPDATE CASCADE)

7. Book
- id: TEXT (PRIMARY KEY)
- subject_id: TEXT (NOT NULL, FOREIGN KEY referencing `subject(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- book_details: TEXT (NOT NULL)

8. Student Mark
- id: INTEGER (PRIMARY KEY AUTOINCREMENT)
- student_id: TEXT (NOT NULL, FOREIGN KEY referencing `user_detail(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- subject_id: TEXT (NOT NULL, FOREIGN KEY referencing `subject(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- department_id: TEXT (NOT NULL, FOREIGN KEY referencing `department(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- internal_mark: REAL (NOT NULL, CHECK between 0 and 40)
- external_mark: REAL (NOT NULL, CHECK between 0 and 60)

9. Attendance
- id: INTEGER (PRIMARY KEY AUTOINCREMENT)
- user_detail_id: TEXT (NOT NULL, FOREIGN KEY referencing `user_detail(id)` ON DELETE CASCADE ON UPDATE CASCADE)
- no_of_days_present: REAL (NOT NULL, CHECK greater than or equal to 0)

Also save all the responses. Get the response from the previous chat too.

---

### *Additional Notes:*

1. *General Data Access:* For all queries that involve *non-sensitive information* (such as subjects, department names), both roles can access the data without restrictions.



'''

# Function to load role-specific prompts
def load_role_prompt(role):
    prompt_file = f"{role}_role.txt"
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r') as file:
            return file.read()
    return f"No role-specific prompt available for {role}."

# Function to combine prompts and user question
def create_combined_prompt(question, role_prompt):
    return f"{DEFAULT_PROMPT}\n\n{role_prompt}\n\n{question}"

# Function to interact with the Google Gemini model
def get_gemini_response(combined_prompt):
    response = model.generate_content(combined_prompt)

    if not response or 'candidates' not in response:
        return "The model could not generate a valid response. Please try again."

    candidate_content = response['candidates'][0].get('content', None)
    return candidate_content if candidate_content else "No valid content returned from the candidate."

# Function to query the SQL database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        return f"SQLite error: {e}"

# Function to retrieve user role
def get_user_role(user_id, pwd):
    try:
        conn = sqlite3.connect('university.db')
        cur = conn.cursor()
        cur.execute("SELECT role FROM user_detail WHERE id = ? AND password = ?", (user_id, pwd))
        role = cur.fetchone()
        conn.close()
        return role[0] if role else None
    except Exception as e:
        return None

# Streamlit App Layout
st.set_page_config(page_title='I can Retrieve Any SQL query')
st.header('Gemini App To Retrieve SQL Data')

# Initialize session state
if 'qa_list' not in st.session_state:
    st.session_state.qa_list = []

# Get User ID and Password
user_id = st.text_input('Enter your User ID for role-based access:')
pwd = st.text_input("Enter your password:", type="password")

if user_id and pwd:
    user_role = get_user_role(user_id, pwd)
    if not user_role:
        st.error("Invalid User ID or Password.")
    else:
        st.success(f"Welcome, your role is '{user_role}'!")
        
        # Retrieve role-based prompt
        role_prompt = load_role_prompt(user_role)

        question = st.text_input('Input your question:', key='input')
        submit = st.button('Ask the question')

        if submit:
            combined_prompt = create_combined_prompt(question, role_prompt)
            response = get_gemini_response(combined_prompt)

            # Display the SQL query
            st.write("Generated SQL Query:", response)

            # Query the database
            data = read_sql_query(response, 'univeristy.db')

            if isinstance(data, list):
                st.write("Query Results:")
                st.table(data)
            else:
                st.write(data)  # Display any errors

            # Generate response for the question and answer
            answer = model.generate_content(f"Answer this question: {question} with results {str(data)}")
            result_text = answer.candidates[0].content.parts[0].text

            # Store the question and answer in session state
            st.session_state.qa_list.append({'question': question, 'answer': result_text})

if st.session_state.qa_list:
    for qa in reversed(st.session_state.qa_list):
        # Display previous questions and answers
        st.write(f"**Question:** {qa['question']}")
        st.write(f"**Answer:** {qa['answer']}")
        st.write("---")
