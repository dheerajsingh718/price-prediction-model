import pandas as pd

def forecast_next_7_days(model, df, feature_columns, us_holidays):

    forecast_df = df.copy()
    predictions = []

    for _ in range(7):

        last_date = forecast_df.index[-1]
        next_date = last_date + pd.Timedelta(days=1)

        new_row = {}

        # calendar features
        new_row["month"] = next_date.month
        new_row["week"] = int(next_date.isocalendar().week)
        new_row["quarter"] = next_date.quarter
        new_row["is_weekend"] = int(next_date.weekday() >= 5)
        new_row["week_of_year"] = int(next_date.isocalendar().week)
        new_row["day_of_week"] = next_date.weekday()

        # holiday features
        is_hol = int(next_date.date() in us_holidays)
        new_row["is_holiday"] = is_hol

        holiday_dates = pd.to_datetime(list(us_holidays.keys()))
        future_holidays = holiday_dates[holiday_dates >= pd.Timestamp(next_date)]

        if len(future_holidays) == 0:
            new_row["days_to_next_holiday"] = 365
        else:
            new_row["days_to_next_holiday"] = (
                future_holidays.min() - pd.Timestamp(next_date)
            ).days

        # store status
        if is_hol == 1:
            new_row["store_open"] = 0
            new_row["is_closed"] = 1
        else:
            new_row["store_open"] = 1
            new_row["is_closed"] = 0

        new_row["is_suspicious_zero"] = 0

        # lag features
        new_row["lag_1"] = forecast_df["total"].iloc[-1]
        new_row["lag_7"] = forecast_df["total"].iloc[-7]
        new_row["lag_14"] = forecast_df["total"].iloc[-14]

        # rolling features
        new_row["total_10_days_rolling"] = forecast_df["total"].iloc[-10:].mean()
        new_row["total_30_days_rolling"] = forecast_df["total"].iloc[-30:].mean()
        new_row["total_50_days_rolling"] = forecast_df["total"].iloc[-50:].mean()

        new_row_df = pd.DataFrame([new_row], index=[next_date])

        X = new_row_df.reindex(columns=feature_columns)

        pred = model.predict(X)[0]

        new_row_df["total"] = pred

        forecast_df = pd.concat([forecast_df, new_row_df])

        predictions.append(pred)

    return predictions