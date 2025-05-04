import random
import os
import pygame
pygame.init()

def draw_swaps():
    font = pygame.font.SysFont(None, 32)
    text = font.render(f'Кол-во перестановок: {swaps}', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

def game_over():
    font = pygame.font.SysFont(None, 32)
    text = font.render('Ура, картина собрана!', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 4))
    screen.blit(text, text_rect)

def draw_tiles():
    for i in range(len(tiles)):
        tile = tiles[i]
        row = i // rows
        col = i % cols
        x = col * (tile_width + margin) + margin
        y = row * (tile_height + margin) + margin
        if i == selected:
            pygame.draw.rect(screen, (0, 255, 0), (x - margin, y- margin, tile_width + margin * 2, tile_height + margin * 2))
        screen.blit(tile, (x, y))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пазл")
Background = (0, 0, 0)
screen.fill(Background)
rows = 3
cols = 3
margin = 2
FPS = 60
clock = pygame.time.Clock()

pictures = os.listdir('pictures')
picture = random.choice(pictures)
image = pygame.image.load('pictures/' + picture)

image_width, image_height = image.get_size()
tile_width = image_width // cols
tile_height = image_height // rows

tiles = []
for i in range(rows):
    for j in range(cols):
        rect = pygame.Rect(j * tile_width, i * tile_height, tile_width, tile_height)
        tile = image.subsurface(rect)
        tiles.append(tile)

origin_tiles = tiles.copy()
random.shuffle(tiles)
swaps = 0
selected = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i in range(len(tiles)):
                row = i // rows
                col = i % cols
                x = col * (tile_width + margin) + margin
                y = row * (tile_height + margin) + margin

                if x <= mouse_x <= x + tile_width and y <= mouse_y <= y + tile_height:
                    if selected is not None and selected != i:
                        tiles[i], tiles[selected] = tiles[selected], tiles[i]
                        selected = None
                        swaps += 1
                    elif selected == i:
                        selected = None
                    else:
                        selected = i

    screen.fill(Background)
    draw_tiles()
    draw_swaps()

    if tiles == origin_tiles:
        game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()