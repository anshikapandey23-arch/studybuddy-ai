import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
from openai import OpenAI
import pandas as pd
import io

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Study Buddy AI",
    page_icon="🎓",
    layout="wide"
)

# ================= PREMIUM UI =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
}
.big-title {
    font-size: 50px;
    font-weight: 800;
    background: -webkit-linear-gradient(#6366f1,#22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.glass {
    background: rgba(255,255,255,0.06);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(14px);
    margin-bottom: 25px;
}
.notification-panel {
    background: rgba(253, 186, 116, 0.2);
    border-left: 5px solid #f59e42;
    padding: 16px 24px;
    border-radius: 14px;
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🎓 Study Buddy AI</div>', unsafe_allow_html=True)
st.caption("AI-Powered Academic Intelligence Platform for AKTU B.Tech Students")

# ================= LOGIN SYSTEM =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.subheader("🔐 Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Login As", ["Student", "Teacher"])

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Enter valid credentials")

    st.stop()

# ================= SIDEBAR =================
st.sidebar.title("Dashboard")
st.sidebar.write(f"Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

role = st.session_state.role

# ================= AKTU CSE SEMESTER DATA =================
aktu_structure = {
    "1st Semester": ["Mathematics-I", "Physics", "Basic Electrical", "Programming for Problem Solving"],
    "2nd Semester": ["Mathematics-II", "Chemistry", "Electronics", "Data Structures"],
    "3rd Semester": ["OOPS", "Digital Logic", "Discrete Structures", "Technical Communication"],
    "4th Semester": ["DBMS", "Operating Systems", "Automata Theory", "Computer Organization"],
    "5th Semester": ["Computer Networks", "Software Engineering", "Compiler Design", "Web Technology"],
    "6th Semester": ["Machine Learning", "Artificial Intelligence", "Cloud Computing", "Data Mining"],
    "7th Semester": ["Blockchain", "Cyber Security", "IoT", "Open Elective"],
    "8th Semester": ["Major Project", "Internship", "Seminar"]
}

# ============== NOTIFICATIONS (For Student) ==============
def student_notifications():
    notifications = [
        {"type": "assignment", "msg": "⚠️ Pending Assignment: DBMS Assignment 2 due in 2 days."},
        {"type": "test", "msg": "🗓 Upcoming Test: OOPS CT2 on Friday."},
        {"type": "announce", "msg": "⭐ Important: Web Tech seminar on 15th July!"},
    ]
    st.markdown('<div class="notification-panel">', unsafe_allow_html=True)
    for note in notifications:
        if note["type"] == "assignment":
            st.warning(note["msg"])
        elif note["type"] == "test":
            st.info(note["msg"])
        elif note["type"] == "announce":
            st.success(note["msg"])
    st.markdown('</div>', unsafe_allow_html=True)

# ================ SESSION STATE (For Planner etc.) ===============
planner_progress_keys = [
    "Prepare Unit 1", "Prepare Unit 2", "Revise Concepts", "Solve PYQs", "Mock Test", "Final Revision"
]
for key in planner_progress_keys:
    if f"planner_{key}" not in st.session_state:
        st.session_state[f"planner_{key}"] = False

if "pyq_files" not in st.session_state:
    st.session_state.pyq_files = []
if "notes_files" not in st.session_state:
    st.session_state.notes_files = []
if "assignment_files" not in st.session_state:
    st.session_state.assignment_files = []
if "teacher_assignment_records" not in st.session_state:
    st.session_state.teacher_assignment_records = []
if "student_marks_df" not in st.session_state:
    # Simulate student names and marks table with random
    students = ["Aman", "Priya", "Rahul", "Sneha", "Arjun", "Kavya"]
    data = {
        "Student": students,
        "Sessionals": [random.randint(65, 100) for _ in students],
        "Class Test 1": [random.randint(50, 98) for _ in students],
        "Class Test 2": [random.randint(58, 95) for _ in students],
        "Assignments": [random.randint(60, 100) for _ in students],
    }
    st.session_state.student_marks_df = pd.DataFrame(data)

# ================= STUDENT DASHBOARD =================
if role == "Student":

    st.subheader("🎯 Academic Control Center")

    student_notifications()  # Notifications at the top

    branch = st.selectbox("Select Branch", ["Computer Science & Engineering"])
    semester = st.selectbox("Select Semester", list(aktu_structure.keys()))
    subject = st.selectbox("Select Subject", aktu_structure[semester])

    tabs = st.tabs([
        "📘 Learning Hub",
        "📊 Analytics",
        "📅 Academic Planner",
        "🤖 AI Companion",
        "📂 PYQ & Notes"
    ])

    # -------- LEARNING HUB --------
    with tabs[0]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader(f"{subject} - Core Learning Areas")

        units = {
            "Unit 1": "Fundamental Concepts & Theory",
            "Unit 2": "Problem Solving & Applications",
            "Unit 3": "Advanced Mechanisms",
            "Unit 4": "Case Studies & Real Implementations",
            "Unit 5": "Exam-Oriented Review"
        }

        for unit, desc in units.items():
            with st.expander(unit):
                st.write(desc)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- ANALYTICS --------
    with tabs[1]:

        attendance = random.randint(75, 95)
        internal = random.randint(60, 90)
        assignment = random.randint(65, 100)

        col1, col2, col3 = st.columns(3)
        col1.metric("Attendance", f"{attendance}%")
        col2.metric("Internal Score", f"{internal}%")
        col3.metric("Assignments", f"{assignment}%")

        exams = ["CT1", "CT2", "MidSem", "Pre-University"]
        marks = [random.randint(55, 95) for _ in exams]

        fig = px.line(x=exams, y=marks,
                      markers=True,
                      title="Performance Trend",
                      template="plotly_dark")

        fig.update_layout(paper_bgcolor="#0f172a", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

        difficulty = random.randint(50, 90)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=difficulty,
            title={'text': "Subject Difficulty Index"},
            gauge={'axis': {'range': [0,100]}}
        ))

        gauge.update_layout(paper_bgcolor="#0f172a", font_color="white")
        st.plotly_chart(gauge, use_container_width=True)

    # -------- ACADEMIC PLANNER --------
    with tabs[2]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Smart Academic Suggestion")

        # Planner checklist
        st.markdown("### 📅 Structured Study Planner")
        planner_cols = st.columns(3)
        for idx, key in enumerate(planner_progress_keys):
            with planner_cols[idx%3]:
                st.session_state[f"planner_{key}"] = st.checkbox(
                    key, value=st.session_state[f"planner_{key}"]
                )

        st.progress(
            sum(st.session_state[f"planner_{k}"] for k in planner_progress_keys)/len(planner_progress_keys)
        )

        month = datetime.now().month
        st.markdown("---")
        if month in [1, 7]:
            st.info("Mid-Sem approaching → Revise Unit 1 & 2 thoroughly.")
        elif month in [3, 9]:
            st.info("Practical & Internal Submissions due → Finalize records.")
        elif month in [5, 11]:
            st.warning("End Semester Exams → Focus on PYQs & Weak Units.")
        else:
            st.info("Build conceptual clarity and solve previous year questions.")

        st.markdown('</div>', unsafe_allow_html=True)

    # -------- AI COMPANION --------
    with tabs[3]:

        query = st.text_area("Ask for Smart Notes / PYQs / Strategy / Important Topics")

        if st.button("Generate AI Assistance"):

            if api_key and query:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"system","content":"You are an academic AI assistant specialized for AKTU B.Tech CSE syllabus. Provide structured, concise, exam-focused content."},
                        {"role":"user","content":query}
                    ]
                )

                st.markdown('<div class="glass">', unsafe_allow_html=True)
                st.success(response.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.warning("Enter API Key and Question")

    # -------- PYQ & Notes --------
    with tabs[4]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📂 PYQ & Notes")
        left, right = st.columns(2)

        # ------ LEFT: Upload/View PYQ Papers ------
        with left:
            st.markdown("#### 📄 Upload / View PYQ Papers")
            uploaded_pyq = st.file_uploader(
                "Upload Previous Year Question Paper (PDF or TXT)", 
                key="pyq_upload", type=["pdf", "txt"]
            )
            if uploaded_pyq:
                st.session_state.pyq_files.append({
                    "name": uploaded_pyq.name,
                    "content": uploaded_pyq.read(),
                    "type": uploaded_pyq.type
                })
                st.success(f"File '{uploaded_pyq.name}' uploaded.")
            
            # List uploaded files
            if st.session_state.pyq_files:
                st.markdown("##### Uploaded PYQ Papers")
                for i, file in enumerate(st.session_state.pyq_files):
                    st.write(f"{i+1}. {file['name']}")
            
            # Text extraction preview + AI analysis
            selected_idx = st.selectbox(
                "Analyze Uploaded PYQ", options=list(range(len(st.session_state.pyq_files))),
                format_func=lambda x: st.session_state.pyq_files[x]["name"] if st.session_state.pyq_files else "", 
                key="pyq_analyze_select"
            ) if st.session_state.pyq_files else None

            if selected_idx is not None and api_key:
                file = st.session_state.pyq_files[selected_idx]
                # PDF text extraction stub (no OCR here; real-world would use 'pdfminer' etc.)
                if file["type"] == "application/pdf":
                    preview_text = "PDF uploaded. [Text extraction for demo -- Not implemented fully in this stub]"
                else:
                    # Assuming txt
                    try:
                        preview_text = file["content"].decode("utf-8")[:1000]
                    except Exception:
                        preview_text = "(Cannot read as text.)"
                st.text_area("Preview/Extracted PYQ Text", value=preview_text, height=120)
                
                # AI analysis button
                if st.button("AI Analyze PYQ Paper", key="pyq_ai_analyze_btn"):
                    with st.spinner("Analyzing with AI..."):
                        ai_prompt = f"Analyze this AKTU B.Tech previous year paper:\n{preview_text}\n\nList:\n- Frequently asked topics\n- Most repeated units (Unit 1-5)\n- Exam pattern summary\nReturn in JSON with keys 'topics', 'units', 'pattern_summary'."
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are an expert academic paper analyzer for syllabus exam patterns."},
                                {"role": "user", "content": ai_prompt}
                            ]
                        )
                        import json
                        try:
                            payload = json.loads(response.choices[0].message.content)
                        except Exception:
                            payload = {
                                "topics": ["Sample Topic 1", "Sample Topic 2"],
                                "units": {"Unit 1": 4, "Unit 2": 3, "Unit 3": 2, "Unit 4": 1, "Unit 5": 1},
                                "pattern_summary": "Usually 5 sections, short & long answer mix."
                            }

                        st.markdown("**Frequently Asked Topics:**")
                        for topic in payload["topics"]:
                            st.write(f"- {topic}")

                        st.markdown("**Most Repeated Units:**")
                        units_data = payload["units"] if isinstance(payload["units"], dict) else {}
                        if units_data:
                            # Bar Chart
                            fig = px.bar(
                                x=list(units_data.keys()),
                                y=list(units_data.values()),
                                labels={"x":"Unit", "y":"No. of Repetitions"},
                                title="Unit Frequency in PYQ",
                                template="plotly_dark"
                            )
                            fig.update_layout(paper_bgcolor="#0f172a", font_color="white")
                            st.plotly_chart(fig, use_container_width=True)
                        st.markdown("**Exam pattern summary:**")
                        st.info(payload["pattern_summary"])

            elif selected_idx is not None:
                st.info("Enter OpenAI API key to enable AI analysis.")

        # ------ RIGHT: Notes Library ------
        with right:
            st.markdown("#### 📚 Subject Notes Library")
            uploaded_note = st.file_uploader(
                "Upload Your Notes (PDF or TXT)", key="notes_upload", type=["pdf", "txt"]
            )
            if uploaded_note:
                st.session_state.notes_files.append({
                    "name": uploaded_note.name,
                    "content": uploaded_note.read(),
                    "type": uploaded_note.type
                })
                st.success(f"Notes '{uploaded_note.name}' uploaded.")
            # List available notes
            if st.session_state.notes_files:
                st.markdown("##### Your Notes Library")
                for i, file in enumerate(st.session_state.notes_files):
                    st.write(f"{i+1}. {file['name']}")

            # Placeholder: download/view logic can go here in future

        st.markdown('</div>', unsafe_allow_html=True)

