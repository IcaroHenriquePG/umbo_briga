import pygame
import sys


# =============================================
#  ASSETS — troque apenas estes caminhos
# =============================================
ASSET_FUNDO        = 'assets/menu/umbobriga.png'       # imagem de fundo do menu
ASSET_BOTAO_START  = 'assets/menu/botao_start.png'      # botão START
ASSET_BOTAO_EXIT   = 'assets/menu/botao_exit.png'       # botão EXIT
ASSET_BOTAO_RESUME = 'assets/menu/botao_resume.png'     # botão RESUME (pausa)
ASSET_BOTAO_QUIT   = 'assets/menu/botao_quit.png'       # botão QUIT   (pausa)
# =============================================


class MenuInicial:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura  = altura

        # Fundo
        self.fundo = pygame.image.load(ASSET_FUNDO).convert()
        self.fundo = pygame.transform.scale(self.fundo, (largura, altura))

        # Botões — tamanho fixo menor (ajuste BTN_W e BTN_H conforme quiser)
        BTN_W, BTN_H = 160, 50

        raw_start = pygame.image.load(ASSET_BOTAO_START).convert_alpha()
        raw_exit  = pygame.image.load(ASSET_BOTAO_EXIT).convert_alpha()
        self.botao_start = pygame.transform.scale(raw_start, (BTN_W, BTN_H))
        self.botao_exit  = pygame.transform.scale(raw_exit,  (BTN_W, BTN_H))

        # Posição: canto inferior direito (onde estão os círculos vermelhos)
        margem = 30
        x = largura - BTN_W // 2 - margem
        self.botao_start_rect = self.botao_start.get_rect(center=(x, altura - BTN_H * 2 - margem))
        self.botao_exit_rect  = self.botao_exit.get_rect(center=(x, altura - BTN_H     - margem // 2))

    def mostrar(self, tela):
        while True:
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.botao_start_rect.collidepoint(evento.pos):
                        return "start"
                    if self.botao_exit_rect.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

            # Fundo
            tela.blit(self.fundo, (0, 0))

            # Hover + desenho — START
            tela.blit(self.botao_start, self.botao_start_rect)
            if self.botao_start_rect.collidepoint(mouse_pos):
                hover = pygame.Surface(self.botao_start_rect.size, pygame.SRCALPHA)
                hover.fill((255, 255, 255, 90))
                tela.blit(hover, self.botao_start_rect.topleft)

            # Hover + desenho — EXIT
            tela.blit(self.botao_exit, self.botao_exit_rect)
            if self.botao_exit_rect.collidepoint(mouse_pos):
                hover = pygame.Surface(self.botao_exit_rect.size, pygame.SRCALPHA)
                hover.fill((255, 255, 255, 90))
                tela.blit(hover, self.botao_exit_rect.topleft)

            pygame.display.flip()


class MenuPausa:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura  = altura

        self.botao_resume = pygame.image.load(ASSET_BOTAO_RESUME).convert_alpha()
        self.botao_quit   = pygame.image.load(ASSET_BOTAO_QUIT).convert_alpha()

        self.botao_resume_rect = self.botao_resume.get_rect(center=(largura // 2, altura // 2 - 40))
        self.botao_quit_rect   = self.botao_quit.get_rect(center=(largura // 2, altura // 2 + 40))

    def _blur(self, surface, scale=0.15):
        """Simula blur com redução e ampliação da superfície."""
        w, h = surface.get_size()
        pequena = pygame.transform.smoothscale(surface, (int(w * scale), int(h * scale)))
        return pygame.transform.smoothscale(pequena, (w, h))

    def mostrar(self, tela):
        tela_blur = self._blur(tela.copy())
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_TAB:
                    return "resume"

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.botao_resume_rect.collidepoint(evento.pos):
                        return "resume"
                    if self.botao_quit_rect.collidepoint(evento.pos):
                        return "menu"

            # Fundo com blur
            tela.blit(tela_blur, (0, 0))

            # Hover + desenho — RESUME
            tela.blit(self.botao_resume, self.botao_resume_rect)
            if self.botao_resume_rect.collidepoint(mouse_pos):
                hover = pygame.Surface(self.botao_resume_rect.size, pygame.SRCALPHA)
                hover.fill((255, 255, 255, 90))
                tela.blit(hover, self.botao_resume_rect.topleft)

            # Hover + desenho — QUIT
            tela.blit(self.botao_quit, self.botao_quit_rect)
            if self.botao_quit_rect.collidepoint(mouse_pos):
                hover = pygame.Surface(self.botao_exit_rect.size, pygame.SRCALPHA)
                hover.fill((255, 255, 255, 90))
                tela.blit(hover, self.botao_quit_rect.topleft)

            pygame.display.flip()
            clock.tick(60)
