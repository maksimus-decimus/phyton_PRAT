import cv2
import mediapipe as mp
import numpy as np
import pickle

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Inicializar la cámara
cap = cv2.VideoCapture(1)

# Diccionario para mapear las letras
LETTERS = {
    0: 'H',
    1: 'E',
    2: 'L',
    3: 'O'
}


def extract_hand_features(hand_landmarks):
    """Extrae características de los landmarks de la mano"""
    features = []
    for landmark in hand_landmarks.landmark:
        features.extend([landmark.x, landmark.y, landmark.z])
    return features


def main():
    # Cargar modelo y scaler
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el modelo entrenado. Por favor, ejecuta train_model.py primero.")
        return

    print("Iniciando detector de señas...")
    print("Presiona 'q' para salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a RGB para MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar manos
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar landmarks
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extraer características
                features = extract_hand_features(hand_landmarks)
                features = scaler.transform([features])

                # Predecir letra
                prediction = model.predict(features)[0]
                letter = LETTERS[prediction]

                # Mostrar predicción
                cv2.putText(frame, f"Letter: {letter}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

        # Mostrar el frame
        cv2.imshow('Detector de Señas', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()