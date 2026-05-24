import streamlit as st
import pandas as pd
from groq import Groq
import json
from datetime import datetime
import plotly.express as px
# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AI Workflow Automation Assistant",
    page_icon="",
    layout="wide"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
/* Main background */
.main { background-color: #f8f9fa; }

/* Title styling */
h1 { color: #1B3A6B !important; font-weight: 800 !important; background: none !important; }
h2, h3 { color: #1B3A6B !important; background: none !important; }

/* Buttons */
.stButton > button {
    background-color: #1B3A6B !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    border: none !important;
}

/* Text area */
textarea {
    border-radius: 8px !important;
    border: 1px solid #d0d0d0 !important;
}

/* Success/info/warning boxes */
.stSuccess, .stInfo, .stWarning {
    border-radius: 10px !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    overflow: visible !important;
    white-space: normal !important;
}
[data-testid="metric-container"] p {
    font-size: 14px !important;
    white-space: normal !important;
    overflow: visible !important;
}

/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #1B3A6B !important;
}

/* All sidebar text white */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar input box */
section[data-testid="stSidebar"] input {
    color: #1B3A6B !important;
    background-color: white !important;
    border: none !important;
    border-radius: 6px !important;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600 !important;
}

/* Sidebar links */
section[data-testid="stSidebar"] a {
    color: #aaccff !important;
}

/* Sidebar divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_..."
    )
    st.caption("Get your free key at console.groq.com")
    st.divider()
    st.markdown("### About This Tool")
    st.caption(
        "An AI-powered enterprise support ticket analyzer. "
        "Paste any support issue and get instant AI classification, "
        "priority assignment, team routing, root cause analysis, "
        "and step-by-step resolution guidance."
    )
    st.divider()
    st.markdown("### Supported Issue Types")
    for issue in [
        "Server and Infrastructure",
        "Authentication and Security",
        "Database and Data Issues",
        "Dashboard and BI Failures",
        "Payment and Finance Systems",
        "Network and Connectivity",
        "Email and Communication",
        "Software and Application Bugs"
    ]:
        st.caption(issue)

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("AI Workflow Automation Assistant")
st.caption("Enterprise Support Ticket Analyzer — Powered by Groq AI (Llama 3)")
st.divider()

# ─────────────────────────────────────────
# AI FUNCTION
# ─────────────────────────────────────────
def analyze_ticket(ticket_text, api_key):
    client = Groq(api_key=api_key)

    prompt = f"""You are a senior enterprise IT support analyst with 10 years of experience.
Analyze this support ticket and respond ONLY with a valid JSON object. No extra text, no markdown.

Ticket:
\"\"\"{ticket_text}\"\"\"

Respond with exactly this JSON:
{{
    "category": "specific issue category",
    "priority": "Low / Medium / High / Critical",
    "team": "responsible team name",
    "cause": "root cause in one sentence",
    "resolution_steps": ["step 1", "step 2", "step 3", "step 4"],
    "estimated_resolution_time": "e.g. 2-4 hours",
    "sentiment": "Frustrated / Neutral / Urgent / Calm / Panicked",
    "summary": "one sentence summary of the issue",
    "impact": "business impact if unresolved"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an enterprise IT support analyst. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )

    text = response.choices[0].message.content.strip()

    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break

    return json.loads(text.strip())

# ─────────────────────────────────────────
# SAMPLE TICKETS
# ─────────────────────────────────────────
st.subheader("Enter Support Ticket")

sample_tickets = {
    "Select a sample...": "",
    "Production Dashboard Down": "Our production sales dashboard has been completely down since 9:00 AM. The entire sales team of 50 people cannot access their daily reports. We have a board presentation at 2 PM today and need this resolved immediately. This is critical.",
    "Login Failure": "Multiple users are reporting that they cannot log into the CRM system since this morning. The error says Session timeout - please contact administrator. This is affecting 20 users across 3 departments.",
    "Database Slow": "The main database has been extremely slow since last night's deployment. Queries that used to take 2 seconds are now taking over 2 minutes. Customer-facing APIs are timing out and we are receiving complaints.",
    "Payment Processing Error": "Customers are reporting failed payment transactions on our e-commerce platform since 6 PM. The payment gateway returns error code 500. We are losing approximately $10,000 per hour in revenue.",
    "Network Outage": "The entire Singapore office has lost internet connectivity. VPN is also not working. Around 200 employees are unable to work. The issue started around 10:30 AM after a scheduled maintenance window."
}

selected_sample = st.selectbox("Try a sample ticket:", list(sample_tickets.keys()))

ticket = st.text_area(
    "Or type your own support issue:",
    value=sample_tickets[selected_sample],
    height=160,
    placeholder="Describe the support issue — what happened, when, who is affected, any error messages..."
)

col1, col2 = st.columns([1, 5])
with col1:
    analyze_btn = st.button("Analyze with AI", type="primary", use_container_width=True)

# ─────────────────────────────────────────
# ANALYSIS RESULTS
# ─────────────────────────────────────────
if analyze_btn:
    if not ticket.strip():
        st.warning("Please enter a support ticket or select a sample.")
    elif not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    else:
        with st.spinner("Analyzing with Groq AI..."):
            try:
                result = analyze_ticket(ticket, api_key)

                st.success("Ticket analyzed successfully by Groq AI")
                st.divider()

                # ── ROW 1: METRICS ──
                
                st.subheader("AI Classification")

                category = result.get("category", "N/A")
                priority = result.get("priority", "N/A")
                team = result.get("team", "N/A")
                resolution = result.get("estimated_resolution_time", "N/A")
                sentiment = result.get("sentiment", "N/A")
                impact = result.get("impact", "N/A")

                priority_colors = {
                    "Critical": "#ff4444",
                    "High": "#ff8800",
                    "Medium": "#ffcc00",
                    "Low": "#00cc44"
                }
                priority_color = priority_colors.get(priority, "#888888")

                st.markdown(f"""
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom:16px;">
                    <div style="background:white; border:1px solid #e0e0e0; border-radius:10px; padding:14px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.07);">
                        <div style="font-size:11px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Category</div>
                        <div style="font-size:14px; font-weight:700; color:#1B3A6B;">{category}</div>
                    </div>
                    <div style="background:white; border:2px solid {priority_color}; border-radius:10px; padding:14px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.07);">
                        <div style="font-size:11px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Priority</div>
                        <div style="font-size:14px; font-weight:700; color:{priority_color};">{priority}</div>
                    </div>
                    <div style="background:white; border:1px solid #e0e0e0; border-radius:10px; padding:14px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.07);">
                        <div style="font-size:11px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Assigned Team</div>
                        <div style="font-size:14px; font-weight:700; color:#1B3A6B;">{team}</div>
                    </div>
                    <div style="background:white; border:1px solid #e0e0e0; border-radius:10px; padding:14px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.07);">
                        <div style="font-size:11px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Est. Resolution</div>
                        <div style="font-size:14px; font-weight:700; color:#1B3A6B;">{resolution}</div>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; margin-bottom:16px;">
                    <div style="background:white; border:1px solid #e0e0e0; border-radius:10px; padding:14px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.07);">
                        <div style="font-size:11px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">User Sentiment</div>
                        <div style="font-size:14px; font-weight:700; color:#1B3A6B;">{sentiment}</div>
                    </div>
                    <div style="background:white; border:1px solid #e0e0e0; border-radius:10px; padding:14px 16px; box-shadow:0 2px 6px rgba(0,0,0,0.07);">
                        <div style="font-size:11px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:6px;">Business Impact</div>
                        <div style="font-size:14px; font-weight:700; color:#1B3A6B;">{impact}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── DIAGNOSIS ──

                st.divider()
               # st.markdown("<br>", unsafe_allow_html=True)

                st.subheader("AI Diagnosis")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.info(f"**Summary**\n\n{result.get('summary', 'N/A')}")
                with col_b:
                    st.warning(f"**Root Cause**\n\n{result.get('cause', 'N/A')}")

                # ── RESOLUTION STEPS ──
                st.divider()

                st.subheader("Recommended Resolution Steps")
                steps = result.get("resolution_steps", [])
                for i, step in enumerate(steps, 1):
                    st.markdown(f"""
                    <div style="background:white; border-left:4px solid #1B3A6B;
                                border-radius:6px; padding:12px 16px; margin-bottom:8px;
                                box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                        <span style="font-weight:700; color:#1B3A6B;">Step {i}</span>
                        <span style="color:#333; margin-left:10px;">{step}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # ── SAVE TO CSV ──
                data = {
                    "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                    "Ticket Summary": [ticket[:80] + "..." if len(ticket) > 80 else ticket],
                    "Category": [result.get("category", "")],
                    "Priority": [result.get("priority", "")],
                    "Team": [result.get("team", "")],
                    "Sentiment": [result.get("sentiment", "")],
                    "Root Cause": [result.get("cause", "")],
                    "Est. Resolution": [result.get("estimated_resolution_time", "")],
                    "Impact": [result.get("impact", "")]
                }
                df = pd.DataFrame(data)

                try:
                    existing = pd.read_csv("tickets.csv")
                    updated = pd.concat([existing, df], ignore_index=True)
                    updated.to_csv("tickets.csv", index=False)
                except FileNotFoundError:
                    df.to_csv("tickets.csv", index=False)

                st.success("Ticket saved to database")

            except json.JSONDecodeError:
                st.error("AI returned unexpected format. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ─────────────────────────────────────────
# TICKET DATABASE + ANALYTICS
# ─────────────────────────────────────────
st.divider()
st.subheader("Ticket Database and Analytics")

try:
    saved_df = pd.read_csv("tickets.csv")

    # ── SUMMARY METRICS ──
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Tickets", len(saved_df))
    m2.metric("Critical", len(saved_df[saved_df["Priority"] == "Critical"]))
    m3.metric("High Priority", len(saved_df[saved_df["Priority"] == "High"]))
    m4.metric("Teams Involved", saved_df["Team"].nunique())

    st.divider()

    # ── PLOTLY CHARTS ──
    import plotly.express as px

    ch1, ch2 = st.columns(2)

    with ch1:
        st.write("**Tickets by Category**")
        cat_df = saved_df["Category"].value_counts().reset_index()
        cat_df.columns = ["Category", "Count"]
        fig1 = px.bar(
            cat_df, x="Category", y="Count",
            color="Count",
            color_continuous_scale=["#cce0ff", "#1B3A6B"],
            text="Count"
        )
        fig1.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="#1B3A6B",
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=10, b=10),
            xaxis=dict(tickangle=-30)
        )
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        st.write("**Tickets by Priority**")
        pri_df = saved_df["Priority"].value_counts().reset_index()
        pri_df.columns = ["Priority", "Count"]
        priority_colors_map = {
            "Critical": "#ff4444",
            "High": "#ff8800",
            "Medium": "#ffcc00",
            "Low": "#00cc44"
        }
        pri_df["Color"] = pri_df["Priority"].map(priority_colors_map).fillna("#888888")
        fig2 = px.bar(
            pri_df, x="Priority", y="Count",
            color="Priority",
            color_discrete_map=priority_colors_map,
            text="Count"
        )
        fig2.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_color="#1B3A6B",
            showlegend=False,
            margin=dict(t=10, b=10)
        )
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)

    # ── SENTIMENT CHART ──
    if "Sentiment" in saved_df.columns:
        st.write("**Tickets by User Sentiment**")
        sent_df = saved_df["Sentiment"].value_counts().reset_index()
        sent_df.columns = ["Sentiment", "Count"]
        sentiment_colors_map = {
            "Panicked": "#ff4444",
            "Frustrated": "#ff8800",
            "Urgent": "#ffaa00",
            "Neutral": "#4488ff",
            "Calm": "#00cc44"
        }
        fig3 = px.pie(
            sent_df, names="Sentiment", values="Count",
            color="Sentiment",
            color_discrete_map=sentiment_colors_map,
            hole=0.4
        )
        fig3.update_layout(
            paper_bgcolor="white",
            font_color="#1B3A6B",
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ── COLOR CODED TABLE ──
    st.write("**All Tickets**")

    priority_badge_colors = {
        "Critical": ("🔴", "#fff0f0", "#ff4444"),
        "High":     ("🟠", "#fff5f0", "#ff8800"),
        "Medium":   ("🟡", "#fffdf0", "#ccaa00"),
        "Low":      ("🟢", "#f0fff4", "#00aa44"),
    }

    for _, row in saved_df.iterrows():
        summary = str(row.get('Ticket Summary','')).replace('<','').replace('>','').replace('/div','').replace('div','').strip()
        p = row.get("Priority", "Medium")
        badge_emoji, bg_color, border_color = priority_badge_colors.get(
            p, ("⚪", "#f9f9f9", "#cccccc")
        )
        st.markdown(f"""
        <div style="background:{bg_color}; border-left: 4px solid {border_color};
                    border-radius:8px; padding:12px 16px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:12px; font-weight:700; color:{border_color};
                                 text-transform:uppercase;">{badge_emoji} {p}</span>
                    <span style="font-size:12px; color:#888; margin-left:12px;">{row.get('Timestamp','')}</span>
                </div>
                <span style="font-size:12px; color:#555; font-weight:600;">{row.get('Team','')}</span>
            </div>
            <div style="font-size:14px; font-weight:600; color:#1B3A6B; margin-top:6px;">
                {row.get('Category','')}
            </div>
            <div style="font-size:13px; color:#555; margin-top:4px;">
                {summary}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    csv_data = saved_df.to_csv(index=False)
    if st.button("Clear Database", type="secondary"):
        import os
        try:
            os.remove("tickets.csv")
            st.success("Database cleared!")
            st.rerun()
        except:
            st.error("No database found.")
    st.download_button(
        label="Download Tickets as CSV",
        data=csv_data,
        file_name=f"tickets_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.info("No tickets saved yet. Analyze your first ticket above!")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.caption("AI Workflow Automation Assistant  ·  Built with Streamlit and Groq AI  ·  Mehwish Khan")
