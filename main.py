import streamlit as st
import pandas as pd
from firebase_config import firebase_auth
from admin_pages import show_admin_interface

# Page configuration
st.set_page_config(
    page_title="Skill Swap Platform",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .user-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #1f2937;
    }
    .user-card h3, .user-card h4 {
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .user-card p {
        color: #374151;
        margin-bottom: 0.25rem;
    }
    .skill-tag {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
        font-weight: 500;
        border: 1px solid #3b82f6;
    }
    .skill-tag-wanted {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #22c55e;
    }
    .request-card {
        background: #fff7ed;
        border: 2px solid #fed7aa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #1f2937;
    }
    .request-card h4 {
        color: #92400e;
        margin-bottom: 0.5rem;
    }
    .request-card p {
        color: #451a03;
        margin-bottom: 0.25rem;
    }
    .status-pending {
        background: #fef3c7;
        color: #92400e;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid #f59e0b;
    }
    .status-accepted {
        background: #d1fae5;
        color: #047857;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid #10b981;
    }
    .status-rejected {
        background: #fee2e2;
        color: #dc2626;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid #ef4444;
    }
    .admin-notice {
        background: #fef2f2;
        border: 2px solid #fca5a5;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #dc2626;
    }
    .debug-info {
        background: #f3f4f6;
        border: 1px solid #d1d5db;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #374151;
        font-size: 0.8rem;
    }
    /* Fix white text issues */
    .stMarkdown, .stText {
        color: #1f2937 !important;
    }
    .element-container p {
        color: #374151 !important;
    }
    /* Make sure all text is readable */
    * {
        color: inherit;
    }
    .main .block-container {
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Firebase
firebase_auth.initialize()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def show_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🔄 Skill Swap Platform</h1>
        <p style="color: #bfdbfe; margin: 0; font-size: 1.2rem;">Connect, Learn, and Share Skills</p>
    </div>
    """, unsafe_allow_html=True)

def show_navigation():
   
    """Display navigation"""
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    with col1:
        if st.button("🏠 Home", use_container_width=True):
            if st.session_state.current_page != 'home':
                st.session_state.current_page = 'home'
                st.rerun()

    with col2:
        if st.button("🎯 Browse Users", use_container_width=True):
            if st.session_state.current_page != 'browse':
                st.session_state.current_page = 'browse'
                st.rerun()

    with col3:
        if st.session_state.user:
            if st.button("👤 Profile", use_container_width=True):
                if st.session_state.current_page != 'profile':
                    st.session_state.current_page = 'profile'
                    st.rerun()

    with col4:
        if st.session_state.user:
            if st.button("📋 My Requests", use_container_width=True):
                if st.session_state.current_page != 'requests':
                    st.session_state.current_page = 'requests'
                    st.rerun()

    with col5:
        if st.session_state.user:
            if st.button("🔄 Transactions", use_container_width=True):
                if st.session_state.current_page != 'transactions':
                    st.session_state.current_page = 'transactions'
                    st.rerun()

    with col6:
        if st.session_state.user and st.session_state.user_profile and st.session_state.user_profile.get('role') == 'admin':
            if st.button("⚙️ Admin", use_container_width=True):
                if st.session_state.current_page != 'admin':
                    st.session_state.current_page = 'admin'
                    st.rerun()

    with col7:
        if st.session_state.user:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.user_profile = None
                st.session_state.current_page = 'home'
                st.success("Logged out successfully!")
                st.rerun()
        else:
            if st.button("🔑 Login", use_container_width=True):
                if st.session_state.current_page != 'auth':
                    st.session_state.current_page = 'auth'
                    st.rerun()


def auth_page():
    """Authentication page"""
    st.subheader("🔑 Welcome to Skill Swap Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.write("**Sign in to your account**")
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("🚀 Login", use_container_width=True):
                    if email and password:
                        with st.spinner("Signing in..."):
                            result = firebase_auth.login_user(email, password)
                        
                        if result['success']:
                            st.session_state.user = result['user']
                            st.session_state.user_profile = result['profile']
                            st.session_state.current_page = 'home'
                            
                            # Debug: Show user role
                            user_role = result['profile'].get('role', 'user')
                            st.success(f"✅ Login successful! Role: {user_role}")
                            
                            # Admin check
                            if user_role == 'admin':
                                st.success("👑 Admin privileges detected!")
                            
                            st.rerun()
                        else:
                            st.error(f"❌ {result['error']}")
                    else:
                        st.error("❌ Please fill in all fields")
            
            with col2:
                if st.form_submit_button("🏠 Back to Home", use_container_width=True):
                    st.session_state.current_page = 'home'
                    st.rerun()
    
    with tab2:
        st.write("**Create your account**")
        with st.form("register_form"):
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Create password (min 6 chars)")
            location = st.text_input("📍 Location (Optional)", placeholder="City, Country")
            
            if st.form_submit_button("📝 Create Account", use_container_width=True):
                if name and email and password:
                    if len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        with st.spinner("Creating account..."):
                            result = firebase_auth.register_user(email, password, name, location)
                        
                        if result['success']:
                            st.success("✅ Account created successfully! Please login above.")
                        else:
                            st.error(f"❌ {result['error']}")
                else:
                    st.error("❌ Please fill in all required fields")

def home_page():
    """Home page"""
    if st.session_state.user:
        profile = st.session_state.user_profile
        st.subheader(f"👋 Welcome back, {profile['name']}!")
        
        # Debug info for admin
        with st.expander("🔧 Debug Info (Admin Check)"):
            st.markdown(f"""
            <div class="debug-info">
            <strong>User ID:</strong> {st.session_state.user.get('localId', 'N/A')}<br>
            <strong>Email:</strong> {profile.get('email', 'N/A')}<br>
            <strong>Current Role:</strong> {profile.get('role', 'user')}<br>
            <strong>Is Admin:</strong> {profile.get('role') == 'admin'}<br>
            <strong>Profile Keys:</strong> {list(profile.keys())}
            </div>
            """, unsafe_allow_html=True)
            
            # Quick admin promotion for testing
            if profile.get('role') != 'admin':
                if st.button("🔧 Make Me Admin (Dev Only)"):
                    result = firebase_auth.update_user_profile(
                        st.session_state.user['localId'],
                        {'role': 'admin'}
                    )
                    if result['success']:
                        st.session_state.user_profile['role'] = 'admin'
                        st.success("👑 You are now an admin! Refresh to see admin button.")
                        st.rerun()
        
        # User stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # Get user skills count
            skills_result = firebase_auth.get_user_skills(st.session_state.user['localId'])
            offered_count = len([s for s in skills_result.get('skills', []) if s['type'] == 'offered']) if skills_result['success'] else 0
            st.metric("🎯 Skills Offered", offered_count)
        
        with col2:
            wanted_count = len([s for s in skills_result.get('skills', []) if s['type'] == 'wanted']) if skills_result['success'] else 0
            st.metric("📚 Skills Wanted", wanted_count)
        
        with col3:
            st.metric("⭐ Rating", f"{profile.get('rating_avg', 0)}/5")
        
        with col4:
            st.metric("🔄 Total Swaps", profile.get('total_swaps', 0))
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎯 Add Skills", use_container_width=True):
                st.session_state.current_page = 'profile'
                st.rerun()
        
        with col2:
            if st.button("👥 Browse Users", use_container_width=True):
                st.session_state.current_page = 'browse'
                st.rerun()
        
        with col3:
            if st.button("📋 View Requests", use_container_width=True):
                st.session_state.current_page = 'requests'
                st.rerun()
        
        # System messages
        messages_result = firebase_auth.get_active_messages()
        if messages_result['success'] and messages_result['messages']:
            st.markdown("---")
            st.subheader("📢 Platform Updates")
            for msg in messages_result['messages'][:2]:
                st.info(f"**{msg['title']}**: {msg['message']}")
    
    else:
        st.subheader("🌟 Connect, Learn, and Grow Together")
        st.markdown("""
        <div class="user-card">
            <h3>Welcome to Skill Swap Platform!</h3>
            <p>Join our community to exchange skills and knowledge with others around the world!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Get Started - Sign Up", use_container_width=True, type="primary"):
                st.session_state.current_page = 'auth'
                st.rerun()
        
        with col2:
            if st.button("👥 Browse Community", use_container_width=True):
                st.session_state.current_page = 'browse'
                st.rerun()

def browse_users_page():
    """Browse users page"""
    st.subheader("👥 Browse Skill Swappers")
    
    # Get public users
    users_result = firebase_auth.get_public_users(50)
    
    if users_result['success']:
        users = users_result['users']
        
        if users:
            # Search and filter
            col1, col2 = st.columns([3, 1])
            with col1:
                search_term = st.text_input("🔍 Search by name or location")
            with col2:
                availability_filter = st.selectbox("📅 Availability", ["All", "weekends", "evenings", "flexible", "anytime"])
            
            # Filter users
            filtered_users = users
            if search_term:
                filtered_users = [u for u in filtered_users if
                                search_term.lower() in u.get('name', '').lower() or
                                search_term.lower() in u.get('location', '').lower()]
            if availability_filter != "All":
                filtered_users = [u for u in filtered_users if u.get('availability') == availability_filter]
            
            # Display users
            for user in filtered_users:
                # Get user skills
                skills_result = firebase_auth.get_user_skills(user['user_id'])
                offered_skills = [s['skill_name'] for s in skills_result.get('skills', []) if s['type'] == 'offered'] if skills_result['success'] else []
                wanted_skills = [s['skill_name'] for s in skills_result.get('skills', []) if s['type'] == 'wanted'] if skills_result['success'] else []
                
                with st.container():
                    st.markdown(f"""
                    <div class="user-card">
                        <h3>👤 {user['name']}</h3>
                        <p>📍 {user.get('location', 'Location not specified')}</p>
                        <p>📅 Available: {user.get('availability', 'Not specified')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([3, 3, 1])
                    
                    with col1:
                        st.write("**🎯 Skills Offered:**")
                        if offered_skills:
                            skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in offered_skills])
                            st.markdown(skills_html, unsafe_allow_html=True)
                        else:
                            st.write("No skills offered yet")
                    
                    with col2:
                        st.write("**📚 Skills Wanted:**")
                        if wanted_skills:
                            skills_html = "".join([f'<span class="skill-tag skill-tag-wanted">{skill}</span>' for skill in wanted_skills])
                            st.markdown(skills_html, unsafe_allow_html=True)
                        else:
                            st.write("No skills wanted yet")
                    
                    with col3:
                        rating = user.get('rating_avg', 0)
                        count = user.get('rating_count', 0)
                        st.write(f"⭐ {rating}/5.0")
                        st.write(f"({count} reviews)")
                        
                        if st.session_state.user and st.session_state.user['localId'] != user['user_id']:
                            if st.button(f"🤝 Request Swap", key=f"request_{user['user_id']}"):
                                st.session_state.selected_user = user
                                st.session_state.current_page = 'request_form'
                                st.rerun()
        else:
            st.info("No users found. Be the first to join!")
    else:
        st.error(f"Failed to load users: {users_result.get('error', 'Unknown error')}")

def profile_page():
    """User profile management"""
    if not st.session_state.user:
        st.error("Please login to view your profile")
        return
    
    st.subheader("👤 My Profile")
    
    user_id = st.session_state.user['localId']
    profile = st.session_state.user_profile
    
    # Profile information
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📋 Profile Information**")
        with st.form("profile_form"):
            name = st.text_input("Full Name", value=profile.get('name', ''))
            location = st.text_input("Location", value=profile.get('location', ''))
            availability = st.selectbox(
                "Availability",
                ["weekends", "evenings", "flexible", "anytime"],
                index=["weekends", "evenings", "flexible", "anytime"].index(profile.get('availability', 'weekends'))
            )
            profile_visibility = st.selectbox(
                "Profile Visibility",
                ["public", "private"],
                index=0 if profile.get('profile_visibility') == 'public' else 1
            )
            
            if st.form_submit_button("💾 Update Profile"):
                updates = {
                    'name': name,
                    'location': location,
                    'availability': availability,
                    'profile_visibility': profile_visibility
                }
                
                result = firebase_auth.update_user_profile(user_id, updates)
                if result['success']:
                    st.session_state.user_profile.update(updates)
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result['error']}")
    
    with col2:
        st.write("**🎯 Manage Skills**")
        
        # Add new skill
        with st.form("add_skill_form"):
            skill_name = st.text_input("Skill Name", placeholder="e.g., Python Programming")
            skill_type = st.radio("Skill Type", ["offered", "wanted"])
            proficiency = st.selectbox("Proficiency Level", ["beginner", "intermediate", "advanced", "expert"])
            description = st.text_area("Description (Optional)", placeholder="Brief description of your experience...")
            
            if st.form_submit_button("➕ Add Skill"):
                if skill_name:
                    result = firebase_auth.add_user_skill(user_id, skill_name, skill_type, proficiency, description)
                    if result['success']:
                        st.success("✅ Skill added successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result['error']}")
                else:
                    st.error("❌ Please enter a skill name")
    
    # Display current skills
    st.markdown("---")
    st.subheader("📚 My Current Skills")
    
    skills_result = firebase_auth.get_user_skills(user_id)
    if skills_result['success']:
        skills = skills_result['skills']
        
        if skills:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🎯 Skills I Offer:**")
                offered_skills = [s for s in skills if s['type'] == 'offered']
                for skill in offered_skills:
                    st.markdown(f"""
                    <div class="skill-tag">
                        {skill['skill_name']} ({skill['proficiency_level']})
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🗑️ Remove", key=f"remove_offered_{skill['skill_name']}"):
                        result = firebase_auth.remove_user_skill(user_id, skill['skill_name'], 'offered')
                        if result['success']:
                            st.success("Skill removed!")
                            st.rerun()
            
            with col2:
                st.write("**📚 Skills I Want:**")
                wanted_skills = [s for s in skills if s['type'] == 'wanted']
                for skill in wanted_skills:
                    st.markdown(f"""
                    <div class="skill-tag skill-tag-wanted">
                        {skill['skill_name']} ({skill['proficiency_level']})
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🗑️ Remove", key=f"remove_wanted_{skill['skill_name']}"):
                        result = firebase_auth.remove_user_skill(user_id, skill['skill_name'], 'wanted')
                        if result['success']:
                            st.success("Skill removed!")
                            st.rerun()
        else:
            st.info("No skills added yet. Add some skills above!")
    else:
        st.error(f"Failed to load skills: {skills_result.get('error', 'Unknown error')}")

def requests_page():
    """Manage barter requests"""
    if not st.session_state.user:
        st.error("Please login to view requests")
        return
    
    st.subheader("📋 My Skill Swap Requests")
    
    user_id = st.session_state.user['localId']
    requests_result = firebase_auth.get_user_requests(user_id)
    
    if requests_result['success']:
        requests = requests_result['requests']
        
        if requests:
            # Separate sent and received requests
            sent_requests = [r for r in requests if r['type'] == 'sent']
            received_requests = [r for r in requests if r['type'] == 'received']
            
            tab1, tab2 = st.tabs([f"📤 Sent ({len(sent_requests)})", f"📥 Received ({len(received_requests)})"])
            
            with tab1:
                if sent_requests:
                    for req in sent_requests:
                        render_request_card(req, is_sender=True)
                else:
                    st.info("No sent requests")
            
            with tab2:
                if received_requests:
                    for req in received_requests:
                        render_request_card(req, is_sender=False)
                else:
                    st.info("No received requests")
        else:
            st.info("No requests yet. Start by browsing users and requesting skill swaps!")
    else:
        st.error(f"Failed to load requests: {requests_result.get('error', 'Unknown error')}")

def render_request_card(req, is_sender):
    """Render a request card"""
    status_class = f"status-{req['status']}"
    
    with st.container():
        st.markdown(f"""
        <div class="request-card">
            <h4>{'📤 Request to' if is_sender else '📥 Request from'}: User</h4>
            <p><strong>Skills:</strong> {req['offered_skill_name']} ↔️ {req['requested_skill_name']}</p>
            <p><strong>Status:</strong> <span class="{status_class}">{req['status'].upper()}</span></p>
            <p><strong>Message:</strong> {req.get('message', 'No message')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        if not is_sender and req['status'] == 'pending':
            with col1:
                if st.button(f"✅ Accept", key=f"accept_{req['request_id']}"):
                    result = firebase_auth.update_request_status(req['request_id'], 'accepted')
                    if result['success']:
                        st.success("Request accepted!")
                        st.rerun()
            
            with col2:
                if st.button(f"❌ Reject", key=f"reject_{req['request_id']}"):
                    result = firebase_auth.update_request_status(req['request_id'], 'rejected')
                    if result['success']:
                        st.success("Request rejected!")
                        st.rerun()

def transactions_page():
    """View transactions"""
    if not st.session_state.user:
        st.error("Please login to view transactions")
        return
    
    st.subheader("🔄 My Transactions")
    
    user_id = st.session_state.user['localId']
    transactions_result = firebase_auth.get_user_transactions(user_id)
    
    if transactions_result['success']:
        transactions = transactions_result['transactions']
        
        if transactions:
            for trans in transactions:
                st.markdown(f"""
                <div class="user-card">
                    <h4>🔄 Transaction: {trans['user1_skill']} ↔️ {trans['user2_skill']}</h4>
                    <p><strong>Status:</strong> {trans['status']}</p>
                    <p><strong>Progress:</strong> {trans['completion_percentage']}%</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No transactions yet. Accept some swap requests to start!")
    else:
        st.error(f"Failed to load transactions: {transactions_result.get('error', 'Unknown error')}")

def request_form_page():
    """Create swap request form"""
    if 'selected_user' not in st.session_state:
        st.error("No user selected")
        return
    
    user = st.session_state.selected_user
    st.subheader(f"🤝 Request Skill Swap with {user['name']}")
    
    # Get current user's offered skills
    user_id = st.session_state.user['localId']
    skills_result = firebase_auth.get_user_skills(user_id, 'offered')
    my_skills = [s['skill_name'] for s in skills_result.get('skills', [])] if skills_result['success'] else []
    
    # Get target user's offered skills
    target_skills_result = firebase_auth.get_user_skills(user['user_id'], 'offered')
    target_skills = [s['skill_name'] for s in target_skills_result.get('skills', [])] if target_skills_result['success'] else []
    
    with st.form("swap_request_form"):
        if not my_skills:
            st.error("You need to add skills to your profile first!")
            if st.form_submit_button("📝 Go to Profile"):
                st.session_state.current_page = 'profile'
                st.rerun()
            return
        
        offered_skill = st.selectbox("🎯 Your skill to offer:", my_skills)
        requested_skill = st.selectbox("📚 Skill you want to learn:", target_skills)
        message = st.text_area("💬 Message:", placeholder="Introduce yourself and explain what you'd like to learn...")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("📤 Send Request", use_container_width=True):
                if offered_skill and requested_skill:
                    result = firebase_auth.create_barter_request(
                        user_id, user['user_id'], offered_skill, requested_skill, message
                    )
                    if result['success']:
                        st.success("Request sent successfully!")
                        st.session_state.current_page = 'requests'
                        del st.session_state.selected_user
                        st.rerun()
                    else:
                        st.error(f"Failed to send request: {result.get('error', 'Unknown error')}")
                else:
                    st.error("Please select both skills")
        
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.session_state.current_page = 'browse'
                del st.session_state.selected_user
                st.rerun()

def main():
    """Main application"""
    show_header()
    show_navigation()
    
    st.markdown("---")
    
    # Route to different pages
    if st.session_state.current_page == 'auth':
        auth_page()
    elif st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'browse':
        browse_users_page()
    elif st.session_state.current_page == 'profile':
        profile_page()
    elif st.session_state.current_page == 'requests':
        requests_page()
    elif st.session_state.current_page == 'transactions':
        transactions_page()
    elif st.session_state.current_page == 'request_form':
        request_form_page()
    elif st.session_state.current_page == 'admin':
        show_admin_interface()

if __name__ == "__main__":
    main()
