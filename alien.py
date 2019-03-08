#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen, ):
        """外星人管理类"""

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载外星人图像并获取其外接矩形

        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
