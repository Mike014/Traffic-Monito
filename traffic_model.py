# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

def train_knn_model(data):
    X = data[['feature1', 'feature2']]  
    y = data['traffic']
    model = KNeighborsRegressor(n_neighbors=3)
    model.fit(X, y)
    return model

def predict_traffic(model, current_conditions):
    current_conditions_df = pd.DataFrame([current_conditions], columns=['feature1', 'feature2'])
    return model.predict(current_conditions_df)

if __name__ == '__main__':
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4],
        'feature2': [4, 3, 2, 1],
        'traffic': [100, 200, 300, 400]
    })
    model = train_knn_model(data)
    print(predict_traffic(model, [3, 2]))  # [300.]




