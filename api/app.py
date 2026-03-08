from fastapi import FastAPI
import pandas as pd

from src.model_loader import load_model
from src.forecast_pipeline import forecast_next_7_days

import holidays

us_holidays = holidays.US()
app = FastAPI()

model, feature_columns = load_model()


@app.get("/forecast")

def forecast():

    df = pd.read_csv(
        "datasets/eda_cleaned.csv",
        parse_dates=True,
        index_col="date"
    )

    predictions = forecast_next_7_days(
        model,
        df,
        feature_columns,
        us_holidays
    )

    return {"forecast": predictions}