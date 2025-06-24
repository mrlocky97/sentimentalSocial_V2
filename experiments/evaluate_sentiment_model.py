import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Cargar el dataset
df = pd.read_csv('sentiment_dataset.csv')  # Debe tener columnas 'text' y 'label'

# Preprocesado
X = df['text']
y = df['label']
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Modelo
model = LogisticRegression()

# Validación cruzada
scores = cross_val_score(model, X_vec, y, cv=5, scoring='accuracy')
print("Precisión promedio (cross-validation):", scores.mean())

# Entrenamiento y evaluación final
model.fit(X_vec, y)
y_pred = model.predict(X_vec)
print(classification_report(y, y_pred))