#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一群外星人
    aliens = Group()
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    # 创建积分牌
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ship, ai_settings, screen, bullets, stats, play_button, aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            gf.update_aliens(stats, screen, bullets, ship, ai_settings, aliens)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb)


run_game()
