import cv2
from pyzbar.pyzbar import decode
import os
import sys

def main():
    cap = cv2.VideoCapture(0)  # Abre la cámara (0 para la cámara predeterminada)
    
    barcode_data = set()  # Usamos un conjunto para almacenar datos únicos

    while True:
        ret, frame = cap.read()  # Captura un fotograma de la cámara
        
        if not ret:
            break
        
        decoded_objects = decode(frame)
        
        for obj in decoded_objects:
            barcode = obj.data.decode('utf-8')
            if barcode not in barcode_data:
                barcode_data.add(barcode)
                x, y, w, h = obj.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dibuja un rectángulo verde alrededor del código de barras
                cv2.putText(frame, f"Código de Barras: {barcode}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                create_output_file(barcode)
            
            print("Código de Barras:", barcode)  # Imprime en la terminal
        
        cv2.imshow('Barcode Reader', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
            break

    cap.release()
    cv2.destroyAllWindows()

def create_output_file(data):
    if not os.path.exists('barcodes.txt'):
        with open('barcodes.txt', 'w') as file:
            file.write(data + '\n')
    else:
        with open('barcodes.txt', 'r') as file:
            existing_data = file.read().splitlines()
        
        if data not in existing_data:
            with open('barcodes.txt', 'a') as file:
                file.write(data + '\n')

if __name__ == '__main__':
    try:
      main()
    except KeyboardInterrupt:
      sys.exit()
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror(title="titulo", message=f"{e}")
