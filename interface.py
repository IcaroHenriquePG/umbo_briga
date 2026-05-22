import pygame
from constantes import *

def desenhar_hud(tela, p1, p2, L, A):
    larg_b, alt_b = int(L * 0.35), int(A * 0.06)
    fonte = pygame.font.SysFont("Impact", int(A * 0.04))
    
    # HUD P2 (Esquerda) e P1 (Direita) conforme sua lógica anterior
    for p, pos_x in [(p2, 30), (p1, L - larg_b - 30)]:
        pygame.draw.rect(tela, CINZA_HUD, (pos_x, 30, larg_b, alt_b))
        pygame.draw.rect(tela, VERDE, (pos_x, 30, (larg_b/100)*p.hp, alt_b))
        txt = fonte.render(p.nome, True, PRETO)
        tela.blit(txt, (pos_x if p == p2 else L - txt.get_width() - 30, 30 + alt_b))