import streamlit as st
import pandas as pd

st.set_page_config(page_title="Explainable Lead Scoring System", layout="wide")

st.title("Explainable Lead Scoring + Smart Outreach Assistant")
st.write(
    "This app improves traditional lead scoring by showing not only which leads rank highest, "
    "but also why they rank highly, what action to take next, and a suggested outreach message."
)

# -----------------------------
# TARGET INPUTS
# -----------------------------
st.sidebar.header("Target Criteria")
target_industry = st.sidebar.text_input("Target Industry", value="Healthcare")
target_location = st.sidebar.text_input("Target Location", value="London")

# -----------------------------
# WEIGHTS
# -----------------------------
st.sidebar.header("Scoring Weights")
industry_weight_raw = st.sidebar.slider("Industry Match", 0, 50, 25)
location_weight_raw = st.sidebar.slider("Location Match", 0, 50, 20)
contactability_weight_raw = st.sidebar.slider("Contactability", 0, 50, 20)
confidence_weight_raw = st.sidebar.slider("Confidence", 0, 50, 15)
revenue_weight_raw = st.sidebar.slider("Revenue Potential", 0, 50, 20)

# -----------------------------
# UX Warning for Equal Weights
# -----------------------------
weights = [
    industry_weight_raw,
    location_weight_raw,
    contactability_weight_raw,
    confidence_weight_raw,
    revenue_weight_raw
]

if len(set(weights)) == 1:
    st.warning(
        "All weights are equal. This reduces prioritization. "
        "Consider adjusting weights based on your goal."
    )
total_weight = (
    industry_weight_raw
    + location_weight_raw
    + contactability_weight_raw
    + confidence_weight_raw
    + revenue_weight_raw
)

st.sidebar.markdown(f"**Total Weight:** {total_weight} / 250")

if total_weight == 0:
    st.error("Total weight cannot be zero.")
    st.stop()

industry_weight = (industry_weight_raw / total_weight) * 100
location_weight = (location_weight_raw / total_weight) * 100
contactability_weight = (contactability_weight_raw / total_weight) * 100
confidence_weight = (confidence_weight_raw / total_weight) * 100
revenue_weight = (revenue_weight_raw / total_weight) * 100



with st.sidebar.expander("Normalized Weights"):
    st.write(f"Industry Match: {industry_weight:.2f}")
    st.write(f"Location Match: {location_weight:.2f}")
    st.write(f"Contactability: {contactability_weight:.2f}")
    st.write(f"Confidence: {confidence_weight:.2f}")
    st.write(f"Revenue Potential: {revenue_weight:.2f}")

# -----------------------------
# FILE UPLOAD
# -----------------------------
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

required_columns = [
    "company_name",
    "industry",
    "location",
    "website",
    "company_linkedin",
    "owner_linkedin",
    "revenue",
]

# -----------------------------
# SAMPLE DATA
# -----------------------------
sample_data = [
    {
        "company_name": "HealthTech Solutions",
        "industry": "Healthcare",
        "location": "London",
        "website": "Yes",
        "company_linkedin": "Yes",
        "owner_linkedin": "Yes",
        "revenue": 500000,
    },
    {
        "company_name": "Retail Boost Ltd",
        "industry": "Retail",
        "location": "Manchester",
        "website": "Yes",
        "company_linkedin": "No",
        "owner_linkedin": "No",
        "revenue": 200000,
    },
    {
        "company_name": "MediCare AI",
        "industry": "Healthcare",
        "location": "Birmingham",
        "website": "Yes",
        "company_linkedin": "Yes",
        "owner_linkedin": "No",
        "revenue": 750000,
    },
    {
        "company_name": "FinEdge Group",
        "industry": "Finance",
        "location": "London",
        "website": "No",
        "company_linkedin": "Yes",
        "owner_linkedin": "No",
        "revenue": 1200000,
    },
    {
        "company_name": "AI Nexus",
        "industry": "AI",
        "location": "Dubai",
        "website": "Yes",
        "company_linkedin": "Yes",
        "owner_linkedin": "Yes",
        "revenue": 950000,
    },
    {
        "company_name": "LogiMove Global",
        "industry": "Logistics",
        "location": "Dubai",
        "website": "Yes",
        "company_linkedin": "No",
        "owner_linkedin": "Yes",
        "revenue": 450000,
    },
    {
        "company_name": "PharmaNova",
        "industry": "Pharma",
        "location": "London",
        "website": "Yes",
        "company_linkedin": "Yes",
        "owner_linkedin": "No",
        "revenue": 880000,
    },
]

