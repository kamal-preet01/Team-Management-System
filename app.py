import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import uuid
from datetime import datetime

# File paths remain unchanged
TASKS_FILE = 'tasks.json'
MEMBERS_FILE = 'team_members.json'
COMMENTS_FILE = 'task_comments.json'
BOSS_CREDENTIALS_FILE = 'boss_credentials.json'
MEMBERS_CREDENTIALS_FILE = 'member_credentials.json'
GROUPS_FILE = 'groups.json'
GROUP_MESSAGES_FILE = 'group_messages.json'
NOTIFICATIONS_FILE = 'notifications.json'

# Enhanced CSS styles with modern design
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Card Styles */
    .modern-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border: 1px solid #eee;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Status Badges */
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
    }

    .status-completed {
        background-color: #dcffe4;
        color: #0a5d1e;
    }

    .status-pending {
        background-color: #fff1f0;
        color: #cf1322;
    }

    .status-inprogress {
        background-color: #fff7e6;
        color: #d46b08;
    }

    .status-followup {
        background-color: #e6f7ff;
        color: #096dd9;
    }

    /* Comment Section */
    .comment-box {
        background-color: #f9f9f9;
        border-left: 4px solid #1890ff;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
    }

    .comment-meta {
        color: #8c8c8c;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    /* Group Chat */
    .chat-message {
        margin: 0.5rem 0;
        padding: 0.8rem 1rem;
        border-radius: 12px;
        max-width: 80%;
    }

    .message-sent {
        background-color: #1890ff;
        color: white;
        margin-left: auto;
    }

    .message-received {
        background-color: #f0f2f5;
        color: #000;
    }

    /* Navigation */
    .nav-item {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.2rem 0;
        transition: background-color 0.2s ease;
    }

    .nav-item:hover {
        background-color: #f0f2f5;
    }

    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #fff, #f0f2f5);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #eee;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1890ff;
    }

    .metric-label {
        color: #8c8c8c;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Form Controls */
    .stTextInput, .stTextArea, .stSelectbox {
        border-radius: 8px !important;
    }

    .stButton>button {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Notifications */
    .notification-dot {
        background-color: #ff4d4f;
        border-radius: 50%;
        width: 8px;
        height: 8px;
        display: inline-block;
        margin-left: 5px;
    }

    /* Task List */
    .task-list {
        border: 1px solid #f0f0f0;
        border-radius: 12px;
        overflow: hidden;
    }

    .task-item {
        padding: 1rem;
        border-bottom: 1px solid #f0f0f0;
        transition: background-color 0.2s ease;
    }

    .task-item:hover {
        background-color: #fafafa;
    }

    /* Member List */
    .member-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        padding: 1rem 0;
    }

    .member-card {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #eee;
        transition: transform 0.2s ease;
    }

    .member-card:hover {
        transform: translateY(-2px);
    }

    /* Group List */
    .group-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1.5rem;
        padding: 1rem 0;
    }

    .group-card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #eee;
        transition: all 0.2s ease;
    }

    .group-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }

    /* Login Form */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .member-list, .group-grid {
            grid-template-columns: 1fr;
        }

        .chat-message {
            max-width: 90%;
        }
    
    
    }
