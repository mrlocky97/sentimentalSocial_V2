import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from sklearn.model_selection import train_test_split, cross_val_score

# 1. Carga de datos
df = pd.read_csv("data/emotions.csv")
X = df["text"]
y = df["label"]

# 2. División train/test (opcional)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Definir pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=5000,
        ngram_range=(1,2),
        stop_words="english"
    )),
    ("clf", MultinomialNB(alpha=0.1))
])

# 4. Validación cruzada rápida
scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="accuracy")
print(f"Accuracy CV: {scores.mean():.3f} ± {scores.std():.3f}")

# 5. Entrenar en todo el set de entrenamiento
pipeline.fit(X_train, y_train)

# 6. Evaluar en test (opcional)
test_acc = pipeline.score(X_test, y_test)
print(f"Accuracy test: {test_acc:.3f}")

# 7. Guardar el modelo
joblib.dump(pipeline, "app/models/emotion_clf.pkl")
print("Modelo guardado en app/models/emotion_clf.pkl")
