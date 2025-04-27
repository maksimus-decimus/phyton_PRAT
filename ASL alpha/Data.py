import cv2
import mediapipe as mp
import numpy as np
import os
import time

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Diccionario de letras
LETTERS = {
    'h': 'H',
    'e': 'E',
    'l': 'L',
    'o': 'O'
}


def extract_hand_features(hand_landmarks):
    """Extrae características de los landmarks de la mano"""
    features = []
    for landmark in hand_landmarks.landmark:
        features.extend([landmark.x, landmark.y, landmark.z])
    return features


def create_dataset():
    # Crear directorio para los datos si no existe
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    # Cambia el índice aquí si tienes más de una cámara (0, 1, 2, ...)
    camera_index = 1
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(
            f"No se pudo abrir la cámara con el índice {camera_index}. Prueba con otro (1, 2, etc.) o revisa los permisos.")
        return

    print("Iniciando recolección de datos...")
    print("Presiona la tecla correspondiente para guardar la seña:")
    print("h - H")
    print("e - E")
    print("l - L")
    print("o - O")
    print("q - Salir")

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

                # Mostrar instrucciones en pantalla
                cv2.putText(frame, "Presiona h,e,l,o para guardar", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Mostrar el frame
        cv2.imshow('Recoleccion de Datos', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in [ord('h'), ord('e'), ord('l'), ord('o')]:
            if results.multi_hand_landmarks:
                # Guardar características
                letter = chr(key)
                features = extract_hand_features(results.multi_hand_landmarks[0])
                np.save(f'dataset/{letter}_{int(time.time())}.npy', features)
                print(f"Seña {LETTERS[letter]} guardada")
                time.sleep(0.5)  # Pequeña pausa para evitar guardar duplicados

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    create_dataset()