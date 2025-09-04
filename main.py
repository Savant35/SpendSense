# import pandas as pd
# import plotly.express as px
import streamlit as st
# import json
# import os

# used to configure the layout and appearance of your Streamlit app before you render anything
st.set_page_config(page_title="Finace Tracker", page_icon=" ", layout="wide")


def load_transactions(file):
    pass


def main():
    st.title("Finance tracker")
    uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)


main()
