import pip


if __name__ == '__main__':
    pip.main(['install', 'pygame'])

    import pygame

    pygame.init()

    pygame.display.set_caption("Nitzanim Junior Hackathon")
    window_surface = pygame.display.set_mode((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color("#ffffff"))

    is_running = True

    font = pygame.font.SysFont(None, 48)
    text_img = font.render("Environment is good!", True, pygame.Color("#7755ff"))

    text_x_center = 400
    clock = pygame.time.Clock()

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(background, (0, 0))
        window_surface.blit(text_img, (text_x_center - text_img.get_width() // 2, 80))

        text_x_center = (text_x_center + 5 + text_img.get_width() // 2) % (800 + text_img.get_width()) \
                        - text_img.get_width() // 2

        pygame.display.update()
        clock.tick(60)
