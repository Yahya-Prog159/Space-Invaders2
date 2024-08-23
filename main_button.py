import pygame
import button

pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('buttons')

# Load button images
start_btn_img = pygame.image.load('img/pixel_art_start.png').convert_alpha()
exit_btn_img = pygame.image.load('img/pixel_art_exit.png').convert_alpha()


    


# Create the button instances
start_btn = button.Button(0, 50, start_btn_img, 1)
exit_btn = button.Button(45, 20, exit_btn_img, 1)


run = True
while run:

    screen.fill((202, 228, 241))

    if start_btn.draw(screen):
        print("Start")

    if exit_btn.draw(screen):
        run = False
        print("Exit")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
