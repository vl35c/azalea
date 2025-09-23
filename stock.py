import pygame


class Stock:
    def __init__(self):
        self.window = pygame.display.get_surface()
        self.name: str
        self.share_value: float
        self.total_shares: int
