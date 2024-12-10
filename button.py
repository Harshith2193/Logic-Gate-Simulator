import pygame

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
