import cv2
import os
from pathlib import Path
import shutil  # Para mover archivos

# Directorio de imágenes y etiquetas
directorio_imagenes = 'data/train/images/'  # Carpeta de imágenes
directorio_labels = 'data/train/labels/'  # Carpeta de etiquetas
directorio_sin_etiqueta = 'data/train/images_sin_etiqueta/'  # Carpeta para imágenes sin etiquetas

# Crear la carpeta para imágenes sin etiquetas si no existe
os.makedirs(directorio_sin_etiqueta, exist_ok=True)

# Diccionario para las clases (ajústalo según tus clases)
clases = {0: '1', 1: '2', 2: '3', 3: '4'}  # Ajusta esto según tus clases

def visualizar_labels_en_imagen(imagen_path, label_path):
    img = cv2.imread(imagen_path)
    img_height, img_width = img.shape[:2]

    # Leer el archivo de etiquetas
    with open(label_path, 'r') as f:
        labels = f.readlines()

    # Dibujar cada etiqueta en la imagen
    for label in labels:
        clase_id, x_centro, y_centro, ancho, alto = map(float, label.split())

        # Desnormalizar las coordenadas y dimensiones (convertir a píxeles)
        x_centro *= img_width
        y_centro *= img_height
        ancho *= img_width
        alto *= img_height

        # Obtener las esquinas del bounding box
        x1 = int(x_centro - ancho / 2)
        y1 = int(y_centro - alto / 2)
        x2 = int(x_centro + ancho / 2)
        y2 = int(y_centro + alto / 2)

        # Dibujar el bounding box en la imagen
        color = (0, 255, 0)  # Verde
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Añadir el nombre de la clase
        text = clases[int(clase_id)]
        cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Mostrar la imagen con los bounding boxes
    cv2.imshow("Imagen con Labels", img)
    cv2.waitKey(0)  # Presiona cualquier tecla para cerrar la ventana
    cv2.destroyAllWindows()

# Procesar todas las imágenes y etiquetas
for archivo_imagen in os.listdir(directorio_imagenes):
    img_path = os.path.join(directorio_imagenes, archivo_imagen)
    label_path = os.path.join(directorio_labels, Path(archivo_imagen).stem + '.txt')

    if os.path.exists(label_path):
        visualizar_labels_en_imagen(img_path, label_path)
    else:
        print(f"No se encontró etiqueta para {archivo_imagen}")
        # Mover la imagen a la carpeta de imágenes sin etiquetas
        shutil.move(img_path, os.path.join(directorio_sin_etiqueta, archivo_imagen))

print("Las imágenes sin etiquetas han sido movidas a la carpeta:", directorio_sin_etiqueta)
