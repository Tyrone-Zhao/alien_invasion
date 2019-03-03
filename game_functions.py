import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets,
                         stats, aliens, sb, play_button):
    ''' 响应按键 '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if ai_settings.bullets_continuous:
            ship.continuous_fire = True
        fire_bullet(ai_settings, screen, ship, bullets, stats)
    elif event.key == pygame.K_q:
        sys.exit(0)
    elif event.key == pygame.K_b and not stats.game_active:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb,
                   play_button)


def check_keyup_events(event, ship):
    ''' 响应松开 '''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        ship.continuous_fire = False


def check_events(ai_settings, screen, ship, bullets, stats, play_button,
                 aliens, sb):
    ''' 响应按键和鼠标事件 '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship,
                                 bullets, stats, aliens, sb, play_button)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens,
                              bullets, ai_settings, screen, ship, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets,
                      ai_settings, screen, ship, sb):
    ''' 在玩家单击Play按钮时开始新游戏 '''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb,
                   play_button)


def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb,
               play_button):
    ''' 初始化游戏统计信息及界面 '''
    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 重置记分板图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    sb.destory_str = ''
    sb.prep_destory()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 显示进入页面
    show_begin_page(ai_settings, screen, ship, aliens, stats,
                    play_button, sb)

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def update_tip(str_msg, sleep_time, ai_settings, screen, ship, aliens, stats,
               play_button, sb):
    ''' 更新提示消息 '''
    sb.destory_str = str_msg
    sb.prep_destory()
    update_screen(ai_settings, screen, ship, aliens, stats,
                  play_button, sb)
    sleep(sleep_time)


def show_begin_page(ai_settings, screen, ship, aliens, stats,
                    play_button, sb):
    ''' 显示进入界面 '''
    str_msg = '加载ing........'
    update_tip(str_msg, 1, ai_settings, screen, ship, aliens, stats,
               play_button, sb)
    str_msg = '加载ing..............'
    update_tip(str_msg, 1, ai_settings, screen, ship, aliens, stats,
               play_button, sb)
    str_msg = '加载ing..........................'
    update_tip(str_msg, 1, ai_settings, screen, ship, aliens, stats,
               play_button, sb)
    str_msg = '公元2043年，外星人袭击地球...'
    update_tip(str_msg, 2, ai_settings, screen, ship, aliens, stats,
               play_button, sb)
    str_msg = '保护地球生命的使命，消灭所有外星人！'
    update_tip(str_msg, 2, ai_settings, screen, ship, aliens, stats,
               play_button, sb)
    str_msg = '必须在外星人抵达地球之前完成！'
    update_tip(str_msg, 2, ai_settings, screen, ship, aliens, stats,
               play_button, sb)
    str_msg = ''
    update_tip(str_msg, 0, ai_settings, screen, ship, aliens, stats,
               play_button, sb)


def update_screen_bullets(bullets):
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_screen(ai_settings, screen, ship, aliens, stats,
                  play_button, sb):
    ''' 更新屏幕上的图像，并切换到新屏幕 '''
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 绘制飞船和外星人
    ship.blitme()
    aliens.draw(screen)

    # 显示得分及提示信息
    sb.show_score()
    sb.show_destory()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, sb,
                   stats):
    ''' 更新子弹的位置，并删除已消失的子弹 '''
    tmp_bullet = 0
    # 更新子弹的位置
    bullets.update()

    # 连续射击时添加子弹
    if ship.continuous_fire == True:
        fire_bullet(ai_settings, screen, ship, bullets, stats)

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    ''' 响应子弹和外星人的碰撞 '''
    # 删除发生碰撞的子弹和外星人 True为是否删除子弹和外星人
    if ai_settings.bullets_penetration == True:
        collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    elif ai_settings.bullets_penetration == False:
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹，加快游戏节奏，并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        # 如果整群外星人都被消灭，就提高一个等级
        stats.level += 1
        sb.prep_level()


def fire_bullet(ai_settings, screen, ship, bullets, stats):
    ''' 如果还没有到达限制，就发射一颗子弹 '''
    # 创建一颗子弹，并将其加入到编组bullets中
    tmp_bullet = 0
    for bullet in bullets:
        if bullet.rect.y > \
                (ship.rect.top - ai_settings.bullets_continuous_distance):
            tmp_bullet += 1
    if tmp_bullet == 0 and stats.proceeding_controler and \
            len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    ''' 计算每行可容纳多少个外星人 '''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    ''' 创建一个外星人并将其放在当前行 '''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    ''' 创建外星人群 '''
    # 创建一个外星人，并计算一行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建多行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    ''' 计算屏幕可容纳多少行外星人 '''
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows


def check_fleet_edges(ai_settings, aliens):
    ''' 有外星人到达边缘时采取相应的措施 '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    ''' 将整群外星人下移，并改变它们的方向 '''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb,
             play_button):
    ''' 响应被外星人撞到的飞船 '''
    if stats.ships_left > 1:
        # 限制游戏过程中字幕状态不可发射子弹
        stats.proceeding_controler = False

        # 更新提示信息
        str_msg = '飞船被撞毁！下一波外星人马上来袭！'
        update_tip(str_msg, 2, ai_settings, screen, ship, aliens, stats,
                   play_button, sb)
        if stats.ships_left > 2:
            str_msg = '集中火力，先消灭完一侧的外星人容易通关！'
            update_tip(str_msg, 3.5, ai_settings, screen, ship, aliens, stats,
                       play_button, sb)
            str_msg = '外星人来袭！'
            update_tip(str_msg, 2, ai_settings, screen, ship, aliens, stats,
                       play_button, sb)
        str_msg = ''
        update_tip(str_msg, 0, ai_settings, screen, ship, aliens, stats,
                   play_button, sb)

        # 将ships_left减1
        stats.ships_left -= 1

        # 更新记分板
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 可以发射子弹
        stats.proceeding_controler = True
    else:
        sb.destory_str = 'Game Over！'
        sb.prep_destory()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,
                        sb, play_button):
    ''' 检查是否有外星人到达了屏幕底端 '''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb,
                     play_button)
            break


def update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb,
                  play_button):
    ''' 
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb,
                 play_button)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets,
                        sb, play_button)


def check_high_score(stats, sb):
    ''' 检查是否诞生了新的最高得分 '''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
