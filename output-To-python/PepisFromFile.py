# ASCII FROM https://github.com/wang0618/ascii-art

import time

print("MPO ;)")
CLEAR = "\033[1A\x1b[2K"
i = 0
def main():
    while True:
        with open('AsciiOutput.txt', 'r', encoding='utf-8') as archivo:
            # Lee las primeras 5 líneas del archivo
            while True:
                # Lee las próximas 5 líneas del archivo
                lineas = [archivo.readline() for _ in range(52)]
                #primeras_lineas = archivo.readlines()[:52]
                
                # Si no hay más líneas, sal del bucle
                if not lineas[0]:
                    break

                # Imprime las 5 líneas juntas
                contenido_bloque = ''.join(lineas)
                print(contenido_bloque)
                print(CLEAR*100, end = "")
                time.sleep(0.05)
            # Imprime las primeras 5 líneas juntas
            
main()