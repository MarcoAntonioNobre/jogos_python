import sys
import pygame
from entity import Entity
from settings import *
from support import import_folder

# Definição das cores


telaFinal = pygame.display.set_mode((WIDTH, HEIGHT))


def sairDoJogo():
    pygame.quit()
    sys.exit()



def stop():
    main_sound = pygame.mixer.Sound('./audio/main.ogg')


def reiniciarJogo():
    import main
    pygame.mixer.quit()
    game = main.Game()
    game.run()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (231, 76, 60)
GREEN = (46, 204, 113)
YELLOW = (241, 196, 15)

class Button:
    def __init__(self, text, position, size, color, text_color, action):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position, self.size), border_radius=10)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        x, y = mouse_pos
        if self.position[0] < x < self.position[0] + self.size[0] and self.position[1] < y < self.position[1] + self.size[1]:
            return True
        return False


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100, 'energy': 90, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 300, 'energy': 160, 'attack': 20, 'magic': 10, 'speed': 10}
        self.upgrade_cost = {'health': 80, 'energy': 95, 'attack': 80, 'magic': 110, 'speed': 200}
        self.health = self.stats['health']
        self.energy = self.stats['energy'] * 0.8

        self.exp = 0
        self.total_exp = 0
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('./audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

        self.death_sound = pygame.mixer.Sound('./audio/death.wav')
        self.death_sound.set_volume(0.6)


    def import_player_assets(self):
        character_path = './graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def morte(self):
        if self.health <= 0:

            tela_morte = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Zelda ACM - Você perdeu")

            imagem = pygame.image.load('./graphics/fundobrabo.jpg').convert()
            imagem = pygame.transform.scale(imagem, (WIDTH, HEIGHT))
            tela_morte.blit(imagem, (0, 0))

            fonte = pygame.font.SysFont('Arial', 60)
            texto = fonte.render('GAME OVER', True, (255, 255, 255))
            texto2 = fonte.render('GAME OVER', True, (0, 0, 0))

            botao_reiniciar2 = Button("Reiniciar", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_RESTART), (173, 53), BLACK, BLACK, reiniciarJogo)
            botao_reiniciar = Button("Reiniciar", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_RESTART), (170, 50), YELLOW, BLACK, reiniciarJogo)
            botao_sair2 = Button("Sair do Jogo", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_SAIR), (173, 53), BLACK, BLACK, sairDoJogo)
            botao_sair = Button("Sair do Jogo", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_SAIR), (170, 50), RED, WHITE, sairDoJogo)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if botao_reiniciar.is_clicked(mouse_pos):
                            reiniciarJogo()
                        elif botao_sair.is_clicked(mouse_pos):
                            sairDoJogo()

                telaFinal.blit(texto2, (WIDTH_GAMEOVER2, HEIGTH_GAMEOVER2))
                telaFinal.blit(texto, (WIDTH_GAMEOVER, HEIGTH_GAMEOVER))
                botao_reiniciar2.draw(tela_morte)
                botao_reiniciar.draw(tela_morte)
                botao_sair2.draw(tela_morte)
                botao_sair.draw(tela_morte)

                pygame.display.flip()



    def vitoria(self):

        if self.total_exp >= 6210:

            tela_vitoria = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Zelda ACM - Você ganhou")

            imagem = pygame.image.load('./graphics/fundobrabo.jpg').convert()
            imagem = pygame.transform.scale(imagem, (WIDTH, HEIGHT))
            tela_vitoria.blit(imagem, (0, 0))

            fonte = pygame.font.SysFont('Arial', 60)
            texto = fonte.render('Você Ganhou!', True, (255, 255, 255))
            texto2 = fonte.render('Você Ganhou!', True, (0, 0, 0))

            botao_reiniciar2 = Button("Jogar Novamente", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_RESTART), (223, 53), BLACK, BLACK, reiniciarJogo)
            botao_reiniciar = Button("Jogar Novamente", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_RESTART), (220, 50), GREEN, BLACK, reiniciarJogo)
            botao_sair2 = Button("Sair do Jogo", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_SAIR), (223, 53), BLACK, BLACK, sairDoJogo)
            botao_sair = Button("Sair do Jogo", (WIDTH_GAMEOVER_BUTTON, HEIGHT_GAMEOVER_BUTTON_SAIR), (220, 50), RED, WHITE, sairDoJogo)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if botao_reiniciar.is_clicked(mouse_pos):
                            reiniciarJogo()
                        elif botao_sair.is_clicked(mouse_pos):
                            sairDoJogo()

                telaFinal.blit(texto2, (WIDTH_GAMEOVER2, HEIGTH_GAMEOVER2))
                telaFinal.blit(texto, (WIDTH_GAMEOVER, HEIGTH_GAMEOVER))
                botao_reiniciar2.draw(tela_vitoria)
                botao_reiniciar.draw(tela_vitoria)
                botao_sair2.draw(tela_vitoria)
                botao_sair.draw(tela_vitoria)

                pygame.display.flip()

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']




    def update(self):

        self.morte()
        self.vitoria()
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
