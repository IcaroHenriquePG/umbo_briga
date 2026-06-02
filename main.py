import pygame, sys
from constantes import *
from lutador import Lutador
from interface import desenhar_hud
from input_manager import InputHandler
from menu import MenuInicial

# --- INICIALIZAÇÃO ---
pygame.init()
pygame.joystick.init()

# ... (imports anteriores)

L, A = 800, 450
tela = pygame.display.set_mode((L, A), pygame.RESIZABLE)
pygame.display.set_caption("Joguin de Luta - Teclado + Gamepad")

# --- LÓGICA DO ÍCONE ---
try:
    # Carrega a imagem
    icone = pygame.image.load('perf.png')
    # Define como ícone da janela
    pygame.display.set_icon(icone)
    print("Ícone carregado com sucesso!")
except Exception as e:
    print(f"Não foi possível carregar perf.png: {e}")
# -----------------------

# ... (restante do código: teclas_p1, h1, p1, etc)

# Configuração de Teclado: [ESQ, DIR, ATK, PULO, BAIXO]
teclas_p1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_UP, pygame.K_DOWN]
teclas_p2 = [pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.K_w, pygame.K_s]

# Handlers seguem a ordem de criação (P1 pega primeiro, P2 depois)
h1 = InputHandler()
h2 = InputHandler()

# Criar Lutadores
p1 = Lutador(0.7, AZUL, "P1", teclas_p1, 
             sprite_path=r'assets\sprites\sprite-p1.png', col_idle=7,
             sprite_ataque_path=r'assets\sprites\soccu-1.png', col_ataque=4,
             sprite_pulo_path=r'assets\sprites\pulo-1.png', col_pulo=2,
             sprite_agachar_path=r'assets\sprites\dicoca-1.png', col_agachar=1,
             inverter_base=True)

p2 = Lutador(0.2, VERMELHO, "P2", teclas_p2, 
             sprite_path=r'assets\sprites\sprite-p1.png', col_idle=7,
             sprite_ataque_path=r'assets\sprites\soccu-1.png', col_ataque=4,
             sprite_pulo_path=r'assets\sprites\pulo-1.png', col_pulo=2,
             sprite_agachar_path=r'assets\sprites\dicoca-1.png', col_agachar=1,
             inverter_base=True)

p1.ajustar(L, A); p2.ajustar(L, A)
clock, rodando, ativo = pygame.time.Clock(), True, True

# --- MENU INICIAL ---
menu = MenuInicial(L, A)
menu.mostrar(tela)
# --------------------

# --- LOOP PRINCIPAL ---
while rodando:
    tela.fill(BRANCO)
    L, A = tela.get_size()

    # Captura de Eventos do Sistema
    for e in pygame.event.get():
        if e.type == pygame.QUIT: 
            rodando = False
            
        if e.type == pygame.VIDEORESIZE:
            tela = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            p1.ajustar(e.w, e.h); p2.ajustar(e.w, e.h)

        # Lógica de Reinício (Se o jogo acabou)
        if not ativo:
            tecla_r = (e.type == pygame.KEYDOWN and e.key == pygame.K_r)
            btn_start = h1.start_pressionado() or h2.start_pressionado()
            
            if tecla_r or btn_start:
                p1.hp, p2.hp, ativo = 100, 100, True
                p1.ajustar(L, A, True); p2.ajustar(L, A, True)

        # Hot-Plug: Se conectar controle novo com jogo aberto
        if e.type == pygame.JOYDEVICEADDED:
            if h1.joystick is None: h1.atualizar_controles()
            elif h2.joystick is None: h2.atualizar_controles()

    # Lógica de Frame
    if ativo:
        # Pega comandos dos handlers (Mistura Teclado + Gamepad)
        cmds_p1 = h1.get_comandos(teclas_p1)
        cmds_p2 = h2.get_comandos(teclas_p2)

        # Atualiza os lutadores
        p1.atualizar(p2, L, cmds_p1)
        p1.atacar(p2, L, cmds_p1)
        
        p2.atualizar(p1, L, cmds_p2)
        p2.atacar(p1, L, cmds_p2)

        if p1.hp <= 0 or p2.hp <= 0: ativo = False

    # Desenho
    p1.desenhar(tela, L)
    p2.desenhar(tela, L)
    desenhar_hud(tela, p1, p2, L, A)

    if not ativo:
        f = pygame.font.SysFont("Impact", int(L * 0.06))
        txt = f"P1 VENCEU!" if p2.hp <= 0 else "P2 VENCEU!"
        v = f.render(f"{txt} - START/R p/ Reset", True, VERMELHO)
        tela.blit(v, (L//2 - v.get_width()//2, A//2 - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()