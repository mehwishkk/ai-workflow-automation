import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Workflow Automation Assistant",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("AI Workflow Automation Assistant")

st.write("Enterprise Support Ticket Analyzer")

# -----------------------------
# USER INPUT
# -----------------------------
ticket = st.text_area(
    "Enter support issue",
    height=200
)

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("Analyze Ticket"):

    # -----------------------------
    # BASIC VALIDATION
    # -----------------------------
    if ticket.strip() == "":
        st.warning("Please enter a support issue.")

    else:

        # -----------------------------
        # DEFAULT VALUES
        # -----------------------------
        category = "General Technical Issue"
        priority = "Medium"
        team = "IT Support"
        cause = "Requires further investigation"

        ticket_lower = ticket.lower()

        # -----------------------------
        # RULE-BASED ANALYSIS
        # -----------------------------

        # Dashboard Issues
        if "dashboard" in ticket_lower:
            category = "Dashboard / BI Failure"
            priority = "High"
            team = "BI / DevOps Team"
            cause = "Deployment or backend integration issue"

        # Login Issues
        elif "login" in ticket_lower or "password" in ticket_lower:
            category = "Authentication Issue"
            priority = "Medium"
            team = "Security / IAM Team"
            cause = "Credential validation failure"

        # Database Issues
        elif "database" in ticket_lower or "sql" in ticket_lower:
            category = "Database Failure"
            priority = "High"
            team = "Database Administration Team"
            cause = "Database connectivity or query issue"

        # Network Issues
        elif "network" in ticket_lower or "wifi" in ticket_lower:
            category = "Network Issue"
            priority = "Medium"
            team = "Infrastructure Team"
            cause = "Network connectivity interruption"

        # Server Issues
        elif "server" in ticket_lower:
            category = "Server Failure"
            priority = "Critical"
            team = "Cloud / Infrastructure Team"
            cause = "Server downtime or overload"

        # Payment Issues
        elif "payment" in ticket_lower:
            category = "Payment Processing Issue"
            priority = "High"
            team = "Finance Systems Team"
            cause = "Transaction processing failure"

        # Urgent Override
        if "urgent" in ticket_lower:
            priority = "Critical"

        # -----------------------------
        # DISPLAY RESULTS
        # -----------------------------
        st.success("Ticket analyzed successfully")

        st.subheader("AI Analysis")

        st.write(f"### Issue Category")
        st.info(category)

        st.write(f"### Priority Level")
        st.warning(priority)

        st.write(f"### Suggested Team")
        st.info(team)

        st.write(f"### Possible Cause")
        st.info(cause)

        # -----------------------------
        # CREATE DATAFRAME
        # -----------------------------
        data = {
            "Timestamp": [datetime.now()],
            "Ticket": [ticket],
            "Category": [category],
            "Priority": [priority],
            "Team": [team],
            "Cause": [cause]
        }

        df = pd.DataFrame(data)

        # -----------------------------
        # SAVE TO CSV
        # -----------------------------
        try:
            existing_df = pd.read_csv("tickets.csv")

            updated_df = pd.concat(
                [existing_df, df],
                ignore_index=True
            )

            updated_df.to_csv(
                "tickets.csv",
                index=False
            )

        except:
            df.to_csv(
                "tickets.csv",
                index=False
            )

        st.success("Ticket saved to database")

# -----------------------------
# VIEW SAVED TICKETS
# -----------------------------
st.divider()

st.subheader("Saved Tickets Database")

try:
    saved_df = pd.read_csv("tickets.csv")

    st.dataframe(saved_df)

    # -----------------------------
    # ANALYTICS
    # -----------------------------
    st.subheader("Ticket Analytics")

    category_counts = saved_df["Category"].value_counts()

    st.bar_chart(category_counts)

except:
    st.info("No tickets saved yet.")