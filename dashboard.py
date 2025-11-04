import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import date
import streamlit.components.v1 as components
# import google.generativeai as genai
import textwrap
import json


# Set page configuration
# 🔐 Gemini AI API Setup# 🔐 Gemini AI API Setup
# api_key = st.secrets["GEMINI_API_KEY"]
# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("models/gemini-1.5-flash-8b")
# Import necessary libraries

# Set up Streamlit page configuration
st.set_page_config(page_title="AI Task Management", layout="wide", page_icon="📘")

# Custom CSS for animations and styling
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .animated-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        background: linear-gradient(90deg, #ff512f, #dd2476, #ff512f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 4s infinite linear;
    }
    @keyframes glow {
        0% { background-position: -400px; }
        100% { background-position: 400px; }
    }
    .stButton > button {
        background-color: #0072ff;
        color: white;
        border-radius: 12px;
        padding: 0.5em 1em;
        font-weight: bold;
        box-shadow: 0 4px 14px rgba(0, 114, 255, 0.4);
        transition: 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #0052cc;
        transform: scale(1.05);
    }
    .block-style {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Animated title
st.markdown("<div class='animated-title'>🧠 AI-Powered Task Management Dashboard</div><br>", unsafe_allow_html=True)



# 🔽 FILE PATHS
task_file = "tasks_cleaned.csv"
user_file = "user_data.csv"
prediction_file = "model_predictions.csv"

# 🔽 CUSTOM CSS
st.markdown("""
<style>
.expander-header {
    font-weight: bold;
    font-size: 18px;
    color: #0072ff;
}
.stTextInput > div > input,
.stDateInput > div > input,
.stSelectbox > div > div,
.stButton > button {
    border-radius: 10px;
}
.stButton > button {
    background-color: #0072ff;
    color: white;
    font-weight: bold;
    transition: 0.2s ease-in-out;
}
.stButton > button:hover {
    background-color: #0052cc;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# 🔽 LOAD DATA
def load_tasks():
    if os.path.exists(task_file):
        return pd.read_csv(task_file)
    return pd.DataFrame(columns=["TaskID", "Description", "Deadline", "AssignedTo", "Priority", "Status"])

def save_tasks(df):
    df.to_csv(task_file, index=False)

# Session state to control expanders
if "expanded" not in st.session_state:
    st.session_state["expanded"] = None

def toggle_expander(name):
    st.session_state["expanded"] = name if st.session_state["expanded"] != name else None

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add Task", use_container_width=True):
        toggle_expander("add")
with col2:
    if st.button("🔄 Update Task Status" , use_container_width=True):
        toggle_expander("update")
with col3:
    if st.button("🗑️ Delete Task", use_container_width=True):
        toggle_expander("delete")

# 🔽 EXPANDER: ADD NEW TASK
if st.session_state["expanded"] == "add":
    with st.expander("➕ Add New Task", expanded=True):
        # 🔽 Paste your FULL "Add Task" form code here
        st.markdown("<div class='expander-header'>Enter new task details:</div>", unsafe_allow_html=True)
        with st.form("add_task_form"):
            col1, col2 = st.columns(2)
            with col1:
                description = st.text_input("📝 Task Description")
                deadline = st.date_input("📅 Deadline")
            with col2:
                assigned_to = st.text_input("👤 Assigned To")
            status = st.selectbox("📌 Status", ["Pending", "In Progress", "Completed"])
            submit_add = st.form_submit_button("Add Task")

            if submit_add:
                if description.strip() == "":
                    st.warning("⚠️ Description is required.")
                elif deadline < date.today():
                    st.warning("⚠️ Deadline cannot be in the past.")
                else:
                    try:
                        prompt = f"""
                        You are a helpful assistant classifying task priority. 
                        Task description: "{description}"
                        Choose only one of these categories: High, Medium, or Low.
                        Reply with just the priority label.
                        """
                        response = model.generate_content(textwrap.dedent(prompt))
                        priority = response.text.strip()
                    except Exception as e:
                        st.error(f"Gemini AI Error: {e}")
                        priority = "Medium"  # fallback

                    tasks = load_tasks()
                    next_id = int(tasks["TaskID"].max()) + 1 if not tasks.empty else 1
                    new_row = pd.DataFrame([{
                        "TaskID": next_id,
                        "Description": description,
                        "Deadline": str(deadline),
                        "AssignedTo": assigned_to,
                        "Priority": priority,
                        "Status": status
                    }])
                    tasks = pd.concat([tasks, new_row], ignore_index=True)
                    save_tasks(tasks)
                    st.success(f"✅ Task added with AI-priority: {priority}!")

# 🔽 EXPANDER: UPDATE TASK STATUS
elif st.session_state["expanded"] == "update":
    with st.expander("🔄 Update Task Status", expanded=True):
        # 🔽 Paste your FULL update task logic here
        st.markdown("<div class='expander-header'>Select a task to update:</div>", unsafe_allow_html=True)
        tasks = load_tasks()
        if not tasks.empty:
            task_options = [f"{row['Description']} (ID: {int(row['TaskID'])})" for _, row in tasks.iterrows()]
            selected = st.selectbox("📋 Select Task", task_options)
            new_status = st.selectbox("🔁 New Status", ["Pending", "In Progress", "Completed"])
            update_btn = st.button("Update Status")
            if update_btn:
                task_id = int(selected.split("(ID:")[1].replace(")", "").strip())
                tasks.loc[tasks["TaskID"] == task_id, "Status"] = new_status
                save_tasks(tasks)
                st.success("✅ Status updated!")
        else:
            st.info("ℹ️ No tasks available.")

# 🔽 EXPANDER: DELETE TASK
elif st.session_state["expanded"] == "delete":
    with st.expander("🗑️ Delete Task", expanded=True):
        # 🔽 Paste your FULL delete task logic here
        st.markdown("<div class='expander-header'>Select a task to delete:</div>", unsafe_allow_html=True)
        tasks = load_tasks()
        if not tasks.empty:
            delete_options = [f"{row['Description']} (ID: {int(row['TaskID'])})" for _, row in tasks.iterrows()]
            selected = st.selectbox("🗂️ Choose Task", delete_options, key="delete")
            delete_btn = st.button("Delete Task")
            if delete_btn:
                task_id = int(selected.split("(ID:")[1].replace(")", "").strip())
                tasks = tasks[tasks["TaskID"] != task_id]
                save_tasks(tasks)
                st.success("✅ Task deleted!")
        else:
            st.info("ℹ️ No tasks to delete.")





if not os.path.exists(task_file):
    st.error("❌ File 'tasks_cleaned.csv' not found.")
elif not os.path.exists(user_file):
    st.error("❌ File 'user_data.csv' not found.")
elif not os.path.exists(prediction_file):
    st.error("❌ File 'model_predictions.csv' not found.")
else:
    tasks = pd.read_csv(task_file)
    user_data = pd.read_csv(user_file)
    predictions = pd.read_csv(prediction_file)

    # Task Table
    # Task Table (Updated with Priority Sorting)
with st.container():
    st.markdown("<div class='block-style'>", unsafe_allow_html=True)
    st.subheader("1️⃣ Task Assignment Table")

    # 👉 Define desired priority order
    priority_order = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)

    # 👉 Convert Priority column to categorical with defined order
    tasks['Priority'] = tasks['Priority'].astype(priority_order)

    # 👉 Sort by Priority first, then Deadline
    tasks_sorted = tasks.sort_values(by=['Priority', 'Deadline'])

    # 👉 Display the sorted table
    st.dataframe(tasks_sorted)

    st.markdown("</div>", unsafe_allow_html=True)

# 🔮 Gemini AI Assistant Section
with st.container():
    st.markdown("<div class='block-style'>", unsafe_allow_html=True)
    st.subheader("💡 Ask Gemini AI About Your Tasks")

    # Chat-style interface
    user_query = st.text_area("🧠 Ask something like:", "What are the most urgent tasks to complete today?")
    if st.button("💬 Ask Gemini"):
        with st.spinner("Thinking..."):
            try:
                prompt = f"""
                You are an assistant for a task manager app. The user has provided the following tasks:
                {tasks_sorted.to_string(index=False)}

                Based on this, answer the question:
                {user_query}
                """
                response = model.generate_content(textwrap.dedent(prompt))
                st.success("🧠 Gemini AI Says:")
                st.write(response.text)
            except Exception as e:
                st.error(f"❌ Gemini AI Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)


with st.container():
    st.markdown("<div class='block-style'>", unsafe_allow_html=True)
    st.subheader("Task Priority Distribution")
    if 'Priority' in tasks.columns:
        fig = px.pie(tasks, names='Priority', title="Task Priority Breakdown", hole=0.3)
        st.plotly_chart(fig)
    else:
        st.warning("⚠️ 'Priority' column not found in tasks.")
    st.markdown("</div>", unsafe_allow_html=True)


with st.container():
    st.markdown("<div class='block-style'>", unsafe_allow_html=True)
    st.subheader("🧑‍💻 User Performance Tracker")

    tasks = load_tasks()
    if not tasks.empty:
        task_users = tasks[["AssignedTo", "Status"]].copy()

        summary = task_users.groupby(["AssignedTo", "Status"]).size().unstack(fill_value=0).reset_index()

        summary = summary.rename(columns={
            "AssignedTo": "Username",
            "Completed": "CompletedTasks",
            "Pending": "PendingTasks",
            "In Progress": "InProgressTasks"
        })

        # Ensure all expected columns are present
        for col in ["CompletedTasks", "PendingTasks", "InProgressTasks"]:
            if col not in summary.columns:
                summary[col] = 0

        summary["CurrentTasks"] = summary["PendingTasks"] + summary["InProgressTasks"]
        summary["TotalTasks"] = summary[["CompletedTasks", "PendingTasks", "InProgressTasks"]].sum(axis=1)
        summary["BehaviourScore"] = ((summary["CompletedTasks"] / summary["TotalTasks"]) * 100).round(2)

        # Assign colored tags to BehaviourScore
        def score_tag(score):
            if score >= 80:
                return f"🟢 {score}%"
            elif score >= 50:
                return f"🟡 {score}%"
            else:
                return f"🔴 {score}%"

        summary["BehaviourScoreTag"] = summary["BehaviourScore"].apply(score_tag)

        # Sort by BehaviourScore descending
        summary = summary.sort_values(by="BehaviourScore", ascending=False)

        # 🎯 Display Metrics Table
        st.markdown("### 📋 Performance Metrics Table")
        st.dataframe(
            summary[["Username", "CompletedTasks", "PendingTasks", "InProgressTasks", "CurrentTasks", "BehaviourScoreTag"]],
            use_container_width=True
        )

        # 📊 Bar Chart: Completed Tasks
        st.markdown("### 📊 Completed Tasks Per User")
        st.markdown("<br>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(6,6))#Smaller graph size
        sns.barplot(data=summary, x="Username", y="CompletedTasks", palette="Blues_d", ax=ax)
        ax.set_title("✅ Completed Tasks by User", fontsize=12)
        ax.set_ylabel("Completed")
        ax.set_xlabel("User")
        plt.xticks(rotation=0, fontsize=10)

        # Center the graph using columns
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.pyplot(fig)


    else:
        st.warning("⚠️ No tasks available.")
    st.markdown("</div>", unsafe_allow_html=True)
