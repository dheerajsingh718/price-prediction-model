import joblib

def load_model():

    model = joblib.load("model/ridge_model.pkl")
    features = joblib.load("model/feature_columns.pkl")

    return model, features