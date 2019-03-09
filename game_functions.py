#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys

import pygame

from alien import Alien
from bullet import Bullet


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False


def fire_bullet(bullets, ai_settings, screen, ship):
    """发射子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


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


def check_events(ship, ai_settings, screen, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_settings, screen, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


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


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """更新子弹位置并删除消失在屏幕的子弹"""
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    # print(len(bullets))
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # print(collisions)
    if len(aliens) == 0:
        create_fleet(ai_settings, screen, aliens, ship)



def get_number_aliens_x(ai_settings, alien_width):
    """
    计算每行可容纳多少个外星人

    :param ai_settings: 设置
    :param alien_width: 外星人宽度
    :return: 每一行的外星人数目
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, alien_height, ship_height):
    """
    计算屏幕可容纳多少行外星人

    :param ai_settings: 设置
    :param alien_height:  外星人高度
    :param ship_height:  飞船高度
    :return: 外星人行数
    """

    # 屏幕高度减去第一行外星人的上边距（外 星人高度）、飞船的高度以及最初外星人群与飞船的距离（外星人高度的两倍）
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    # 外星人高度 + 间隔高度(alien_height)
    number_rows = int(available_space_y / (2 * alien_height))
    print("number_rows=", number_rows)
    return number_rows


def create_alien(ai_settings, alien_number, aliens, screen, number_row):
    """创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * number_row
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    """
    创建外星人群

    :param ai_settings: 设置
    :param screen: 屏幕
    :param aliens: 外星人
    :param ship: 飞船
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
    # 创建第一群外星人
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, alien_number, aliens, screen, number_row)


def change_fleet_direction(ai_settings, aliens):
    """改变外星人的移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def update_aliens(ai_settings, aliens):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
