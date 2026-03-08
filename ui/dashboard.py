import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Store Sales Forecast", layout="wide")

st.title("Store Sales Forecast Dashboard")
st.write("Next 7 days sales forecast from the deployed ML model.")

API_URL = "http://127.0.0.1:8000/forecast"

try:
    response = requests.get(API_URL)
    response.raise_for_status()

    data = response.json()
    forecast_values = data["forecast"]

    forecast_dates = pd.date_range(
        start=pd.Timestamp.today().normalize(),
        periods=7,
        freq="D"
    )

    forecast_df = pd.DataFrame({
        "Date": forecast_dates,
        "Forecasted Sales": forecast_values
    })

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("7-Day Forecast Trend")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(
            forecast_df["Date"],
            forecast_df["Forecasted Sales"],
            marker="o"
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Forecasted Sales")
        ax.set_title("Forecasted Sales for Next 7 Days")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader("Summary")
        st.metric("Average Forecast", f"{forecast_df['Forecasted Sales'].mean():.2f}")
        st.metric("Max Forecast", f"{forecast_df['Forecasted Sales'].max():.2f}")
        st.metric("Min Forecast", f"{forecast_df['Forecasted Sales'].min():.2f}")

    st.subheader("Forecast Table")
    st.dataframe(forecast_df, use_container_width=True)

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the FastAPI server. Make sure it is running on http://127.0.0.1:8000")
except Exception as e:
    st.error(f"Something went wrong: {e}")