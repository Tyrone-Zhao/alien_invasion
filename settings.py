class Settings():
    ''' 存储《外星人入侵》的所有设置的类 '''

    def __init__(self):
        ''' 初始化游戏的静态设置 '''
        # 屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed_factor = 1.5				# 飞船移动速度
        self.ship_limit = 3 						# 飞船生命值

        # 子弹设置
        self.bullet_speed_factor = 3				# 子弹速度
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (30, 20, 230)			# 子弹颜色
        self.bullets_allowed = 3					# 同时允许的最多子弹数
        self.bullets_penetration = True				# 子弹穿透特效
        self.bullets_continuous = True				# 持续开火
        self.bullets_continuous_distance = 200		# 持续开火子弹间距

        # 外星人设置
        self.fleet_drop_speed = 30

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        ''' 初始化随游戏进行而变化的设置 '''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50

    def increase_speed(self):
        ''' 设置游戏速度和外星人点数的提升 '''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)