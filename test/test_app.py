import pytest
import pandas as pd
import pickle
import os
from sklearn.metrics import accuracy_score



def test_data_file_exists():
    """Check if the dataset file exists"""
    assert os.path.exists("Files/Data/Telco-Customer-Churn.csv") 
    


def test_data_loading():
    """Test if data loads correctly and has expected structure"""
    
    df = pd.read_csv("Files/Data/Telco-Customer-Churn.csv")  # update path
    
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0
    assert "Churn" in df.columns


def test_no_duplicate_columns():
    df = pd.read_csv("Files/Data/Telco-Customer-Churn.csv")
    assert df.columns.duplicated().sum() == 0


def test_churn_column_values():
    """Churn should normally contain 0 and 1 (or Yes/No)"""
    df = pd.read_csv("Files/Data/Telco-Customer-Churn.csv")
    unique_values = df["Churn"].nunique()
    assert unique_values >= 2




def test_model_columns_file_exists():
    assert os.path.exists("models/model_columns.pkl")


def test_model_columns_loading():
    with open("models/model_columns.pkl", "rb") as f:
        model_columns = pickle.load(f)
    
    assert isinstance(model_columns, list)
    assert len(model_columns) > 0
    print(f"Total features expected by model: {len(model_columns)}")




def test_model_files_exist():
    model_files = [
        "models/model_xgb.sav",
        "models/best_xgb.sav",
        "models/model_rf_smote.sav",
        "models/best_rf.sav",
        "models/model_lr.sav",
        "models/model_nb.sav"
    ]
    
    for model_file in model_files:
        assert os.path.exists(model_file), f"{model_file} is missing"


def test_model_loading_and_prediction():
    """Test if a model can be loaded and can make a prediction"""
    
    # Load column order
    with open("models/model_columns.pkl", "rb") as f:
        model_columns = pickle.load(f)
    
    # Create a dummy input matching the column structure
    import numpy as np
    dummy_input = pd.DataFrame(
        np.zeros((1, len(model_columns))), 
        columns=model_columns
    )
    
    # Test with one model (XGBoost)
    with open("models/model_xgb.sav", "rb") as f:
        model = pickle.load(f)
    
    prediction = model.predict(dummy_input)
    
    assert prediction is not None
    assert len(prediction) == 1
    assert prediction[0] in [0, 1]


def test_multiple_models_prediction():
    """Test prediction with multiple models"""
    
    with open("models/model_columns.pkl", "rb") as f:
        model_columns = pickle.load(f)
    
    dummy_input = pd.DataFrame(
        [[0] * len(model_columns)], 
        columns=model_columns
    )
    
    models_to_test = [
        "models/model_xgb.sav",
        "models/model_rf_smote.sav",
        "models/model_lr.sav",
        "models/model_nb.sav"
    ]
    
    for model_path in models_to_test:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        
        pred = model.predict(dummy_input)[0]
        assert pred in [0, 1], f"Invalid prediction from {model_path}"


