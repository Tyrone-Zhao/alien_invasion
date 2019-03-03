import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    ''' 显示得分信息的类 '''

    def __init__(self, ai_settings, screen, stats):
        ''' 初始化显示得分涉及的属性 '''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 初始化死亡提示信息
        self.destory_str = '方向键移动，空格键射击，b键开始游戏，q键退出！'

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)
        self.font_chinese = pygame.font.SysFont(
            'songtisc', 15)

        # 准备初始化最高得分和得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_destory()

    def prep_score(self):
        ''' 将得分转换为一幅渲染的图像 '''
        rounded_score = round(self.stats.score, -1)
        chn_str = '当前得分:'
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        self.chn_img = self.font_chinese.render(chn_str, True, self.text_color,
                                                self.ai_settings.bg_color)

        # 将得分英文放在放在屏幕顶部中央左侧
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.centerx - 50
        self.score_rect.top = 20

        # 将得分中文放在英文左侧
        self.chn_str_rect = self.chn_img.get_rect()
        self.chn_str_rect.right = self.score_rect.left
        self.chn_str_rect.top = self.score_rect.top

    def prep_high_score(self):
        ''' 将最高得分转换为渲染的图像 '''
        high_score = round(self.stats.high_score, -1)
        high_chn_str = '最高得分:'
        high_score_str = "{:,}".format(high_score)
        self.high_score_img = self.font.render(high_score_str, True, self.text_color,
                                               self.ai_settings.bg_color)
        self.high_chn_img = self.font_chinese.render(high_chn_str, True,
                                                     self.text_color, self.ai_settings.bg_color)

        # 将最高得分中文放在屏幕左上方
        self.high_chn_str_rect = self.high_chn_img.get_rect()
        self.high_chn_str_rect.left = 20
        self.high_chn_str_rect.top = self.score_rect.top

        # 将最高得分英文放在中文右侧
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.left = self.high_chn_str_rect.right
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        ''' 将等级转换为渲染的图像 '''
        level_chn_str = '难度等级:'
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color)
        self.level_chn_img = self.font_chinese.render(level_chn_str, True,
                                                      self.text_color)

        # 将等级中文放在屏幕中央右侧
        self.level_chn_rect = self.level_chn_img.get_rect()
        self.level_chn_rect.left = self.screen_rect.centerx + 50
        self.level_chn_rect.top = self.score_rect.top

        # 将等级英文放在中文右侧
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.level_chn_rect.right
        self.level_rect.top = self.score_rect.top

    def prep_ships(self):
        ''' 显示还余下多少艘飞船 '''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.image = pygame.image.load(
                'images/ship_small.bmp')
            ship.rect.right = self.screen_rect.right - ship_number * \
                ship.rect.width + 5
            ship.rect.top = 15
            self.ships.add(ship)

    def show_score(self):
        ''' 在屏幕上显示等级和得分 '''
        self.screen.blit(self.chn_img, self.chn_str_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_chn_img, self.high_chn_str_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.level_chn_img, self.level_chn_rect)

        # 绘制剩余飞船数量
        self.ships.draw(self.screen)

    def prep_destory(self):
        ''' 将死亡提示转换为渲染的图像 '''
        self.destory_image = self.font_chinese.render(self.destory_str,
                                                      True, self.text_color)

        # 将死亡提示移动到屏幕右下角
        self.destory_rect = self.destory_image.get_rect()
        self.destory_rect.right = self.screen_rect.right - 30
        self.destory_rect.bottom = self.screen_rect.bottom - 15

    def show_destory(self):
        ''' 在屏幕上显示死亡提示 '''
        self.screen.blit(self.destory_image, self.destory_rect)
