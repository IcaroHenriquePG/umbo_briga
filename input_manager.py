import pygame

class InputHandler:
    # Lista global para rastrear quais IDs de joystick já foram ocupados
    controles_em_uso = []

    def __init__(self):
        self.joystick = None
        self.atualizar_controles()

    def atualizar_controles(self):
        """Busca o próximo controle disponível na 'pilha' do sistema"""
        quantidade = pygame.joystick.get_count()
        
        for i in range(quantidade):
            if i not in InputHandler.controles_em_uso:
                try:
                    joy = pygame.joystick.Joystick(i)
                    joy.init()
                    self.joystick = joy
                    InputHandler.controles_em_uso.append(i)
                    print(f"-> Player vinculado ao controle {i}: {joy.get_name()}")
                    break
                except pygame.error:
                    continue

    def start_pressionado(self):
        """Verifica se o botão Start (geralmente ID 7) foi pressionado"""
        if self.joystick:
            try:
                # Botão 7 é o padrão para Start em Xbox/Playstation
                return self.joystick.get_button(7)
            except:
                return False
        return False

    def get_comandos(self, teclas):
        """Retorna um dicionário com os estados dos comandos (Híbrido)"""
        keys = pygame.key.get_pressed()
        
        # Mapeamento base via Teclado
        cmds = {
            "esquerda": keys[teclas[0]],
            "direita":  keys[teclas[1]],
            "ataque":   keys[teclas[2]],
            "pulo":     keys[teclas[3]],
            "baixo":    keys[teclas[4]]
        }

        # Sobreposição via Gamepad (se conectado)
        if self.joystick:
            try:
                # Eixos analógicos e D-Pad
                eixo_x = self.joystick.get_axis(0)
                eixo_y = self.joystick.get_axis(1)
                hat = self.joystick.get_hat(0)

                if eixo_x < -0.5 or hat[0] == -1: cmds["esquerda"] = True
                if eixo_x > 0.5 or hat[0] == 1:  cmds["direita"] = True
                if eixo_y > 0.5 or hat[1] == -1: cmds["baixo"] = True
                
                # Botões de ação
                if self.joystick.get_button(0): cmds["ataque"] = True # Botão A/X
                if self.joystick.get_button(1) or self.joystick.get_button(2): 
                    cmds["pulo"] = True # Botão B ou Y
            except pygame.error:
                self.joystick = None
                
        return cmds