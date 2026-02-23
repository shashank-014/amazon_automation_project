import streamlit as st
import pandas as pd
import json
import requests

st.set_page_config(page_title="Amazon Automation Uploader")

st.title("Amazon Workflow Automation - Data Uploader")

st.write(
    "Upload the required CSV files. The dataset will be pushed to the automation engine via webhook."
)

# 🔹 Replace with your actual n8n webhook production URL
WEBHOOK_URL = "https://shankssks09.app.n8n.cloud/webhook-test/amazon-upload"

# File Uploads
listings_file = st.file_uploader("Upload competitor_listings.csv", type=["csv"])
reviews_file = st.file_uploader("Upload reviews.csv", type=["csv"])
ppc_file = st.file_uploader("Upload ppc_terms.csv", type=["csv"])

if listings_file and reviews_file and ppc_file:

    # Read CSVs
    listings_df = pd.read_csv(listings_file)
    reviews_df = pd.read_csv(reviews_file)
    ppc_df = pd.read_csv(ppc_file)

    st.success("Files uploaded successfully!")

    # Preview data
    with st.expander("Preview Competitor Listings"):
        st.dataframe(listings_df)

    with st.expander("Preview Reviews"):
        st.dataframe(reviews_df)

    with st.expander("Preview PPC Terms"):
        st.dataframe(ppc_df)

    # Combine into structured JSON
    combined_data = {
        "listings": listings_df.to_dict(orient="records"),
        "reviews": reviews_df.to_dict(orient="records"),
        "ppc": ppc_df.to_dict(orient="records"),
        "manual_time_estimate_hours": 6,
        "automated_time_estimate_hours": 1,
        "estimated_efficiency_gain_percent": 83
    }

    st.subheader("Ready to Send Data to Automation Engine")

    if st.button("Send Data to Automation Engine"):

        if "PASTE_YOUR_N8N_WEBHOOK_URL_HERE" in WEBHOOK_URL:
            st.error("Please update the WEBHOOK_URL in app.py with your actual n8n webhook URL.")
        else:
            try:
                response = requests.post(WEBHOOK_URL, json=combined_data)

                if response.status_code == 200:
                    st.success("Data successfully sent to automation engine!")
                    st.subheader("Automation Engine Response:")
                    st.json(response.json())
                else:
                    st.error(f"Error sending data: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Connection failed: {e}")

else:
    st.info("Please upload all three CSV files to continue.")