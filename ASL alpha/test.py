import cv2

camera_index = 1  # Prueba con 0, luego 1, luego 2 si no funciona
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print(f"No se pudo abrir la cámara con el índice {camera_index}.")
    exit()

print("Cámara abierta correctamente. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la cámara.")
        break
    cv2.imshow('Test Cámara', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()