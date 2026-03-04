# -*- coding: utf-8 -*-
import socket
import psycopg2

# --- CONFIGURACIÓN ---
UDP_IP = "0.0.0.0"
UDP_PORT = 5005 #Cambiar al puerto donde entran las tramas
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "password"
}

def iniciar_servidor():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        
        print(f"Escuchando UDP en puerto {UDP_PORT}...")

        while True:
            data, addr = sock.recvfrom(1024)
            trama = data.decode('utf-8').strip()
            
            try:
                valores = trama.split(',')
                
                if len(valores) == 4:
                    
                    query = '''
                        INSERT INTO "Location-Data" (Latitud, Longitud, Fecha, Hora) 
                        VALUES (%s, %s, %s, %s)
                    '''
                    cursor.execute(query, (valores[0], valores[1], valores[2], valores[3]))
                    conn.commit()
                    print(f"OK desde {addr}: {trama}")
                else:
                    print(f"Trama inválida (se esperaban 4 valores): {trama}")

            except Exception as e:
                conn.rollback()
                print(f"Error al insertar: {e}")

    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    iniciar_servidor()