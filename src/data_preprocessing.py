# data_preprocessing.py

import pandas as pd


def load_data(path):
    """
    Load dataset from given path
    """
    df = pd.read_csv(path)
    return df


def clean_data(df):
    """
    Clean dataset:
    - Remove unnecessary columns
    - Handle missing values
    - Convert data types
    """

    # Drop customerID (not useful for modeling)
    if 'customerID' in df.columns:
        df = df.drop(columns=['customerID'])

    # Convert TotalCharges to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Fill missing values
    df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

    return df


def encode_target(df):
    """
    Encode target variable (Churn)
    """
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df


def encode_categorical(df):
    """
    Convert categorical variables using one-hot encoding
    """
    df = pd.get_dummies(df, drop_first=True)
    return df


def preprocess_pipeline(path):
    """
    Complete preprocessing pipeline
    """
    import os
    print("Files in raw folder:", os.listdir("../data/raw"))
    df = load_data(path)
    df = clean_data(df)
    df = encode_target(df)
    df = encode_categorical(df)

    return df


if __name__ == "__main__":
    path = "../data/raw/churn.csv"
    df = preprocess_pipeline(path)

    print("Preprocessing completed.")
    print(df.head())