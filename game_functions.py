#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys

import pygame

from alien import Alien
from bullet import Bullet


def check_events(ship, ai_settings, screen, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings, screen, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False


def check_keydown_events(event, ship, ai_settings, screen, bullets):
    """
    响应按键

    :param event: 事件
    :param ship: 飞船对象
    :param ai_settings: 设置对象
    :param screen: 屏幕
    :param bullets: 子弹编组
    """
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)


def update_screen(ai_settings, screen, ship, bullets, aliens):
    """
    更新屏幕上的图像，并切换到新屏幕

    :param ai_settings: 设置对象
    :param screen:  屏幕
    :param ship: 飞船对象
    :param bullets: 子弹编组
    :param aliens: 外星人
    """

    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    """更新子弹位置并删除消失在屏幕的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    # print(len(bullets))


def fire_bullet(bullets, ai_settings, screen, ship):
    """发射子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, aliens):
    """
    创建外星人群

    :param ai_settings: 设置
    :param screen: 屏幕
    :param aliens: 外星人
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))

    # 创建第一行外星人
    for alien_number in range(number_aliens_x):
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
