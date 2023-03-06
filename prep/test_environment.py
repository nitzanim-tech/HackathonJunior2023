import pygame
import qrcode


def main():
    pygame.init()

    pygame.display.set_caption("Nitzanim Junior Hackathon")
    window_surface = pygame.display.set_mode((800, 600))

    background = pygame.Surface((800, 600))
    background.fill(pygame.Color("#ffffff"))

    is_running = True

    code = qrcode.make("https://www.nitzanim.tech/").convert('RGB')
    code_image = pygame.image.fromstring(code.tobytes(), code.size, code.mode)

    font = pygame.font.SysFont(None, 48)
    text_img = font.render("Environment is good!", True, pygame.Color("#7755ff"))

    text_x_center = 400

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        window_surface.blit(background, (0, 0))
        window_surface.blit(code_image, (400 - code_image.get_width() // 2, 200))
        window_surface.blit(text_img, (text_x_center - text_img.get_width() // 2, 80))

        text_x_center = (text_x_center + 2 + text_img.get_width() // 2) % (800 + text_img.get_width())\
                        - text_img.get_width() // 2

        pygame.display.update()


if __name__ == '__main__':
    main()
