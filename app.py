import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Amazon Automation Data Uploader")

st.title("Amazon Workflow Automation - Data Uploader")

st.write("Upload the three required CSV files below to generate structured JSON for automation.")

# Upload files
listings_file = st.file_uploader("Upload competitor_listings.csv", type=["csv"])
reviews_file = st.file_uploader("Upload reviews.csv", type=["csv"])
ppc_file = st.file_uploader("Upload ppc_terms.csv", type=["csv"])

if listings_file and reviews_file and ppc_file:

    # Read CSVs
    listings_df = pd.read_csv(listings_file)
    reviews_df = pd.read_csv(reviews_file)
    ppc_df = pd.read_csv(ppc_file)

    st.success("Files uploaded successfully!")

    # Show previews
    st.subheader("Preview - Competitor Listings")
    st.dataframe(listings_df)

    st.subheader("Preview - Reviews")
    st.dataframe(reviews_df)

    st.subheader("Preview - PPC Terms")
    st.dataframe(ppc_df)

    # Combine data
    combined_data = {
        "listings": listings_df.to_dict(orient="records"),
        "reviews": reviews_df.to_dict(orient="records"),
        "ppc": ppc_df.to_dict(orient="records"),
        "manual_time_estimate_hours": 6,
        "automated_time_estimate_hours": 1,
        "estimated_efficiency_gain_percent": 83
    }

    json_data = json.dumps(combined_data, indent=4)

    st.subheader("Download Combined JSON for n8n")
    st.download_button(
        label="Download amazon_combined_data.json",
        data=json_data,
        file_name="amazon_combined_data.json",
        mime="application/json"
    )

else:
    st.info("Please upload all three CSV files to generate JSON.")