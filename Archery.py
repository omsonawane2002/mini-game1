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

# class for the target
class Target(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

    def update(self):
        # randomly change the position of the target
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

# class for the bow and arrow
class Bow(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface([40, 20])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        
    def update(self):
        # set the position of the bow to the mouse cursor
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

# create sprite groups
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
bows = pygame.sprite.Group()

# create target and add to sprite groups
for i in range(10):
    target = Target()
    target.rect.x = random.randint(0, screen_width - target.rect.width)
    target.rect.y = random.randint(0, screen_height - target.rect.height)
    
    targets.add(target)
    all_sprites.add(target)

# create bow and add to sprite groups
bow = Bow()
bows.add(bow)
all_sprites.add(bow)

# set up timer
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
game_over = False

# main game loop
while not game_over:
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if arrow hits target
            hits = pygame.sprite.spritecollide(bow, targets, True)
            for hit in hits:
                # create new target and add to sprite groups
                target = Target()
                targets.add(target)
                all_sprites.add(target)
                
                # increment score
                score += 1
    
    # update sprites
    all_sprites.update()
    
    # clear screen
    screen.fill(WHITE)
    
    # draw sprites
    all_sprites.draw(screen)
    
    # display score and time
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))
    
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_text = font.render("Time: " + str(int(elapsed_time)), True, BLACK)
    screen.blit(time_text, (10, 30))
    
    pygame.display.flip()
    clock.tick(60)

# quit game
pygame.quit()