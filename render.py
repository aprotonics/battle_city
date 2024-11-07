import pygame
from configuration import Configuratuion


def draw_text(surf, x, y, text, size, color=(255, 255, 255)):
    font = pygame.font.Font(Configuratuion.font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_life_bar(surf, x, y, pict1, pict2):
    if pict2 < 0:
        pict2 = 0
    if pict1 < 0:
        pict1 = 0
    LIFE_BAR_LENGTH = 100 * 2 / 3
    ARMOR_BAR_LENGTH = pict2 * 2 / 3
    BAR_TOTAL_LENGTH = LIFE_BAR_LENGTH + ARMOR_BAR_LENGTH
    BAR_HEIGHT = 10
    outline_rect = pygame.Rect(x, y, BAR_TOTAL_LENGTH, BAR_HEIGHT)
    fill_rect1 = pygame.Rect(x, y, pict1 * 2 / 3, BAR_HEIGHT)
    fill_rect2 = pygame.Rect(x + LIFE_BAR_LENGTH, y, pict2 * 2 / 3, BAR_HEIGHT)
    pygame.draw.rect(surf, Configuratuion.GREEN, fill_rect1)
    pygame.draw.rect(surf, Configuratuion.WHITE, fill_rect2)
    pygame.draw.rect(surf, Configuratuion.WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img.set_colorkey(Configuratuion.BLACK)
        img_rect = img.get_rect()
        img_rect.x = x - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def render():
    Configuratuion.screen.fill(Configuratuion.BLACK)
    Configuratuion.all_sprites.draw(Configuratuion.screen)
    Configuratuion.layers.draw(Configuratuion.screen)
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 3, 5, str(Configuratuion.formatted_now_time), 24)                        # Время
    draw_text(Configuratuion.screen, Configuratuion.WIDTH / 3 * 2 - 25, 5, str(Configuratuion.total_score), 24)                      # Очки
    draw_life_bar(Configuratuion.screen, 5, 10, Configuratuion.player.life, Configuratuion.player.armor)                             # Уровень жизни
    draw_lives(Configuratuion.screen, Configuratuion.WIDTH - 30, 5, Configuratuion.player.lives, Configuratuion.player_mini_img)                    # Количество жизней
    draw_text(Configuratuion.screen, Configuratuion.current_score_centerx, Configuratuion.current_score_top, str(Configuratuion.current_score), 18) # Локальные очки
    draw_text(Configuratuion.screen, Configuratuion.game_over_string_centerx, Configuratuion.game_over_string_top, Configuratuion.game_over_string, 45)   # "GAME OVER"

    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()
