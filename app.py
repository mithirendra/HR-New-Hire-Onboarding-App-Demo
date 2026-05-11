import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Mitma Onboarding App",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = "data/data_files"

@st.cache_data
def load_data():
    hires      = pd.read_csv(f"{DATA_DIR}/new_hires.csv")
    tasks      = pd.read_csv(f"{DATA_DIR}/onboarding_tasks.csv")
    completion = pd.read_csv(f"{DATA_DIR}/task_completion.csv")
    checkins   = pd.read_csv(f"{DATA_DIR}/checkin_responses.csv")
    sentiment  = pd.read_csv(f"{DATA_DIR}/sentiment_data.csv")
    managers   = pd.read_csv(f"{DATA_DIR}/managers.csv")
    buddies    = pd.read_csv(f"{DATA_DIR}/buddies.csv")
    return hires, tasks, completion, checkins, sentiment, managers, buddies

# Call the function and unpack all 7 dataframes into named variables
# Each variable now holds the contents of its corresponding CSV file
hires, tasks, completion, checkins, sentiment, managers, buddies = load_data()

# ─────────────────────────────────────────────
# MAIN APP — only renders if user is logged in
# We check the user role and render the correct
# view. We start with the New Hire view.
# ─────────────────────────────────────────────

view = st.selectbox(
    "Select View",
    ["New Hire", "Manager", "HR"]
)

st.markdown("---")

