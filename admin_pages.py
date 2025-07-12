import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from firebase_config import firebase_auth

def check_admin_access():
    """Check if current user is admin"""
    if not st.session_state.user or not st.session_state.user_profile:
        st.error("🔒 Please login to access this page")
        st.stop()
    
    if st.session_state.user_profile.get('role') != 'admin':
        st.error("⚠️ Admin access required")
        st.info("Contact an administrator to get admin privileges")
        st.stop()

def admin_dashboard():
    """Main admin dashboard"""
    check_admin_access()
    
    st.subheader("⚙️ Admin Dashboard")
    
    # Welcome message
    admin_name = st.session_state.user_profile.get('name', 'Admin')
    st.success(f"👑 Welcome, {admin_name}! You have admin privileges.")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    # Get platform statistics
    users_result = firebase_auth.get_public_users(1000)
    total_users = len(users_result.get('users', [])) if users_result['success'] else 0
    
    skills_result = firebase_auth.get_all_skills()
    total_skills = len(skills_result.get('skills', [])) if skills_result['success'] else 0
    
    with col1:
        st.metric("👥 Total Users", total_users)
    
    with col2:
        st.metric("🎯 Total Skills", total_skills)
    
    with col3:
        st.metric("🔄 Active Swaps", "Coming Soon")
    
    with col4:
        st.metric("📋 Pending Reviews", "Coming Soon")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📢 Send Platform Message", use_container_width=True):
            st.session_state.admin_action = 'send_message'
            st.rerun()
    
    with col2:
        if st.button("🔧 Setup Sample Data", use_container_width=True):
            with st.spinner("Setting up sample data..."):
                result = firebase_auth.setup_sample_data()
            if result['success']:
                st.success("✅ Sample data created successfully!")
                st.rerun()
            else:
                st.error(f"❌ Error: {result['error']}")
    
    with col3:
        if st.button("📊 Generate Report", use_container_width=True):
            st.session_state.admin_action = 'generate_report'
            st.rerun()
    
    # Show recent activity
    st.markdown("---")
    st.subheader("📈 Recent Activity")
    
    if users_result['success'] and users_result['users']:
        recent_users = sorted(users_result['users'],
                            key=lambda x: x.get('created_at', ''), reverse=True)[:5]
        
        st.write("**🆕 Recent User Registrations:**")
        for user in recent_users:
            st.write(f"• {user['name']} ({user['email']}) - {user.get('created_at', 'Unknown date')}")

def admin_users_management():
    """User management interface"""
    check_admin_access()
    
    st.subheader("👥 User Management")
    
    # Get all users
    users_result = firebase_auth.get_public_users(1000)
    
    if users_result['success']:
        users = users_result['users']
        
        if users:
            # Search and filter
            col1, col2 = st.columns([3, 1])
            with col1:
                search_term = st.text_input("🔍 Search users", placeholder="Search by name or email")
            with col2:
                role_filter = st.selectbox("👑 Role Filter", ["All", "user", "admin"])
            
            # Filter users
            filtered_users = users
            if search_term:
                filtered_users = [u for u in filtered_users if
                                search_term.lower() in u.get('name', '').lower() or
                                search_term.lower() in u.get('email', '').lower()]
            if role_filter != "All":
                filtered_users = [u for u in filtered_users if u.get('role') == role_filter]
            
            # Display users
            st.write(f"**Found {len(filtered_users)} users**")
            
            for user in filtered_users:
                with st.expander(f"👤 {user['name']} ({user['email']})"):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**📧 Email:** {user['email']}")
                        st.write(f"**📍 Location:** {user.get('location', 'Not specified')}")
                        st.write(f"**📅 Joined:** {user.get('created_at', 'Unknown')}")
                        st.write(f"**⭐ Rating:** {user.get('rating_avg', 0)}/5 ({user.get('rating_count', 0)} reviews)")
                    
                    with col2:
                        current_role = user.get('role', 'user')
                        is_banned = user.get('is_banned', False)
                        
                        st.write(f"**👑 Role:** {current_role}")
                        st.write(f"**🔒 Status:** {'🚫 Banned' if is_banned else '✅ Active'}")
                        st.write(f"**👁️ Profile:** {user.get('profile_visibility', 'public')}")
                        st.write(f"**🔄 Total Swaps:** {user.get('total_swaps', 0)}")
                    
                    with col3:
                        # Admin actions
                        user_id = user['user_id']
                        
                        # Ban/Unban user
                        if not is_banned:
                            if st.button(f"🚫 Ban User", key=f"ban_{user_id}"):
                                ban_result = firebase_auth.update_user_profile(user_id, {
                                    'is_banned': True,
                                    'ban_reason': 'Banned by admin',
                                })
                                if ban_result['success']:
                                    st.success("User banned!")
                                    st.rerun()
                                else:
                                    st.error("Failed to ban user")
                        else:
                            if st.button(f"✅ Unban", key=f"unban_{user_id}"):
                                unban_result = firebase_auth.update_user_profile(user_id, {
                                    'is_banned': False,
                                    'ban_reason': '',
                                })
                                if unban_result['success']:
                                    st.success("User unbanned!")
                                    st.rerun()
                                else:
                                    st.error("Failed to unban user")
                        
                        # Make admin
                        if current_role != 'admin':
                            if st.button(f"👑 Make Admin", key=f"admin_{user_id}"):
                                admin_result = firebase_auth.update_user_profile(user_id, {
                                    'role': 'admin'
                                })
                                if admin_result['success']:
                                    st.success("User promoted to admin!")
                                    st.rerun()
                                else:
                                    st.error("Failed to promote user")
                        else:
                            if st.button(f"👤 Remove Admin", key=f"remove_admin_{user_id}"):
                                remove_result = firebase_auth.update_user_profile(user_id, {
                                    'role': 'user'
                                })
                                if remove_result['success']:
                                    st.success("Admin privileges removed!")
                                    st.rerun()
                                else:
                                    st.error("Failed to remove admin privileges")
        else:
            st.info("No users found.")
    else:
        st.error("Failed to load users")

