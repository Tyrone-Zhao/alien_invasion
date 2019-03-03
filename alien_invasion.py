import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # 查看系统可用字体
    # print(pygame.font.get_fonts())
    # print(pygame.font.get_fonts())

    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 创建Play按钮
    play_button = Button(ai_settings, screen, 'Play')

    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一艘飞船、子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button,
                        aliens, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, sb,
                              stats)
            gf.update_aliens(ai_settings, aliens, ship, stats, screen, bullets,
                             sb, play_button)
            gf.update_screen_bullets(bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, stats,
                         play_button, sb)


run_game()
