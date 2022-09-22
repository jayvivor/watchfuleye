import pygame
import visuals
import player
import utils
import season
import constants

pygame.init()
pygame.font.init()

# screen_size = constants.screen_size
screen_size = 1280, 720
screen = pygame.display.set_mode(screen_size)
bg_color = 0, 255, 171
text_color = 255, 106, 0
screen.fill(bg_color)

szn = season.Season()
visuals.initialize(szn.cast)

player_icons = {p:pygame.image.load(visuals.player_avs[p]) for p in szn.cast}

## Blit icons onto the screen
icon_buffer = .4
sidebar_buffer = .25
bottom_bar_buffer = .4
dimensions = (screen_size[0]*(1-sidebar_buffer),screen_size[1]*(1-bottom_bar_buffer))

grid, icon_width, icon_height = utils.gridify(szn.cast, dimensions)  #icon_width/height are the total size for the icons
buffer = .4
for hg, x, y in grid:
    player_icons[hg] = pygame.transform.scale(player_icons[hg], (icon_width*(1-icon_buffer), icon_height*(1-icon_buffer)))
    screen.blit(player_icons[hg], (x+icon_width*(buffer/2),y+icon_height*(buffer/2)))


## Helper Functions
bottom_rect = pygame.Rect(0,screen_size[1]*(1-bottom_bar_buffer),screen_size[0]*(1-sidebar_buffer),screen_size[1]*bottom_bar_buffer )
bottom_disp = (screen_size[0]*(1-sidebar_buffer), screen_size[1]*bottom_bar_buffer)

def display_stats(hg: player.Player):

    y_buffer = (1-bottom_bar_buffer) * screen_size[1]
    x_buffer = screen_size[0]*.02
    b_grid, stat_width, stat_height = utils.gridify(hg.stats.items(), bottom_disp)
    font_scale = stat_width//15

    pygame.draw.rect(screen,bg_color, bottom_rect)
    for stat_tuple, x, y in b_grid:
        stat_name, stat_val = stat_tuple
        font = pygame.font.SysFont("minecraftmono", int(font_scale))
        stat_labels = font.render(f"{stat_name}", True, text_color)
        font = pygame.font.SysFont("minecraftmono", int(font_scale*1.5))
        stat_value = font.render(f"{stat_val}/100", True, text_color)
        screen.blit(stat_labels, (x+x_buffer, y+y_buffer))
        screen.blit(stat_value, (x+x_buffer, y+y_buffer+stat_height/3))



#Main loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check to see the icon clicked on; display their stats
            position = event.pos
            click_x = position[0]
            click_y = position[1]
            total_width = dimensions[0]
            total_height = dimensions[1]
            if click_x < total_width and click_y < total_height:
                for p, player_x, player_y in grid:
                    if player_x < click_x < player_x+icon_width and player_y < click_y < player_y+icon_height:
                        display_stats(p)
            
            






    # Flip the display

    pygame.display.flip()


# Done! Time to quit.

pygame.quit()
visuals.clean_up()