</style>
""", unsafe_allow_html=True)


# Helper functions for loading and saving data
def load_tasks():
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading tasks: {str(e)}")
    return []


def save_tasks():
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(st.session_state.tasks, f)
    except Exception as e:
        st.error(f"Error saving tasks: {str(e)}")


def load_team_members():
    try:
        if os.path.exists(MEMBERS_FILE):
            with open(MEMBERS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading team members: {str(e)}")
    return []


def save_team_members():
    try:
        with open(MEMBERS_FILE, 'w') as f:
            json.dump(st.session_state.team_members, f)
    except Exception as e:
        st.error(f"Error saving team members: {str(e)}")


def load_comments():
    try:
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading comments: {str(e)}")
    return {}


def save_comments():
    try:
        with open(COMMENTS_FILE, 'w') as f:
            json.dump(st.session_state.task_comments, f)
    except Exception as e:
        st.error(f"Error saving comments: {str(e)}")


def load_boss_credentials():
    try:
        if os.path.exists(BOSS_CREDENTIALS_FILE):
            with open(BOSS_CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading credentials: {str(e)}")
    return {"username": "admin", "password": "admin123"}


def save_boss_credentials(credentials):
    try:
        with open(BOSS_CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f)
    except Exception as e:
        st.error(f"Error saving credentials: {str(e)}")


def load_member_credentials():
    try:
        if os.path.exists(MEMBERS_CREDENTIALS_FILE):
            with open(MEMBERS_CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading member credentials: {str(e)}")
    return {}


def save_member_credentials():
    try:
        with open(MEMBERS_CREDENTIALS_FILE, 'w') as f:
            json.dump(st.session_state.member_credentials, f)
    except Exception as e:
        st.error(f"Error saving member credentials: {str(e)}")


def load_groups():
    try:
        if os.path.exists(GROUPS_FILE):
            with open(GROUPS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading groups: {str(e)}")
    return []


def save_groups():
    try:
        with open(GROUPS_FILE, 'w') as f:
            json.dump(st.session_state.groups, f)
    except Exception as e:
        st.error(f"Error saving groups: {str(e)}")


def load_group_messages():
    try:
        if os.path.exists(GROUP_MESSAGES_FILE):
            with open(GROUP_MESSAGES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading group messages: {str(e)}")
    return {}


def save_group_messages():
    try:
        with open(GROUP_MESSAGES_FILE, 'w') as f:
            json.dump(st.session_state.group_messages, f)
    except Exception as e:
        st.error(f"Error saving group messages: {str(e)}")


def load_notifications():
    try:
        if os.path.exists(NOTIFICATIONS_FILE):
            with open(NOTIFICATIONS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading notifications: {str(e)}")
    return {}


def save_notifications():
    try:
        with open(NOTIFICATIONS_FILE, 'w') as f:
            json.dump(st.session_state.notifications, f)
    except Exception as e:
        st.error(f"Error saving notifications: {str(e)}")


# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()
if 'team_members' not in st.session_state:
    st.session_state.team_members = load_team_members()
if 'task_comments' not in st.session_state:
    st.session_state.task_comments = load_comments()
if 'is_boss' not in st.session_state:
    st.session_state.is_boss = False
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'member_credentials' not in st.session_state:
    st.session_state.member_credentials = load_member_credentials()
if 'groups' not in st.session_state:
    st.session_state.groups = load_groups()
if 'group_messages' not in st.session_state:
    st.session_state.group_messages = load_group_messages()
if 'current_group' not in st.session_state:
    st.session_state.current_group = None
if 'notifications' not in st.session_state:
    st.session_state.notifications = load_notifications()
if 'page_history' not in st.session_state:
    st.session_state.page_history = []


def go_back():
    if st.session_state.page_history:
        previous_page = st.session_state.page_history.pop()
        if previous_page.get('type') == 'member':
            st.session_state.selected_member = previous_page.get('data')
        elif previous_page.get('type') == 'group':
            st.session_state.current_group = previous_page.get('data')
        else:
            st.session_state.selected_member = None
            st.session_state.current_group = None
    else:
        st.session_state.selected_member = None
        st.session_state.current_group = None
    st.rerun()


def show_back_button():
    if st.button("⬅️ Back", key="back_button", use_container_width=False):
        go_back()


def show_group_chat_management():
    st.sidebar.markdown("---")
    st.sidebar.header("👥 Group Chats")

    # Add Create Group feature
    if st.session_state.is_boss or st.session_state.logged_in_user in st.session_state.team_members:
        show_create_group()

    # Show available groups with notification indicators
    with st.sidebar.expander("💬 View Groups", expanded=False):
        available_groups = [
            group for group in st.session_state.groups
            if st.session_state.logged_in_user == "Boss" or
               st.session_state.logged_in_user in group['members']
        ]

        if not available_groups:
            st.info("No groups available")
        else:
            for group in available_groups:
                has_new_messages = group['id'] in st.session_state.notifications.get(
                    st.session_state.logged_in_user, {}).get('groups', {})
                col1, col2 = st.columns([3, 1])
                with col1:
                    button_label = f"💬 {group['title']} ({len(group['members'])} members)"
                    if has_new_messages:
                        button_label += " 🔴"
                    if st.button(button_label, key=f"group_{group['id']}"):
                        st.session_state.current_group = group
                        st.rerun()


def show_group_chat():
    if st.session_state.current_group:
        group = st.session_state.current_group
        group_id = group['id']

        # Clear notifications for this group when viewed
        if group_id in st.session_state.notifications.get(st.session_state.logged_in_user, {}).get('groups', {}):
            st.session_state.notifications[st.session_state.logged_in_user]['groups'].pop(group_id)
            save_notifications()

        # Group header
        st.header(f"💬 {group['title']}")
        with st.expander("👥 Group Info"):
            st.write("Members:", ", ".join(group['members']))
            st.write("Created by:", "Shammi Kapoor" if group['created_by'] == "Boss" else group['created_by'])
            st.write("Created at:", group['created_at'])

        st.divider()

        if group_id not in st.session_state.group_messages:
            st.session_state.group_messages[group_id] = []

        # Display messages
        for message in st.session_state.group_messages[group_id]:
            sender_name = "Shammi Kapoor" if message['sender'] == "Boss" else message['sender']
            with st.container():
                st.markdown(f"""
                <div style="
                    background-color: {'#e3f2fd' if message['sender'] == st.session_state.logged_in_user else '#f5f5f5'};
                    padding: 10px;
                    border-radius: 10px;
                    margin: 5px 0;
                ">
                    <div style="font-size: 0.8em; color: #666;">
                        {sender_name} - {message['timestamp']}
                    </div>
                    <div style="margin-top: 5px;">
                        {message['text']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Message input and notification handling
        with st.form(key="message_form", clear_on_submit=True):
            message_text = st.text_area("Type your message", key="message_input")
            if st.form_submit_button("Send"):
                if message_text:
                    new_message = {
                        'sender': st.session_state.logged_in_user,
                        'text': message_text,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    st.session_state.group_messages[group_id].append(new_message)

                    # Add notifications for all group members except sender
                    for member in group['members']:
                        if member != st.session_state.logged_in_user:
                            if member not in st.session_state.notifications:
                                st.session_state.notifications[member] = {'groups': {}, 'tasks': {}}
                            if 'groups' not in st.session_state.notifications[member]:
                                st.session_state.notifications[member]['groups'] = {}
                            st.session_state.notifications[member]['groups'][group_id] = True

                    save_group_messages()
                    save_notifications()
                    st.rerun()


def show_create_group():
    st.sidebar.markdown("---")
    with st.sidebar.expander("➕ Create New Group", expanded=False):
        with st.form("create_group_form", clear_on_submit=True):
            group_title = st.text_input("Group Title", placeholder="e.g., Project A Team")

            # Allow selecting multiple members
            available_members = st.session_state.team_members.copy()
            if not st.session_state.is_boss:
                available_members = [m for m in available_members if m != st.session_state.logged_in_user]

            selected_members = st.multiselect(
                "Select Members",
                options=available_members,
                default=None
            )

            # Always include the current user in the group
            if not st.session_state.is_boss and st.session_state.logged_in_user not in selected_members:
                selected_members.append(st.session_state.logged_in_user)

            if st.form_submit_button("Create Group"):
                if not group_title:
                    st.error("Please provide a group title!")
                elif not selected_members:
                    st.error("Please select at least one member!")
                else:
                    new_group = {
                        'id': str(uuid.uuid4()),
                        'title': group_title,
                        'members': selected_members,
                        'created_by': st.session_state.logged_in_user,
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    st.session_state.groups.append(new_group)
                    save_groups()
                    st.success(f"✅ Group '{group_title}' created successfully!")
                    st.rerun()


# Login Page
def show_login():
    st.markdown("""
        <div class="login-container">
            <h1 style='text-align: center; margin-bottom: 2rem;'>📋 Task Management</h1>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        login_type = st.radio("Select Login Type:", ["Boss", "Team Member"])

        with st.form("login_form"):
            if login_type == "Boss":
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
            else:
                username = st.selectbox("Select Your Name", st.session_state.team_members)
                password = st.text_input("Password", type="password")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            boss_credentials = load_boss_credentials()
            if login_type == "Boss":
                if username == boss_credentials["username"] and password == boss_credentials["password"]:
                    st.session_state.is_boss = True
                    st.session_state.logged_in_user = "Boss"
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
            else:
                # Check member credentials
                if username in st.session_state.member_credentials:
                    if password == st.session_state.member_credentials[username]:
                        st.session_state.is_boss = False
                        st.session_state.logged_in_user = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid password!")
                else:
                    st.error("Member not found or password not set!")


def show_boss_team_management():
    with st.sidebar:
        st.header('👥 Team Management')

        # Display team members count
        member_count = len(st.session_state.team_members)
        st.markdown(f"### Team Members <span class='member-count'>{member_count}</span>",
                    unsafe_allow_html=True)

        # Add Team Member expander
        with st.expander("➕ Add Team Member", expanded=False):
            with st.form("add_member_form", clear_on_submit=True):
                new_member = st.text_input("Enter member name",
                                           placeholder="e.g., John Smith")
                member_password = st.text_input("Set member password",
                                                type="password",
                                                help="Set a password for this team member")
                confirm_password = st.text_input("Confirm password",
                                                 type="password")

                add_member = st.form_submit_button("Add Member")

                if add_member:
                    if not new_member or not member_password:
                        st.error("Please provide both name and password!")
                    elif member_password != confirm_password:
                        st.error("Passwords do not match!")
                    elif new_member in st.session_state.team_members:
                        st.error("⚠️ Member already exists!")
                    else:
                        st.session_state.team_members.insert(0, new_member)
                        st.session_state.member_credentials[new_member] = member_password
                        save_team_members()
                        save_member_credentials()
                        st.success(f"✅ Added {new_member} to the team!")

        # Team Members List in an expander
        with st.expander("👥 View Team Members", expanded=False):
            if not st.session_state.team_members:
                st.info("No team members added yet.")
            else:
                for member in st.session_state.team_members:
                    col1, col2 = st.columns([3, 1])
                    pending_tasks = len([task for task in st.session_state.tasks
                                         if task['assignee'] == member and
                                         task['status'] != 'Completed'])

                    with col1:
                        if st.button(f"👤 {member} ({pending_tasks} pending)",
                                     key=f"select_{member}"):
                            st.session_state.selected_member = member

                    with col2:
                        if st.button("🔑", key=f"reset_pass_{member}"):
                            st.session_state.member_to_reset = member

        # Password reset form
        if 'member_to_reset' in st.session_state:
            with st.form(key="reset_password_form"):
                st.subheader(f"Reset Password for {st.session_state.member_to_reset}")
                new_password = st.text_input("New password", type="password")
                confirm_new_password = st.text_input("Confirm new password", type="password")

                if st.form_submit_button("Reset Password"):
                    if not new_password:
                        st.error("Please enter a new password!")
                    elif new_password != confirm_new_password:
                        st.error("Passwords do not match!")
                    else:
                        st.session_state.member_credentials[st.session_state.member_to_reset] = new_password
                        save_member_credentials()
                        del st.session_state.member_to_reset
                        st.success("✅ Password reset successfully!")
                        st.rerun()


def show_group_list():
    st.header("💬 Group Chats")

    user = st.session_state.logged_in_user
    user_notifications = st.session_state.notifications.get(user, {})

    # Display available groups in a grid
    cols = st.columns(3)
    available_groups = [
        group for group in st.session_state.groups
        if user == "Boss" or user in group['members']
    ]

    if not available_groups:
        st.info("No groups available. Create a new group from the sidebar.")
    else:
        for idx, group in enumerate(available_groups):
            col = cols[idx % 3]
            with col:
                has_new_messages = group['id'] in user_notifications.get('groups', {})
                card_content = f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 5px 0;
                    background-color: {'#e3f2fd' if has_new_messages else 'white'};
                    cursor: pointer;
                ">
                    <h4>{group['title']}</h4>
                    <p style="font-size: 0.8em; color: #666;">
                        {len(group['members'])} members
                    </p>
                </div>
                """
                st.markdown(card_content, unsafe_allow_html=True)

                if st.button("Open Chat", key=f"open_group_{group['id']}"):
                    st.session_state.current_group = group
                    st.rerun()


# Main App
def show_app():
    if st.session_state.is_boss and 'selected_member' in st.session_state:
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button("⬅️", help="Back to Team Overview"):
                del st.session_state.selected_member
                st.rerun()
        with col2:
            st.title('📋 Team Task Management System')
    else:
        st.title('📋 Team Task Management System')

    # Add group chat management to sidebar
    show_group_chat_management()

    # Main content area tabs
    tab1, tab2 = st.tabs(["Tasks", "Group Chat"])

    with tab1:
        if st.session_state.is_boss:
            show_boss_team_management()
            if 'selected_member' in st.session_state:
                show_member_dashboard(st.session_state.selected_member)
            else:
                st.header("📊 Team Overview")
                show_team_overview()
        else:
            show_member_dashboard(st.session_state.logged_in_user, is_personal=True)

    with tab2:
        if st.session_state.current_group:
            show_group_chat()
        else:
            show_group_list()

    # Add logout button at the bottom of the sidebar
    with st.sidebar:
        st.markdown("---")  # Add a separator
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            st.session_state.is_boss = False
            st.session_state.logged_in_user = None
            st.rerun()


def show_team_overview():
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([task for task in st.session_state.tasks if task['status'] == 'Completed'])
    pending_tasks = total_tasks - completed_tasks

    # Create three columns for vertical metrics
    col1, col2, col3 = st.columns(3)

    # Define metrics
    metrics = [
        {"label": "Total Tasks", "value": total_tasks, "icon": "📊"},
        {"label": "Completed", "value": completed_tasks, "icon": "✅"},
        {"label": "Pending", "value": pending_tasks, "icon": "⏳"}
    ]

    # Custom CSS for vertical metric cards
    st.markdown("""
        <style>
        .vertical-metric {
            background: white;
            border-radius: 8px;
            padding: 1.2rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
            border: 1px solid #f0f0f0;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .vertical-metric:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .metric-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #1890ff;
            margin: 0.5rem 0;
        }
        .metric-label {
            color: #666;
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display metrics in columns
    for col, metric in zip([col1, col2, col3], metrics):
        with col:
            st.markdown(f"""
                <div class="vertical-metric">
                    <div class="metric-icon">{metric['icon']}</div>
                    <div class="metric-value">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Show all tasks grouped by member
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("All Tasks by Member")
    for member in st.session_state.team_members:
        member_tasks = [task for task in st.session_state.tasks
                       if task['assignee'] == member]
        if member_tasks:
            st.markdown(f"### 👤 {member} ({len(member_tasks)} tasks)")
            show_tasks_list(member_tasks)
            st.divider()

def show_member_dashboard(member, is_personal=False):
    # Add Home button at the top

    st.markdown(f"### 👤 {member}'s Dashboard")

    # Get member's tasks
    member_tasks = [task for task in st.session_state.tasks
                    if task['assignee'] == member]

    # Show statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", len(member_tasks))
    with col2:
        completed = len([t for t in member_tasks if t['status'] == 'Completed'])
        st.metric("Completed", completed)
    with col3:
        st.metric("Pending", len(member_tasks) - completed)

    st.divider()

    # Task management section
    tab1, tab2 = st.tabs(["📝 Tasks", "➕ New Task"])

    with tab1:
        show_tasks_list(member_tasks, is_personal)

    with tab2:
        if st.session_state.is_boss:  # Only boss can create new tasks
            show_new_task_form(member)
        else:
            st.info("Only the boss can assign new tasks.")


def show_tasks_list(tasks, is_personal=False):
    if not tasks:
        st.info("No tasks assigned yet.")
        return

    sorted_tasks = sorted(tasks,
                          key=lambda x: datetime.strptime(x['assigned_date'], '%Y-%m-%d'),
                          reverse=True)

    for task in sorted_tasks:
        task_id = str(task['id'])
        has_new_comments = False

        # Check for new comments
        if st.session_state.logged_in_user in st.session_state.notifications:
            if task_id in st.session_state.notifications[st.session_state.logged_in_user].get('tasks', {}):
                has_new_comments = True

        status_class = {
            'Completed': 'task-header-completed',
            'Pending': 'task-header-pending',
            'In Progress': 'task-header-inprogress',
            'Need Follow-up': 'task-header-followup'
        }[task['status']]

        # Add notification indicator to task header if there are new comments
        task_header = f"🔍 {task['task']} ({task['due_date']})"
        if has_new_comments:
            task_header += " 🔴"

        with st.expander(task_header):
            # Clear notification when task is opened
            if has_new_comments:
                st.session_state.notifications[st.session_state.logged_in_user]['tasks'].pop(task_id)
                save_notifications()

            st.markdown(f"""
                <div class="{status_class}" style="margin-bottom: 15px;">
                    {task['status']}
                </div>
            """, unsafe_allow_html=True)

            # Task details
            col1, col2 = st.columns(2)
            with col1:
                st.write("📅 Assigned date:", task['assigned_date'])
                assigned_by = "Shammi Kapoor" if task['assigned_by'] == "Boss" else task['assigned_by']
                st.write("👤 Assigned by:", assigned_by)
            with col2:
                st.write("⏳ Due date:", task['due_date'])
                st.write("👤 Assigned to:", task['assignee'])

            # Status update section for personal tasks or boss
            if is_personal or st.session_state.is_boss:
                current_status = task['status']
                new_status = st.selectbox(
                    "Update Status",
                    ['Pending', 'In Progress', 'Completed', 'Need Follow-up'],
                    index=['Pending', 'In Progress', 'Completed', 'Need Follow-up'].index(current_status),
                    key=f"status_{task['id']}"
                )

                if new_status != current_status:
                    task['status'] = new_status
                    save_tasks()
                    st.success("Status updated!")
                    st.rerun()

            # Comments section
            st.markdown("### 💬 Comments")

            # Display existing comments
            if task_id in st.session_state.task_comments:
                for comment in st.session_state.task_comments[task_id]:
                    st.markdown(f"""
                        <div style="
                            background-color: #f0f2f5;
                            padding: 10px;
                            border-radius: 8px;
                            margin: 5px 0;
                        ">
                            <div style="font-size: 0.8em; color: #666;">
                                {comment['author']} - {comment['timestamp']}
                            </div>
                            <div style="margin-top: 5px;">
                                {comment['text']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No comments yet.")

            # Add comment form
            if st.session_state.is_boss or is_personal:
                with st.form(key=f"comment_form_{task['id']}", clear_on_submit=True):
                    comment_text = st.text_area("Add a comment", key=f"comment_{task['id']}")
                    if st.form_submit_button("Post Comment"):
                        if comment_text:
                            if task_id not in st.session_state.task_comments:
                                st.session_state.task_comments[task_id] = []

                            new_comment = {
                                'author': "Shammi Kapoor" if st.session_state.logged_in_user == "Boss" else st.session_state.logged_in_user,
                                'text': comment_text,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                            }

                            st.session_state.task_comments[task_id].append(new_comment)

                            # Add notification for task assignee or boss
                            notify_user = task['assignee'] if st.session_state.logged_in_user == "Boss" else "Boss"
                            if notify_user not in st.session_state.notifications:
                                st.session_state.notifications[notify_user] = {'groups': {}, 'tasks': {}}
                            if 'tasks' not in st.session_state.notifications[notify_user]:
                                st.session_state.notifications[notify_user]['tasks'] = {}
                            st.session_state.notifications[notify_user]['tasks'][task_id] = True

                            save_comments()
                            save_notifications()
                            st.success("💬 Comment added!")
                            st.rerun()


def show_new_task_form(member):
    with st.form("new_task_form", clear_on_submit=True):
        st.text_area("Task Description", key="task_description",
                     placeholder="Enter detailed task description...")

        col1, col2 = st.columns(2)
        with col1:
            due_date = st.date_input(
                "Due Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=7),
                key="due_date"
            )

        if st.form_submit_button("Assign Task"):
            task_description = st.session_state.task_description
            if task_description:
                new_task = {
                    'id': len(st.session_state.tasks),
                    'assignee': member,
                    'task': task_description,
                    'assigned_by': "Boss",
                    'assigned_date': datetime.now().strftime('%Y-%m-%d'),
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'status': 'Pending'
                }
                st.session_state.tasks.insert(0, new_task)
                save_tasks()
                st.success("✅ Task assigned successfully!")
                st.rerun()
            else:
                st.error("⚠️ Please enter a task description")


def add_custom_css():
    st.markdown("""
    <style>
    /* Existing CSS styles remain unchanged */

    /* Add styles for the expander sections */
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 5px;
    }

    .streamlit-expanderHeader:hover {
        background-color: #e8eaed;
    }

    /* Style for the content inside expanders */
    .streamlit-expanderContent {
        border-left: 1px solid #ddd;
        margin-left: 10px;
        padding-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# Main app flow
if __name__ == "__main__":
    add_custom_css()
    if not st.session_state.logged_in_user:
        show_login()
    else:
        show_app()