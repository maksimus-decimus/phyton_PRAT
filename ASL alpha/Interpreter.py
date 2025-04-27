import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import pickle


def load_dataset():
    X = []
    y = []

    # Mapeo de letras a números
    letter_to_num = {'h': 0, 'e': 1, 'l': 2, 'o': 3}

    # Cargar todos los archivos del dataset
    for filename in os.listdir('dataset'):
        if filename.endswith('.npy'):
            # Extraer la letra del nombre del archivo
            letter = filename[0]
            # Cargar características
            features = np.load(os.path.join('dataset', filename))
            X.append(features)
            y.append(letter_to_num[letter])

    return np.array(X), np.array(y)


def train_model():
    print("Cargando dataset...")
    X, y = load_dataset()

    if len(X) == 0:
        print("Error: No se encontraron datos en el dataset")
        return

    print(f"Dataset cargado: {len(X)} muestras")

    # Dividir en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Estandarizar características
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Entrenar modelo SVM
    print("Entrenando modelo...")
    model = SVC(kernel='rbf', C=10, gamma='scale')
    model.fit(X_train, y_train)

    # Evaluar modelo
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"Precisión en entrenamiento: {train_score:.2f}")
    print(f"Precisión en prueba: {test_score:.2f}")

    # Guardar modelo y scaler
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    print("Modelo guardado en model.pkl y scaler.pkl")


if __name__ == "__main__":
    train_model()