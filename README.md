Problem Statement: 1
In many communities, people possess valuable skills but lack access to services they can’t afford. This platform empowers users to exchange skills directly — for example:

A developer can teach coding in exchange for guitar lessons

A chef can offer cooking classes in return for graphic design help

A digital marketer can get language tutoring by mentoring someone in social media

This fosters community learning, knowledge sharing, and non-monetary collaboration.


Team Members Name: 
ADHYA KOUL  Adhyakoul05@gmail.com
GURANSH CHUGH gchugh_be23@thapar.edu
KEVAL AMBANI ambanikeval2@gmail.com
KASHISH GUPTA guptakashish1012@gmail.com



skill-swap/
├── main.py                   # ← RUN THIS with Streamlit
├── firebase_config.py        # ← Backend logic (imported by main.py)
├── complete_database.py      # ← Database operations (imported by firebase_config.py)
├── admin_pages.py            # ← Admin interface (imported by main.py)
├── .env                      # ← Your Firebase credentials
├── firebase-credentials.json # ← Service account key
└── requirements.txt          # ← Dependencies



🔄 Skill Swap Platform — Summary
What it is:
A community-based web application where users can exchange skills with one another — like “I teach you Photoshop, you teach me Excel.”

🌟 Key Features
📝 User Registration & Login

Users can sign up or log in securely using Firebase Authentication.

👤 Create a Public or Private Profile

Add your name, location, availability, and skill interests (both skills you offer and want to learn).

Choose whether your profile is public or private.

🎯 Skill Listing

Users can add skills they offer or want to learn.

Each skill includes a proficiency level and optional description.

🔍 Browse & Search Users

View a list of other users with their offered/wanted skills and availability.

Filter by availability and search by name or location.

🤝 Request Skill Swaps

If you see a match, you can send a barter request offering one of your skills in exchange.

Requests include an optional message and are tracked in your account.

📥 Accept or Reject Requests

Received requests can be accepted or rejected with one click.

Status updates are shown clearly with labels like “Pending,” “Accepted,” or “Rejected.”

🔄 Track Transactions

Once a swap is accepted, it becomes a transaction that can be tracked with a progress percentage.

⚙️ Admin Panel

Special interface for admins to view platform-wide stats or moderate content.

📢 Platform Messages

Admins can send notices and system updates visible to all users.

🛠️ Tech Stack
Frontend: Streamlit (Python-based web UI framework)

Backend: Firebase (Authentication, Realtime DB, Firestore, etc.)

Styling: Custom CSS embedded in Streamlit

Session Management: Streamlit session_state

Role Management: User roles (admin vs regular user)

💡 Example Use Case
John knows video editing and wants to learn Excel automation.

Sara is an Excel pro who wants to improve in video editing.

Both find each other, send requests, and swap skills through sessions.


