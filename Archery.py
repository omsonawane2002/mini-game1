import pygame
import random

# initialise pygame module
pygame.init()

# screen dimensions
screen_width = 800
screen_height = 600

# set up screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Archery Game")

# colour definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# font setup
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# class for the target
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(50, screen_height - self.rect.height)

# class for the bow and arrow
class Bow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        # center bow on mouse cursor
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

def countdown(screen):
    for i in range(3, 0, -1):
        screen.fill(WHITE)
        count_text = font.render(str(i), True, BLACK)
        screen.blit(count_text, (screen_width // 2 - count_text.get_width() // 2,
                                 screen_height // 2 - count_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)

# create sprite groups
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()

# create targets and add to groups
for _ in range(10):
    target = Target()
    targets.add(target)
    all_sprites.add(target)

# create bow and add to group
bow = Bow()
all_sprites.add(bow)

# game variables
score = 0
clock = pygame.time.Clock()
game_over = False
start_time = None
game_duration = 60  # seconds

# countdown before game starts
countdown(screen)
start_time = pygame.time.get_ticks()

# main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hits = pygame.sprite.spritecollide(bow, targets, False)
            for hit in hits:
                hit.reset_position()
                score += 1

    all_sprites.update()

    # clear screen
    screen.fill(WHITE)

    # draw all sprites
    all_sprites.draw(screen)

    # display score
    score_text = small_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # display timer
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, int(game_duration - elapsed_time))
    time_text = small_font.render(f"Time Left: {time_left}s", True, BLACK)
    screen.blit(time_text, (10, 40))

    # check if time is up
    if elapsed_time >= game_duration:
        game_over = True

    pygame.display.flip()
    clock.tick(60)

# Game Over screen
screen.fill(WHITE)
over_text = font.render("Game Over!", True, RED)
final_score = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(over_text, (screen_width // 2 - over_text.get_width() // 2, screen_height // 2 - 50))
screen.blit(final_score, (screen_width // 2 - final_score.get_width() // 2, screen_height // 2 + 10))
pygame.display.flip()

# Wait a few seconds before quitting
pygame.time.delay(4000)
pygame.quit()
