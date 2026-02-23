import streamlit as st
import pandas as pd
import json
import requests

st.set_page_config(page_title="Amazon Automation Engine", layout="wide")

st.title("Amazon Automation Engine - AI Insight Dashboard")

st.write(
    "Upload the required Amazon datasets. The automation engine will analyze performance and generate strategic insights."
)

# 🔹 Replace with your actual PRODUCTION webhook URL
WEBHOOK_URL = "https://shankssks09.app.n8n.cloud/webhook/amazon-upload"

# File Uploads
listings_file = st.file_uploader("Upload competitor_listings.csv", type=["csv"])
reviews_file = st.file_uploader("Upload reviews.csv", type=["csv"])
ppc_file = st.file_uploader("Upload ppc_terms.csv", type=["csv"])

if listings_file and reviews_file and ppc_file:

    listings_df = pd.read_csv(listings_file)
    reviews_df = pd.read_csv(reviews_file)
    ppc_df = pd.read_csv(ppc_file)

    st.success("Files uploaded successfully.")

    with st.expander("Preview Uploaded Data"):
        st.write("Competitor Listings")
        st.dataframe(listings_df)

        st.write("Reviews")
        st.dataframe(reviews_df)

        st.write("PPC Terms")
        st.dataframe(ppc_df)

    combined_data = {
        "listings": listings_df.to_dict(orient="records"),
        "reviews": reviews_df.to_dict(orient="records"),
        "ppc": ppc_df.to_dict(orient="records"),
        "manual_time_estimate_hours": 6,
        "automated_time_estimate_hours": 1,
        "estimated_efficiency_gain_percent": 83
    }

    st.subheader("Send Data to Automation Engine")

    if st.button("Run AI Analysis"):

        if "PASTE_YOUR_N8N_PRODUCTION_WEBHOOK_URL_HERE" in WEBHOOK_URL:
            st.error("Please update the WEBHOOK_URL in app.py with your actual production webhook URL.")
        else:
            try:
                response = requests.post(WEBHOOK_URL, json=combined_data)

                if response.status_code == 200:

                    st.success("Automation engine completed analysis.")

                    result = response.json()[0]

                    st.header("📊 Automation Insights Report")

                    # 🔹 Complaint Themes
                    st.subheader("Top Complaint Themes")
                    for complaint in result.get("complaints", []):
                        st.markdown(f"- {complaint}")

                    # 🔹 PPC Waste Table
                    st.subheader("High Spend – Low Conversion PPC Terms")

                    if result.get("ppc_waste"):
                        ppc_df_result = pd.DataFrame(result["ppc_waste"])
                        st.dataframe(ppc_df_result)

                        if "spend" in ppc_df_result.columns and "conversion_rate" in ppc_df_result.columns:
                            st.subheader("Spend vs Conversion Rate")
                            st.scatter_chart(
                                ppc_df_result.set_index("keyword")[["spend", "conversion_rate"]]
                            )

                        total_waste = sum(item.get("spend", 0) for item in result["ppc_waste"])
                        projected_recovery = total_waste * 0.3

                        st.subheader("Projected Optimization Impact")
                        st.metric("Potential Recoverable Ad Spend (30%)", f"${projected_recovery:,.2f}")

                    else:
                        st.info("No major PPC inefficiencies detected.")

                    # 🔹 Keyword Opportunities
                    st.subheader("Keyword Opportunity Gaps")

                    if result.get("keyword_opportunities"):
                        kw_df = pd.DataFrame(result["keyword_opportunities"])
                        st.dataframe(kw_df)
                    else:
                        st.info("No significant keyword gaps detected.")

                    # 🔹 Strategic Recommendations
                    st.subheader("Strategic Recommendations")
                    for rec in result.get("recommendations", []):
                        st.markdown(f"- {rec}")

                    # 🔹 Efficiency Summary
                    st.subheader("Automation Efficiency Impact")
                    st.success(result.get("efficiency_summary", ""))

                else:
                    st.error(f"Error from automation engine: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Connection failed: {e}")

else:
    st.info("Please upload all three CSV files to begin.")