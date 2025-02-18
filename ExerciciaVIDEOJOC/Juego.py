import pygame
import random
import sys

# ========================
# Configuració inicial
# ========================
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Inicialitzar Pygame i la finestra
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc Extensible - Ampliació 4: Menú i Reinici")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Cargar imagen de fondo del menú
menu_background = pygame.image.load("menu_fondo.png").convert()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla


# Cargar la imagen de fondo
background = pygame.image.load("cielo.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla

# Cargar sprites
# Cargar imágenes del jugador con escalado
player_image = pygame.image.load("avion_jugador.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (100, 100))


enemy_images = [
    pygame.image.load("enemigo1.png").convert_alpha(),
    pygame.image.load("enemigo2.png").convert_alpha(),
    pygame.image.load("enemigo3.png").convert_alpha()
]

# Cargar imágenes de explosión (debes tener estas imágenes en tu proyecto)
explosion_images = [
    pygame.image.load("ExEnemigo_1.png").convert_alpha(),
    pygame.image.load("ExEnemigo_2.png").convert_alpha(),
    pygame.image.load("ExEnemigo_3.png").convert_alpha(),

]

explosion_images = [pygame.transform.scale(img, (100, 100)) for img in explosion_images]


# Sonidos y canciones
pygame.mixer.music.load("menu.mp3")  # Canción para el menú
juego_music = "stage_1.mp3"            # Canción para el juego (la cargaremos más tarde)
pygame.mixer.music.set_volume(0.5)
disparo_aliado_sound = pygame.mixer.Sound("disparo_aliado.mp3")
disparo_enemigo_sound = pygame.mixer.Sound("disparo_enemigo.mp3")

# Ajustar el volumen de los sonidos (30% del volumen máximo)
disparo_aliado_sound.set_volume(0.3)  # Volumen al 30%
disparo_enemigo_sound.set_volume(0.3)  # Volumen al 30%

# Cargar sonidos de motor
motor_jugador_sound = pygame.mixer.Sound("motor_jugador.mp3")
motor_enemigo1_sound = pygame.mixer.Sound("motor_enemigo1.mp3")
motor_enemigo2_sound = pygame.mixer.Sound("motor_enemigo2.mp3")
motor_enemigo3_sound = pygame.mixer.Sound("motor_enemigo3.mp3")

# Cargar sonido de explosión
explosion_sound = pygame.mixer.Sound("explosion.mp3")



# Ajustar el volumen de los sonidos de motor (30% del volumen máximo)
motor_jugador_sound.set_volume(0.3)
motor_enemigo1_sound.set_volume(0.3)
motor_enemigo2_sound.set_volume(0.3)
motor_enemigo3_sound.set_volume(0.3)
explosion_sound.set_volume(0.5)  # Ajustar volumen si es necesario
# ========================
# Variables Globals del Joc
# ========================
score = 0
difficulty_level = 1
lives = 3
last_difficulty_update_time = pygame.time.get_ticks()
spawn_interval = 1500
ADD_OBSTACLE = pygame.USEREVENT + 1
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 2000)  # Generar una nube cada 2 segundos
paused = False

# ========================
# Funcions Auxiliars
# ========================

def draw_text(surface, text, font, color, x, y):
    """Dibuixa un text a la pantalla."""
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# ========================
# Classes del Joc
# ========================

class Player(pygame.sprite.Sprite):
    """Classe per al jugador."""
    def __init__(self):
        super().__init__()
        self.image = player_image  # Usar la imagen del avión del jugador
        self.image = pygame.transform.scale(self.image, (100, 100   ))  # Escalar si es necesario
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5
        self.motor_sound = motor_jugador_sound  # Asignar el sonido del motor del jugador
        self.motor_sound.play(-1)  # Reproducir el sonido del motor en bucle

        self.is_destroyed = False  # Indica si el jugador está en estado de destrucción
        self.destruction_timer = 0
        self.invincible = False  # Indica si el jugador es invencible (parpadeo)
        self.invincible_timer = 0  # Temporizador para el parpadeo



    def destroy(self):
        """Inicia la animación de destrucción."""
        self.is_destroyed = True
        self.motor_sound.stop()  # Detener el sonido del motor
        play_explosion_sound()
        self.destruction_timer = pygame.time.get_ticks()  # Guardar el tiempo actual
        explosion = Explosion(self.rect.centerx, self.rect.centery, explosion_images, fall_speed=10, gravity=0.8)
        all_sprites.add(explosion)

    def revive(self):
        """Revive al jugador y activa la invencibilidad."""
        self.is_destroyed = False
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks()  # Guardar el tiempo actual
        self.motor_sound.play(-1)  # Reproducir el sonido del motor


    def update(self):
        """Actualiza la posición del jugador."""
        if self.is_destroyed:
            # Esperar a que termine la animación de destrucción (1 segundo)
            if pygame.time.get_ticks() - self.destruction_timer > 1000:
                self.revive()  # Revivir al jugador después de 1 segundo
        else:
            if self.invincible:
                # Parpadeo durante 2 segundos
                if pygame.time.get_ticks() - self.invincible_timer > 2000:
                    self.invincible = False  # Desactivar la invencibilidad
                else:
                    # Alternar visibilidad cada 100 ms
                    if (pygame.time.get_ticks() // 100) % 2 == 0:
                        self.image.set_alpha(255)  # Visible
                    else:
                        self.image.set_alpha(0)  # Invisible
            else:
                self.image.set_alpha(255)  # Siempre visibl


        """Actualitza la posició del jugador segons les tecles premudes."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = player_image
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = player_image



        # Evitar que el jugador surti de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Obstacle(pygame.sprite.Sprite):
    """Classe per als obstacles."""
    def __init__(self):
        super().__init__()
        # Seleccionar una imagen aleatoria para el enemigo
        self.tipo = random.randint(1, 3)  # Asignar un tipo aleatorio (1, 2 o 3)
        self.image = enemy_images[self.tipo - 1]  # Usar la imagen correspondiente al tipo
        self.image = pygame.transform.scale(self.image, (100, 100))  # Escalar si es necesario
        self.rect = self.image.get_rect()
        # Posició inicial: fora de la pantalla per la dreta
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        # La velocitat s'incrementa amb la dificultat
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)
        self.direction = 1  # Dirección de movimiento para el enemigo 2 (1: abajo, -1: arriba)
        self.last_shot_time = pygame.time.get_ticks()  # Tiempo del último disparo

        self.is_destroyed = False  # Indica si el jugador está en estado de destrucción



        if self.tipo == 1:
            self.motor_sound = motor_enemigo1_sound
        elif self.tipo == 2:
            self.motor_sound = motor_enemigo2_sound
        elif self.tipo == 3:
            self.motor_sound = motor_enemigo3_sound

        self.motor_sound.play(-1)  # Reproducir el sonido del motor en bucle

    def destroy(self):
        """Inicia la animación de destrucción."""
        self.is_destroyed = True

        self.motor_sound.stop()  # Detener el sonido del motor
        play_explosion_sound()
        explosion = Explosion(self.rect.centerx, self.rect.centery, explosion_images)
        all_sprites.add(explosion)

    def kill(self):
        """Detener el sonido del motor cuando el enemigo es destruido."""
        self.motor_sound.stop()  # Detener el sonido del motor
        super().kill()  # Llamar al método kill() de la clase padre

    def update(self):
        """Actualitza la posició de l'obstacle segons el seu tipus."""
        global score
        # Movimiento común: todos los enemigos se mueven hacia la izquierda
        self.rect.x -= self.speed

        # Comportamiento específico según el tipo de enemigo
        if self.tipo == 1:
            # Enemigo 1: se mueve en línea recta
            pass  # No necesita comportamiento adicional

        elif self.tipo == 2:
            # Enemigo 2: se mueve de arriba a abajo
            self.rect.y += self.direction * 2  # Velocidad vertical
            if self.rect.top < 0 or self.rect.bottom > HEIGHT:
                self.direction *= -1  # Cambiar dirección al llegar a los bordes

        elif self.tipo == 3:
            # Enemigo 3: apunta hacia el jugador
            delta_y = player.rect.centery - self.rect.centery
            if delta_y > 0:
                self.rect.y += min(2, delta_y)  # Moverse hacia abajo
            elif delta_y < 0:
                self.rect.y -= min(2, -delta_y)  # Moverse hacia arriba

        # Disparar según el tipo de enemigo
        current_time = pygame.time.get_ticks()
        if self.tipo == 1 and current_time - self.last_shot_time >= 1000:  # Disparar cada 1 segundo
            enemy_projectile = EnemyProjectile(self.rect.left, self.rect.centery)
            enemy_projectiles.add(enemy_projectile)
            all_sprites.add(enemy_projectile)
            disparo_enemigo_sound.play()
            self.last_shot_time = current_time

        elif self.tipo == 2 and current_time - self.last_shot_time >= 500:  # Disparar cada 0.5 segundos
            for _ in range(2):  # Disparar 2 proyectiles
                enemy_projectile = EnemyProjectile(self.rect.left, self.rect.centery)
                enemy_projectiles.add(enemy_projectile)
                all_sprites.add(enemy_projectile)
                disparo_enemigo_sound.play()
            self.last_shot_time = current_time

        elif self.tipo == 3 and current_time - self.last_shot_time >= 700:  # Disparar cada 0.7 segundos
            for _ in range(3):  # Disparar 3 proyectiles
                enemy_projectile = EnemyProjectile(self.rect.left, self.rect.centery)
                enemy_projectiles.add(enemy_projectile)
                all_sprites.add(enemy_projectile)
                disparo_enemigo_sound.play()
            self.last_shot_time = current_time

        # Eliminar el enemigo si sale de la pantalla
        if self.rect.right < 0:
            score += 1
            self.kill()

class Cloud(pygame.sprite.Sprite):
    """Clase para las nubes que se mueven en el fondo."""
    def __init__(self):
        super().__init__()
        # Cargar la imagen de la nube
        self.image = pygame.image.load("nube.png").convert_alpha()
        # Escalar la imagen de manera aleatoria
        scale_factor = random.uniform(0.5, 1.5)  # Escala entre 50% y 150%
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale_factor), int(self.image.get_height() * scale_factor))
        )
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 200)  # Aparece fuera de la pantalla (derecha)
        self.rect.y = random.randint(0, HEIGHT // 2)  # Posición vertical aleatoria
        self.speed = random.randint(1, 3)  # Velocidad aleatoria

    def update(self):
        """Mueve la nube de derecha a izquierda."""
        self.rect.x -= self.speed  # Mover hacia la izquierda
        if self.rect.right < 0:  # Si la nube sale de la pantalla por la izquierda, se elimina
            self.kill()

    def update(self):
        """Actualitza la posició de l'obstacle movent-lo cap a l'esquerra.
           Quan surt completament de la pantalla, s'incrementa la puntuació i s'elimina."""
        global score
        self.rect.x -= self.speed
        if self.rect.right < 0:
            score += 1
            self.kill()


class Projectile(pygame.sprite.Sprite):
    """Clase para los proyectiles del jugador."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("proyectil_aliado.png").convert_alpha()  # Cargar imagen PNG
        self.image = pygame.transform.scale(self.image, (20, 10))  # Escalar si es necesario
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Posición inicial del proyectil
        self.speed = 10  # Velocidad del proyectil
        self.hits = 0  # Contador de colisiones

    def update(self):
        """Mueve el proyectil hacia la derecha."""
        self.rect.x += self.speed
        if self.rect.left > WIDTH:  # Si el proyectil sale de la pantalla, se elimina
            self.kill()

class EnemyProjectile(pygame.sprite.Sprite):
    """Clase para los proyectiles de los enemigos."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("proyectil_enemigo.png").convert_alpha()  # Cargar imagen PNG
        self.image = pygame.transform.scale(self.image, (20, 10))  # Escalar si es necesario
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Posición inicial del proyectil
        self.speed = -7  # Velocidad del proyectil (hacia la izquierda)

    def update(self):
        """Mueve el proyectil hacia la izquierda."""
        self.rect.x += self.speed
        if self.rect.right < 0:  # Si el proyectil sale de la pantalla, se elimina
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Clase para la animación de destrucción."""
    def __init__(self, x, y, images, fall_speed=5, gravity=0.5):
        super().__init__()
        self.images = images  # Lista de imágenes para la animación
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.fall_speed = fall_speed  # Velocidad de caída
        self.gravity = gravity
        self.animation_speed = 100  # Tiempo entre frames (en milisegundos)
        self.last_update = pygame.time.get_ticks()


    def update(self):
        """Actualiza la animación y hace caer el objeto."""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.images):
                self.kill()  # Terminar la animación
            else:
                self.image = self.images[self.index]

        self.fall_speed += self.gravity

        # Hacer caer el objeto
        self.rect.y += self.fall_speed
        if self.rect.top > HEIGHT:  # Si sale de la pantalla, eliminar
            self.kill()


def play_explosion_sound():
    """Reproduce el sonido de explosión con una tonalidad aleatoria."""
    pitch_variation = random.uniform(0.8, 1.2)  # Variación del 80% al 120% del tono original
    explosion_sound.set_volume(0.5)  # Ajustar volumen si es necesario
    explosion_sound.play()

    try:
        explosion_sound.set_frequency(int(44100 * pitch_variation))
    except AttributeError:
        pass  # Si set_frequency no está disponible, ignorar el error



def draw_button(surface, text, font, color, rect, action=None):
    """Dibuja un botón en la pantalla y detecta clics."""
    pygame.draw.rect(surface, color, rect, border_radius=10)  # Dibujar el botón (fondo redondeado)
    text_obj = font.render(text, True, BLACK)
    text_rect = text_obj.get_rect(center=rect.center)
    surface.blit(text_obj, text_rect)

    # Detectar clics del ratón
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse_pos):  # Si el cursor está sobre el botón
        pygame.draw.rect(surface, (200, 200, 200), rect, border_radius=10)  # Cambiar color al pasar el mouse
        if mouse_click[0] == 1 and action is not None:
            action()  # Ejecutar la acción del botón


def show_pause_menu():
    """Muestra el menú de pausa con opciones."""
    global paused  # Declarar 'paused' como global
    font_large = pygame.font.SysFont("Arial", 36)

    # Crear fondo oscuro translúcido
    pause_overlay = pygame.Surface((WIDTH, HEIGHT))
    pause_overlay.set_alpha(180)  # Opacidad (0 = transparente, 255 = opaco)
    pause_overlay.fill((0, 0, 0))  # Color negro translúcido

    # Botones de pausa
    button_resume = pygame.Rect(300, 350, 250, 50)  # Botón "Continuar"
    button_exit = pygame.Rect(300, 420, 250, 50)  # Botón "Salir al Menú"

    while paused:
        screen.blit(pause_overlay, (0, 0))  # Dibujar fondo oscuro
        draw_text(screen, "Juego Pausado", font_large, WHITE, 280, 200)
        draw_text(screen, "Presiona ESC para volver", font, WHITE, 270, 250)

        # Dibujar botones
        draw_button(screen, "Continuar", font_large, (100, 200, 100), button_resume, exit_pause_menu)
        draw_button(screen, "Salir al Menú", font_large, (200, 100, 100), button_exit, show_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Reanudar el juego

        pygame.display.flip()
        clock.tick(FPS)

def exit_pause_menu():
    """Función vacía para cerrar el menú de pausa con el botón 'Continuar'."""
    global paused
    paused = False

# ========================
# Funció per reinicialitzar el Joc
# ========================

def new_game():
    """Reinicialitza totes les variables i grups per començar una nova partida."""
    global score, difficulty_level, lives, last_difficulty_update_time, spawn_interval, all_sprites, obstacles, player, clouds, enemy_projectiles, paused
    score = 0
    paused = False  # Inicializa la variable 'paused'
    difficulty_level = 1
    lives = 3
    last_difficulty_update_time = pygame.time.get_ticks()
    spawn_interval = 1500
    pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()  # Crear el grupo de proyectiles enemigos
    player = Player()
    all_sprites.add(player)

# ========================
# Funció per mostrar el menú principal
# ========================

def show_menu():
    """Muestra la pantalla de menú con una imagen de fondo y botones interactivos."""
    pygame.mixer.music.play(-1)
    font_large = pygame.font.SysFont("Arial", 36)

    button_play = pygame.Rect(300, 350, 200, 50)  # Botón "Jugar"
    button_exit = pygame.Rect(300, 420, 200, 50)  # Botón "Salir"

    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.blit(menu_background, (0, 0))  # Dibujar imagen de fondo del menú

        draw_text(screen, "AS DEL CIELO", font_large, BLACK, 300, 200)

        # Dibujar botones
        draw_button(screen, "Jugar", font_large, (100, 200, 100), button_play, game_loop)
        draw_button(screen, "Salir", font_large, (200, 100, 100), button_exit, exit_game)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Actualizar pantalla


def exit_game():
    """Cierra el juego de forma segura."""
    pygame.quit()
    sys.exit()


# ========================
# Funció per executar la partida
# ========================

def game_loop():
    """Ejecuta el bucle principal de la partida."""
    global difficulty_level, last_difficulty_update_time, spawn_interval, lives, score, paused
    new_game()
    pygame.mixer.music.load(juego_music)  # Cargar la canción del juego
    pygame.mixer.music.set_volume(0.3)  # Establecer volumen al 30%
    pygame.mixer.music.play(-1)  # Reproducir en bucle
    game_state = "playing"
    running = True
    paused = False  # Variable para controlar el estado de pausa
    projectiles = pygame.sprite.Group()  # Grupo para los proyectiles del jugador
    last_enemy_shot_time = pygame.time.get_ticks()  # Tiempo del último disparo enemigo

    while running and game_state == "playing":
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ADD_OBSTACLE:
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            elif event.type == ADD_CLOUD:  # Generar nubes
                cloud = Cloud()
                clouds.add(cloud)  # Añadir la nube solo al grupo clouds
            elif event.type == pygame.KEYDOWN:  # Detectar cuando se presiona una tecla
                if event.key == pygame.K_l:  # Si se presiona la tecla L
                    projectile = Projectile(player.rect.right, player.rect.centery)
                    projectiles.add(projectile)
                    all_sprites.add(projectile)
                    disparo_aliado_sound.play()  # Reproducir sonido de disparo del jugador
                elif event.key == pygame.K_ESCAPE:  # Si se presiona la tecla ESC
                    paused = not paused  # Alternar entre pausa y reanudar
                    if paused:
                        show_pause_menu()  # Mostrar el menú de pausa

        if not paused:  # Solo actualizar el juego si no está en pausa
            # Disparar proyectiles de los enemigos cada 1 segundo
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_shot_time >= 1000:  # Cada 1 segundo
                for obstacle in obstacles:
                    if obstacle.tipo == 1:  # Enemigo 1
                        enemy_projectile = EnemyProjectile(obstacle.rect.left, obstacle.rect.centery)
                        enemy_projectiles.add(enemy_projectile)
                        all_sprites.add(enemy_projectile)
                        disparo_enemigo_sound.play()
                    elif obstacle.tipo == 2:  # Enemigo 2
                        for _ in range(2):  # Disparar 2 proyectiles
                            enemy_projectile = EnemyProjectile(obstacle.rect.left, obstacle.rect.centery)
                            enemy_projectiles.add(enemy_projectile)
                            all_sprites.add(enemy_projectile)
                            disparo_enemigo_sound.play()
                    elif obstacle.tipo == 3:  # Enemigo 3
                        for _ in range(3):  # Disparar 3 proyectiles
                            enemy_projectile = EnemyProjectile(obstacle.rect.left, obstacle.rect.centery)
                            enemy_projectiles.add(enemy_projectile)
                            all_sprites.add(enemy_projectile)
                            disparo_enemigo_sound.play()
                last_enemy_shot_time = current_time

            # Incrementar la dificultad cada 15 segundos
            current_time = pygame.time.get_ticks()
            if current_time - last_difficulty_update_time >= 15000:
                difficulty_level += 1
                last_difficulty_update_time = current_time
                spawn_interval = max(500, 1500 - difficulty_level * 100)
                pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)

            # Actualizar los sprites
            all_sprites.update()
            clouds.update()  # Actualizar las nubes (si es necesario)

            # Comprobar colisiones entre proyectiles del jugador y obstáculos
            for projectile in projectiles:
                hits = pygame.sprite.spritecollide(projectile, obstacles, False)
                for hit in hits:
                    projectile.kill()  # Eliminar el proyectil
                    hit.destroy()
                    hit.kill()  # Eliminar el obstáculo
                    score += 1  # Incrementar la puntuación

            # Comprobar colisiones entre proyectiles de los enemigos y el jugador
            if pygame.sprite.spritecollideany(player, enemy_projectiles) and not player.invincible:
                lives -= 1
                if lives > 0:
                    # Reinicializar la posición del jugador y borrar los obstáculos
                    player.destroy()
                    player.rect.center = (100, HEIGHT // 2)
                    player.revive()
                    for obs in obstacles:
                        obs.kill()
                else:
                    # Detener todos los sonidos de los motores de los enemigos
                    for obstacle in obstacles:
                        obstacle.motor_sound.stop()  # Detener el sonido del motor de cada enemigo
                    player.motor_sound.stop()  # Detener el sonido del motor del jugador
                    game_state = "game_over"
                    pygame.mixer.music.stop()  # Detener la música del juego al perder

            # Comprobar colisiones entre el jugador y los obstáculos
            if pygame.sprite.spritecollideany(player, obstacles) and not player.invincible:
                lives -= 1
                if lives > 0:
                    player.destroy()
                    # Reinicializar la posición del jugador y borrar los obstáculos
                    player.rect.center = (100, HEIGHT // 2)
                    for obs in obstacles:
                        obs.kill()
                else:
                    # Detener todos los sonidos de los motores de los enemigos
                    for obstacle in obstacles:
                        obstacle.motor_sound.stop()  # Detener el sonido del motor de cada enemigo
                    player.motor_sound.stop()  # Detener el sonido del motor del jugador
                    game_state = "game_over"
                    pygame.mixer.music.stop()  # Detener la música del juego al perder

        # Dibujar la escena (siempre se dibuja, incluso en pausa)
        screen.blit(background, (0, 0))  # Dibujar el fondo
        clouds.draw(screen)  # Dibujar las nubes primero (por debajo del jugador)
        all_sprites.draw(screen)  # Dibujar el resto de los sprites (jugador, enemigos, proyectiles)

        # Dibujar la puntuación, dificultad y vidas
        score_text = font.render("Puntuació: " + str(score), True, BLACK)
        difficulty_text = font.render("Dificultat: " + str(difficulty_level), True, BLACK)
        lives_text = font.render("Vides: " + str(lives), True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(difficulty_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        pygame.display.flip()
    return score

# ========================
# Funció per mostrar la pantalla de Game Over
# ========================

def show_game_over(final_score):
    """Mostra la pantalla de Game Over amb la puntuació final i espera per reiniciar."""
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
        screen.fill(WHITE)
        draw_text(screen, "Game Over!", font, RED, 350, 200)
        draw_text(screen, "Puntuació Final: " + str(final_score), font, BLACK, 320, 250)
        draw_text(screen, "Prem qualsevol tecla per reiniciar", font, BLACK, 250, 300)
        pygame.display.flip()

# ========================
# Bucle principal del programa
# ========================

while True:
    pygame.mixer.music.load("menu.mp3")  # Cargar la música del menú
    pygame.mixer.music.set_volume(0.5)  # Establecer el volumen
    pygame.mixer.music.play(-1)
    show_menu()                   # Mostrar menú d'inici
    final_score = game_loop()       # Executar la partida
    show_game_over(final_score)     # Mostrar pantalla de Game Over i esperar reinici
    pygame.mixer.music.stop()