# -----------------------------
# LOAD DATA
# -----------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(
            "Uploaded file is missing these required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    st.success("CSV uploaded successfully.")
else:
    df = pd.DataFrame(sample_data)
    st.info("No CSV uploaded. Using sample dataset.")

for col in required_columns:
    if col not in df.columns:
        df[col] = ""

df = df.fillna("")

st.subheader("Input Data")
st.dataframe(df, use_container_width=True)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def safe_lower(x):
    return str(x).strip().lower()

def yes_no(val):
    return safe_lower(val) == "yes"

def is_filled(val):
    if pd.isna(val):
        return False
    return str(val).strip() != ""

def classify_priority(score):
    if score >= 80:
        return "High Priority"
    elif score >= 55:
        return "Medium Priority"
    return "Low Priority"

def revenue_bucket(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return 0, "Low"

    if value >= 1000000:
        return revenue_weight, "High"
    elif value >= 500000:
        return revenue_weight * 0.6, "Medium"
    elif value > 0:
        return revenue_weight * 0.3, "Low"
    return 0, "Low"

def generate_explanation(
    industry_label,
    location_label,
    contact_label,
    confidence_label,
    revenue_label
):
    reasons = []

    if industry_label == "High":
        reasons.append("matches the target industry")
    if location_label == "High":
        reasons.append("matches the target location")
    if contact_label == "High":
        reasons.append("has strong contact coverage")
    elif contact_label == "Medium":
        reasons.append("has partial contact coverage")
    if confidence_label == "High":
        reasons.append("has high data completeness")
    elif confidence_label == "Medium":
        reasons.append("has moderate data completeness")
    if revenue_label == "High":
        reasons.append("shows strong revenue potential")
    elif revenue_label == "Medium":
        reasons.append("shows moderate revenue potential")

    if reasons:
        return "Strong lead because it " + ", ".join(reasons) + "."
    return "This lead has limited value because it has weak targeting signals and incomplete business data."

def recommend_action(priority, contact_label):
    if priority == "High Priority" and contact_label in ["High", "Medium"]:
        return "Send outreach now"
    elif priority == "High Priority" and contact_label == "Low":
        return "Enrich contact data first"
    elif priority == "Medium Priority":
        return "Review manually"
    return "Do not prioritize"

def generate_outreach_message(company, industry, location, action):
    return (
        f"Hi, I came across {company} while reviewing companies in the {industry} space. "
        f"I noticed your presence in {location}, and based on the available business signals, "
        f"your company appears to be a strong prospect. "
        f"My recommendation for this lead is: {action.lower()}. "
        f"I’d love to start a conversation and explore whether there could be a relevant opportunity to collaborate."
    )

def dataframe_to_csv_download(df_to_download):
    return df_to_download.to_csv(index=False).encode("utf-8")

# -----------------------------
# CALCULATIONS
# -----------------------------
results = []

for _, row in df.iterrows():

    # INDUSTRY MATCH
    if safe_lower(target_industry) in safe_lower(row["industry"]):
        industry_score = industry_weight
        industry_label = "High"
    else:
        industry_score = 0
        industry_label = "Low"

    # LOCATION MATCH
    if safe_lower(target_location) in safe_lower(row["location"]):
        location_score = location_weight
        location_label = "High"
    else:
        location_score = 0
        location_label = "Low"

    # RELEVANCE
    relevance_score = industry_score + location_score
    if relevance_score >= 0.7 * (industry_weight + location_weight):
        relevance_label = "High"
    elif relevance_score > 0:
        relevance_label = "Medium"
    else:
        relevance_label = "Low"

    # CONTACTABILITY
    contact_points = sum([
        yes_no(row["website"]),
        yes_no(row["company_linkedin"]),
        yes_no(row["owner_linkedin"])
    ])

    if contact_points == 3:
        contact_score = contactability_weight
        contact_label = "High"
    elif contact_points == 2:
        contact_score = contactability_weight * 0.6
        contact_label = "Medium"
    elif contact_points == 1:
        contact_score = contactability_weight * 0.3
        contact_label = "Low"
    else:
        contact_score = 0
        contact_label = "Low"

    # CONFIDENCE
    filled = sum([
        is_filled(row["industry"]),
        is_filled(row["location"]),
        is_filled(row["website"]),
        is_filled(row["company_linkedin"]),
        is_filled(row["owner_linkedin"]),
        is_filled(row["revenue"]),
    ])

    completeness = filled / 6

    if completeness >= 0.8:
        confidence_score = confidence_weight
        confidence_label = "High"
    elif completeness >= 0.5:
        confidence_score = confidence_weight * 0.5
        confidence_label = "Medium"
    else:
        confidence_score = 0
        confidence_label = "Low"

    # REVENUE
    revenue_score, revenue_label = revenue_bucket(row["revenue"])

    # FINAL SCORE
    final_score = relevance_score + contact_score + confidence_score + revenue_score
    final_score = round(final_score, 2)

    priority = classify_priority(final_score)
    explanation = generate_explanation(
        industry_label,
        location_label,
        contact_label,
        confidence_label,
        revenue_label,
    )
    action = recommend_action(priority, contact_label)
    outreach_message = generate_outreach_message(
        row["company_name"],
        row["industry"],
        row["location"],
        action,
    )

    results.append({
        "Company": row["company_name"],
        "Industry": row["industry"],
        "Location": row["location"],
        "Industry Match": industry_label,
        "Location Match": location_label,
        "Relevance": relevance_label,
        "Contactability": contact_label,
        "Confidence": confidence_label,
        "Revenue Potential": revenue_label,
        "Final Score": final_score,
        "Priority": priority,
        "Recommended Action": action,
        "Explanation": explanation,
        "Suggested Outreach Message": outreach_message,
    })

# -----------------------------
# OUTPUT
# -----------------------------
result_df = pd.DataFrame(results).sort_values(by="Final Score", ascending=False)

st.subheader("Scored Leads")
st.dataframe(result_df, use_container_width=True)

csv_data = dataframe_to_csv_download(result_df)
st.download_button(
    label="Download scored leads as CSV",
    data=csv_data,
    file_name="scored_leads.csv",
    mime="text/csv",
)

# -----------------------------
# TOP 3 LEADS
# -----------------------------
st.subheader("Top 3 Recommended Leads")

top_3 = result_df.head(3)

if not top_3.empty:
    cols = st.columns(len(top_3))
    medal_labels = ["🥇", "🥈", "🥉"]

    for i, (_, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            st.markdown(f"### {medal_labels[i]} {row['Company']}")
            st.metric("Score", row["Final Score"])
            st.write(f"**Priority:** {row['Priority']}")
            st.write(f"**Action:** {row['Recommended Action']}")
            st.caption(row["Explanation"])
else:
    st.warning("No leads available to score.")

# -----------------------------
# OUTREACH ASSISTANT
# -----------------------------
st.subheader("Smart Outreach Assistant")

if not result_df.empty:
    selected_company = st.selectbox(
        "Select a lead to view suggested outreach",
        result_df["Company"].tolist()
    )

    selected_row = result_df[result_df["Company"] == selected_company].iloc[0]

    st.write(f"**Priority:** {selected_row['Priority']}")
    st.write(f"**Recommended Action:** {selected_row['Recommended Action']}")
    st.write(f"**Why this lead matters:** {selected_row['Explanation']}")

    st.text_area(
        "Suggested Outreach Message",
        value=selected_row["Suggested Outreach Message"],
        height=180,
    )
else:
    st.info("Upload or generate leads to use the outreach assistant.")