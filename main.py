import pandas as pd

# import plotly.express as px
import streamlit as st
# import json
# import os

# used to configure the layout and appearance of your Streamlit app before you render anything
st.set_page_config(page_title="Finace Tracker", page_icon=" ", layout="wide")


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]  # removes all leading spaces
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")

        st.write(df)
        return df
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
                st.write(debits_df)
            with tab2:
                st.write(credits_df)


main()
