import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Параметры персонажа и объектов
PLAYER_SIZE = 50
PLAYER_SPEED = 5
JUMP_FORCE = -15
GRAVITY = 1
ATTACK_SIZE = 100  # Размер зоны атаки

# Инициализация окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Game with Melee Attack")
clock = pygame.time.Clock()

# Переменные персонажа
player_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT - PLAYER_SIZE - 1]
player_velocity = [0, 0]
on_ground = True

# Платформы
platforms = [
    pygame.Rect(100, 500, 200, 10),
    pygame.Rect(400, 400, 200, 10),
    pygame.Rect(200, 300, 200, 10)
]

# Враги
objects = [
    pygame.Rect(200, 150, PLAYER_SIZE, PLAYER_SIZE),
    pygame.Rect(400, 300, PLAYER_SIZE, PLAYER_SIZE),
    pygame.Rect(600, 450, PLAYER_SIZE, PLAYER_SIZE)
]

def handle_input():
    """Обрабатывает пользовательский ввод."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:  # Движение влево
        player_velocity[0] = -PLAYER_SPEED
    elif keys[pygame.K_d]:  # Движение вправо
        player_velocity[0] = PLAYER_SPEED
    else:
        player_velocity[0] = 0

    if keys[pygame.K_w] and on_ground:  # Прыжок
        player_velocity[1] = JUMP_FORCE
        return False  # Устанавливаем, что персонаж в воздухе
    return on_ground

def apply_gravity():
    """Применяет гравитацию к персонажу."""
    if not on_ground:
        player_velocity[1] += GRAVITY

def check_platform_collisions():
    """Обрабатывает столкновения с платформами и проверяет, находится ли игрок на земле."""
    global on_ground
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    on_ground = False

    # Проверка на нижнюю границу экрана
    if player_pos[1] + PLAYER_SIZE >= WINDOW_HEIGHT:
        player_pos[1] = WINDOW_HEIGHT - PLAYER_SIZE
        player_velocity[1] = 0
        on_ground = True

    # Проверка на платформы
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity[1] >= 0:
            player_pos[1] = platform.top - PLAYER_SIZE
            player_velocity[1] = 0
            on_ground = True
            break

def spawn_enemy():
    """Добавляет нового врага на карту."""
    if len(objects) >= 10:
        return
    while True:
        x = random.randint(0, WINDOW_WIDTH - PLAYER_SIZE)
        y = random.randint(0, WINDOW_HEIGHT - PLAYER_SIZE)
        new_enemy = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        if not new_enemy.colliderect(pygame.Rect(*player_pos, PLAYER_SIZE, PLAYER_SIZE)) and \
           not any(new_enemy.colliderect(obj) for obj in objects):
            objects.append(new_enemy)
            break

SPAWN_INTERVAL = 3000  # Интервал появления врагов (в миллисекундах)
time_since_last_spawn = 0

# Основной игровой цикл
running = True
while running:
    delta_time = clock.tick(FPS)
    time_since_last_spawn += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обработка ввода
    on_ground = handle_input()

    # Применение гравитации
    apply_gravity()

    # Обновление позиции персонажа
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Ограничение движения персонажа в пределах экрана
    player_pos[0] = max(0, min(player_pos[0], WINDOW_WIDTH - PLAYER_SIZE))
    if player_pos[1] + PLAYER_SIZE >= WINDOW_HEIGHT:
        player_pos[1] = WINDOW_HEIGHT - PLAYER_SIZE
        player_velocity[1] = 0
        on_ground = True

    # Проверка столкновений с платформами
    check_platform_collisions()

    # Появление нового врага
    if time_since_last_spawn >= SPAWN_INTERVAL:
        spawn_enemy()
        time_since_last_spawn = 0

    # Атака ближнего боя
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Атака ближнего боя
        attack_zone = pygame.Rect(
            player_pos[0] - (ATTACK_SIZE - PLAYER_SIZE) // 2,
            player_pos[1] - (ATTACK_SIZE - PLAYER_SIZE) // 2,
            ATTACK_SIZE,
            ATTACK_SIZE
        )
        # Удаление врагов, попавших в зону атаки
        objects = [obj for obj in objects if not attack_zone.colliderect(obj)]

    # Рендеринг
    screen.fill(WHITE)

    # Отрисовка персонажа
    pygame.draw.rect(screen, BLUE, (*player_pos, PLAYER_SIZE, PLAYER_SIZE))

    # Отрисовка платформ
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)

    # Отрисовка врагов
    for obj in objects:
        pygame.draw.rect(screen, RED, obj)

    # Обновление экрана
    pygame.display.flip()


