import pygame
import random

# initialize pygame
pygame.init()

# screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("🎯 Archery Master")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)

# fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 30)

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 40)
        self.rect.y = random.randint(50, screen_height - 40)
        self.speed_x = random.choice([-2, -1, 1, 2])
        self.speed_y = random.choice([-2, -1, 1, 2])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        if self.rect.top < 50 or self.rect.bottom > screen_height:
            self.speed_y *= -1

# Bow class
class Bow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

# countdown before game starts
def countdown(screen):
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        count_text = font.render(str(i), True, BLACK)
        screen.blit(count_text, (screen_width // 2 - count_text.get_width() // 2,
                                 screen_height // 2 - count_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)

# display menu
def show_menu():
    menu = True
    while menu:
        screen.fill(WHITE)
        title = font.render("🎯 Archery Master", True, BLACK)
        start = small_font.render("Press [S] to Start", True, BLACK)
        quit_game = small_font.render("Press [Q] to Quit", True, BLACK)

        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 200))
        screen.blit(start, (screen_width // 2 - start.get_width() // 2, 280))
        screen.blit(quit_game, (screen_width // 2 - quit_game.get_width() // 2, 320))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# main game function
def run_game():
    all_sprites = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    bow = Bow()
    all_sprites.add(bow)

    for _ in range(5):
        t = Target()
        targets.add(t)
        all_sprites.add(t)

    score = 0
    level = 1
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    game_duration = 60
    game_over = False

    countdown(screen)
    start_time = pygame.time.get_ticks()

    while not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_left = max(0, int(game_duration - elapsed_time))
        if time_left <= 0:
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hits = pygame.sprite.spritecollide(bow, targets, True)
                for _ in hits:
                    score += 1
                    new_target = Target()
                    targets.add(new_target)
                    all_sprites.add(new_target)

        if score >= level * 10:
            level += 1
            for _ in range(2):
                t = Target()
                targets.add(t)
                all_sprites.add(t)

        all_sprites.update()
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # HUD
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        time_text = small_font.render(f"Time: {time_left}s", True, BLACK)
        level_text = small_font.render(f"Level: {level}", True, BLACK)

        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 30))
        screen.blit(level_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    # Game Over screen
    screen.fill(WHITE)
    end_text = font.render("Game Over!", True, RED)
    score_result = font.render(f"Your Score: {score}", True, BLACK)
    screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, 250))
    screen.blit(score_result, (screen_width // 2 - score_result.get_width() // 2, 300))
    pygame.display.flip()
    pygame.time.delay(4000)

# start here
show_menu()
run_game()
  
