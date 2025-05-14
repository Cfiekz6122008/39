import pygame
import sys


pygame.init()


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Рисовалка с палитрой и прямоугольниками")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
PINK = (255, 192, 203)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
BORDER_COLOR = BLACK


colors = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET, PINK, GRAY, BLACK]
CUR_INDEX = 0
color_size = 50
palette_rect = pygame.Rect(10, 10, color_size * len(colors), color_size)
palette = pygame.Surface(palette_rect.size)
dragging_palette = False
offset = (0, 0)


brush_color = BLACK
brush_width = 5
fill_mode = False


canvas = pygame.Surface(screen.get_size())
canvas.fill(WHITE)


drawing_rect = False
start_pos = (0, 0)
current_rect = None
rectangles = []


def draw_palette():
    """Отрисовка палитры цветов"""
    palette.fill(WHITE)

    for i in range(len(colors)):
        color_rect = pygame.Rect(i * color_size, 0, color_size, color_size)
        pygame.draw.rect(palette, colors[i], color_rect)

    border_rect = pygame.Rect(CUR_INDEX * color_size, 0, color_size, color_size)
    pygame.draw.rect(palette, BORDER_COLOR, border_rect, width=3)
    screen.blit(palette, palette_rect.topleft)



clock = pygame.time.Clock()
FPS = 60
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(canvas, "screenshot.png")
            running = False


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if palette_rect.collidepoint(mouse_pos):
                    selected_color_index = (mouse_pos[0] - palette_rect.left) // color_size
                    CUR_INDEX = selected_color_index
                    brush_color = colors[CUR_INDEX]
                else:
                    drawing_rect = True
                    start_pos = mouse_pos
                    current_rect = pygame.Rect(start_pos, (0, 0))

            elif event.button == 3:
                if palette_rect.collidepoint(mouse_pos):
                    dragging_palette = True
                    offset = (mouse_pos[0] - palette_rect.left, mouse_pos[1] - palette_rect.top)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing_rect:
                drawing_rect = False
                if current_rect.width > 5 and current_rect.height > 5:
                    rectangles.append((current_rect.copy(), brush_color, fill_mode))
                current_rect = None

            elif event.button == 3:
                dragging_palette = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fill_mode = not fill_mode


    if dragging_palette:
        new_pos = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
        palette_rect.topleft = new_pos


    if drawing_rect and mouse_pressed[0]:
        x = min(start_pos[0], mouse_pos[0])
        y = min(start_pos[1], mouse_pos[1])
        width = abs(mouse_pos[0] - start_pos[0])
        height = abs(mouse_pos[1] - start_pos[1])
        current_rect = pygame.Rect(x, y, width, height)


    screen.blit(canvas, (0, 0))


    for rect, color, fill in rectangles:
        if fill:
            pygame.draw.rect(canvas, color, rect)
        else:
            pygame.draw.rect(canvas, color, rect, 2)


    if current_rect:
        if fill_mode:
            pygame.draw.rect(screen, brush_color, current_rect)
        else:
            pygame.draw.rect(screen, brush_color, current_rect, 2)


    draw_palette()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()