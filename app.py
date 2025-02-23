import streamlit as st
import random
import datetime
import pandas as pd
import io

# Initialize session state for user data
if "users" not in st.session_state:
    st.session_state.users = {}  # Stores user data (points, streaks, etc.)
if "current_user" not in st.session_state:
    st.session_state.current_user = None  # Tracks the logged-in user

# List of Growth Mindset Challenges
default_challenges = [
    "Embrace a difficult task today and see it as an opportunity to learn.",
    "Ask for feedback from someone and use it to improve yourself.",
    "Replace 'I can't' with 'I can't yet' and try again.",
    "Learn something new today that pushes you out of your comfort zone.",
    "Write down a mistake you made and what you learned from it.",
    "Encourage someone else to keep going when they struggle.",
    "Spend 10 minutes today reflecting on a challenge and brainstorming solutions.",
    "Celebrate small wins and acknowledge your progress.",
    "Turn a past failure into a lesson for the future.",
    "Practice self-compassion—treat yourself as you would a friend."
]

# Motivational Quotes
quotes = [
    "“The only limit to our realization of tomorrow is our doubts of today.” – Franklin D. Roosevelt",
    "“Success is not final, failure is not fatal: it is the courage to continue that counts.” – Winston Churchill",
    "“You are never too old to set another goal or to dream a new dream.” – C.S. Lewis",
    "“Growth and comfort do not coexist.” – Ginni Rometty",
    "“The mind is just like a muscle—the more you exercise it, the stronger it gets.” – Carol Dweck"
]

# User Login System
st.sidebar.title("🔑 User Login")
username = st.sidebar.text_input("Enter your name", value="", max_chars=20)
if st.sidebar.button("Login"):
    if username:
        st.session_state.current_user = username
        if username not in st.session_state.users:
            st.session_state.users[username] = {"points": 0, "streak": 0, "completed": []}
        st.sidebar.success(f"Logged in as {username}")
    else:
        st.sidebar.error("Please enter a valid name.")

if st.session_state.current_user:
    user_data = st.session_state.users[st.session_state.current_user]

    # Display User's Progress
    st.sidebar.write(f"👤 **User:** {st.session_state.current_user}")
    st.sidebar.write(f"🔥 **Streak:** {user_data['streak']} days")
    st.sidebar.write(f"🌟 **Points:** {user_data['points']}")
    st.write("Made with ❤️ Basit Ali")
    # Main App Title
    st.title("🌱 Growth Mindset Challenge")

    # Daily Challenge Section
    today = datetime.date.today()
    challenge_index = today.day % len(default_challenges)
    daily_challenge = default_challenges[challenge_index]

    st.write("### Today's Challenge:")
    st.success(daily_challenge)

    # Mark Challenge as Completed
    if st.button("Mark as Completed"):
        if daily_challenge not in user_data["completed"]:
            user_data["completed"].append(daily_challenge)
            user_data["points"] += 10  # Points for completion
            user_data["streak"] += 1  # Streak counter
            st.success(f"Great job! 🎉 You've earned 10 points.")
        else:
            st.warning("You've already completed this challenge today!")

    # Generate Random Challenge
    if st.button("Get a Random Challenge"):
        st.success(random.choice(default_challenges))

    # Motivational Quote
    st.write("### 💡 Motivation for Today:")
    st.info(random.choice(quotes))

    # Progress Tracker
    st.write("### 📊 Track Your Progress")
    progress = st.slider("How much effort did you put in today?", 0, 100, 50)
    st.write(f"Your effort level: {progress}% 🚀 Keep pushing forward!")

    # Leaderboard System
    st.write("### 🏆 Leaderboard")
    sorted_users = sorted(st.session_state.users.items(), key=lambda x: x[1]["points"], reverse=True)
    for i, (user, data) in enumerate(sorted_users[:5]):  # Show top 5
        st.write(f"**{i+1}. {user}** - {data['points']} points")

    # Community Reflection Wall
    st.write("### 📝 Community Reflection Wall")
    reflection = st.text_area("Share your growth mindset reflection:")
    if st.button("Post Reflection"):
        if "community_wall" not in st.session_state:
            st.session_state.community_wall = []
        st.session_state.community_wall.append(f"💬 {st.session_state.current_user}: {reflection}")
        st.success("Your reflection has been posted!")

    # Display community reflections (last 5 posts)
    if "community_wall" in st.session_state:
        for post in reversed(st.session_state.community_wall[-5:]):
            st.write(post)

    # 🧹 Data Sweeper Feature
    st.write("### 🧹 Data Sweeper (Reset Progress)")
    if st.button("Reset My Progress"):
        confirm = st.checkbox("I confirm that I want to reset my progress.")
        if confirm:
            st.session_state.users[st.session_state.current_user] = {"points": 0, "streak": 0, "completed": []}
            st.success("Your progress has been reset!")

    # Admin-Only: Reset All Users
    st.write("### 🔥 Reset All Users (Admin Only)")
    if st.session_state.current_user.lower() == "admin":
        if st.button("Reset All Users' Data"):
            confirm_all = st.checkbox("I confirm that I want to reset ALL user data.")
            if confirm_all:
                st.session_state.users = {}
                st.success("All user data has been wiped!")

    st.write("---")


    # 🚀 New Feature: File Upload & CSV Conversion
    st.header("📁 Upload a File and Convert to CSV")
    uploaded_file = st.file_uploader("Choose a file (Excel, CSV, or text file)", type=["xlsx", "csv", "txt"])
    if uploaded_file is not None:
        try:
            # Attempt to read as CSV first
            df = pd.read_csv(uploaded_file)
            st.write("File successfully loaded as CSV:")
        except Exception:
            try:
                # Try reading as Excel
                df = pd.read_excel(uploaded_file)
                st.write("File successfully loaded as Excel:")
            except Exception:
                try:
                    # Try reading a text file as CSV (assuming comma-separated values)
                    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                    df = pd.read_csv(stringio, delimiter=",")
                    st.write("File successfully loaded as text (CSV format):")
                except Exception as e:
                    st.error(f"Error loading file: {e}")
                    df = None

        if df is not None:
            st.dataframe(df)

            # Convert DataFrame to CSV
            csv_buffer = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv_buffer,
                file_name="converted_file.csv",
                mime="text/csv"
            )
