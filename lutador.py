import pygame
from constantes import *

class Lutador:
    def __init__(self, x_inicial_rel, cor, nome, controles, sprite_path=None, col_idle=1, 
                 sprite_ataque_path=None, col_ataque=1, 
                 sprite_pulo_path=None, col_pulo=2,
                 sprite_agachar_path=None, col_agachar=1, # Adicionado col_agachar
                 inverter_base=False):
        
        self.nome, self.cor, self.controles = nome, cor, controles
        self.hp = 100
        self.x_origem_rel = x_inicial_rel
        self.pos_x_rel = x_inicial_rel
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direcao, self.atacando = 1, False
        self.inverter_base = inverter_base
        
        # --- Estados ---
        self.vel_y = 0
        self.pulando = False
        self.agachado = False
        self.gravidade = 1.2
        self.forca_pulo = -20
        
        # --- Lógica de Sprites ---
        self.usa_sprite = False
        if sprite_path:
            try:
                self.frames_idle = self.carregar_frames(sprite_path, col_idle)
                self.frames_ataque = self.carregar_frames(sprite_ataque_path, col_ataque) if sprite_ataque_path else None
                self.frames_pulo = self.carregar_frames(sprite_pulo_path, col_pulo) if sprite_pulo_path else None
                # Agora usa a variável col_agachar enviada pelo main
                self.frames_agachar = self.carregar_frames(sprite_agachar_path, col_agachar) if sprite_agachar_path else None
                
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()
                self.usa_sprite = True
            except Exception as e:
                print(f"Erro ao carregar sprites de {nome}: {e}")

    def carregar_frames(self, path, colunas):
        sheet = pygame.image.load(path).convert_alpha()
        largura_frame = sheet.get_width() // colunas
        altura_frame = sheet.get_height()
        lista = []
        for i in range(colunas):
            sub = sheet.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame))
            lista.append(sub)
        return lista

    def ajustar(self, L, A, reset=False):
        if reset: self.pos_x_rel = self.x_origem_rel
        larg, alt = int(L * 0.16), int(A * 0.7)  
        self.rect = pygame.Rect(int(L * self.pos_x_rel), A - alt - int(A * 0.05), larg, alt)
        self.chao_y = A - alt - int(A * 0.05)
        self.vel = int(L * 0.008)

    def animar(self):
        if self.agachado:
            self.frame_index = 0
            return
            
        if self.pulando and self.frames_pulo:
            self.frame_index = 0 if self.vel_y < 5 else 1
            return

        cooldown = 100 if self.atacando else 500 
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.atacando:
                if self.frame_index >= len(self.frames_ataque):
                    self.atacando = False
                    self.frame_index = 0
            else:
                self.frame_index %= len(self.frames_idle)

    def atualizar(self, alvo, L, comandos):
        self.agachado = False

        if not self.atacando:
            # Agachar
            if comandos["baixo"] and not self.pulando:
                self.agachado = True
            
            # Movimento Lateral
            if not self.agachado:
                if comandos["esquerda"]: self.rect.x -= self.vel
                if comandos["direita"]:  self.rect.x += self.vel
                
                # Pulo
                if comandos["pulo"] and not self.pulando:
                    self.vel_y = self.forca_pulo
                    self.pulando = True

        # Gravidade
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.y >= self.chao_y:
            self.rect.y = self.chao_y
            self.vel_y = 0
            self.pulando = False

        self.rect.clamp_ip(pygame.Rect(0, 0, L, 10000))
        self.direcao = 1 if self.rect.centerx < alvo.rect.centerx else -1
        self.pos_x_rel = self.rect.x / L
        if self.usa_sprite: self.animar()

    def atacar(self, alvo, L, comandos):
        # Unificado para usar o dicionário 'comandos' (Teclado + Gamepad)
        if comandos["ataque"] and not self.atacando:
            self.atacando, self.frame_index = True, 0
            
            # O soco só acerta se o alvo NÃO estiver agachado
            if not alvo.agachado:
                alcance = int(L * 0.08)
                area = pygame.Rect(0, 0, alcance, 40)
                if self.direcao == 1:
                    area.midleft = self.rect.midright
                else:
                    area.midright = self.rect.midleft
                
                area.y = self.rect.y + 30 # Ajuste de altura do soco
                
                if area.colliderect(alvo.rect): 
                    alvo.hp -= 10

    def desenhar(self, tela, L):
        if self.usa_sprite:
            if self.agachado and self.frames_agachar:
                lista = self.frames_agachar
            elif self.pulando and self.frames_pulo:
                lista = self.frames_pulo
            elif self.atacando and self.frames_ataque:
                lista = self.frames_ataque
            else:
                lista = self.frames_idle
                
            idx = self.frame_index if self.frame_index < len(lista) else 0
            img = lista[idx]
            
            deve_inverter = (self.direcao == -1)
            if self.inverter_base: deve_inverter = not deve_inverter
            if deve_inverter: img = pygame.transform.flip(img, True, False)
            
            # --- Correção de Deformação no Agachamento ---
            if self.agachado:
                # Reduz altura visual para 60% e cola no chão
                nova_alt = int(self.rect.height * 0.6)
                novo_y = self.rect.bottom - nova_alt
                img_f = pygame.transform.scale(img, (self.rect.width, nova_alt))
                tela.blit(img_f, (self.rect.x, novo_y))
            else:
                img_f = pygame.transform.scale(img, (self.rect.width, self.rect.height))
                tela.blit(img_f, self.rect)
        else:
            # Fallback Retângulos
            r = self.rect.copy()
            if self.agachado: 
                r.height //= 2
                r.y = self.rect.bottom - r.height
            pygame.draw.rect(tela, self.cor, r)