import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Amazon Automation Engine", layout="wide")

st.title("📊 Amazon Automation Insights Report")

st.write(
    "Upload Amazon datasets. The automation engine will analyze PPC, reviews, and competitor data."
)

# 🔥 PUT YOUR PRODUCTION WEBHOOK URL HERE
WEBHOOK_URL = "https://shankssks09.app.n8n.cloud/webhook/amazon-upload"


# ---------------------------
# File Upload
# ---------------------------

listings_file = st.file_uploader("Upload competitor_listings.csv", type=["csv"])
reviews_file = st.file_uploader("Upload reviews.csv", type=["csv"])
ppc_file = st.file_uploader("Upload ppc_terms.csv", type=["csv"])


if listings_file and reviews_file and ppc_file:

    listings_df = pd.read_csv(listings_file)
    reviews_df = pd.read_csv(reviews_file)
    ppc_df = pd.read_csv(ppc_file)

    st.success("Files uploaded successfully.")

    combined_data = {
        "listings": listings_df.to_dict(orient="records"),
        "reviews": reviews_df.to_dict(orient="records"),
        "ppc": ppc_df.to_dict(orient="records"),
        "manual_time_estimate_hours": 6,
        "automated_time_estimate_hours": 1,
        "estimated_efficiency_gain_percent": 83
    }

    if st.button("Run AI Analysis"):

        if "PASTE_YOUR_N8N_PRODUCTION_WEBHOOK_URL_HERE" in WEBHOOK_URL:
            st.error("Please update WEBHOOK_URL in app.py with your actual production webhook URL.")
        else:
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json=combined_data,
                    timeout=30
                )

                if response.status_code != 200:
                    st.error(f"Webhook returned status {response.status_code}")
                    st.text(response.text)
                    st.stop()

                if not response.text.strip():
                    st.error("Empty response from webhook")
                    st.stop()

                raw = response.json()

                # ---------------------------
                # UNIVERSAL RESPONSE PARSER
                # ---------------------------

                if isinstance(raw, list) and len(raw) > 0:
                    result = raw[0]
                else:
                    result = raw

                # If wrapped in "json"
                if isinstance(result, dict) and "json" in result:
                    result = result["json"]

                # If wrapped in "body"
                if isinstance(result, dict) and "body" in result:
                    result = result["body"]

                # Final safety
                if not isinstance(result, dict):
                    st.error("Unexpected response format from automation engine.")
                    st.json(raw)
                    st.stop()

                st.success("Automation engine completed analysis.")

                # ---------------------------
                # DISPLAY RESULTS
                # ---------------------------

                st.header("Top Complaint Themes")

                complaints = result.get("complaints", [])
                if complaints:
                    for c in complaints:
                        st.markdown(f"- {c}")
                else:
                    st.info("No complaint patterns detected.")


                st.header("High Spend – Low Conversion PPC Terms")

                ppc_waste = result.get("ppc_waste", [])
                if ppc_waste:
                    ppc_df = pd.DataFrame(ppc_waste)
                    st.dataframe(ppc_df)

                    total_waste = sum(x.get("spend", 0) for x in ppc_waste)
                    st.metric("Total Inefficient Spend Identified", f"${total_waste:,.2f}")
                else:
                    st.info("No major PPC inefficiencies detected.")


                st.header("Keyword Opportunity Gaps")

                keyword_opps = result.get("keyword_opportunities", [])
                if keyword_opps:
                    kw_df = pd.DataFrame(keyword_opps, columns=["Keyword"])
                    st.dataframe(kw_df)
                else:
                    st.info("No significant keyword gaps detected.")


                st.header("Strategic Recommendations")

                recs = result.get("recommendations", [])
                if recs:
                    for r in recs:
                        st.markdown(f"- {r}")
                else:
                    st.info("No recommendations generated.")


                st.header("Automation Efficiency Impact")

                efficiency = result.get("efficiency_summary", "")
                if efficiency:
                    st.success(efficiency)
                else:
                    st.info("Efficiency summary not available.")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection failed: {e}")

else:
    st.info("Please upload all three CSV files to begin.")