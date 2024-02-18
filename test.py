from random import choice, randint

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/batyrnew2.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/batyrnew3.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/batyrnew4.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
                self.gravity = -20
                self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load("graphics/fly/wolfnewfly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/wolfnewfly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/wolfnew1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/wolfnew2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
        self.speed = 6

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f"Время: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (screen.get_width() / 2, 50))
    screen.blit(score_surf, score_rect)

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Атака Шакалов')
clock = pygame.time.Clock()
running = True
game_active = False
death = False
start_time = 0
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.set_volume(0.3)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load("graphics/sky.png").convert()
ground_surf = pygame.image.load("graphics/snowground.png").convert()

text_font = pygame.font.Font("font/Hardpixel.otf", 30)
text_font_larger = pygame.font.Font("font/Hardpixel.otf", 50)
score_surf = text_font.render('Score', False, (64, 64, 64))
score_rect = score_surf.get_rect(center = (screen.get_width() / 2, 50))

# Intro screen
legion_surf = pygame.image.load("graphics/legion.jpeg").convert()
legion_surf_scaled = pygame.transform.scale(legion_surf, (800, 400))
legion_surf_rect = legion_surf_scaled.get_rect(center = (screen.get_width() / 2, screen.get_height() / 2))

title_surf = text_font_larger.render("АТАКА ШАКАЛОВ", False, 'black')
title_rect = title_surf.get_rect(center = (550, 75))

credits_surf = text_font.render("LEGION INTERACTIVE", False, 'black')
credits_rect = credits_surf.get_rect(center = (550, 110))

guide_surf = text_font.render("Нажимайте пробел чтобы прыгать", False, 'white')
guide_rect = guide_surf.get_rect(center = (screen.get_width() / 2, 330))

# Death screen
death_surf = text_font_larger.render("ВАС ЗАШАКАЛИЛИ", False, 'black')
death_rect = death_surf.get_rect(center = (400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = int(pygame.time.get_ticks() / 1000)
                game_active = True

    if game_active:
        bg_music.play(loops = -1)
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, sky_surf.get_height()))
        display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        death = collision_sprite()
    else:
        screen.blit(legion_surf_scaled, legion_surf_rect)
        pygame.draw.rect(screen, 'black', guide_rect)
        screen.blit(guide_surf, guide_rect)
        if death:
            screen.blit(death_surf, death_rect)
        else:
            screen.blit(title_surf, title_rect)
            screen.blit(credits_surf, credits_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()