def admin_system_messages():
    """System messages management"""
    check_admin_access()
    
    st.subheader("📢 Platform Messages")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Send New Message**")
        with st.form("send_message_form"):
            title = st.text_input("📝 Message Title", placeholder="e.g., Maintenance Notice")
            message = st.text_area("💬 Message Content", placeholder="Enter your platform-wide message...")
            message_type = st.selectbox("📂 Message Type", ["announcement", "maintenance", "feature_update", "warning"])
            
            if st.form_submit_button("📤 Send Message", use_container_width=True):
                if title and message:
                    admin_id = st.session_state.user['localId']
                    result = firebase_auth.create_system_message(admin_id, title, message, message_type)
                    
                    if result['success']:
                        st.success("✅ Message sent to all users!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to send message: {result['error']}")
                else:
                    st.error("❌ Please fill in title and message")
    
    with col2:
        st.write("**Active Messages**")
        messages_result = firebase_auth.get_active_messages()
        
        if messages_result['success']:
            messages = messages_result['messages']
            
            if messages:
                for msg in messages:
                    with st.expander(f"📢 {msg['title']} ({msg['type']})"):
                        st.write(f"**Message:** {msg['message']}")
                        st.write(f"**Type:** {msg['type']}")
                        st.write(f"**Created:** {msg.get('created_at', 'Unknown')}")
                        
                        if st.button("🗑️ Delete Message", key=f"delete_msg_{msg.get('message_id', 'unknown')}"):
                            st.warning("Message deletion functionality coming soon!")
            else:
                st.info("No active messages")
        else:
            st.error("Failed to load messages")

