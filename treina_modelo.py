from ucimlrepo import fetch_ucirepo
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

heart_disease = fetch_ucirepo(id=45)
X = heart_disease.data.features
y = 1 * (heart_disease.data.targets > 0)

# 80% treino 20% teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))

joblib.dump(modelo, 'modelo_xgboost.pkl')
joblib.dump(X.median(), 'medianas.pkl')
