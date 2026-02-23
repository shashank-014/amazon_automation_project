import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Amazon Automation Engine", layout="wide")

st.title("Amazon Automation Engine – Performance Insights")

st.write(
    "Upload Amazon datasets. The automation engine will analyze PPC, reviews, and competitor data."
)

# 🔹 PUT YOUR PRODUCTION WEBHOOK URL HERE
WEBHOOK_URL = "PASTE_YOUR_N8N_PRODUCTION_WEBHOOK_URL_HERE"


# ---------------------------
# File Upload Section
# ---------------------------

listings_file = st.file_uploader("Upload competitor_listings.csv", type=["csv"])
reviews_file = st.file_uploader("Upload reviews.csv", type=["csv"])
ppc_file = st.file_uploader("Upload ppc_terms.csv", type=["csv"])

if listings_file and reviews_file and ppc_file:

    listings_df = pd.read_csv(listings_file)
    reviews_df = pd.read_csv(reviews_file)
    ppc_df = pd.read_csv(ppc_file)

    st.success("Files uploaded successfully.")

    with st.expander("Preview Uploaded Data"):
        st.subheader("Competitor Listings")
        st.dataframe(listings_df)

        st.subheader("Customer Reviews")
        st.dataframe(reviews_df)

        st.subheader("PPC Terms")
        st.dataframe(ppc_df)

    combined_data = {
        "listings": listings_df.to_dict(orient="records"),
        "reviews": reviews_df.to_dict(orient="records"),
        "ppc": ppc_df.to_dict(orient="records"),
        "manual_time_estimate_hours": 6,
        "automated_time_estimate_hours": 1,
        "estimated_efficiency_gain_percent": 83
    }

    st.subheader("Run Automation")

    if st.button("Run AI Analysis"):

        if "PASTE_YOUR_N8N_PRODUCTION_WEBHOOK_URL_HERE" in WEBHOOK_URL:
            st.error("Please update WEBHOOK_URL in app.py with your actual production webhook URL.")
        else:
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json=combined_data,
                    timeout=20
                )

                if response.status_code == 200:

                    raw = response.json()

                    # n8n returns a list of items
                    if isinstance(raw, list) and len(raw) > 0:
                        result = raw[0]
                    else:
                        result = raw

                    st.success("Automation engine completed analysis.")

                    st.header("📊 Automation Insights Report")

                    # ---------------------------
                    # Complaints
                    # ---------------------------
                    st.subheader("Top Complaint Themes")
                    if result.get("complaints"):
                        for complaint in result["complaints"]:
                            st.markdown(f"- {complaint}")
                    else:
                        st.info("No complaint patterns detected.")

                    # ---------------------------
                    # PPC Waste
                    # ---------------------------
                    st.subheader("High Spend – Low Conversion PPC Terms")

                    if result.get("ppc_waste"):
                        ppc_result_df = pd.DataFrame(result["ppc_waste"])
                        st.dataframe(ppc_result_df)

                        # Optional: Simple metric summary
                        total_waste = sum(item["spend"] for item in result["ppc_waste"])
                        st.metric("Total Inefficient Spend Identified", f"${total_waste:,.2f}")
                    else:
                        st.info("No major PPC inefficiencies detected.")

                    # ---------------------------
                    # Keyword Opportunities
                    # ---------------------------
                    st.subheader("Keyword Opportunity Gaps")

                    if result.get("keyword_opportunities"):
                        kw_df = pd.DataFrame(result["keyword_opportunities"], columns=["Keyword"])
                        st.dataframe(kw_df)
                    else:
                        st.info("No significant keyword gaps detected.")

                    # ---------------------------
                    # Recommendations
                    # ---------------------------
                    st.subheader("Strategic Recommendations")
                    if result.get("recommendations"):
                        for rec in result["recommendations"]:
                            st.markdown(f"- {rec}")
                    else:
                        st.info("No recommendations generated.")

                    # ---------------------------
                    # Efficiency Summary
                    # ---------------------------
                    st.subheader("Automation Efficiency Impact")
                    st.success(result.get("efficiency_summary", ""))

                else:
                    st.error(f"Engine returned status {response.status_code}")
                    st.text(response.text)

            except requests.exceptions.RequestException as e:
                st.error(f"Connection failed: {e}")

else:
    st.info("Please upload all three CSV files to begin.")