import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV
from tabulate import tabulate
from sklearn.datasets import fetch_california_housing

'''Wczytaj dane california housing'''
california_housing = fetch_california_housing()
data = pd.DataFrame(data=california_housing.data, columns=california_housing.feature_names)
target = california_housing.target

'''Standaryzacja danych'''
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

'''Podziel dane na zbiór uczący i testujący'''
X_train, X_test, y_train, y_test = tts(data_scaled, target, test_size=0.3, random_state=42)

'''Utwórz model MLPRegressor z dodatkowymi parametrami'''
mlp = MLPRegressor(max_iter=2000, random_state=42, hidden_layer_sizes=(100,), learning_rate='adaptive', alpha=0.0001)

'''Naucz model na danych uczących'''
mlp.fit(X_train, y_train)

'''Ocena jakości modelu na danych testowych i uczących'''
y_pred_train = mlp.predict(X_train)
y_pred_test = mlp.predict(X_test)

'''Ocena jakości modelu na danych testowych i uczących'''
mae_train_percent = mean_absolute_error(y_train, y_pred_train) / np.mean(y_train) * 100
mse_train_percent = mean_squared_error(y_train, y_pred_train) / np.mean(y_train) * 100
mae_test_percent = mean_absolute_error(y_test, y_pred_test) / np.mean(y_test) * 100
mse_test_percent = mean_squared_error(y_test, y_pred_test) / np.mean(y_test) * 100

print("MAE (mean absolute error) na danych uczących: {:.2f}%".format(mae_train_percent))
print("MSE (mean squared error) na danych uczących: {:.2f}%".format(mse_train_percent))
print("MAE (mean absolute error) na danych testowych: {:.2f}%".format(mae_test_percent))
print("MSE (mean squared error) na danych testowych: {:.2f}%".format(mse_test_percent))

'''Definiuj przestrzeń parametrów do przeszukania'''
param_grid = {
    'alpha': [0.0001, 0.001, 0.01, 0.1, 1],
    'hidden_layer_sizes': [(100,), (10,), (10, 10)],
    'learning_rate': ['constant', 'adaptive']
}

'''Użyj klasy GridSearchCV do przeszukania przestrzeni parametrów'''
grid_search = GridSearchCV(MLPRegressor(max_iter=2000, random_state=42), param_grid, scoring='neg_mean_squared_error', cv=3)
grid_search.fit(X_train, y_train)

'''Wyniki grid search'''
results = pd.DataFrame(grid_search.cv_results_)
best_params = grid_search.best_params_

'''Umieść wyniki w spojnej tabelce przy pomocy funkcji tabulate'''
table = tabulate(results, headers='keys', tablefmt='double_grid')
print(table)

print("\nNajlepsze parametry:")
print(best_params)

''' 
2) (g) Czy udało się uzyskać błędy niższe niż przy użyciu LinearRegression z poprzedniego laboratorium?

Obydwa kody (lab3 i lab4) skupiają się na różnych zadaniach uczenia maszynowego i wykorzystują różne algorytmy. 

Wartośc zbioru testującego:  6192 obietków 
Wartość zbiór uczącego:  14448 obiektów

W laboratorium 3 (LinearRegression) używany model liniowy i był uczony do przewidywania cen mieszkań na podstawie 
indywidualnych cech oraz mierzył średni błąd bezwzględny (MAE) i średni błąd kwadratowy (MSE).

MedInc - MAE: 30.15%, MSE: 33.47%
HouseAge - MAE: 43.61%, MSE: 62.82%
AveRooms - MAE: 42.98%, MSE: 62.04%
AveBedrms - MAE: 43.77%, MSE: 63.39%
Population - MAE: 43.84%, MSE: 63.46%
AveOccup - MAE: 43.82%, MSE: 63.45%
Latitude - MAE: 43.38%, MSE: 62.07%
Longitude - MAE: 43.67%, MSE: 63.42%

Ocena jakości modelu:
Dane uczące - MAE: 25.66%, MSE: 25.29%
Dane testujące - MAE: 25.51%, MSE: 25.67%

W laboratorium 4 (MLPRegressor) używany modelu sieci neuronowej był do przewidywania cen mieszkań na podstawie 
wszystkich funkcji, a także mierzysz MAE i MSE.

Lab4 (MLPRegressor) - Najlepsze parametry:
Alpha: 1
Hidden Layer Sizes: (10,)
Learning Rate: 'constant'
MAE (mean absolute error) na danych uczących: 30.66%
MSE (mean squared error) na danych uczących: 30.97%
MAE (mean absolute error) na danych testowych: 30.72%
MSE (mean squared error) na danych testowych: 30.88%

Wydajność modelu regresji liniowej (lab3) jest znacznie lepsza w porównaniu do MLPRegressor (lab4) na podstawie błędów 
na danych testowych. Model regresji liniowej osiąga znacznie niższe błędy, co wskazuje na lepszą zdolność do 
przewidywania cen mieszkań na nowych danych.

Wniosek:
Model regresji liniowej jest bardziej efektywny w tym konkretnym przypadku, co wskazuje na lepszą zdolność do 
przewidywania cen mieszkań w Kalifornii na nowych danych.


* choć wnioski już były sporządzone odpaliłem jeszcze raz kod (lab4) w celu weryfikacji, wyniki:
Alpha: 0.1
Hidden Layer Sizes: (10, 10)
Learning Rate: 'constant'
MAE (mean absolute error) na danych uczących: 17.61%
MSE (mean squared error) na danych uczących: 14.53%
MAE (mean absolute error) na danych testowych: 18.11%
MSE (mean squared error) na danych testowych: 14.08%

i jeśli rozumiem w tym przypadku MLPRegressor jes efektywniejszy ponieważ błąd jest niższy.

'''
