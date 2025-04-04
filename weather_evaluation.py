import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

class WeatherMLModel:
    '''Represents a machine learning model for predicting rainfall.'''

    def __init__(self):
        self.model = None
        self.data = None
        self.labels = None

    def load_dataset(self, file_path: str):
        '''
        Loads the Rain in Australia dataset.
        Preconditions:
        - file_path must be a non-empty string.
        Postconditions:
        - self.data must not be empty.
        - self.labels must not be empty.
        '''
        assert isinstance(file_path, str) and file_path.strip(), "Precondition: file_path must be a non-empty string."
        assert '\x00' not in file_path, "Precondition: file_path cannot contain null characters."
        assert os.path.exists(file_path) and os.path.isfile(file_path), "Precondition: File must exist and it should be a file not folder."

        df = pd.read_csv(file_path)

        df = df.drop(columns=['Date', 'Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm'])

        #converting string to numerical values
        df["RainToday"] = df["RainToday"].map({"No": 0, "Yes": 1})
        df["RainTomorrow"] = df["RainTomorrow"].map({"No": 0, "Yes": 1})

        #initial_rows = df.shape[0]
        df = df.dropna()
        #assert df.shape[0] > 0.75 * initial_rows, "Postcondition: More than 75% of data lost after dropping NaN values."
        # self.labels = df["RainTomorrow"].apply(lambda x: 1 if x == "Yes" else 0).values
        # self.data = df.drop(columns=["RainTomorrow"]).values

        self.labels = df["RainTomorrow"].values  # Target variable (0 or 1)
        self.data = df.drop(columns=["RainTomorrow"]).values

        assert self.data is not None and len(self.data) > 0, "Postcondition: Data must not be empty."
        assert self.labels is not None and len(self.labels) > 0, "Postcondition: Labels must not be empty."

    def train_model(self, test_size: float):
        '''
        Trains a Logistic Regression model.
        Preconditions:
        - test_size must be between 0 and 1.
        - The dataset must be loaded before training.
        Postconditions:
        - The model must be trained (self.model should not be None).
        '''
        assert 0 < test_size < 1, "Precondition: test_size must be between 0 and 1."
        assert self.data is not None, "Precondition: Data must be loaded before training."

        X_train, X_test, y_train, y_test = train_test_split(self.data, self.labels, test_size=test_size)
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

        assert self.model is not None, "Postcondition: Model must be trained."

    def evaluate_model(self, test_size: float) -> float:
        '''
        Evaluates the trained model using accuracy.
        Preconditions:
        - Model must be trained before evaluation.
        Postconditions:
        - Accuracy must be between 0 and 1.
        '''
        assert self.model is not None, "Precondition: Model must be trained before evaluation."
        assert 0 < test_size < 1, "Precondition: test_size must be between 0 and 1."

        X_train, X_test, y_train, y_test = train_test_split(self.data, self.labels, test_size=test_size)
        accuracy = self.model.score(X_test, y_test)

        assert 0 <= accuracy <= 1, "Postcondition: Accuracy must be between 0 and 1."
        return accuracy

    def predict(self, features: np.ndarray) -> int:
        '''
        Makes a prediction using the trained model.
        Preconditions:
        - Model must be trained before prediction.
        - Features must be a valid numpy array.
        Postconditions:
        - Output must be 0 (No Rain) or 1 (Rain).
        '''
        assert self.model

#for manual testing
if __name__ == "__main__":
    model = WeatherMLModel()
    model.load_dataset("weatherAUS.csv")
    model.train_model(test_size=0.2)

    test_features = model.data[0]  # Taking first row as an example
    prediction = model.predict(test_features)

    print("Prediction:", "Rain" if prediction == 1 else "No Rain")
