import pygame

RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, x, y, width, height, color, text, text_size, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("couriernew", text_size, bold=True)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.action:
                self.action()
