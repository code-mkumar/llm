import sqlite3
import random
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

#totally 9 tables
# Create 'graduate' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS graduate (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
''')

# Create 'department' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS department (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    phone_no TEXT NOT NULL,
    graduate_id TEXT NOT NULL,
    FOREIGN KEY (graduate_id) REFERENCES graduate(id) ON DELETE CASCADE ON UPDATE CASCADE
);
''')

# Create 'course' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS course (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL CHECK(name IN ('Core', 'Allied', 'Elective', 'Non-Major Elective'))
);
''')

# Create 'user_detail' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_detail (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    gender TEXT,
    role TEXT NOT NULL CHECK(role IN ('student', 'staff', 'admin')),
    phone_no TEXT NOT NULL,
    password TEXT NOT NULL,
    department_id TEXT,
    multifactor INTEGER NOT NULL CHECK(multifactor IN(1,0)) DEFAULT 0,
    FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE SET NULL ON UPDATE CASCADE
);
''')

# Create 'subject' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS subject (
    id TEXT PRIMARY KEY,
    department_id TEXT NOT NULL,
    staff_id TEXT NOT NULL,
    name TEXT NOT NULL,
    course_id TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES user_detail(id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE ON UPDATE CASCADE
);
''')

# Create 'syllabus' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS syllabus (
    id TEXT PRIMARY KEY ,
    subject_id TEXT NOT NULL,
    unit_no INTEGER NOT NULL CHECK(unit_no BETWEEN 1 AND 5),
    unit_name TEXT NOT NULL,
    topics TEXT NOT NULL,
    book_id TEXT,
    FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE SET NULL ON UPDATE CASCADE
);
''')

# Create 'book' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS book (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL,
    book_details TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE ON UPDATE CASCADE
    
);
''')

# Create 'student_mark' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student_mark (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    department_id TEXT NOT NULL,
    internal_mark REAL NOT NULL CHECK(internal_mark BETWEEN 0 AND 40),
    external_mark REAL NOT NULL CHECK(external_mark BETWEEN 0 AND 60),
    FOREIGN KEY (student_id) REFERENCES user_detail(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subject(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE CASCADE ON UPDATE CASCADE
);
''')