# ================= TEACHER DASHBOARD =================
if role == "Teacher":

    st.subheader("👩‍🏫 Faculty Analytics Dashboard")

    semester = st.selectbox("Select Semester", list(aktu_structure.keys()))
    subject = st.selectbox("Select Subject", aktu_structure[semester])

    teacher_tabs = st.tabs([
        "📊 Performance Overview", 
        "📝 Assignment Manager", 
        "🗃 Student Marks Record", 
        "📉 Topic Difficulty Analysis",
        "👤 Student Progress"
    ])

    # --------- Performance Overview (Original) ---------
    with teacher_tabs[0]:
        students = ["Aman", "Priya", "Rahul", "Sneha", "Arjun", "Kavya"]
        scores = [random.randint(60, 95) for _ in students]

        fig = px.bar(x=students, y=scores,
                    title=f"{subject} - Performance Overview",
                    template="plotly_dark")

        fig.update_layout(paper_bgcolor="#0f172a", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        avg_score = sum(scores)/len(scores)
        st.metric("Class Average", f"{int(avg_score)}%")
        st.success("AI Insight: Units with highest error rate require targeted revision session.")

    # --------- Assignment Manager ---------
    with teacher_tabs[1]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📝 Assignment Manager")

        assign_col_1, assign_col_2 = st.columns([2, 1])
        with assign_col_1:
            uploaded_assignment = st.file_uploader("Upload Assignment (PDF or TXT)", key="teacher_ass_upload", type=["pdf", "txt"])
        with assign_col_2:
            assign_sem = st.selectbox("Assign Semester", list(aktu_structure.keys()), key="assign_sem")
            assign_sub = st.selectbox("Assign Subject", aktu_structure[assign_sem], key="assign_sub")

        if uploaded_assignment:
            st.session_state.assignment_files.append({
                "name": uploaded_assignment.name,
                "sem": assign_sem,
                "sub": assign_sub,
                "content": uploaded_assignment.read(),
                "type": uploaded_assignment.type
            })
            st.success(f"Assignment '{uploaded_assignment.name}' uploaded for {assign_sem} - {assign_sub}.")

        if st.session_state.assignment_files:
            st.markdown("##### Uploaded Assignment Records")
            for i, rec in enumerate(st.session_state.assignment_files):
                st.write(f"{i+1}. {rec['name']} | {rec['sem']} - {rec['sub']}")

        st.markdown('</div>', unsafe_allow_html=True)

    # --------- Student Marks Record System ---------
    with teacher_tabs[2]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🗃 Student Marks Record")
        st.info("Edit marks and click outside the cell to update. Data is session-based (demo).")
        edited_df = st.data_editor(
            st.session_state.student_marks_df, 
            use_container_width=True,
            key="editable_marks"
        )
        st.session_state.student_marks_df = edited_df
        st.markdown('</div>', unsafe_allow_html=True)

    # --------- Topic Difficulty Analysis ---------
    with teacher_tabs[3]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("📉 Topic Difficulty Analysis")
        st.markdown("Analyze student marks to determine weak topics.")

        # Simulated mapping for mock analysis
        topic_map = {
            "Sessionals": "Unit 1",
            "Class Test 1": "Unit 2",
            "Class Test 2": "Unit 3",
            "Assignments": "Unit 4",
        }

        # Count students scoring below 60 in each area (demo)
        df = st.session_state.student_marks_df
        low_score_topics = {}
        for test, unit in topic_map.items():
            count = sum(df[test] < 60)
            low_score_topics[unit] = count

        fig = px.pie(
            names=list(low_score_topics.keys()),
            values=list(low_score_topics.values()),
            title="Distribution of Weak Topics",
            template="plotly_dark"
        )
        fig.update_layout(paper_bgcolor="#0f172a", font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        # AI Insight / Weak areas
        weak_units = [k for k, v in low_score_topics.items() if v > 0]
        if weak_units:
            insight_str = (
                f"AI Insight: Majority of students struggled with {', '.join(weak_units)}. "
                "Revisit these during revision sessions."
            )
            st.warning(insight_str)
        else:
            st.success("AI Insight: All units have good performance so far.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --------- Individual Student Progress Dashboard ---------
    with teacher_tabs[4]:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("👤 Individual Student Progress Dashboard")

        df = st.session_state.student_marks_df
        chosen_student = st.selectbox("Select Student", df["Student"].tolist(), key="student_progress_select")

        if chosen_student:
            row = df[df["Student"] == chosen_student]
            tests = ["Class Test 1", "Class Test 2", "Sessionals", "Assignments"]
            student_marks = [int(row[t].values[0]) for t in tests]
            # Line graph for test performance
            fig_line = px.line(x=tests, y=student_marks, markers=True,
                               title=f"{chosen_student} - Test Performance", template="plotly_dark")
            fig_line.update_layout(paper_bgcolor="#0f172a", font_color="white")
            st.plotly_chart(fig_line, use_container_width=True)

            # Bar graph for subject scores (simulated, per unit)
            subj_units = ["Unit 1", "Unit 2", "Unit 3", "Unit 4"]
            subj_scores = [random.randint(60, 100) for _ in subj_units]
            fig_bar = px.bar(x=subj_units, y=subj_scores, labels={"x":"Unit", "y":"Score"},
                             title="Unit-wise Performance (Simulated)", template="plotly_dark")
            fig_bar.update_layout(paper_bgcolor="#0f172a", font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)

            # Overall improvement indicator (trend)
            diffs = [student_marks[i+1]-student_marks[i] for i in range(len(student_marks)-1)]
            if sum(diffs) > 0:
                st.success("Overall Improvement: 👍 Upward performance trend.")
            elif sum(diffs) < 0:
                st.warning("Overall Improvement: 📉 Needs attention! Downward trend.")
            else:
                st.info("Overall Improvement: Stable performance.")

        st.markdown('</div>', unsafe_allow_html=True)