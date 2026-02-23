import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Amazon Automation Engine", layout="wide")

st.title("📊 Amazon Automation Insights Report")

st.write(
    "Upload Amazon datasets. The automation engine will analyze PPC, reviews, and competitor data."
)

# 🔥 PRODUCTION WEBHOOK URL
WEBHOOK_URL = "https://shankssks09.app.n8n.cloud/webhook/amazon-upload"


# =========================================================
# FILE UPLOAD
# =========================================================

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
        "automated_time_estimate_hours": 1
    }

    if st.button("🚀 Run AI Analysis"):

        try:
            response = requests.post(
                WEBHOOK_URL,
                json=combined_data,
                timeout=60
            )

            if not response.text.strip():
                st.error("Empty response from automation engine.")
                st.stop()

            raw = response.json()

            # Handle n8n array wrapper
            if isinstance(raw, list):
                result = raw[0]
            else:
                result = raw

            if "json" in result:
                result = result["json"]

            st.success("Automation engine completed analysis.")

            # =========================================================
            # EXECUTIVE AI INSIGHTS
            # =========================================================

            st.header("🧠 AI Executive Summary")

            st.write(result.get("executive_summary", "No summary generated."))

            col1, col2 = st.columns(2)

            col1.metric("Risk Level", result.get("risk_level", "N/A"))
            col2.metric(
                "Growth Opportunity",
                f"{result.get('growth_opportunity_percent', '0')}%"
            )

            urgent_actions = result.get("urgent_actions", [])
            if urgent_actions:
                st.subheader("Top Urgent Actions")
                for action in urgent_actions:
                    st.markdown(f"- {action}")

            # =========================================================
            # COMPLAINT THEMES
            # =========================================================

            st.header("🔎 Top Complaint Themes")

            complaints = result.get("complaints", [])

            if complaints:
                comp_df = pd.DataFrame({
                    "Complaint": complaints,
                    "Count": [1]*len(complaints)
                })

                fig = px.bar(
                    comp_df,
                    x="Complaint",
                    y="Count",
                    title="Complaint Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No complaint patterns detected.")

            # =========================================================
            # PPC INEFFICIENCIES
            # =========================================================

            st.header("💰 High Spend – Low Conversion PPC Terms")

            ppc_waste = result.get("ppc_waste", [])

            if ppc_waste:
                waste_df = pd.DataFrame(ppc_waste)
                st.dataframe(waste_df)

                total_waste = waste_df["spend"].sum()
                st.metric("Total Inefficient Spend Identified", f"${total_waste:,.2f}")

                fig2 = px.scatter(
                    waste_df,
                    x="spend",
                    y="conversion_rate",
                    text="keyword",
                    title="PPC Inefficiency Map"
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No major PPC inefficiencies detected.")

            # =========================================================
            # KEYWORD OPPORTUNITIES
            # =========================================================

            st.header("🚀 Keyword Opportunity Gaps")

            keyword_opps = result.get("keyword_opportunities", [])

            if keyword_opps:
                kw_df = pd.DataFrame(keyword_opps, columns=["Keyword"])
                st.dataframe(kw_df)
            else:
                st.info("No significant keyword gaps detected.")

            # =========================================================
            # PREDICTION SECTION
            # =========================================================

            st.header("📈 30-Day Financial Projection")

            prediction = result.get("prediction", {})

            if prediction:
                col1, col2 = st.columns(2)

                col1.metric(
                    "Projected Monthly Waste",
                    f"${prediction.get('projected_monthly_waste', 0):,.2f}"
                )

                col2.metric(
                    "Potential Revenue Lift",
                    f"{prediction.get('potential_revenue_lift_percent', 0)}%"
                )
            else:
                st.info("Prediction data not available.")

            # =========================================================
            # STRATEGIC RECOMMENDATIONS
            # =========================================================

            st.header("🎯 Strategic Recommendations")

            recs = result.get("recommendations", [])

            if recs:
                for r in recs:
                    st.markdown(f"- {r}")
            else:
                st.info("No recommendations generated.")

            # =========================================================
            # EFFICIENCY IMPACT
            # =========================================================

            st.header("⚡ Automation Efficiency Impact")

            efficiency = result.get("efficiency_summary", "")
            if efficiency:
                st.success(efficiency)
            else:
                st.info("Efficiency summary not available.")

        except Exception as e:
            st.error(f"Connection failed: {e}")

else:
    st.info("Please upload all three CSV files to begin.")