# Create 'attendance' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_detail_id TEXT NOT NULL,
    no_of_days_present REAL NOT NULL CHECK(no_of_days_present >= 0),
    FOREIGN KEY (user_detail_id) REFERENCES user_detail(id) ON DELETE CASCADE ON UPDATE CASCADE
);
''')

# Adding indexes for optimization
cursor.execute('CREATE INDEX IF NOT EXISTS idx_department_graduate_id ON department(graduate_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_detail_department_id ON user_detail(department_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_subject_department_id ON subject(department_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_subject_course_id ON subject(course_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_syllabus_subject_id ON syllabus(subject_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_mark_subject_id ON student_mark(subject_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_mark_department_id ON student_mark(department_id);')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_user_detail_id ON attendance(user_detail_id);')





# Insert dummy data

# Graduate data
graduates = [
    ('UG', 'Undergraduate'),
    ('PG', 'Postgraduate'),
    ('A', 'admin')
]



# Department data
departments = [
    ('CS', 'Computer Science', '123-456-7890', 'UG'),
    ('EE', 'Electrical Engineering', '987-654-3210', 'UG'),
    ('ME', 'Mechanical Engineering', '555-666-7777', 'PG'),
    ('CE', 'Civil Engineering', '444-555-6666', 'PG'),
    ('IT', 'Information Technology', '777-888-9999', 'UG'),
    ('AA','Administration','1234567890' ,'A')
]



# Course data
courses = [
    ('C1', 'Core'),
    ('C2', 'Allied'),
    ('C3', 'Elective'),
    ('C4', 'Non-Major Elective'),
    
]


books = [
    ('B1', '20UCS101', 'Data Structures by Mark Allen Weiss, 2nd Edition'),
    ('B2', '20UAS102', 'Operating Systems Concepts by Silberschatz et al., 10th Edition'),
    ('B3', '20UES103', 'Machine Learning by Tom M. Mitchell, 1st Edition'),
    ('B4', '20UCE101', 'Electrical Circuits by James W. Nilsson, 10th Edition'),
    ('B5', '20UAE102', 'Control Systems by Katsuhiko Ogata, 5th Edition'),
    ('B6', '20UNE103', 'Electromagnetic Fields by Sadiku, 6th Edition'),
    ('B7', '20PCM101', 'Thermodynamics by Yunus Çengel, 8th Edition'),
    ('B8', '20PAM102', 'Fluid Mechanics by Frank M. White, 7th Edition'),
    ('B9', '20PEM103', 'Engineering Mechanics by R.C. Hibbeler, 14th Edition'),
    ('B10', '20PCC101', 'Structural Analysis by R.C. Hibbeler, 9th Edition'),
    ('B11', '20PAC102', 'Geotechnical Engineering by Braja M. Das, 8th Edition'),
    ('B12', '20PEC103', 'Transportation Engineering by Khanna and Justo, 11th Edition'),
    ('B13', '20UCT101', 'Computer Networks by Andrew S. Tanenbaum, 5th Edition'),
    ('B14', '20UAT102', 'Database Management Systems by Raghu Ramakrishnan, 3rd Edition'),
    ('B15', '20UNT103', 'Web Development by Robin Nixon, 5th Edition')
]


# Syllabus data
syllabus = [
    # Data Structures
    ('SYUCS01', '20UCS101', 1, 'Foundations of Data Structures', 'Introduction to Data Structures, Arrays, and Linked Lists', 'B1'),
    ('SYUCS02', '20UCS101', 2, 'Efficient Storage and Retrieval', 'Stacks, Queues, and Hashing Techniques', 'B1'),
    ('SYUCS03', '20UCS101', 3, 'Hierarchical and Graph-Based Structures', 'Trees, Graphs, and Advanced Data Structures', 'B1'),

    # Operating Systems
    ('SYUAS01', '20UAS102', 1, 'Understanding Process Management', 'Basics of Operating Systems, Process Management', 'B2'),
    ('SYUAS02', '20UAS102', 2, 'Memory and File Systems', 'Memory Management, File Systems, and Scheduling', 'B2'),
    ('SYUAS03', '20UAS102', 3, 'Advanced Topics in OS', 'Security, Virtualization, and Advanced OS Topics', 'B2'),

    # Machine Learning
    ('SYUES01', '20UES103', 1, 'Introduction to ML Concepts', 'Introduction to Machine Learning, Supervised Learning', 'B3'),
    ('SYUES02', '20UES103', 2, 'Exploring Unsupervised Learning', 'Unsupervised Learning, Clustering, and Dimensionality Reduction', 'B3'),
    ('SYUES03', '20UES103', 3, 'Deep Learning and Beyond', 'Reinforcement Learning and Neural Networks', 'B3'),

    # Electrical Circuits
    ('SYUCE01', '20UCE101', 1, 'Circuit Basics and Theorems', 'Basics of Electrical Circuits, Ohm’s Law, and KVL', 'B4'),
    ('SYUCE02', '20UCE101', 2, 'AC Analysis and Power Systems', 'AC Circuits, Transformers, and Power Systems', 'B4'),
    ('SYUCE03', '20UCE101', 3, 'Three-Phase and Network Analysis', 'Three-Phase Circuits and Circuit Analysis Techniques', 'B4'),

    # Control Systems
    ('SYUAE01', '20UAE102', 1, 'Modeling Control Systems', 'Introduction to Control Systems, Block Diagrams', 'B5'),
    ('SYUAE02', '20UAE102', 2, 'Analyzing System Stability', 'Time Domain Analysis, Stability, and Root Locus', 'B5'),
    ('SYUAE03', '20UAE102', 3, 'Frequency Response Techniques', 'Frequency Domain Analysis and Compensator Design', 'B5'),

    # Electromagnetic Fields
    ('SYUNE01', '20UNE103', 1, 'Fundamentals of Electromagnetics', 'Basics of Electromagnetic Fields, Gauss’s Law', 'B6'),
    ('SYUNE02', '20UNE103', 2, 'Applications of Maxwell’s Equations', 'Maxwell’s Equations and Applications', 'B6'),
    ('SYUNE03', '20UNE103', 3, 'Wave Propagation Phenomena', 'Wave Propagation and Electromagnetic Spectrum', 'B6'),

    # Thermodynamics
    ('SYPCM01', '20PCM101', 1, 'Principles of Thermodynamics', 'Introduction to Thermodynamics, Laws of Thermodynamics', 'B7'),
    ('SYPCM02', '20PCM101', 2, 'Thermal Energy Conversion', 'Thermodynamic Cycles and Applications', 'B7'),
    ('SYPCM03', '20PCM101', 3, 'Heat Transfer Mechanisms', 'Heat Transfer and Energy Systems', 'B7'),

    # Fluid Mechanics
    ('SYPAM01', '20PAM102', 1, 'Basics of Fluid Mechanics', 'Fluid Properties and Fluid Statics', 'B8'),
    ('SYPAM02', '20PAM102', 2, 'Flow Dynamics and Bernoulli’s Principles', 'Fluid Dynamics and Bernoulli’s Equation', 'B8'),
    ('SYPAM03', '20PAM102', 3, 'Pipe Flow and Open Channels', 'Flow Through Pipes and Open Channel Flow', 'B8'),

    # Engineering Mechanics
    ('SYPEM01', '20PEM103', 1, 'Statics and Force Systems', 'Introduction to Engineering Mechanics, Statics', 'B9'),
    ('SYPEM02', '20PEM103', 2, 'Kinetics of Rigid Bodies', 'Dynamics and Kinematics of Rigid Bodies', 'B9'),
    ('SYPEM03', '20PEM103', 3, 'Mechanical Vibrations and Applications', 'Mechanical Vibrations and Applications', 'B9'),

    # Structural Analysis
    ('SYPCC01', '20PCC101', 1, 'Load Assessment and Analysis', 'Basics of Structural Analysis, Load Analysis', 'B10'),
    ('SYPCC02', '20PCC101', 2, 'Internal Forces in Structures', 'Shear Force and Bending Moment Diagrams', 'B10'),
    ('SYPCC03', '20PCC101', 3, 'Deflections and Stability', 'Deflection of Beams and Frames', 'B10'),

    # Geotechnical Engineering
    ('SYPAC01', '20PAC102', 1, 'Soil Behavior and Properties', 'Introduction to Soil Mechanics', 'B11'),
    ('SYPAC02', '20PAC102', 2, 'Consolidation and Shear Strength', 'Soil Strength and Consolidation', 'B11'),
    ('SYPAC03', '20PAC102', 3, 'Foundation Design Techniques', 'Foundation Design and Stability Analysis', 'B11'),

    # Transportation Engineering
    ('SYPEC01', '20PEC103', 1, 'Planning and Design of Highways', 'Highway Planning and Design', 'B12'),
    ('SYPEC02', '20PEC103', 2, 'Traffic Management Systems', 'Traffic Engineering and Management', 'B12'),
    ('SYPEC03', '20PEC103', 3, 'Pavement Analysis and Maintenance', 'Pavement Materials and Maintenance', 'B12'),

    # Computer Networks
    ('SYUCT01', '20UCT101', 1, 'Introduction to Networking', 'Network Fundamentals, OSI Model', 'B13'),
    ('SYUCT02', '20UCT101', 2, 'Protocol Analysis and Design', 'Transport Layer and Network Layer Protocols', 'B13'),
    ('SYUCT03', '20UCT101', 3, 'Wireless and Secure Networks', 'Wireless Networks and Security', 'B13'),

    # Database Management Systems
    ('SYUAT01', '20UAT102', 1, 'Database Fundamentals', 'Introduction to Databases, ER Modeling', 'B14'),
    ('SYUAT02', '20UAT102', 2, 'Query Design and Optimization', 'Relational Algebra, SQL, and Transactions', 'B14'),
    ('SYUAT03', '20UAT102', 3, 'Advanced Database Techniques', 'Indexing, Query Optimization, and Security', 'B14'),

    # Web Development
    ('SYUNT01', '20UNT103', 1, 'Basics of Web Design', 'HTML, CSS, and JavaScript Basics', 'B15'),
    ('SYUNT02', '20UNT103', 2, 'Responsive and Dynamic Websites', 'Web Frameworks and Responsive Design', 'B15'),
    ('SYUNT03', '20UNT103', 3, 'Backend and Deployment Strategies', 'Backend Development and Deployment', 'B15')
]






# Subject data
subjects = [
    ('20UCS101', 'CS', 'STCS1', 'Data Structures', 'C1'),
    ('20UAS102', 'CS', 'STCS2', 'Operating Systems', 'C2'),
    ('20UES103', 'CS', 'STCS3', 'Machine Learning', 'C3'),
    ('20UCE101', 'EE', 'STEE1', 'Electrical Circuits', 'C1'),
    ('20UAE102', 'EE', 'STEE2', 'Control Systems', 'C2'),
    ('20UNE103', 'EE', 'STEE3', 'Electromagnetic Fields', 'C4'),
    ('20PCM101', 'ME', 'STME1', 'Thermodynamics', 'C1'),
    ('20PAM102', 'ME', 'STME2', 'Fluid Mechanics', 'C2'),
    ('20PEM103', 'ME', 'STME3', 'Engineering Mechanics', 'C3'),
    ('20PCC101', 'CE', 'STCE1', 'Structural Analysis', 'C1'),
    ('20PAC102', 'CE', 'STCE2', 'Geotechnical Engineering', 'C2'),
    ('20PEC103', 'CE', 'STCE3', 'Transportation Engineering', 'C3'),
    ('20UCT101', 'IT', 'STIT1', 'Computer Networks', 'C1'),
    ('20UAT102', 'IT', 'STIT2', 'Database Management Systems', 'C2'),
    ('20UNT103', 'IT', 'STIT3', 'Web Development', 'C4')
]




# cursor.execute("PRAGMA foreign_key_check;")
# violations = cursor.fetchall()
# print("Foreign Key Violations:", violations)

cursor.executemany('''
INSERT INTO graduate (id, name) 
VALUES (?, ?)
''', graduates)


cursor.executemany('''
INSERT INTO course (id, name) 
VALUES (?, ?)
''', courses)



cursor.executemany('''
INSERT INTO department (id, name, phone_no, graduate_id) 
VALUES (?, ?, ?, ?)
''', departments)



cursor.executemany('''
INSERT INTO user_detail (id, name, department_id, email, gender,phone_no, password, role)
VALUES (?, ?, ?, ?, ?, ?, ?,?)
''', [
    ('STCS1', 'John Doe', 'CS', '22us23@anjaconline.org', 'male','1234567890', 'pass_staff', 'staff'),
    ('STCS2', 'Malathi', 'CS', '22us23@anjaconline.org', 'female','1234567891', 'pass_staff', 'staff'),
    ('STCS3', 'Alice Brown', 'CS', '22us23@anjaconline.org','male', '1234567892', 'pass_staff', 'staff'),
    
    ('STEE1', 'Michael Green', 'EE', '22us23@anjaconline.org', 'male','9876543210', 'pass_staff', 'staff'),
    ('STEE2', 'Sarah Miller', 'EE', '22us23@anjaconline.org', 'male','9876543211', 'pass_staff', 'staff'),
    ('STEE3', 'revathi', 'EE', '22us23@anjaconline.org','female', '9876543212', 'pass_staff', 'staff'),
   

    ('STME1', 'James Clark', 'ME', '22us23@anjaconline.org','male', '5556667770', 'pass_staff', 'staff'),
    ('STME2', 'Malar', 'ME', '22us23@anjaconline.org','female', '5556667771', 'pass_staff', 'staff'),
    ('STME3', 'Henry Lewis', 'ME', '22us23@anjaconline.org','male', '5556667772', 'pass_staff', 'staff'),
   
    ('STCE1', 'Abirami', 'CE', '22us23@anjaconline.org', 'female','4445556660', 'pass_staff', 'staff'),
    ('STCE2', 'Elizabeth Hall', 'CE', '22us23@anjaconline.org', 'male','4445556661', 'pass_staff', 'staff'),
    ('STCE3', 'Christopher Allen', 'CE', '22us23@anjaconline.org', 'male','4445556662', 'pass_staff', 'staff'),
   
    ('STIT1', 'William King', 'IT', '22us23@anjaconline.org', 'male','7778889990', 'pass_staff', 'staff'),
    ('STIT2', 'Jessica Scott', 'IT', '22us23@anjaconline.org','male', '7778889991', 'pass_staff', 'staff'),
    ('STIT3', 'Devi', 'IT', '22us23@anjaconline.org','female', '7778889992', 'pass_staff', 'staff'),

])
cursor.executemany('''
INSERT INTO user_detail (id, name, department_id, email, gender,phone_no, password, role)
VALUES (?, ?, ?, ?, ?, ?, ?,?)
''', [
    
     ('A001', 'Admin1', 'AA', '22us25@anjaconline.org', '7778889990','male', 'pass_admin', 'admin'),
    ('A002', 'Admin2', 'AA', '22us25@anjaconline.org', '7778889991', 'female','pass_admin', 'admin'),
    ('A003', 'Admin3', 'AA', '22us25@anjaconline.org', '7778889992', 'female','pass_admin', 'admin'),

])


cursor.executemany('''
INSERT INTO subject (id, department_id, staff_id, name, course_id) 
VALUES (?, ?, ?, ?, ?)
''', subjects)

cursor.executemany('''
INSERT INTO book (id, subject_id, book_details) 
VALUES (?, ?, ?)
''', books)


cursor.executemany('''
INSERT INTO syllabus (id, subject_id, unit_no, unit_name, topics, book_id) 
VALUES (?, ?, ?, ?, ?, ?)
''', syllabus)

students = [
    ('SCS1', 'Alice Smith', 'CS', 'alice.smith@example.com', 'male','9876543210', 'password', 'CS'),
    ('SCS2', 'Abirami', 'CS', 'abirami.c@anjaconline.org', 'female','9876543211', 'password', 'CS'),
    ('SCS3', 'Charlie Davis', 'CS', 'charlie.davis@example.com','male', '9876543212', 'password', 'CS'),
    ('SCS4', 'Dhivya', 'CS', 'diana.moore@example.com', 'female','9876543213', 'password', 'CS'),
    ('SCS5', 'Ethan Taylor', 'CS', 'ethan.taylor@example.com', 'male','9876543214', 'password', 'CS'),

    ('SEE1', 'Faith White', 'EE', 'faith.white@example.com','male', '5556667770', 'password', 'EE'),
    ('SEE2', 'George Harris', 'EE', 'abirami.c@anjaconline.org', 'male','5556667771', 'password', 'EE'),
    ('SEE3', 'mathi', 'EE', 'helen.martin@example.com', 'female','5556667772', 'password', 'EE'),
    ('SEE4', 'Ian Thompson', 'EE', 'ian.thompson@example.com','male', '5556667773', 'password', 'EE'),
    ('SEE5', 'Jackie Wilson', 'EE', 'jackie.wilson@example.com', 'male','5556667774', 'password', 'EE'),

    ('SME1', 'priya', 'ME', 'liam.lee@example.com', 'female','4445556660', 'password', 'ME'),
    ('SME2', 'Mia Clark', 'ME', 'mia.clark@example.com', 'male','4445556661', 'password', 'ME'),
    ('SME3', 'Nathan Adams', 'ME', 'nathan.adams@example.com', 'male','4445556662', 'password', 'ME'),
    ('SME4', 'Olivia Robinson', 'ME', 'olivia.robinson@example.com','male', '4445556663', 'password', 'ME'),
    ('SME5', 'muthu', 'ME', 'paul.lewis@example.com','female', '4445556664', 'password', 'ME'),

    ('SCE1', 'Quinn Young', 'CE', 'quinn.young@example.com','male', '3334445550', 'password', 'CE'),
    ('SCE2', 'rani', 'CE', 'rachel.walker@example.com','female', '3334445551', 'password', 'CE'),
    ('SCE3', 'manju', 'CE', 'samuel.king@example.com', 'female','3334445552', 'password', 'CE'),
    ('SCE4', 'renu', 'CE', 'tina.scott@example.com', 'female','3334445553', 'password', 'CE'),
    ('SCE5', 'Ursula Nelson', 'CE', 'ursula.nelson@example.com', 'male','3334445554', 'password', 'CE'),

    ('SIT1', 'mariselvi', 'IT', 'victor.green@example.com','female', '7778889990', 'password', 'IT'),
    ('SIT2', 'meena', 'IT', 'wendy.adams@example.com','female', '7778889991', 'password', 'IT'),
    ('SIT3', 'sharu', 'IT', 'xander.nelson@example.com','female', '7778889992', 'password', 'IT'),
    ('SIT4', 'Yara Perez', 'IT', 'yara.perez@example.com','male', '7778889993', 'password', 'IT'),
    ('SIT5', 'Zane Garcia', 'IT', 'zane.garcia@example.com', 'male','7778889994', 'password', 'IT')
]

# Insert student data into user_detail table (assuming a student table or similar exists)
cursor.executemany('''
INSERT INTO user_detail (id, name, department_id, email,gender, phone_no, password, role)
VALUES (?, ?, ?, ?, ?, ?, ?,?)
''', [(student_id, name, department, email, gender,phone, password, 'student') for student_id, name, department, email, gender,phone, password, department in students])




cursor.executemany('''
INSERT INTO student_mark (student_id, subject_id, department_id, internal_mark, external_mark) 
VALUES (?, ?, ?, ?, ?)
''', [
    # ('SCS1', '20UCS101', 'CS', 40, 60),
    # ('SCS2', '20UCS101', 'CS', 35, 55),
    # CS Department (Core: P'C'C103, Allied: P'A'C102, Elective: P'E'C103)
    ( 'SCS1', '20UCS101', 'CS', 30, 35),  # Core: Data Structures
    ( 'SCS1', '20UAE102', 'EE', 32, 38),  # Allied: Control Systems
    ('SCS1', '20UNT103', 'IT', 35, 42),  # Elective: Electrical Circuits

    ( 'SCS2', '20UCS101', 'CS', 31, 36),  # Core: Data Structures
    ( 'SCS2', '20UAE102', 'EE', 33, 39),  # Allied: Fluid Mechanics
    ( 'SCS2', '20UNE103', 'EE', 38, 45),  # Elective: Structural Analysis

    ( 'SCS3', '20UCS101', 'CS', 36, 40),  # Core: Data Structures
    ( 'SCS3', '20UAE102', 'EE', 34, 40),  # Allied: Web Development
    ( 'SCS3', '20UNT103', 'IT', 37, 43),  # Elective: Transportation Engineering

    ( 'SCS4', '20UCS101', 'CS', 38, 34),  # Core: Data Structures
    ( 'SCS4', '20UAE102', 'EE', 30, 36),  # Allied: Thermodynamics
    ( 'SCS4', '20UNE103', 'EE', 37, 43),  # Elective: Structural Analysis

    ( 'SCS5', '20UCS101', 'CS', 33, 39),  # Core: Data Structures
    ('SCS5', '20UAE102', 'EE', 31, 37),  # Allied: Web Development
    ( 'SCS5', '20UNT103', 'IT', 30, 35),  # Elective: Fluid Mechanics

    # EE Department (Core: P'C'C103, Allied: P'A'C102, Elective: P'E'C103)
    ( 'SEE1', '20UCE101', 'EE', 35, 42),  # Core: Electrical Circuits
    ( 'SEE1', '20UAT102', 'IT', 36, 44),  # Allied: Thermodynamics
    ( 'SEE1', '20UES103', 'CS', 31, 37),  # Elective: Data Structures

    ( 'SEE2', '20UCE101', 'EE', 32, 38),  # Core: Electrical Circuits
    ( 'SEE2', '20UAT102', 'IT', 34, 40),  # Allied: Data Structures
    ( 'SEE2', '20UES103', 'CS', 30, 36),  # Elective: Web Development
    ( 'SEE3', '20UCE101', 'EE', 36, 42),  # Core: Electrical Circuits
    ( 'SEE3', '20UAT102', 'IT', 35, 41),  # Allied: Engineering Mechanics
    ( 'SEE3', '20UES103', 'CS', 38, 44),  # Elective: Structural Analysis

    ( 'SEE4', '20UCE101', 'EE', 38, 45),  # Core: Electrical Circuits
    ( 'SEE4', '20UAT102', 'IT', 35, 42),  # Allied: Fluid Mechanics
    ( 'SEE4', '20UES103', 'CS', 32, 38),  # Elective: Data Structures
    ( 'SEE5', '20UCE101', 'EE', 31, 37),  # Core: Electrical Circuits
    ( 'SEE5', '20UAT102', 'IT', 34, 40),  # Allied: Web Development
    ( 'SEE5', '20UES103', 'CS', 36, 43),  # Elective: Thermodynamics

    # ME Department (Core: P'C'C103, Allied: P'A'C102, Elective: P'E'C103)
    ( 'SME1', '20PCM101', 'ME', 35, 41),  # Core: Thermodynamics
    ( 'SME1', '20PAC102', 'CE', 37, 43),  # Allied: Data Structures
    ( 'SME1', '20PEC103', 'CE', 36, 42),  # Elective: Web Development

    ( 'SME2', '20PCM101', 'ME', 38, 44),  # Core: Thermodynamics
    ( 'SME2', '20PAC102', 'CE', 32, 38),  # Allied: Data Structures
    ( 'SME2', '20PEC103', 'CE', 33, 39),  # Elective: Web Development

    ( 'SME3', '20PCM101', 'ME', 32, 38),  # Core: Thermodynamics
    ( 'SME3', '20PAC102', 'CE', 35, 40),  # Allied: Web Development
    ( 'SME3', '20PEC103', 'CE', 36, 42),  # Elective: Control Systems

    ( 'SME4', '20PCM101', 'ME', 34, 40),  # Core: Thermodynamics
    ( 'SME4', '20PAC102', 'CE', 32, 38),  # Allied: Data Structures
    ( 'SME4', '20PEC103', 'CE', 37, 43),  # Elective: Web Development

    ( 'SME5', '20PCM101', 'ME', 30, 36),  # Core: Thermodynamics
    ( 'SME5', '20PAC102', 'CE', 31, 37),  # Allied: Control Systems
    ( 'SME5', '20PEC103', 'CE', 34, 40),  # Elective: Web Development

    # CE Department (Core: P'C'C103, Allied: P'A'C102, Elective: P'E'C103)
    ( 'SCE1', '20PCC101', 'CE', 35, 41),  # Core: Structural Analysis
    ( 'SCE1', '20PAM102', 'ME', 37, 43),  # Allied: Web Development
    ( 'SCE1', '20PEM103', 'ME', 36, 42),  # Elective: Engineering Mechanics

    ( 'SCE2', '20PCC101', 'CE', 34, 40),  # Core: Structural Analysis
    ( 'SCE2', '20PAM102', 'ME', 35, 41),  # Allied: Thermodynamics
    ( 'SCE2', '20PEM103', 'ME', 38, 45),  # Elective: Control Systems

    ( 'SCE3', '20PCC101', 'CE', 33, 40),  # Core: Structural Analysis
    ( 'SCE3', '20PAM102', 'ME', 34, 41),  # Allied: Web Development
    ( 'SCE3', '20PEM103', 'ME', 37, 43),  # Elective: Fluid Mechanics

    ( 'SCE4', '20PCC101', 'CE', 32, 38),  # Core: Structural Analysis
    ( 'SCE4', '20PAM102', 'ME', 33, 40),  # Allied: Thermodynamics
    ( 'SCE4', '20PEM103', 'ME', 36, 42),  # Elective: Data Structures

    ( 'SCE5', '20PCC101', 'CE', 34, 40),  # Core: Structural Analysis
    ( 'SCE5', '20PAM102', 'ME', 35, 42),  # Allied: Web Development
    ( 'SCE5', '20PEM103', 'ME', 37, 43),   # Elective: Thermodynamics


    # IT Department (Core: P'C'C103, Allied: P'A'C102, Elective: P'E'C103)
    ( 'SIT1', '20UCT101', 'IT', 35, 41),  # Core: Structural Analysis
    ( 'SIT1', '20UAS102', 'CS', 37, 43),  # Allied: Web Development
    ( 'SIT1', '20UNE103', 'EE', 36, 42),  # Elective: Engineering Mechanics

    ( 'SIT2', '20UCT101', 'IT', 34, 40),  # Core: Structural Analysis
    ( 'SIT2', '20UAS102', 'CS', 35, 41),  # Allied: Thermodynamics
    ( 'SIT2', '20UNE103', 'EE', 38, 45),  # Elective: Control Systems

    ( 'SIT3', '20UCT101', 'IT', 33, 40),  # Core: Structural Analysis
    ( 'SIT3', '20UAS102', 'CS', 34, 41),  # Allied: Web Development
    ( 'SIT3', '20UNE103', 'EE', 37, 43),  # Elective: Fluid Mechanics

    ( 'SIT4', '20UCT101', 'IT', 32, 38),  # Core: Structural Analysis
    ( 'SIT4', '20UAS102', 'CS', 33, 40),  # Allied: Thermodynamics
    ( 'SIT4', '20UNE103', 'EE', 36, 42),  # Elective: Data Structures

    ( 'SIT5', '20UCT101', 'IT', 34, 40),  # Core: Structural Analysis
    ( 'SIT5', '20UAS102', 'CS', 35, 42),  # Allied: Web Development
    ( 'SIT5', '20UNE103', 'EE', 37, 43)   # Elective: Thermodynamics
])
attendance_data = [
    # Student Attendance (25 students)
    ( 'SCS1', random.randint(10, 30)),  # Student 1
    ( 'SCS2', random.randint(10, 30)),  # Student 2
    ( 'SCS3', random.randint(10, 30)),  # Student 3
    ( 'SCS4', random.randint(10, 30)),  # Student 4
    ( 'SCS5', random.randint(10, 30)),  # Student 5
    ( 'SEE1', random.randint(10, 30)),  # Student 6
    ( 'SEE2', random.randint(10, 30)),  # Student 7
    ( 'SEE3', random.randint(10, 30)),  # Student 8
    ( 'SEE4', random.randint(10, 30)),  # Student 9
    ( 'SEE5', random.randint(10, 30)), # Student 10
    ( 'SME1', random.randint(10, 30)), # Student 11
    ('SME2', random.randint(10, 30)), # Student 12
    ( 'SME3', random.randint(10, 30)), # Student 13
    ( 'SME4', random.randint(10, 30)), # Student 14
    ( 'SME5', random.randint(10, 30)), # Student 15
    ( 'SCE1', random.randint(10, 30)), # Student 16
    ( 'SCE2', random.randint(10, 30)), # Student 17
    ('SCE3', random.randint(10, 30)), # Student 18
    ( 'SCE4', random.randint(10, 30)), # Student 19
    ( 'SCE5', random.randint(10, 30)), # Student 20
    ( 'SIT1', random.randint(10, 30)), # Student 21
    ('SIT2', random.randint(10, 30)), # Student 22
    ( 'SIT3', random.randint(10, 30)), # Student 23
    ('SIT4', random.randint(10, 30)), # Student 24
    ( 'SIT5', random.randint(10, 30)), # Student 25

    # Staff Attendance (20 staff members)
    ( 'STCS1', random.randint(20, 30)), # Staff 1
    ( 'STCS2', random.randint(20, 30)), # Staff 2
    ( 'STCS3', random.randint(20, 30)), # Staff 3
    ( 'STEE1', random.randint(20, 30)), # Staff 4
    ( 'STEE2', random.randint(20, 30)), # Staff 5
    ( 'STEE3', random.randint(20, 30)), # Staff 6
    ( 'STME1', random.randint(20, 30)), # Staff 7
    ( 'STME2', random.randint(20, 30)), # Staff 8
    ( 'STME3', random.randint(20, 30)), # Staff 9
    ('STCE1', random.randint(20, 30)), # Staff 10
    ( 'STCE2', random.randint(20, 30)), # Staff 11
    ( 'STCE3', random.randint(20, 30)), # Staff 12
    ( 'STIT1', random.randint(20, 30)), # Staff 13
    ( 'STIT2', random.randint(20, 30)), # Staff 14
    ('STIT3', random.randint(20, 30)), # Staff 15

    # Admin Attendance (3 admins)
    ( 'A001', random.randint(15, 30)), # Admin 1
    ('A002', random.randint(15, 30)), # Admin 2
    ( 'A003', random.randint(15, 30))  # Admin 3
]

# Insert the attendance data into the attendance table
cursor.executemany('''
INSERT INTO attendance ( user_detail_id, no_of_days_present)
VALUES (?, ?)
''', attendance_data)

# Commit and close the connection
conn.commit()
conn.close()

print("Dummy data inserted successfully!")
