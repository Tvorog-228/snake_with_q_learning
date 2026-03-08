import pygame
import random
import numpy as np

# Direcciones en orden horario para facilitar los giros
# 0: RIGHT, 1: DOWN, 2: LEFT, 3: UP
DIRECTIONS = ['RIGHT', 'DOWN', 'LEFT', 'UP']

class SnakeGameAI:
    def __init__(self, w=720, h=480):
        self.w = w
        self.h = h
        self.headless = False
        self.games_to_skip = 0
        # Inicializar display
        self.speed = 40
        pygame.init()
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # Estado inicial
        self.direction = 'RIGHT'
        self.head = [100, 50]
        self.snake = [[100, 50], [90, 50], [80, 50]]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randrange(0, (self.w // 10)) * 10
        y = random.randrange(0, (self.h // 10)) * 10
        self.food = [x, y]
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. Eventos de usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:   # Tecla 1: Lento
                    self.speed = 20
                elif event.key == pygame.K_2: # Tecla 2: Rápido
                    self.speed = 100
                elif event.key == pygame.K_3: # Tecla 3: Turbo
                    self.speed = 1000

                elif event.key == pygame.K_h: # Tecla H: Toggle Headless (ocultar/mostrar)
                    self.headless = not self.headless

        # 2. Mover
        self._move(action)
        self.snake.insert(0, list(self.head))

        # 3. Comprobar si terminó (Colisión o bucle infinito)
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10

            if self.games_to_skip > 0:
                self.games_to_skip -= 1
                if self.games_to_skip == 0:
                    self.headless = False

            return reward, game_over, self.score

        # 4. Comer comida o simplemente moverse
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
            # Opcional: recompensa pequeña por estar vivo/acercarse
            reward = -0.01

        # 5. Actualizar UI y reloj
        if not self.headless:
            self._update_ui()
            self.clock.tick(self.speed)

        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Choca con límites
        if pt[0] > self.w - 10 or pt[0] < 0 or pt[1] > self.h - 10 or pt[1] < 0:
            return True
        # Choca consigo misma
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill((0, 0, 0))
        for pos in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(self.food[0], self.food[1], 10, 10))
        font = pygame.font.SysFont('arial', 18)
        text = font.render(f"Velocidad (1-2-3): {self.speed} FPS", True, (255, 255, 255))
        self.display.blit(text, [10, self.h - 30])
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.display.blit(score_text, [10, 10])
        pygame.display.flip()

    def _move(self, action):
        # [recto, derecha, izquierda]
        idx = DIRECTIONS.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = DIRECTIONS[idx] # No cambia
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = DIRECTIONS[next_idx] # Giro a la derecha horario
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = DIRECTIONS[next_idx] # Giro a la izquierda anti-horario

        self.direction = new_dir

        if self.direction == 'UP': self.head[1] -= 10
        elif self.direction == 'DOWN': self.head[1] += 10
        elif self.direction == 'LEFT': self.head[0] -= 10
        elif self.direction == 'RIGHT': self.head[0] += 10
