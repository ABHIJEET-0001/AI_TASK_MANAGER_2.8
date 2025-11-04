# 🧠 AI Task Manager 2.8

A Streamlit-based AI Task Management dashboard that classifies, visualizes, and analyzes tasks using machine learning.

--- <h1 align="center">🤖 AI-Powered Task Management System</h1>

<p align="center">
  <strong>Live Demo:</strong> 
  <a href="https://aitaskmanager28-bxahukjkzparonrie229uy.streamlit.app/" target="_blank">
    Click Here 🚀
  </a>
</p>

<p align="center">
  <em>“Where Artificial Intelligence meets Productivity.”</em><br>
  An enterprise-level AI-driven platform that intelligently classifies, prioritizes, and assigns tasks using NLP and Machine Learning — designed to supercharge teams with data-driven automation.
</p>

<hr>

<h2>✨ Key Highlights</h2>
<ul>
  <li>🧠 <strong>Smart Task Allocation:</strong> Automatically assigns tasks based on workload, deadlines, and behavior analytics.</li>
  <li>📊 <strong>Interactive Dashboard:</strong> Real-time analytics with priority charts, performance graphs, and summaries.</li>
  <li>⚙️ <strong>Adaptive ML Model:</strong> Predicts priority levels with continuous learning for enhanced accuracy.</li>
  <li>📝 <strong>Manual + Automated Control:</strong> Add, edit, or auto-assign tasks seamlessly.</li>
  <li>🚀 <strong>Future-Ready:</strong> Fully compatible with Trello, Jira, and Slack integrations.</li>
</ul>

<h2>🛠️ Tech Stack</h2>
<ul>
  <li>💻 <strong>Languages & Libraries:</strong> Python, Pandas, Streamlit, Matplotlib, Seaborn, Scikit-learn, NumPy</li>
  <li>🤖 <strong>Machine Learning:</strong> Classification models (scikit-learn) for intelligent prioritization</li>
  <li>📈 <strong>Data:</strong> Simulated CSV datasets (Tasks, Users, Model Predictions)</li>
  <li>🎨 <strong>UI:</strong> Streamlit dashboard with responsive data visualization</li>
</ul>

<h2>📁 Project Structure</h2>
<ul>
  <li><code>dashboard.py</code> — Main Streamlit dashboard and UI entry point</li>
  <li><code>smart_assigner.py</code> — Core ML-based task assignment logic</li>
  <li><code>task_classifier.py</code> — Task classification model (trains and predicts priority levels)</li>
  <li><code>tasks_cleaned.csv</code> — Task data with descriptions, deadlines, assignees, priority, and status</li>
  <li><code>user_data.csv</code> — User performance/workload data with behavior scores</li>
  <li><code>model_predictions.csv</code> — Model accuracy metrics and predictions log</li>
  <li><code>requirements.txt</code> — Python dependencies with pinned versions</li>
</ul>

## 🚀 Run Locally

```bash
# Clone this repository
git clone https://github.com/ABHIJEET-0001/AI_TASK_MANAGER_2.8.git
cd AI_TASK_MANAGER_2.8

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Ensure CSV data files are present (tasks_cleaned.csv, user_data.csv, model_predictions.csv)
# See "Data Format" section below for structure and sample rows

# Run the app
streamlit run dashboard.py
# Open http://localhost:8501 in your browser
```

<h2>📸 Dashboard Preview</h2>
<p align="center">
  <img src="./assets/dashboard.png" alt="AI Task Manager Dashboard" width="100%"/>
</p>

<h2>📊 Dashboard Modules</h2>
<ul>
  <li>📋 Task Overview Table</li>
  <li>🥧 Priority Distribution Chart</li>
  <li>📈 User Performance Analytics</li>
  <li>🧩 Model Accuracy Tracker</li>
  <li>🤖 Smart Task Auto-Assigner</li>
  <li>✏️ Add/Edit Task Interface</li>
  <li>🔍 Summary Metrics (Total & Overdue Tasks)</li>
</ul>

<h2>🧩 Data Format</h2>

<p><strong>user_data.csv</strong> — User workload and behavior metrics:</p>
<pre><code>Username,CurrentTasks,CompletedTasks,PendingTasks,BehaviorScore
Alice,3,15,2,85
Bob,5,10,3,78
Carol,2,20,1,92</code></pre>

<p><strong>tasks_cleaned.csv</strong> — Task details:</p>
<pre><code>TaskID,Description,Deadline,AssignedTo,Priority,Status
T001,Fix login bug,2025-11-10,Alice,High,In Progress
T002,Update documentation,2025-11-15,Bob,Medium,Pending
T003,Deploy to production,2025-11-08,Carol,High,Completed</code></pre>

<p><strong>model_predictions.csv</strong> — ML model performance log:</p>
<pre><code>TaskID,PredictedPriority,ActualPriority,Confidence
T001,High,High,0.92
T002,Medium,Medium,0.85
T003,High,High,0.88</code></pre>

<p><em>Note: Use consistent spelling for "Behavior" (not "Behaviour") across all CSV files and code.</em></p>

<h2>🚧 Future Enhancements</h2>
<ul>
  <li>Integration with Trello, Jira & Slack APIs</li>
  <li>Smart Notifications via Email/Chatbot</li>
  <li>Role-based Authentication & Multi-user Login</li>
  <li>Real-time Cloud Sync & Updates</li>
</ul>

<h2>� Troubleshooting</h2>
<ul>
  <li><strong>Missing CSV files:</strong> Ensure <code>tasks_cleaned.csv</code>, <code>user_data.csv</code>, and <code>model_predictions.csv</code> are in the project root with correct column headers (see "Data Format").</li>
  <li><strong>Module not found:</strong> Activate your virtual environment and run <code>pip install -r requirements.txt</code>.</li>
  <li><strong>Streamlit version issues:</strong> Use Python 3.10–3.12 and ensure <code>streamlit==1.39.0</code> is installed.</li>
  <li><strong>File path errors:</strong> Run <code>streamlit run dashboard.py</code> from the project root directory.</li>
  <li><strong>Port already in use:</strong> Stop other services on port 8501 or run <code>streamlit run dashboard.py --server.port 8502</code>.</li>
</ul>

<h2>�📜 License</h2>
<p>
  Licensed under the <a href="./LICENSE"><strong>MIT License</strong></a> — free to use, improve, and deploy.
</p>

<p align="center">
  💡 Crafted with precision, powered by AI, and designed for innovation.<br>
  <strong>Made with ❤️ by Abhijeet Kasera</strong>
</p>

