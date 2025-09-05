import pandas as pd
import time

import plotly.express as px
import streamlit as st
import json
import os

# used to configure the layout and appearance of your Streamlit app before you render anything
st.set_page_config(page_title="Finace Tracker", page_icon=" ", layout="wide")

category_file = "categories.json"

if "categories" not in st.session_state:
    st.session_state.categories = {"Uncategorized": []}

if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)


def save_categories():
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)


def categorize_transactions(df):
    df["Category"] = "Uncategorized"

    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue

        lowered_keywords = [keyword.lower().strip() for keyword in keywords]

        for idx, row in df.itterrows():
            details = row["Details"].lower().strip()

            if details in lowered_keywords:
                df.at[idx, "Category"] = category

    return df


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]  # removes all leading spaces
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

        return categorize_transactions(df)
    except Exception as e:
        st.error(f"Error proecessing file: {str(e)}")
        return None  # no data loaded


def main():
    st.title("Finance tracker")
    uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Debit"].copy()

            tab1, tab2 = st.tabs(["Expenses (Debits)", "Payments (Credits)"])
            with tab1:
                new_category = st.text_input("New Category Name")
                add_button = st.button("Add Category")

                if new_category not in st.session_state.categories:
                    st.session_state.categories[new_category] = []
                    save_categories()
                    st.success(f"New Category Added: {new_category}")
                    time.sleep(1)
                    st.rerun()

                st.write(debits_df)
            with tab2:
                st.write(credits_df)


main()
