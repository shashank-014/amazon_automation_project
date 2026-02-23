import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Amazon Automation Data Uploader")

DATA_PATH = "amazon_combined_data.json"

# 🔹 API MODE
query_params = st.query_params

if "api" in query_params:

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        st.json(data)
    else:
        st.json({"error": "No data uploaded yet."})

    st.stop()


# 🔹 NORMAL UI MODE
st.title("Amazon Workflow Automation - Data Uploader")

st.write("Upload the three required CSV files below to generate structured JSON.")

listings_file = st.file_uploader("Upload competitor_listings.csv", type=["csv"])
reviews_file = st.file_uploader("Upload reviews.csv", type=["csv"])
ppc_file = st.file_uploader("Upload ppc_terms.csv", type=["csv"])

if listings_file and reviews_file and ppc_file:

    listings_df = pd.read_csv(listings_file)
    reviews_df = pd.read_csv(reviews_file)
    ppc_df = pd.read_csv(ppc_file)

    st.success("Files uploaded successfully!")

    combined_data = {
        "listings": listings_df.to_dict(orient="records"),
        "reviews": reviews_df.to_dict(orient="records"),
        "ppc": ppc_df.to_dict(orient="records"),
        "manual_time_estimate_hours": 6,
        "automated_time_estimate_hours": 1,
        "estimated_efficiency_gain_percent": 83
    }

    with open(DATA_PATH, "w") as f:
        json.dump(combined_data, f, indent=4)

    st.success("JSON data saved successfully!")

    st.subheader("Preview")
    st.json(combined_data)

    st.write("API endpoint available at:")
    st.code(st.experimental_get_query_params())

else:
    st.info("Please upload all three CSV files.")