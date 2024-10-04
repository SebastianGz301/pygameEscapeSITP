import pygame
import os

#Desarrollado por Sebasitan Gomez

pygame.init()

# Definimos las dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Creamos la ventana del juego
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("EscapeSITP")

# Establecemos el framerate del juego
clock = pygame.time.Clock()
FPS = 60

# Variables del juego
GRAVITY = 0.75  # Definimos la gravedad para afectar los saltos

# Variables de acción del jugador
moving_left = False  # Variable para moverse a la izquierda
moving_right = False  # Variable para moverse a la derecha
shoot = False #Variable para disparar



#Cargar Imagenes
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# Definimos colores
BG = (220, 220, 220)  # Color del fondo
BLACK = (0, 0, 0)  # Color negro para las líneas y otros elementos

# Función para dibujar el fondo
def draw_bg():
    screen.fill(BG)  # Rellenamos la pantalla con el color de fondo
    pygame.draw.line(screen, BLACK, (0, 300), (SCREEN_WIDTH, 300))  # Dibujamos una línea horizontal para representar el suelo

# Clase para los personajes del juego
class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True  # Estado de vida del personaje
        self.char_type = char_type  # Tipo de personaje (jugador o enemigo)
        self.speed = speed  # Velocidad del personaje
        self.shoot_cooldown = 0
        self.direction = 1  # Dirección del movimiento
        self.jump = False  # Variable para saber si está saltando
        self.in_air = True  # Variable para saber si está en el aire
        self.vel_y = 0  # Velocidad vertical
        self.flip = False  # Controla si se voltea la imagen del personaje
        self.animation_list = []  # Lista de animaciones
        self.frame_index = 0  # Índice de frames de animación
        self.action = 0  # Acción actual (idle, run, jump)
        self.update_time = pygame.time.get_ticks()  # Marca temporal para la animación
        
        # Cargar las imágenes para las diferentes animaciones
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))  # Contamos el número de frames
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha() # Cargamos la imagen
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # Redimensionamos la imagen
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]  # Establecemos la imagen inicial
        self.rect = self.image.get_rect()  # Obtenemos el rectángulo para el personaje
        self.rect.center = (x, y)


    def update(self):
        self.update_animation()
        #Metodo cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        # Reiniciamos las variables de movimiento
        dx = 0
        dy = 0

        # Si se mueve a la izquierda o derecha, asignamos los valores correspondientes
        if moving_left:
            dx = -self.speed
            self.flip = True  # Volteamos la imagen si va a la izquierda
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False  # Imagen sin voltear si va a la derecha
            self.direction = 1

        # Control del salto
        if self.jump and not self.in_air:
            self.vel_y = -11  # Establecemos una velocidad negativa para saltar
            self.jump = False
            self.in_air = True

        # Aplicamos la gravedad
        self.vel_y += GRAVITY
        if self.vel_y > 10:  # Limitamos la velocidad de caída
            self.vel_y = 10
        dy += self.vel_y

        # Verificamos colisión con el suelo
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False  # Si toca el suelo, ya no está en el aire

        # Actualizamos la posición del personaje
        self.rect.x += dx
        self.rect.y += dy


    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 4
        bullet = Bullet(player.rect.centerx + (0.6 * self.rect.size[0] * self.direction ),self.rect.centery, self.direction)
        bullet_group.add(bullet)

    def update_animation(self):
        # Control del tiempo entre frames
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0  # Reiniciamos la animación

    def update_action(self, new_action):
        # Cambiamos la acción si es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0  # Reiniciamos el índice de frames
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        # Dibujamos el personaje en la pantalla
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.direction = direction


    def update(self):
        #Movimineto Bala
        self.rect.x += (self.direction * self.speed)
        #Check si la bala se salio de la pantalla
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill() 

#Crear grupos sprite
bullet_group = pygame.sprite.Group()








# Creación del jugador y enemigo
player = Character('player', 200, 200, 3, 5)
enemy = Character('enemy', 400, 200, 3, 5)

run = True
while run:
    clock.tick(FPS)  # Establecemos la velocidad del juego

    draw_bg()  # Dibujamos el fondo

    player.update()  # Actualizamos la animación del jugador
    player.draw()  # Dibujamos el jugador
    enemy.draw()  # Dibujamos el enemigo

    #Actualizar y dibujar grupos
    bullet_group.update()
    bullet_group.draw(screen)

    # Actualizamos las acciones del jugador
    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)  # 2 = salto
        elif moving_left or moving_right:
            player.update_action(1)  # 1 = correr
        else:
            player.update_action(0)  # 0 = idle (quieto)
        player.move(moving_left, moving_right)  # Movemos al jugador

    for event in pygame.event.get():
        # Si se cierra la ventana, salimos del bucle
        if event.type == pygame.QUIT:
            run = False
        
        # Controles del teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True  # Se mueve a la izquierda
            if event.key == pygame.K_d:
                moving_right = True  # Se mueve a la derecha
            if event.key == pygame.K_SPACE:
                shoot = True  # Boton disparo
            if event.key == pygame.K_w and player.alive:
                player.jump = True  # Inicia un salto
            if event.key == pygame.K_ESCAPE:
                run = False  # Sale del juego con ESC


        # Detectamos cuando se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False  # Boton disparo
    

    pygame.display.update()  # Actualizamos la pantalla

pygame.quit()  # Salimos de Pygame