if view == "New Hire":

    # New hire selector only shows in New Hire view
    selected_name = st.selectbox(
        "Select New Hire",
        hires["full_name"].tolist()
    )
    
    # Hardcode a new hire for Ver 0 demo
    # Ver 1 will use login to select the correct hire
    hire = hires[hires["full_name"] == selected_name].iloc[0]

    # Calculate how many days they have been employed
    # This drives what tasks and phases are visible
    start_date    = datetime.strptime(hire["start_date"], "%Y-%m-%d")
    today         = datetime.today()
    days_employed = max(0, (today - start_date).days)

    # ── Welcome Header ──
    # Shows the new hire's name, role, manager and buddy
    st.markdown(f"## Welcome, {hire['first_name']} 👋")
    st.markdown(f"**{hire['role']}** · Reporting to {hire['manager_name']} · Buddy: {hire['buddy_name']}")
    st.markdown(f"📅 Day **{days_employed}** of 90")
    st.markdown("---")


    # ── Journey Map ──
    # Shows the 5 phases of the onboarding journey
    # The current phase is highlighted based on days_employed
    # Each phase has a day range that determines if it is
    # done, active, or upcoming

    st.markdown("### Your 90-Day Journey")

    # Define the 5 phases with their day ranges
    phases = [
        {"name": "Pre-Boarding",      "label": "Offer → Day 1",   "start": -14, "end": 0},
        {"name": "Orientation",       "label": "Week 1 → Week 2", "start": 1,   "end": 14},
        {"name": "Role Clarity",      "label": "Month 1",         "start": 15,  "end": 30},
        {"name": "Contribution",      "label": "Month 2",         "start": 31,  "end": 60},
        {"name": "Full Productivity", "label": "Month 3 · Day 90","start": 61,  "end": 90},
    ]

    # Create one column per phase
    cols = st.columns(5)

    for i, (col, phase) in enumerate(zip(cols, phases)):
        with col:
            # Determine the status of each phase
            if days_employed > phase["end"]:
                status = "✅ Complete"
                colour = "#3a8c5c"  # green
            elif days_employed >= phase["start"]:
                status = "📍 You are here"
                colour = "#f49052"  # orange accent
            else:
                status = "🔒 Upcoming"
                colour = "#9a8880"  # muted grey

            # Render each phase as a styled card
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #f0d9cc;
                    border-radius:10px;
                    padding:14px;
                    text-align:center;
                    border-top: 4px solid {colour};
                ">
                    <div style="font-size:12px;color:#9a8880;margin-bottom:4px">Phase {i+1}</div>
                    <div style="font-weight:600;color:{colour};margin-bottom:4px">{phase['name']}</div>
                    <div style="font-size:11px;color:#9a8880;margin-bottom:8px">{phase['label']}</div>
                    <div style="font-size:11px;color:{colour}">{status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Task Tracker ──
    # Tasks shown in chronological order grouped by phase.
    # Each task shows its status so the new hire can see
    # exactly where they are in the journey and what still
    # needs to be done.

    st.markdown("### Your Tasks")

    # Join completion with tasks to get description and category
    # Drop category from completion before merging to avoid duplicate columns
    my_tasks = completion.drop(columns=["category"]).merge(
        tasks[["task_id", "description", "category"]],
        on="task_id", how="left"
    )

    # Use hire_id from the selected hire instead of session state
    my_tasks = my_tasks[
        (my_tasks["hire_id"] == hire["hire_id"]) &
        (my_tasks["assigned_to"] == "new_hire")
    ].copy()

    # Total tasks in scope = complete + overdue + pending (not upcoming)
    # Upcoming tasks are excluded as they are not yet due
    # Total = all new hire tasks regardless of status
    # This gives an honest picture of overall journey completion
    total    = len(my_tasks)
    complete = len(my_tasks[my_tasks["status"] == "complete"])
    overdue  = len(my_tasks[my_tasks["status"] == "overdue"])
    pending  = len(my_tasks[my_tasks["status"] == "pending"])
    pct      = int((complete / total * 100) if total > 0 else 0)

    st.markdown(f"**{complete} of {total} tasks complete · {overdue} overdue · {pending} pending**")
    st.progress(pct / 100)
    st.markdown("")

    # Status icons for each task
    status_icons = {
        "complete": "✅",
        "overdue":  "🔴",
        "pending":  "🟡",
        "upcoming": "🔵",
    }

    # Phase order for grouping
    phase_order = ["Pre-boarding", "Week 1", "Month 1", "Month 2", "Month 3"]

    for phase in phase_order:
        phase_tasks = my_tasks[my_tasks["category"] == phase].sort_values("due_day")
        if phase_tasks.empty:
            continue

        st.markdown(f"**{phase}**")

        for _, task in phase_tasks.iterrows():
            icon = status_icons.get(task["status"], "🔵")
            col1, col2, col3 = st.columns([1, 5, 1])
            with col1:
                st.markdown(icon)
            with col2:
                # Strike through completed tasks
                if task["status"] == "complete":
                    st.markdown(f"~~{task['description']}~~")
                else:
                    st.markdown(task["description"])
            with col3:
                st.markdown(f"Day {task['due_day']}")

        st.markdown("")

    # ── Task Legend ──
    # Explains what each emoji means so the new hire
    # understands the status of each task at a glance
    st.markdown("")
    st.markdown(
        """
        <div style="
            background:#ffffff;
            border:1px solid #f0d9cc;
            border-radius:10px;
            padding:12px 20px;
            font-size:12px;
            color:#9a8880;
        ">
        ✅ &nbsp; Complete &nbsp;&nbsp;&nbsp;
        🔴 &nbsp; Overdue &nbsp;&nbsp;&nbsp;
        🟡 &nbsp; Pending &nbsp;&nbsp;&nbsp;
        🔵 &nbsp; Upcoming
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Meet the Team ──
    # Shows the immediate team members for the new hire
    # Filtered to the same department as the new hire
    # So each hire sees their own team, not everyone

    st.markdown("### Meet Your Team")

    # Filter all hires to the same department
    # Exclude the current new hire from the list
    team = hires[
        (hires["department"] == hire["department"]) &
        (hires["hire_id"] != hire["hire_id"])
    ]

    # Also add the manager and buddy as key team members
    cols = st.columns(4)

    # Show manager first
    with cols[0]:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-radius:10px;
                padding:14px;
                text-align:center;
            ">
                <div style="
                    width:48px;height:48px;
                    border-radius:50%;
                    background:#f49052;
                    color:white;
                    font-weight:600;
                    font-size:16px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    margin:0 auto 8px;
                ">{hire['manager_name'][0]}</div>
                <div style="font-weight:600;font-size:13px">{hire['manager_name']}</div>
                <div style="font-size:11px;color:#9a8880">Your Manager</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Show buddy second
    with cols[1]:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-radius:10px;
                padding:14px;
                text-align:center;
            ">
                <div style="
                    width:48px;height:48px;
                    border-radius:50%;
                    background:#3a8c5c;
                    color:white;
                    font-weight:600;
                    font-size:16px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    margin:0 auto 8px;
                ">{hire['buddy_name'][0]}</div>
                <div style="font-weight:600;font-size:13px">{hire['buddy_name']}</div>
                <div style="font-size:11px;color:#9a8880">Your Buddy</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Show up to 2 teammates from the same department
    for i, (_, member) in enumerate(team.head(2).iterrows()):
        with cols[i + 2]:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #f0d9cc;
                    border-radius:10px;
                    padding:14px;
                    text-align:center;
                ">
                    <div style="
                        width:48px;height:48px;
                        border-radius:50%;
                        background:#9a8880;
                        color:white;
                        font-weight:600;
                        font-size:16px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        margin:0 auto 8px;
                    ">{member['first_name'][0]}</div>
                    <div style="font-weight:600;font-size:13px">{member['full_name']}</div>
                    <div style="font-size:11px;color:#9a8880">Your other team mate <br> - {member['role']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ── Check-In ──
    # Shows the relevant check-in based on days employed.
    # Simple version — no submission tracking.

    st.markdown("### How Are You Settling In?")

    # Determine which check-in to show based on days employed
    if days_employed >= 60:
        checkin_day = 90
        checkin_label = "90-Day Check-In"
    elif days_employed >= 30:
        checkin_day = 60
        checkin_label = "60-Day Check-In"
    elif days_employed >= 14:
        checkin_day = 30
        checkin_label = "30-Day Check-In"
    else:
        st.markdown(
            """
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-radius:10px;
                padding:20px;
                color:#9a8880;
                font-size:13px;
            ">
            Your first check-in will be available on Day 14. 
            Focus on settling in and getting to know your team. 🙂
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown(f"#### {checkin_label}")
    st.markdown("Your response goes to your manager and HR. Be honest — this helps us support you better.")
    st.markdown("")

    sentiment_choice = st.radio(
        "How are you feeling?",
        ["😕 Struggling", "🙂 Getting there", "😊 Good", "🚀 Thriving"],
        horizontal=True,
    )

    comment = st.text_area(
        "Any comments for your manager or HR?",
        placeholder="What is going well? What could be better? Any support you need?",
        height=100,
    )

    if st.button("Submit Check-In", use_container_width=False):
        if comment.strip() == "":
            st.warning("Please add a comment before submitting.")
        else:
            st.success(
                f"Thank you for your {checkin_label}. Your manager and HR have been notified. 🙂"
            )
            st.balloons()

    st.markdown("---")

# ─────────────────────────────────────────────
# MANAGER VIEW — Placeholder
# Full build in Ver 1
# ─────────────────────────────────────────────

elif view == "Manager":
    st.markdown("## Manager View")
    st.markdown(
        """
        <div style="
            background:#ffffff;
            border:1px solid #f0d9cc;
            border-radius:10px;
            padding:40px;
            text-align:center;
        ">
            <div style="font-size:48px">🚧</div>
            <div style="font-size:20px;font-weight:600;margin-top:16px">Coming Soon</div>
            <div style="font-size:14px;color:#9a8880;margin-top:8px">
                The Manager view is currently in development.<br>
                It will include new hire progress tracking, manager 
                checklists, 1-on-1 prompts and sentiment signals.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif view == "HR":
    st.markdown("## HR View")
    st.markdown(
        """
        <div style="
            background:#ffffff;
            border:1px solid #f0d9cc;
            border-radius:10px;
            padding:40px;
            text-align:center;
        ">
            <div style="font-size:48px">🚧</div>
            <div style="font-size:20px;font-weight:600;margin-top:16px">Coming Soon</div>
            <div style="font-size:14px;color:#9a8880;margin-top:8px">
                The HR view is currently in development.<br>
                It will include all hires dashboard, completion rates,
                bottleneck alerts and manager compliance tracking.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )