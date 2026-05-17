import streamlit as st
import pandas as pd
import base64
from datetime import datetime

st.set_page_config(
    page_title="Mitma Onboarding App - Demo Version | Mitma Consulting",
    page_icon="assets/mitma_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLING
# Montserrat font and demo notice styles
# consistent across all Mitma Consulting apps
# ─────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

        /* ─────────────────────────────────────────────
        Force Montserrat across all Streamlit elements
        Streamlit 1.57 requires more specific selectors
        ───────────────────────────────────────────── */
        * {
            font-family: 'Montserrat', sans-serif !important;
        }

        html, body {
            font-family: 'Montserrat', sans-serif !important;
        }

        h1, h2, h3, h4, h5, h6, p, div, span, label, button {
            font-family: 'Montserrat', sans-serif !important;
        }

        [data-testid="stMarkdownContainer"] * {
            font-family: 'Montserrat', sans-serif !important;
        }

        [data-testid="stSidebar"] * {
            font-family: 'Montserrat', sans-serif !important;
        }
            
        [data-testid="stSidebar"] {
            background-color: #ffece1;
        }
            
        /* Main page background */
        [data-testid="stAppViewContainer"] {
            background-color: #fffbf8;
        }
        
        /* ─────────────────────────────────────────────
        Hide Streamlit default header elements
        including the hamburger menu and
        the Deploy button for a cleaner demo look.
        ───────────────────────────────────────────── */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stSidebarCollapseButton"] {display: none;}
                            
        /* ─────────────────────────────────────────────
        DEMO NOTICE STYLING
        ───────────────────────────────────────────── */
            
        .demo-notice {
            background: #ffffff;
            border: 1px solid #f0d9cc;
            border-radius: 12px;
            padding: 48px 40px;
            text-align: center;
            font-family: 'Montserrat', sans-serif;
            max-width: 600px;
            margin: 40px auto;
        }
        .demo-notice-icon {
            font-size: 40px;
            margin-bottom: 16px;
        }
        .demo-notice-title {
            font-size: 22px;
            font-weight: 700;
            color: #000000;
            margin-bottom: 12px;
        }
        .demo-notice-text {
            font-size: 14px;
            color: #505050;
            margin-bottom: 8px;
        }
        .demo-notice-contact {
            font-size: 13px;
            color: #505050;
            margin-bottom: 24px;
        }
        .demo-notice-logo {
            height: 48px;
            margin-bottom: 24px;
        }
        .demo-notice-buttons {
            display: flex;
            flex-direction: row;
            gap: 10px;
            align-items: center;
            justify-content: center;
            margin-top: 8px;
            flex-wrap: wrap;
        }
        .demo-notice-btn {
            padding: 10px 24px;
            background: #f49052;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
        }
        .demo-notice-btn:hover {
            background: #505050;
        }
        .demo-notice-btn-linkedin {
            padding: 10px 24px;
            background: #f49052;
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
        }
        .demo-notice-btn-linkedin:hover {
            background: #505050;
        }
        
        /* ─────────────────────────────────────────────
        SIDEBAR STYLING
        Streamlit sidebar needs explicit targeting
        as it is rendered in a separate container
        from the main page content.
        ───────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: #ffece1;
            font-family: 'Montserrat', sans-serif;
        }

        [data-testid="stSidebar"] * {
            font-family: 'Montserrat', sans-serif;
        }

        [data-testid="stSidebar"] .stRadio label {
            font-size: 13px;
            font-weight: 500;
            color: #505050;
        }
        
        /* ─────────────────────────────────────────────
        LINK BUTTON STYLING
        Targets Streamlit's native link button and
        applies Mitma Consulting orange colour.
        Second button targets LinkedIn blue.
        ───────────────────────────────────────────── */
        [data-testid="stLinkButton"] a {
            background-color: #f49052 !important;
            color: white !important;
            border-radius: 8px !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            border: none !important;
        }

        [data-testid="stLinkButton"] a:hover {
            background-color: #505050 !important;
            color: white !important;
        }
        
        /* ─────────────────────────────────────────────
        Fix link button font colour
        Streamlit link buttons default to blue
        This forces white text on all link buttons
        ───────────────────────────────────────────── */
        [data-testid="stLinkButton"] a {
            color: white !important;
            text-decoration: none !important;
        }

        [data-testid="stLinkButton"] a:hover {
            color: white !important;
        }
        
        [data-testid="stLinkButton"] > a,
        [data-testid="stLinkButton"] > a:visited,
        [data-testid="stLinkButton"] > a:hover,
        [data-testid="stLinkButton"] > a:active {
            color: white !important;
            text-decoration: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
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
# SIDEBAR NAVIGATION
# Replaces login for demo version.
# Visitor can switch between views freely.
# Manager and HR show locked demo notice.
# ─────────────────────────────────────────────

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_base64 = get_image_base64("assets/mitma_logo.png")
logo_src    = f"data:image/png;base64,{logo_base64}"

with st.sidebar:
    st.markdown(
        f"""
        <div style="
            font-family:'Montserrat',sans-serif;
            font-weight:700;
            font-size:18px;
            color:#000000;
            text-align:center;
            margin-bottom:4px;
        ">
        MITMA ONBOARDING APP
        </div>
        <div style="
            font-size:12px;
            color:#9a8880;
            text-align:center;
            margin-bottom:4px;
        ">
        BY MITMA CONSULTING
        </div>
        <div style="text-align:center;margin-bottom:24px;">
            <span style="
                font-size:10px;
                font-weight:600;
                background:#f49052;
                color:white;
                padding:2px 10px;
                border-radius:10px;
            ">DEMO VERSION</span>
        </div>
        <div style="text-align:center;margin-top:50px; margin-bottom:16px;">
            <a href="https://mitmaconsulting.framer.ai" target="_blank">
                <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ─────────────────────────────────────────────
    # Navigation radio buttons
    # Each option maps to a view below
    # ─────────────────────────────────────────────
    view = st.radio(
        "Select to Navigate View",
        ["👤  New Hire", "👔  Manager", "🏢  HR"],
        index=0,
    )

    st.markdown("---")

    # ── Render selected view ──────────────────────────────────────
    if view == "👤  New Hire":
        st.markdown("### EMPLOYEE VIEW")

    elif view == "👔  Manager":
        st.markdown("### MANAGER VIEW")

    elif view == "🏢  HR":
        st.markdown("### 🏢 HR View")

    st.markdown("---")

    # ─────────────────────────────────────────────
    # Contact links
    # ─────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            font-size:13px;
            color:#9a8880;
            text-align:center;
            margin-bottom:40px;
            line-height:1.6;
        ">
        This app is only a <strong>DEMO VERSION</strong> with limited view pages.
        <br><br>
        Contact Mitma Consulting to get access to the <strong>FULL VERSION</strong>, 
        which has a login page and different full views based on who logs in.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("Contact Mitma Consulting →", "https://mitmaconsulting.framer.ai", use_container_width=True)
    st.link_button("Connect on LinkedIn →", "https://www.linkedin.com/in/mithirendra-maniam/", use_container_width=True)

    st.markdown("---")

# ─────────────────────────────────────────────
# MAIN APP — only renders if user is logged in
# We check the user role and render the correct
# view. We start with the New Hire view.
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# NEW HIRE VIEW
# ─────────────────────────────────────────────

if view == "👤  New Hire":

    st.markdown("## New Hire View - Onboarding Journey")

    # New hire selector only shows in New Hire view
    selected_name = st.selectbox(
        "Select New Hire to get personalised view",
        hires["full_name"].tolist()
    )


    st.markdown("---")

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

    # ── Welcome Message ──
    # A personal welcome from leadership sets the tone
    # for the new hire's first experience with the company.
    # Synthetic data used for proof of concept.
    # In Ver 1 this would be customised per company.

    st.markdown(
        f"""
        <div id="welcome-block" style="
            background:#ffffff;
            border:1px solid #f0d9cc;
            border-radius:12px;
            padding:32px 36px;
            margin-bottom:24px;
        ">
            <p style="font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:#9a8880;margin-bottom:12px;">Welcome to Mitma</p>
            <p style="font-size:22px;font-weight:700;color:#000000;margin-bottom:16px;line-height:1.3;">We are thrilled to have you, {hire['first_name']}.</p>
            <p style="font-size:14px;color:#505050;line-height:1.8;margin-bottom:20px;">Starting a new role is one of the most exciting — and sometimes daunting — experiences in a career. We want you to know that everyone here is rooting for you.<br><br>Take it one step at a time. Ask questions. Get to know your team. Welcome aboard.</p>
            <p style="font-size:13px;font-weight:600;color:#f49052;">Ir. Mithirendra Maniam<br><span style="font-weight:400;color:#9a8880;font-size:12px;">Founder and Chief Executive Officer · Mitma Consulting</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Company Values ──
    # Short value cards showing company mission and values.
    # Makes the culture tangible from day one.
    # In Ver 1 these would be customised per company.

    st.markdown("### Our Values")

    values = [
        {"icon": "🤝", "title": "People First",      "desc": "We put our people — employees and clients — at the centre of every decision we make."},
        {"icon": "💡", "title": "Curiosity",          "desc": "We ask questions, challenge assumptions and never stop learning."},
        {"icon": "🎯", "title": "Ownership",          "desc": "We take responsibility for our work, our mistakes and our growth."},
        {"icon": "🌍", "title": "Inclusion",          "desc": "We build a workplace where every voice is heard and every person belongs."},
    ]

    cols = st.columns(4)

    for col, value in zip(cols, values):
        with col:
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #f0d9cc;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                    height:100%;
                ">
                    <div style="font-size:32px;margin-bottom:12px;">{value['icon']}</div>
                    <div style="font-weight:700;font-size:14px;color:#000000;
                                margin-bottom:8px;">{value['title']}</div>
                    <div style="font-size:12px;color:#9a8880;line-height:1.6;">
                        {value['desc']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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
        Task Legend:&nbsp;&nbsp;&nbsp;
        ✅ &nbsp; Complete &nbsp;&nbsp;&nbsp;
        🔴 &nbsp; Overdue &nbsp;&nbsp;&nbsp;
        🟡 &nbsp; Pending &nbsp;&nbsp;&nbsp;
        🔵 &nbsp; Upcoming
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── 30/60/90 Day Goals ──
    # Shows the new hire what is expected of them
    # in each phase of their journey.
    # Tied to the journey map phases above.
    # Gives clarity on what success looks like.

    st.markdown("### Your 30 · 60 · 90 Day Goals")

    goals = [
        {
            "phase":  "First 30 Days",
            "colour": "#f49052",
            "icon":   "🌱",
            "focus":  "Learn & Settle In",
            "goals":  [
                "Understand your role, team and immediate priorities",
                "Complete all onboarding tasks and compliance training",
                "Build relationships with your manager, buddy and team",
                "Get familiar with the tools, systems and workflows",
                "Ask questions — there are no silly ones in your first month",
            ]
        },
        {
            "phase":  "First 60 Days",
            "colour": "#c9861a",
            "icon":   "🚀",
            "focus":  "Contribute & Connect",
            "goals":  [
                "Begin contributing to team projects and deliverables",
                "Develop a clear understanding of your KPIs and targets",
                "Build relationships beyond your immediate team",
                "Identify one area where you can add immediate value",
                "Share early observations and ideas with your manager",
            ]
        },
        {
            "phase":  "First 90 Days",
            "colour": "#3a8c5c",
            "icon":   "🎯",
            "focus":  "Own & Deliver",
            "goals":  [
                "Independently own and deliver a piece of work",
                "Complete your 90-day review with your manager",
                "Set goals for the next 6 months",
                "Be a resource for the next new hire who joins",
                "Feel confident, settled and excited about what comes next",
            ]
        },
    ]

    for goal in goals:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-left:4px solid {goal['colour']};
                border-radius:12px;
                padding:20px 24px;
                margin-bottom:16px;
            ">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                    <div style="font-size:24px;">{goal['icon']}</div>
                    <div>
                        <div style="font-weight:700;font-size:15px;color:#000000;">
                            {goal['phase']}
                        </div>
                        <div style="font-size:12px;color:{goal['colour']};font-weight:600;">
                            {goal['focus']}
                        </div>
                    </div>
                </div>
                <ul style="margin:0;padding-left:20px;color:#505050;font-size:13px;line-height:1.8;">
                    {''.join([f"<li>{g}</li>" for g in goal['goals']])}
                </ul>
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

    # ── Upcoming Events ──
    # Shows upcoming team events, all-hands and socials.
    # Makes the company feel alive and welcoming.
    # In Ver 1 this would connect to a calendar feed.
    # Synthetic data used for proof of concept.

    st.markdown("### Upcoming Events")

    events = [
        {
            "date":  "20 May 2026",
            "day":   "Wed",
            "title": "All-Hands Meeting",
            "desc":  "Company-wide quarterly update from leadership.",
            "type":  "Company",
            "colour": "#f49052",
        },
        {
            "date":  "23 May 2026",
            "day":   "Sat",
            "title": "Team Social — Bowling Night",
            "desc":  "A casual evening out with the team. Partners welcome.",
            "type":  "Social",
            "colour": "#3a8c5c",
        },
        {
            "date":  "28 May 2026",
            "day":   "Thu",
            "title": "New Hire Lunch",
            "desc":  "Lunch with all new hires who joined this month.",
            "type":  "New Hire",
            "colour": "#c9861a",
        },
        {
            "date":  "3 Jun 2026",
            "day":   "Wed",
            "title": "Department Town Hall",
            "desc":  "Monthly department update and Q&A session.",
            "type":  "Department",
            "colour": "#7b6ea7",
        },
    ]

    for event in events:
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                border:1px solid #f0d9cc;
                border-radius:12px;
                padding:16px 20px;
                margin-bottom:12px;
                display:flex;
                align-items:center;
                gap:20px;
            ">
                <div style="
                    background:{event['colour']}22;
                    border-radius:10px;
                    padding:10px 14px;
                    text-align:center;
                    min-width:60px;
                    flex-shrink:0;
                ">
                    <div style="font-size:10px;color:{event['colour']};
                                font-weight:600;text-transform:uppercase;
                                letter-spacing:0.08em;">{event['day']}</div>
                    <div style="font-size:18px;font-weight:700;
                                color:{event['colour']};line-height:1.2;">
                        {event['date'].split()[0]}
                    </div>
                    <div style="font-size:10px;color:{event['colour']};">
                        {' '.join(event['date'].split()[1:])}
                    </div>
                </div>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:13px;
                                color:#000000;margin-bottom:4px;">
                        {event['title']}
                    </div>
                    <div style="font-size:12px;color:#9a8880;">
                        {event['desc']}
                    </div>
                </div>
                <div style="
                    background:{event['colour']}22;
                    color:{event['colour']};
                    font-size:10px;
                    font-weight:600;
                    padding:4px 10px;
                    border-radius:20px;
                    flex-shrink:0;
                ">{event['type']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Locked Sections — Demo Notice ──
    # Training curriculum, Day 1 content, Quick Links,
    # ERG and FAQ are Full Version only.

    st.markdown("### Key Contacts · Training · Day 1 Guide · Resources · ERGs · FAQ")

    st.markdown(
        """
        <div class="demo-notice">
            <div class="demo-notice-icon">🔒</div>
            <h3 class="demo-notice-title">Full Version Only</h3>
            <p class="demo-notice-text">
                Key Contacts, Training Curriculum, Day 1 Onboarding Guide, Quick Links, 
                Employee Resource Groups and FAQ are available in the 
                Full Version of the Mitma Onboarding App.
            </p>
            <p class="demo-notice-contact">
                Contact Mitma Consulting to get access to the Full Version.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align:center;margin-bottom:16px;">
                <a href="https://mitmaconsulting.framer.ai" target="_blank">
                    <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _, btn1, btn2, _ = st.columns([0.5, 2, 2, 0.5])
        with btn1:
            st.link_button("Contact Mitma →", "YOUR_CONTACT_URL", use_container_width=True)
        with btn2:
            st.link_button("Connect on LinkedIn →", "YOUR_LINKEDIN_URL", use_container_width=True)

    st.markdown("---")

    # ── Check-In ──
    st.markdown("### How Are You Settling In?")

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
        checkin_day = None

    if checkin_day is None:
        # Too early — show message but do NOT call st.stop()
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
    else:
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

# ─────────────────────────────────────────────
# MANAGER VIEW — Placeholder
# Full build in Ver 1
# ─────────────────────────────────────────────

elif view == "👔  Manager":
    
    st.markdown("## Manager View - Overall Team Progress")
    st.markdown(
        """
        <div style="
            background:#ffece1;
            border-left:4px solid #f49052;
            border-radius:6px;
            padding:10px 16px;
            font-size:13px;
            color:#505050;
            margin-bottom:24px;
        ">
        👀 <strong>Demo Preview</strong> · You are viewing a sample of the Manager view. 
        Some sections are available in the Full Version only.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ─────────────────────────────────────────────
    # Manager selector dropdown
    # Allows demo visitor to switch between managers
    # and see different data — same pattern as the
    # new hire selector in the New Hire view
    # ─────────────────────────────────────────────
    selected_manager = st.selectbox(
        "Select Manager to get personalised view",
        managers["name"].tolist()
    )

    # Filter hires to the selected manager
    my_hires = hires[hires["manager_name"] == selected_manager].copy()

    # Calculate days employed for each hire
    my_hires["days_employed"] = my_hires["start_date"].apply(
        lambda x: max(0, (datetime.today() - datetime.strptime(x, "%Y-%m-%d")).days)
    )

    # Get manager department
    manager_dept = managers[managers["name"] == selected_manager].iloc[0]["department"]

    st.markdown(f"**{manager_dept} · {len(my_hires)} active new hires**")
    st.markdown("---")

    # ─────────────────────────────────────────────
    # STATS ROW
    # ─────────────────────────────────────────────
    total_tasks = completion[
        (completion["hire_id"].isin(my_hires["hire_id"])) &
        (completion["assigned_to"] == "new_hire") &
        (completion["status"] != "upcoming")
    ]
    complete_tasks = total_tasks[total_tasks["status"] == "complete"]
    overdue_tasks  = total_tasks[total_tasks["status"] == "overdue"]

    avg_completion = int(
        len(complete_tasks) / len(total_tasks) * 100
    ) if len(total_tasks) > 0 else 0

    my_sentiment  = checkins[checkins["hire_id"].isin(my_hires["hire_id"])]
    avg_sentiment = round(my_sentiment["score"].mean(), 1) if len(my_sentiment) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px 20px;">
                <div style="font-size:32px;font-weight:700;color:#000000">{len(my_hires)}</div>
                <div style="font-size:11px;color:#9a8880;margin-top:4px">Active New Hires</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px 20px;">
                <div style="font-size:32px;font-weight:700;color:#f49052">{avg_completion}%</div>
                <div style="font-size:11px;color:#9a8880;margin-top:4px">Avg Task Completion</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px 20px;">
                <div style="font-size:32px;font-weight:700;color:#d4703a">{len(overdue_tasks)}</div>
                <div style="font-size:11px;color:#9a8880;margin-top:4px">Overdue Tasks</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px 20px;">
                <div style="font-size:32px;font-weight:700;color:#3a8c5c">{avg_sentiment}</div>
                <div style="font-size:11px;color:#9a8880;margin-top:4px">Avg Sentiment Score</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("---")

    # ─────────────────────────────────────────────
    # NEW HIRE PROGRESS TRACKER
    # ─────────────────────────────────────────────
    st.markdown("### New Hire Progress")

    for _, h in my_hires.iterrows():

        hire_tasks = completion[
            (completion["hire_id"] == h["hire_id"]) &
            (completion["assigned_to"] == "new_hire") &
            (completion["status"] != "upcoming")
        ]

        h_complete = len(hire_tasks[hire_tasks["status"] == "complete"])
        h_overdue  = len(hire_tasks[hire_tasks["status"] == "overdue"])
        h_total    = len(hire_tasks)
        h_pct      = int(h_complete / h_total * 100) if h_total > 0 else 0

        if h_overdue > 0:
            tag    = "⚠️ Overdue tasks"
            colour = "#d4703a"
        elif h_pct >= 80:
            tag    = "🚀 Ahead"
            colour = "#3a8c5c"
        else:
            tag    = "✅ On track"
            colour = "#f49052"

        col1, col2, col3 = st.columns([3, 4, 2])

        with col1:
            initials = h["first_name"][0] + h["last_name"][0]
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:12px;padding:8px 0;">
                    <div style="
                        width:40px;height:40px;border-radius:50%;
                        background:#f49052;color:white;
                        font-weight:600;font-size:14px;
                        display:flex;align-items:center;justify-content:center;
                        flex-shrink:0;
                    ">{initials}</div>
                    <div>
                        <div style="font-weight:600;font-size:13px">{h['full_name']}</div>
                        <div style="font-size:11px;color:#9a8880">{h['role']} · Day {h['days_employed']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("")
            st.progress(h_pct / 100)
            st.markdown(
                f"<div style='font-size:11px;color:#9a8880'>{h_complete} of {h_total} tasks complete</div>",
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown("")
            st.markdown(
                f"<div style='font-size:12px;color:{colour};font-weight:500;padding-top:8px'>{tag}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ─────────────────────────────────────────────
    # LOCKED SECTIONS — demo notice
    # Manager checklist, 1-on-1 prompts and
    # sentiment tracker are Full Version only
    # ─────────────────────────────────────────────
    st.markdown("### Manager Checklist · 1-on-1 Prompts · Sentiment Tracker")

    st.markdown(
        """
        <div class="demo-notice">
            <div class="demo-notice-icon">🔒</div>
            <h3 class="demo-notice-title">Full Version Only</h3>
            <p class="demo-notice-text">Manager Checklist, 1-on-1 Conversation Prompts and Sentiment Tracker are available in the Full Version.</p>
            <p class="demo-notice-contact">Contact Mitma Consulting to get access to the Full Version.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align:center;margin-top:50px; margin-bottom:16px;">
                <a href="https://mitmaconsulting.framer.ai" target="_blank">
                    <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _, btn1, btn2, _ = st.columns([0.5, 2, 2, 0.5])
        with btn1:
            st.link_button("Contact Mitma Consulting →", "https://mitmaconsulting.framer.ai/contact", use_container_width=True)
        with btn2:
            st.link_button("Connect on LinkedIn →", "https://www.linkedin.com/in/mithirendra-maniam/", use_container_width=True)

# ─────────────────────────────────────────────
# HR VIEW — Demo locked page
# ─────────────────────────────────────────────
elif view == "🏢  HR":

    st.markdown("## HR View - Overall Company Onboarding")

    st.markdown(
        """
        <div style="
            background:#ffece1;
            border-left:4px solid #f49052;
            border-radius:6px;
            padding:10px 16px;
            font-size:13px;
            color:#505050;
            margin-bottom:24px;
        ">
        👀 <strong>Demo Preview</strong> · You are viewing a sample of the HR view. 
        Some sections are available in the Full Version only.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"**All Departments · {len(hires)} active new hires**")
    st.markdown("---")

    # ─────────────────────────────────────────────
    # STATS ROW
    # 5 key metrics across all new hires and
    # all departments in the organisation
    # ─────────────────────────────────────────────
    all_tasks = completion[
        (completion["assigned_to"] == "new_hire") &
        (completion["status"] != "upcoming")
    ]

    all_complete = len(all_tasks[all_tasks["status"] == "complete"])
    all_overdue  = len(all_tasks[all_tasks["status"] == "overdue"])
    all_total    = len(all_tasks)

    overall_completion = int(
        all_complete / all_total * 100
    ) if all_total > 0 else 0

    avg_satisfaction = round(checkins["score"].mean(), 1) if len(checkins) > 0 else 0

    active_hires = hires[hires["days_employed"] > 0]
    avg_days     = int(active_hires["days_employed"].mean()) if len(active_hires) > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px;">
                <div style="font-size:28px;font-weight:700;color:#000000">{len(hires)}</div>
                <div style="font-size:10px;color:#9a8880;margin-top:4px;text-transform:uppercase;letter-spacing:0.06em">Active New Hires</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px;">
                <div style="font-size:28px;font-weight:700;color:#3a8c5c">{overall_completion}%</div>
                <div style="font-size:10px;color:#9a8880;margin-top:4px;text-transform:uppercase;letter-spacing:0.06em">Avg Completion Rate</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px;">
                <div style="font-size:28px;font-weight:700;color:#000000">{avg_days}d</div>
                <div style="font-size:10px;color:#9a8880;margin-top:4px;text-transform:uppercase;letter-spacing:0.06em">Avg Days Employed</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px;">
                <div style="font-size:28px;font-weight:700;color:#f49052">{avg_satisfaction}</div>
                <div style="font-size:10px;color:#9a8880;margin-top:4px;text-transform:uppercase;letter-spacing:0.06em">Avg Satisfaction Score</div>
            </div>
            """, unsafe_allow_html=True)

    with col5:
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #f0d9cc;
                border-radius:12px;padding:16px;">
                <div style="font-size:28px;font-weight:700;color:#d4703a">{all_overdue}</div>
                <div style="font-size:10px;color:#9a8880;margin-top:4px;text-transform:uppercase;letter-spacing:0.06em">Overdue Tasks</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("---")

    # ─────────────────────────────────────────────
    # COMPLETION RATE BY DEPARTMENT
    # ─────────────────────────────────────────────
    st.markdown("### Completion Rate by Department")

    dept_completion = completion[
        (completion["assigned_to"] == "new_hire") &
        (completion["status"] != "upcoming")
    ].merge(
        hires[["hire_id", "department"]],
        on="hire_id", how="left"
    )

    dept_stats = dept_completion.groupby("department").apply(
        lambda x: round(len(x[x["status"] == "complete"]) / len(x) * 100, 1)
    ).reset_index()
    dept_stats.columns = ["department", "completion_rate"]

    dept_hire_count = hires.groupby("department").size().reset_index()
    dept_hire_count.columns = ["department", "hire_count"]

    dept_stats = dept_stats.merge(dept_hire_count, on="department", how="left")
    dept_stats = dept_stats.sort_values("completion_rate", ascending=False)

    for _, row in dept_stats.iterrows():

        if row["completion_rate"] >= 75:
            colour = "#3a8c5c"
        elif row["completion_rate"] >= 50:
            colour = "#c9861a"
        else:
            colour = "#d4703a"

        col1, col2, col3 = st.columns([2, 5, 1])

        with col1:
            st.markdown(
                f"""
                <div style="padding:8px 0;">
                    <div style="font-weight:600;font-size:13px">{row['department']}</div>
                    <div style="font-size:11px;color:#9a8880">{row['hire_count']} new hires</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown("")
            st.progress(row["completion_rate"] / 100)

        with col3:
            st.markdown(
                f"""
                <div style="padding-top:8px;text-align:right;">
                    <div style="font-size:16px;font-weight:700;color:{colour}">{row['completion_rate']}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # ─────────────────────────────────────────────
    # LOCKED SECTIONS — demo notice
    # Bottleneck alerts, satisfaction score and
    # manager compliance are Full Version only
    # ─────────────────────────────────────────────
    st.markdown("### Bottleneck Alerts · Satisfaction Score · Manager Compliance")

    st.markdown(
        """
        <div class="demo-notice">
            <div class="demo-notice-icon">🔒</div>
            <h3 class="demo-notice-title">Full Version Only</h3>
            <p class="demo-notice-text">Bottleneck Alerts, Satisfaction Score and Manager Compliance are available in the Full Version.</p>
            <p class="demo-notice-contact">Contact Mitma Consulting to get access to the Full Version.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align:center;margin-top:50px; margin-bottom:16px;">
                <a href="https://mitmaconsulting.framer.ai" target="_blank">
                    <img src="{logo_src}" height="48" alt="Mitma Consulting"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _, btn1, btn2, _ = st.columns([0.5, 2, 2, 0.5])
        with btn1:
            st.link_button("Contact Mitma Consulting →", "https://mitmaconsulting.framer.ai/contact", use_container_width=True)
        with btn2:
            st.link_button("Connect on LinkedIn →", "https://www.linkedin.com/in/mithirendra-maniam/", use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
# Show footer
st.markdown("""
<div style='text-align:center;padding:20px 0 10px;
            font-size:11px;color:#c0a080;
            border-top:0.5px solid #f0d0b8;
            margin-top:40px;
            font-family:Montserrat,sans-serif;'>
    © 2026 Mitma Consulting · Mitma Onboarding App Demo Version 0 ·
    Built by Mithirendra Maniam
</div>
""", unsafe_allow_html=True)