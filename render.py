def render():
    import main
    
    main.screen.fill(main.BLACK)
    main.all_sprites.draw(main.screen)
    main.layers.draw(main.screen)
    main.draw_text(main.screen, main.WIDTH / 3, 5, str(main.formatted_now_time), 24)                        # Время
    main.draw_text(main.screen, main.WIDTH / 3 * 2 - 25, 5, str(main.total_score), 24)                      # Очки
    main.draw_life_bar(main.screen, 5, 10, main.player.life, main.player.armor)                             # Уровень жизни
    main.draw_lives(main.screen, main.WIDTH - 30, 5, main.player.lives, main.player_mini_img)                    # Количество жизней
    main.draw_text(main.screen, main.current_score_centerx, main.current_score_top, str(main.current_score), 18) # Локальные очки
    main.draw_text(main.screen, main.game_over_string_centerx, main.game_over_string_top, main.game_over_string, 45)   # "GAME OVER"

    # после отрисовки всего, переворачиваем экран
    main.pygame.display.flip()
