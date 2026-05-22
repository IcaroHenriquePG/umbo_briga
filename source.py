import pygame
import sys
import os

# --- Configurações Iniciais ---
pygame.init()
LARGURA, ALTURA = 800, 450
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Street Fighter Pygame - Versão Final")

# --- Troca do Ícone ---
try:
    # Carrega a imagem perf.png
    icone = pygame.image.load('perf.png')
    pygame.display.set_icon(icone)
except:
    # Caso a imagem não esteja na pasta, o jogo não trava
    print("Erro: Arquivo 'perf.png' não encontrado para o ícone.")

clock = pygame.time.Clock()

# Cores Padronizadas
BRANCO    = (255, 255, 255)
PRETO     = (0, 0, 0)
VERMELHO  = (200, 0, 0) 
VERDE     = (0, 200, 0)
AZUL      = (0, 0, 200)
CINZA_HUD = (40, 40, 40)

class Lutador:
    def __init__(self, x_inicial_rel, cor, nome, controles):
        self.nome = nome
        self.cor = cor
        self.hp = 100
        self.controles = controles 
        
        # Proporções e Posicionamento
        self.larg_rel = 0.07
        self.alt_rel = 0.3
        self.x_origem_rel = x_inicial_rel # Guarda a posição inicial para o reset
        self.pos_x_rel = x_inicial_rel  
        
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.velocidade = 0
        self.direcao = 1
        self.atacando = False
        self.timer_ataque = 0

    def ajustar_redimensionamento(self, L, A, reset=False):
        """Ajusta o tamanho e posiciona na origem ou na posição atual."""
        if reset:
            self.pos_x_rel = self.x_origem_rel
            
        largura_corpo = int(L * self.larg_rel)
        altura_corpo = int(A * self.alt_rel)
        
        self.rect.width = largura_corpo
        self.rect.height = altura_corpo
        self.rect.x = int(L * self.pos_x_rel)
        self.rect.y = A - altura_corpo - int(A * 0.05)
        self.velocidade = int(L * 0.008)

    def mover(self, alvo, L):
        keys = pygame.key.get_pressed()
        if keys[self.controles[0]]: self.rect.x -= self.velocidade
        if keys[self.controles[1]]: self.rect.x += self.velocidade
        
        self.rect.clamp_ip(tela.get_rect())
        self.direcao = 1 if self.rect.centerx < alvo.rect.centerx else -1
        self.pos_x_rel = self.rect.x / L

    def atacar(self, alvo, L):
        keys = pygame.key.get_pressed()
        if keys[self.controles[2]] and not self.atacando:
            self.atacando = True
            self.timer_ataque = 12
            alcance = int(L * 0.06)
            area_soco = pygame.Rect(0, 0, alcance, 20)
            if self.direcao == 1: area_soco.midleft = self.rect.midright
            else: area_soco.midright = self.rect.midleft
            
            if area_soco.colliderect(alvo.rect):
                alvo.hp -= 10

    def desenhar(self, L):
        pygame.draw.rect(tela, self.cor, self.rect)
        if self.atacando:
            larg_s = int(L * 0.05)
            x_s = self.rect.right if self.direcao == 1 else self.rect.left - larg_s
            pygame.draw.rect(tela, PRETO, (x_s, self.rect.y + 30, larg_s, 15))
            self.timer_ataque -= 1
            if self.timer_ataque <= 0: self.atacando = False

def desenhar_hud(p1, p2, L, A):
    larg_b = int(L * 0.35)
    alt_b = int(A * 0.06)
    fonte_nome = pygame.font.SysFont("Impact", int(A * 0.04))
    
    # P1 HUD (Direita)
    pygame.draw.rect(tela, CINZA_HUD, (L - larg_b - 30, 30, larg_b, alt_b))
    pygame.draw.rect(tela, VERDE, (L - larg_b - 30, 30, (larg_b/100)*p1.hp, alt_b))
    nome_p1 = fonte_nome.render(p1.nome, True, PRETO)
    tela.blit(nome_p1, (L - nome_p1.get_width() - 30, 30 + alt_b))
    
    # P2 HUD (Esquerda)
    pygame.draw.rect(tela, CINZA_HUD, (30, 30, larg_b, alt_b))
    pygame.draw.rect(tela, VERDE, (30, 30, (larg_b/100)*p2.hp, alt_b))
    nome_p2 = fonte_nome.render(p2.nome, True, PRETO)
    tela.blit(nome_p2, (30, 30 + alt_b))

# --- Setup Jogadores ---
p1 = Lutador(0.7, AZUL, "P1", [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN])
p2 = Lutador(0.2, VERMELHO, "P2", [pygame.K_a, pygame.K_d, pygame.K_SPACE])

p1.ajustar_redimensionamento(LARGURA, ALTURA)
p2.ajustar_redimensionamento(LARGURA, ALTURA)

rodando, jogo_ativo = True, True

while rodando:
    tela.fill(BRANCO)
    L_ATUAL, A_ATUAL = tela.get_size()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.VIDEORESIZE:
            L_NOVA, A_NOVA = evento.w, evento.h
            tela = pygame.display.set_mode((L_NOVA, A_NOVA), pygame.RESIZABLE)
            p1.ajustar_redimensionamento(L_NOVA, A_NOVA)
            p2.ajustar_redimensionamento(L_NOVA, A_NOVA)

        if not jogo_ativo and evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            p1.hp, p2.hp = 100, 100
            p1.ajustar_redimensionamento(L_ATUAL, A_ATUAL, reset=True)
            p2.ajustar_redimensionamento(L_ATUAL, A_ATUAL, reset=True)
            jogo_ativo = True

    if jogo_ativo:
        p1.mover(p2, L_ATUAL); p1.atacar(p2, L_ATUAL)
        p2.mover(p1, L_ATUAL); p2.atacar(p1, L_ATUAL)
        if p1.hp <= 0 or p2.hp <= 0: jogo_ativo = False

    p1.desenhar(L_ATUAL); p2.desenhar(L_ATUAL)
    desenhar_hud(p1, p2, L_ATUAL, A_ATUAL)

    if not jogo_ativo:
        vencedor = "JOGADOR 1" if p2.hp <= 0 else "JOGADOR 2"
        fonte_v = pygame.font.SysFont("Impact", int(L_ATUAL * 0.06))
        txt_v = fonte_v.render(f"{vencedor} VENCEU!", True, VERMELHO)
        txt_r = pygame.font.SysFont("Arial", int(L_ATUAL * 0.02), True).render("Pressione 'R' para Revanche", True, PRETO)
        
        tela.blit(txt_v, (L_ATUAL//2 - txt_v.get_width()//2, A_ATUAL//2 - 50))
        tela.blit(txt_r, (L_ATUAL//2 - txt_r.get_width()//2, A_ATUAL//2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()