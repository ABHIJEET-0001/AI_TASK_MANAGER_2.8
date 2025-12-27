import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import date
import streamlit.components.v1 as components
from components.how_it_works import render_how_it_works
from components.home import render_home

# import google.generativeai as genai
import textwrap
import json
import requests

from components.sidebar import sidebar_navigation  # 🔹 your custom sidebar

API_BASE = "http://127.0.0.1:5000"

# st.set_page_config
st.set_page_config(page_title="AI Task Management", layout="wide", page_icon="📘")

# 🔐 Gemini AI API Setup (commented)
# api_key = st.secrets["GEMINI_API_KEY"]
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("models/gemini-1.5-flash-8b")

# ========== SIDEBAR NAVIGATION ==========
selected_page = sidebar_navigation()

# ========== TOP-LEVEL STYLES ==========

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

# Animated title (shown on all pages; you can restrict to Home if you want)
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
.confirm-row [data-testid="column"] {
    padding-left: 4px;
    padding-right: 4px;
}
/* --- Task table enhancements: font, sticky header, zebra stripes --- */
.task-table-container [data-testid="stDataFrame"] table {
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    font-size: 14px;
}
.task-table-container [data-testid="stDataFrame"] table thead tr th {
    position: sticky;
    top: 0;
    z-index: 2;
    background: #ffffff;
    box-shadow: 0 2px 0 rgba(0,0,0,0.06);
}
.task-table-container [data-testid="stDataFrame"] table tbody tr:nth-child(odd) {
    background-color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# 🔽 LOAD / SAVE HELPERS
def load_tasks():
    if os.path.exists(task_file):
        return pd.read_csv(task_file)
    return pd.DataFrame(columns=["TaskID", "Description", "Deadline", "AssignedTo", "Priority", "Status"])


def save_tasks(df):
    df.to_csv(task_file, index=False)

def priority_badge(priority: str) -> str:
    if priority == "High":
        return "🔴 High"
    elif priority == "Medium":
        return "🟡 Medium"
    elif priority == "Low":
        return "🟢 Low"
    return priority

# Session state to control expanders
if "expanded" not in st.session_state:
    st.session_state["expanded"] = None


def toggle_expander(name):
    st.session_state["expanded"] = name if st.session_state["expanded"] != name else None

# ========== PAGE: HOME ==========
if selected_page == "🏠 Home":
    render_home()


# ========== PAGES THAT NEED CSV DATA ==========
# Preload CSV data once so Tasks / AI / Analytics share it
csv_available = os.path.exists(task_file) and os.path.exists(user_file) and os.path.exists(prediction_file)

if csv_available:
    tasks_csv = pd.read_csv(task_file)
    user_data = pd.read_csv(user_file)
    predictions = pd.read_csv(prediction_file)
else:
    tasks_csv = pd.DataFrame(columns=["TaskID", "Description", "Deadline", "AssignedTo", "Priority", "Status"])

# Apply sidebar quick filters (Priority/Status) for CSV-based views
priority_filter = st.session_state.get("filter_priority", "All")
status_filter = st.session_state.get("filter_status", "All")
filtered_tasks_csv = tasks_csv.copy()

if priority_filter != "All" and "Priority" in filtered_tasks_csv.columns:
    filtered_tasks_csv = filtered_tasks_csv[filtered_tasks_csv["Priority"] == priority_filter]

if status_filter != "All" and "Status" in filtered_tasks_csv.columns:
    filtered_tasks_csv = filtered_tasks_csv[filtered_tasks_csv["Status"] == status_filter]


# ========== PAGE: HOW IT WORKS / FEATURES ==========
elif selected_page == "⚙️ How It Works":
    render_how_it_works()


# ========== PAGE: TASKS (CSV dashboard) ==========
if selected_page == "📋 Tasks":

    if not os.path.exists(task_file):
        st.error("❌ File 'tasks_cleaned.csv' not found.")
    elif not os.path.exists(user_file):
        st.error("❌ File 'user_data.csv' not found.")
    elif not os.path.exists(prediction_file):
        st.error("❌ File 'model_predictions.csv' not found.")
    else:
        # Show transient success after bulk update
        if "bulk_success_msg" in st.session_state:
            st.toast(st.session_state["bulk_success_msg"], icon="✅")
            del st.session_state["bulk_success_msg"]

        # ---------- Top action buttons ----------
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Add Task", use_container_width=True):
                toggle_expander("add")
        with col2:
            if st.button("🔄 Update Task Status", use_container_width=True):
                toggle_expander("update")
        with col3:
            if st.button("🗑️ Delete Task", use_container_width=True):
                toggle_expander("delete")

        # ---------- EXPANDER: ADD NEW TASK ----------
        if st.session_state["expanded"] == "add":
            with st.expander("➕ Add New Task", expanded=True):
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
                            # 🔮 AI priority (fallback to Medium if Gemini not configured)
                            try:
                                prompt = f"""
                                You are a helpful assistant classifying task priority. 
                                Task description: "{description}"
                                Choose only one of these categories: High, Medium, or Low.
                                Reply with just the priority label.
                                """
                                # response = model.generate_content(textwrap.dedent(prompt))
                                # priority = response.text.strip()
                                raise RuntimeError("Gemini not configured in this example")
                            except Exception as e:
                                # st.error(f"Gemini AI Error: {e}")
                                priority = "Medium"

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

        # ---------- EXPANDER: UPDATE TASK STATUS ----------
        elif st.session_state["expanded"] == "update":
            with st.expander("🔄 Update Task Status", expanded=True):
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

        # ---------- EXPANDER: DELETE TASK ----------
        elif st.session_state["expanded"] == "delete":
            with st.expander("🗑️ Delete Task", expanded=True):
                st.markdown("<div class='expander-header'>Select a task to delete:</div>", unsafe_allow_html=True)
                tasks = load_tasks()
                if not tasks.empty:
                    delete_options = [f"{row['Description']} (ID: {int(row['TaskID'])})" for _, row in tasks.iterrows()]
                    selected = st.selectbox("🗂️ Choose Task", delete_options, key="delete")
                    delete_btn = st.button("Delete Task")

                    if "confirm_delete_id" not in st.session_state:
                        st.session_state["confirm_delete_id"] = None

                    if delete_btn:
                        st.session_state["confirm_delete_id"] = int(selected.split("(ID:")[1].replace(")", "").strip())

                    if st.session_state.get("confirm_delete_id") is not None:
                        pending_id = st.session_state["confirm_delete_id"]
                        st.warning(f"Are you sure you want to delete Task ID {pending_id}? This action cannot be undone.")
                        c1, c2 = st.columns(2, gap="small")
                        with c1:
                            confirm = st.button("✅ Confirm Delete", key="confirm_delete")
                        with c2:
                            cancel = st.button("❌ Cancel", key="cancel_delete")

                        if confirm:
                            tasks = tasks[tasks["TaskID"] != pending_id]
                            save_tasks(tasks)
                            st.session_state["confirm_delete_id"] = None
                            st.success("✅ Task deleted!")
                        elif cancel:
                            st.session_state["confirm_delete_id"] = None
                            st.info("Deletion cancelled.")
                else:
                    st.info("ℹ️ No tasks to delete.")

        # ---------- TASK TABLE WITH BULK ACTIONS ----------
        with st.container():
            st.markdown("<div class='block-style'>", unsafe_allow_html=True)
            st.subheader("1️⃣ Task Assignment Table")

            tasks = filtered_tasks_csv.copy()

            if not tasks.empty:
                priority_order = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)
                tasks['Priority'] = tasks['Priority'].astype(priority_order)

                tasks_sorted = tasks.sort_values(by=['Priority', 'Deadline'])

                st.markdown("<div class='task-table-container'>", unsafe_allow_html=True)
                table_for_edit = tasks_sorted.copy()

                # Visual-only priority column
                table_for_edit["Priority (Visual)"] = table_for_edit["Priority"].apply(priority_badge)

                table_for_edit["Select"] = False

                edited_view = st.data_editor(
                    table_for_edit,
                    use_container_width=True,
                    height=400,
                    disabled=[
                        "TaskID",
                        "Description",
                        "Deadline",
                        "AssignedTo",
                        "Priority",
                        "Priority (Visual)",
                        "Status",
                    ],
                    column_config={
                        "Priority (Visual)": st.column_config.TextColumn(
                            "Priority",
                            help="Task priority (visual indicator)",
                        ),
                        "Select": st.column_config.CheckboxColumn(
                            "Select",
                            help="Tick to include this task in bulk actions",
                            default=False,
                        ),
                    },
                    hide_index=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("#### Bulk actions")
                csel1, csel2, csel3 = st.columns([1.2, 1.5, 1])
                with csel1:
                    select_all_visible = st.checkbox("Select all visible", key="bulk_select_all")
                with csel2:
                    bulk_status = st.selectbox("Change Status to", ["Pending", "In Progress", "Completed"], key="bulk_status")
                with csel3:
                    apply_bulk = st.button("Apply", key="apply_bulk_status")

                if apply_bulk:
                    if select_all_visible:
                        target_ids_list = edited_view["TaskID"].tolist()
                    else:
                        target_ids_list = edited_view.loc[edited_view["Select"] == True, "TaskID"].tolist()

                    if len(target_ids_list) > 0:
                        target_ids = pd.Series(target_ids_list).astype(str).str.extract(r"(\d+)")[0].dropna().astype(int).tolist()
                    else:
                        target_ids = []

                    if len(target_ids) == 0:
                        st.info("No tasks selected.")
                    else:
                        tasks_all = load_tasks()
                        tasks_all.loc[tasks_all["TaskID"].astype(int).isin(target_ids), "Status"] = bulk_status
                        save_tasks(tasks_all)
                        st.session_state["bulk_success_msg"] = f" Updated {len(target_ids)} task(s) to '{bulk_status}'."
                        st.rerun()
            else:
                st.info("ℹ️ No tasks available to display.")

            st.markdown("</div>", unsafe_allow_html=True)

# ========== PAGE: AI ASSISTANT (CSV + Gemini) ==========
elif selected_page == "🤖 AI Assistant":

    with st.container():
        st.markdown("<div class='block-style'>", unsafe_allow_html=True)
        st.subheader("💡 Ask Gemini AI About Your Tasks")

        if filtered_tasks_csv.empty:
            st.info("ℹ️ No tasks available for AI analysis.")
        else:
            tasks_sorted = filtered_tasks_csv.copy()
            if "Priority" in tasks_sorted.columns and "Deadline" in tasks_sorted.columns:
                priority_order = pd.CategoricalDtype(['High', 'Medium', 'Low'], ordered=True)
                tasks_sorted['Priority'] = tasks_sorted['Priority'].astype(priority_order)
                tasks_sorted = tasks_sorted.sort_values(by=['Priority', 'Deadline'])

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
                        # response = model.generate_content(textwrap.dedent(prompt))
                        # st.success("🧠 Gemini AI Says:")
                        # st.write(response.text)
                        st.info("Gemini integration is commented out in this example.")
                    except Exception as e:
                        st.error(f"❌ Gemini AI Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# ========== PAGE: ANALYTICS (charts from CSV) ==========
elif selected_page == "📊 Analytics":

    if not csv_available:
        if not os.path.exists(task_file):
            st.error("❌ File 'tasks_cleaned.csv' not found.")
        if not os.path.exists(user_file):
            st.error("❌ File 'user_data.csv' not found.")
        if not os.path.exists(prediction_file):
            st.error("❌ File 'model_predictions.csv' not found.")
    else:
        # Task Priority Distribution
        with st.container():
            st.markdown("<div class='block-style'>", unsafe_allow_html=True)
            st.subheader("Task Priority Distribution")
            if 'Priority' in filtered_tasks_csv.columns and not filtered_tasks_csv.empty:
                fig = px.pie(filtered_tasks_csv, names='Priority', title="Task Priority Breakdown", hole=0.3)
                st.plotly_chart(fig)
            else:
                st.warning("⚠️ 'Priority' column not found or no tasks after filters.")
            st.markdown("</div>", unsafe_allow_html=True)

        # User Performance Tracker
        with st.container():
            st.markdown("<div class='block-style'>", unsafe_allow_html=True)
            st.subheader("🧑‍💻 User Performance Tracker")

            tasks = filtered_tasks_csv.copy()
            if not tasks.empty:
                task_users = tasks[["AssignedTo", "Status"]].copy()

                summary = task_users.groupby(["AssignedTo", "Status"]).size().unstack(fill_value=0).reset_index()

                summary = summary.rename(columns={
                    "AssignedTo": "Username",
                    "Completed": "CompletedTasks",
                    "Pending": "PendingTasks",
                    "In Progress": "InProgressTasks"
                })

                for col in ["CompletedTasks", "PendingTasks", "InProgressTasks"]:
                    if col not in summary.columns:
                        summary[col] = 0

                summary["CurrentTasks"] = summary["PendingTasks"] + summary["InProgressTasks"]
                summary["TotalTasks"] = summary[["CompletedTasks", "PendingTasks", "InProgressTasks"]].sum(axis=1)
                # avoid division by zero
                summary["BehaviourScore"] = summary.apply(
                    lambda r: ((r["CompletedTasks"] / r["TotalTasks"]) * 100) if r["TotalTasks"] > 0 else 0,
                    axis=1
                ).round(2)

                def score_tag(score):
                    if score >= 80:
                        return f"🟢 {score}%"
                    elif score >= 50:
                        return f"🟡 {score}%"
                    else:
                        return f"🔴 {score}%"

                summary["BehaviourScoreTag"] = summary["BehaviourScore"].apply(score_tag)
                summary = summary.sort_values(by="BehaviourScore", ascending=False)

                st.markdown("### 📋 Performance Metrics Table")
                st.dataframe(
                    summary[["Username", "CompletedTasks", "PendingTasks", "InProgressTasks", "CurrentTasks", "BehaviourScoreTag"]],
                    use_container_width=True
                )

                st.markdown("### 📊 Completed Tasks Per User")
                st.markdown("<br>", unsafe_allow_html=True)

                fig, ax = plt.subplots(figsize=(6, 6))
                sns.barplot(data=summary, x="Username", y="CompletedTasks", palette="Blues_d", ax=ax)
                ax.set_title("✅ Completed Tasks by User", fontsize=12)
                ax.set_ylabel("Completed")
                ax.set_xlabel("User")
                plt.xticks(rotation=0, fontsize=10)

                left, center, right = st.columns([1, 2, 1])
                with center:
                    st.pyplot(fig)
            else:
                st.warning("⚠️ No tasks available.")
            st.markdown("</div>", unsafe_allow_html=True)

# ========== PAGE: TEAM / USERS ==========
elif selected_page == "👥 Team / Users":
    with st.container():
        st.markdown("<div class='block-style'>", unsafe_allow_html=True)
        st.subheader("Team / Users")
        st.info("User management and detailed team analytics can be added here.")
        st.markdown("</div>", unsafe_allow_html=True)

# ========== PAGE: SETTINGS ==========
elif selected_page == "⚙️ Settings":
    with st.container():
        st.markdown("<div class='block-style'>", unsafe_allow_html=True)
        st.subheader("Settings")
        st.info("App settings and preferences can be configured here.")
        st.markdown("</div>", unsafe_allow_html=True)

# ========== API-BASED CRUD SECTION ==========
# You had this at the bottom; keep it but under Tasks/Settings if you want a toggle.
# For now it remains always reachable if you still want the API UI; you can
# move it into a specific page in the sidebar later.

def api_get_tasks():
    r = requests.get(f"{API_BASE}/api/tasks", timeout=10)
    r.raise_for_status()
    return r.json()


def api_get_users():
    r = requests.get(f"{API_BASE}/api/users", timeout=10)
    r.raise_for_status()
    return r.json()


def api_create_task(title, description, deadline_iso):
    payload = {"title": title, "description": description, "deadline": deadline_iso}
    r = requests.post(f"{API_BASE}/api/tasks", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()["task"]


def api_update_task_status(task_id, status):
    r = requests.put(f"{API_BASE}/api/tasks/{task_id}", json={"status": status}, timeout=10)
    r.raise_for_status()
    return r.json()["task"]


def api_delete_task(task_id):
    r = requests.delete(f"{API_BASE}/api/tasks/{task_id}", timeout=10)
    r.raise_for_status()
    return True


def api_assign_task(task_id, user_id_or_none):
    r = requests.post(f"{API_BASE}/api/tasks/{task_id}/assign", json={"user_id": user_id_or_none}, timeout=10)
    r.raise_for_status()
    return r.json()["task"]

# Example: expose API UI only under Tasks page (optional)
if selected_page == "📋 Tasks":
    st.subheader("🔌 Data Source")
    source = st.radio("Choose data source", ["API", "CSV"], index=0)

    if source == "API":
        try:
            users = api_get_users()
            tasks_api = api_get_tasks()
            df = pd.DataFrame(tasks_api)
        except requests.RequestException as e:
            st.error(f"❌ API request failed: {e}")
            st.info("Tip: Start the backend: py app.py")
            st.stop()

        search = st.text_input("Search tasks by title")
        if search:
            df = df[df["title"].str.contains(search, case=False, na=False)]

        if not df.empty:
            df_display = df.rename(columns={
                "id": "ID", "title": "Title", "description": "Description",
                "deadline": "Deadline", "assigned_to": "Assigned To", "status": "Status",
            })
            st.dataframe(df_display)
        else:
            st.info("No tasks found.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### ➕ Add Task")
            title = st.text_input("Title")
            description = st.text_area("Description", height=100)
            deadline_dt = st.date_input("Deadline", value=None)
            user_names = [u["username"] for u in users] if users else []
            assign_to = st.selectbox("Assign to (optional)", ["None"] + user_names)

            if st.button("Create Task", type="primary", use_container_width=True):
                if not title:
                    st.error("Title is required.")
                else:
                    deadline_iso = deadline_dt.isoformat() if isinstance(deadline_dt, date) else None
                    try:
                        created = api_create_task(title, description, deadline_iso)
                        if assign_to != "None":
                            target_user = next((u for u in users if u["username"] == assign_to), None)
                            if target_user:
                                api_assign_task(created["id"], target_user["id"])
                        st.success("Task created successfully.")
                        st.rerun()
                    except requests.HTTPError as e:
                        st.error(f"Failed to create task: {e}")

        with col2:
            st.markdown("### 🔄 Update Status")
            task_ids = df["id"].tolist() if not df.empty else []
            selected_id = st.selectbox("Task", task_ids)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])

            if st.button("Update", use_container_width=True):
                try:
                    api_update_task_status(selected_id, status)
                    st.success("Status updated.")
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"Failed to update: {e}")

        with col3:
            st.markdown("### 🗑️ Delete Task")
            del_id = st.selectbox("Task to delete", df["id"].tolist() if not df.empty else [])
            if st.button("Delete", use_container_width=True):
                try:
                    api_delete_task(del_id)
                    st.success("Task deleted.")
                    st.rerun()
                except requests.HTTPError as e:
                    st.error(f"Failed to delete: {e}")