def admin_analytics():
    """Analytics and reporting"""
    check_admin_access()
    
    st.subheader("📊 Analytics & Reports")
    
    # Platform statistics
    st.write("**📈 Platform Statistics**")
    
    # Get basic stats
    users_result = firebase_auth.get_public_users(1000)
    total_users = len(users_result.get('users', [])) if users_result['success'] else 0
    
    skills_result = firebase_auth.get_all_skills()
    total_skills = len(skills_result.get('skills', [])) if skills_result['success'] else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total Users", total_users)
    
    with col2:
        st.metric("🎯 Total Skills", total_skills)
    
    with col3:
        admin_count = len([u for u in users_result.get('users', []) if u.get('role') == 'admin']) if users_result['success'] else 0
        st.metric("👑 Admins", admin_count)
    
    with col4:
        banned_count = len([u for u in users_result.get('users', []) if u.get('is_banned')]) if users_result['success'] else 0
        st.metric("🚫 Banned Users", banned_count)
    
    st.markdown("---")
    
    # Generate reports
    st.write("**📋 Generate Reports**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 User Activity Report", use_container_width=True):
            if users_result['success']:
                users_df = pd.DataFrame(users_result['users'])
                
                st.write("**User Statistics:**")
                if not users_df.empty:
                    # Select relevant columns
                    display_columns = ['name', 'email', 'role', 'rating_avg', 'total_swaps', 'is_banned']
                    available_columns = [col for col in display_columns if col in users_df.columns]
                    st.dataframe(users_df[available_columns], use_container_width=True)
                    
                    # Download option
                    csv = users_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download User Report",
                        data=csv,
                        file_name=f"user_report_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("No user data available")
    
    with col2:
        if st.button("🎯 Skills Report", use_container_width=True):
            if skills_result['success']:
                skills_df = pd.DataFrame(skills_result['skills'])
                
                st.write("**Skills Statistics:**")
                if not skills_df.empty:
                    # Select relevant columns
                    display_columns = ['name', 'category', 'users_offering', 'users_wanting', 'total_swaps']
                    available_columns = [col for col in display_columns if col in skills_df.columns]
                    st.dataframe(skills_df[available_columns], use_container_width=True)
                    
                    # Download option
                    csv = skills_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Skills Report",
                        data=csv,
                        file_name=f"skills_report_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.info("No skills data available")

def admin_database_explorer():
    """Database explorer for admins"""
    check_admin_access()
    
    st.subheader("🗄️ Database Explorer")
    
    st.info("🔍 Explore your Firebase collections and data structure")
    
    # Collection explorer
    collection_tabs = st.tabs(["👥 Users", "🎯 Skills", "🤝 User Skills", "📋 Requests", "🔄 Transactions", "⭐ Reviews", "📢 Messages"])
    
    with collection_tabs[0]:  # Users
        st.write("**👥 Users Collection**")
        users_result = firebase_auth.get_public_users(100)
        if users_result['success'] and users_result['users']:
            users_df = pd.DataFrame(users_result['users'])
            st.dataframe(users_df, use_container_width=True)
            st.write(f"Total users: {len(users_df)}")
        else:
            st.info("No users found")
    
    with collection_tabs[1]:  # Skills
        st.write("**🎯 Skills Collection**")
        skills_result = firebase_auth.get_all_skills()
        if skills_result['success'] and skills_result['skills']:
            skills_df = pd.DataFrame(skills_result['skills'])
            st.dataframe(skills_df, use_container_width=True)
            st.write(f"Total skills: {len(skills_df)}")
        else:
            st.info("No skills found")
    
    with collection_tabs[2]:  # User Skills
        st.write("**🤝 User Skills Collection**")
        st.info("User skills data coming soon!")
    
    with collection_tabs[3]:  # Requests
        st.write("**📋 Barter Requests Collection**")
        st.info("Barter requests data coming soon!")
    
    with collection_tabs[4]:  # Transactions
        st.write("**🔄 Transactions Collection**")
        st.info("Transactions data coming soon!")
    
    with collection_tabs[5]:  # Reviews
        st.write("**⭐ Reviews Collection**")
        st.info("Reviews data coming soon!")
    
    with collection_tabs[6]:  # Messages
        st.write("**📢 System Messages Collection**")
        messages_result = firebase_auth.get_active_messages()
        if messages_result['success'] and messages_result['messages']:
            messages_df = pd.DataFrame(messages_result['messages'])
            st.dataframe(messages_df, use_container_width=True)
        else:
            st.info("No messages found")

def show_admin_interface():
    """Main admin interface with navigation"""
    check_admin_access()
    
    st.markdown("""
    <div style="background: #fef2f2; border: 2px solid #fca5a5; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: #dc2626; margin: 0;">⚙️ Admin Control Panel</h3>
        <p style="margin: 0; color: #7f1d1d;">Administrative access - use with caution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin navigation
    admin_tab = st.selectbox(
        "🔧 Admin Section:",
        ["Dashboard", "User Management", "Database Explorer", "System Messages", "Analytics"],
        key="admin_nav"
    )
    
    st.markdown("---")
    
    # Route to admin pages
    if admin_tab == "Dashboard":
        admin_dashboard()
    elif admin_tab == "User Management":
        admin_users_management()
    elif admin_tab == "Database Explorer":
        admin_database_explorer()
    elif admin_tab == "System Messages":
        admin_system_messages()
    elif admin_tab == "Analytics":
        admin_analytics()
