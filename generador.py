import random
import string
import sys

def generar_input(n, k):
    print(1)  # un caso de prueba
    print(n, k)
    for _ in range(n):
        # Genera cadenas aleatorias de tamaño k con letras minúsculas
        cadena = ''.join(random.choices(string.ascii_lowercase, k=k))
        print(cadena)

if __name__ == "__main__":
    n = 7000
    k = 3
    generar_input(n, k)