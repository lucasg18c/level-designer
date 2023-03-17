import pygame
import os
from os.path import exists


# CLASES


class Camara:
    def __init__(self):
        self.x = 0
        self.y = 0


class Bloque:
    def __init__(self, x_rel, y_rel, ia):
        self.x = x_rel * 50
        self.y = y_rel * 50

        self.x_rel = x_rel
        self.y_rel = y_rel

        self.textura = None

        self.color = (0, 255, 0)
        self.color_actual = 0

        self.indice_actual = ia

    def dibujar(self):
        if self.textura is None:
            pygame.draw.rect(ventana, self.color, (bedrock.x + self.x, bedrock.y + self.y, 50, 50))

    def cambio_color(self):
        colores = (0, 255, 0), (255, 0, 0), (0, 0, 255)
        if self.color_actual < 2:
            self.color_actual += 1
        else:
            self.color_actual = 0

        self.color = colores[self.color_actual]


class Bedrock(Bloque):
    def __init__(self):
        super().__init__(0, 0, -1)


# FUNCIONES


def render():
    ventana.fill((230, 230, 230))

    for i in actuales:
        i.dibujar()


def cuadricula():
    # Verticales
    for x in range(0, ANCHO, 50):
        pygame.draw.line(ventana, (90, 90, 90), (x, -30), (x, ALTO + 30))

    # Horizontales
    for y in range(0, ALTO + 30, 50):
        pygame.draw.line(ventana, (90, 90, 90), (-30, y), (ANCHO + 30, y))

    # Origen (bedrock)
    pygame.draw.rect(ventana, (90, 90, 90), (bedrock.x + 1, bedrock.y + 1, 49, 49))


def puntero():
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(ventana, (90, 90, 90), ((mouse[0] // 50) * 50 + 1, (mouse[1] // 50) * 50 + 1, 49, 49))


def guardar(file):
    print('Guardando Datos de Nivel...')

    data = ''
    for d in actuales:
        data += f'{d.x_rel} {d.y_rel} {d.color_actual}\n'

    if exists(file):
        os.remove(file)
    m = open(file, 'w')
    m.write(data)
    m.close()
    print('- Nivel Guardado Existosamente -')


# SCRIPT PRINCIPAL


def main():
    global ANCHO, ALTO, ventana, bedrock, actuales, bloques

    # INICIALIZACIÓN

    # Sistema
    pygame.init()

    pygame.display.set_caption('Diseñador de Niveles')

    info = pygame.display.Info()
    ANCHO, ALTO = info.current_w, info.current_h
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    file = 'nivel_generado.txt'

    # Variables auxiliares
    last = 0
    presionados = []

    # Diseñador
    bloques = [[None] * 1000 for i in range(1000)]
    actuales = []

    bedrock = Bedrock()

    # MAINLOOP

    run = True
    while run:

        # EVENTOS
        for event in pygame.event.get():

            # Detectar salida del sistema
            if event.type == pygame.QUIT:
                run = False

            # SOLTAR EL MOUSE
            if event.type == pygame.MOUSEBUTTONUP and len(presionados):
                presionados = []

            # GUARDADO DE DATOS
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_SPACE]:
                guardar(file)
                os.system('COPY nivel_generado.txt /A C:\\Users\\lucas\\Desktop\\Proyectos\\games_test /Y')


        # CLICK DEL MOUSE
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pos = [(pos[0] - bedrock.x) // 50, (pos[1] - bedrock.y) // 50]

            b = bloques[pos[0]][pos[1]]

            if b is None:
                bloques[pos[0]][pos[1]] = Bloque(pos[0], pos[1], len(actuales))
                actuales.append(bloques[pos[0]][pos[1]])
                presionados.append(pos)

            else:
                existe = False
                for i in presionados:
                    if i == pos:
                        existe = True

                if not existe:
                    b.cambio_color()
                    presionados.append(pos)

        elif pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            pos = [(pos[0] - bedrock.x) // 50, (pos[1] - bedrock.y) // 50]

            if bloques[pos[0]][pos[1]] is not None:
                for i in range(len(actuales)):
                    a = actuales[i]
                    if a == bloques[pos[0]][pos[1]]:
                        del actuales[i]
                        bloques[pos[0]][pos[1]] = None
                        break
                    
        # MOVIMIENTO DE LA CÁMARA
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_RIGHT] and pygame.time.get_ticks() > last:
            bedrock.x -= 50
            last = pygame.time.get_ticks() + 100
        if teclas[pygame.K_LEFT] and pygame.time.get_ticks() > last:
            bedrock.x += 50
            last = pygame.time.get_ticks() + 100
        if teclas[pygame.K_UP] and pygame.time.get_ticks() > last:
            bedrock.y += 50
            last = pygame.time.get_ticks() + 100
        if teclas[pygame.K_DOWN] and pygame.time.get_ticks() > last:
            bedrock.y -= 50
            last = pygame.time.get_ticks() + 100

        # UPDATE
        render()
        cuadricula()

        # Puntero mouse
        puntero()

        pygame.display.update()

    pygame.quit()


# EJECUCIÓN

if __name__ == '__main__':
    main()
