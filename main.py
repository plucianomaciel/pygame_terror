import pygame
import random
import sys
import math

# Configurações iniciais
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jogo de Matemática com Pygame")

# Configuração de áudio
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)  # Ajusta o volume global para o máximo

# Variáveis de controle
threshold = 0.7
jumpscare_active = False
sound_started = False
score = 0  # Variável de pontuação inicializada
game_over = False
mic_volume = 0.5  # Volume fictício para simular microfone
question, options, correct_answer = "", [], ""
difficulty = None
menu = True

# Botões do menu e do jogo (ajustados para uma posição mais baixa)
easy_button = pygame.Rect(325, 250, 150, 50)
medium_button = pygame.Rect(325, 350, 150, 50)
hard_button = pygame.Rect(325, 450, 150, 50)
reset_button_rect = pygame.Rect(360, 520, 80, 40)
menu_button_rect = pygame.Rect(700, 10, 80, 40)  # Novo botão de Menu

# Carregando a imagem e o som do jumpscare
jumpscare_image = pygame.image.load('assets/monstro.png').convert()
jumpscare_sound = pygame.mixer.Sound('assets/jumpsacare.ogg')
jumpscare_sound.set_volume(1.0)  # Ajusta o volume do som para o máximo

# Carregando a imagem de fundo do menu
menu_background = pygame.image.load('assets/terromatica.jpg').convert()

# Fontes
font_large = pygame.font.Font(None, 50)
font_medium = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 24)
font_score_large = pygame.font.Font(None, 80)  # Fonte grande para pontuação final

def generate_question():
    global question, correct_answer, options
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    # Nível fácil: Soma e Subtração
    if difficulty == "easy":
        operation = random.choice(["+", "-"])

    # Nível médio: Soma, Subtração, Multiplicação e Divisão
    elif difficulty == "medium":
        operation = random.choice(["+", "-", "*", "/"])
        if operation == "/" and num2 == 0:
            num2 = random.randint(1, 10)  # Evitar divisão por zero

    # Nível difícil: Soma, Subtração, Multiplicação, Divisão, Potência e Raiz
    elif difficulty == "hard":
        operation = random.choice(["+", "-", "*", "/", "**", "√"])
        if operation == "/" and num2 == 0:
            num2 = random.randint(1, 10)  # Evitar divisão por zero
        elif operation == "**":
            question = f"{num1} ^ {num2}"
            correct_answer = num1 ** num2
            options = generate_options(correct_answer)
            return
        elif operation == "√":
            question = f"√{num1 * num1}"  # Gera uma raiz quadrada de um quadrado perfeito
            correct_answer = num1
            options = generate_options(correct_answer)
            return

    # Gera a questão e a resposta correta
    if operation == "+":
        question = f"{num1} + {num2}"
        correct_answer = num1 + num2
    elif operation == "-":
        question = f"{num1} - {num2}"
        correct_answer = num1 - num2
    elif operation == "*":
        question = f"{num1} * {num2}"
        correct_answer = num1 * num2
    elif operation == "/":
        question = f"{num1} / {num2}"
        correct_answer = round(num1 / num2, 2)  # Arredonda para 2 casas decimais

    options = generate_options(correct_answer)

def generate_options(correct_answer):
    # Gera opções de resposta (uma correta e três erradas)
    options = [correct_answer]
    while len(options) < 4:
        wrong_answer = correct_answer + random.randint(-5, 5)
        if wrong_answer not in options:
            options.append(wrong_answer)
    random.shuffle(options)
    return options

def draw_text(text, font, color, x, y, align="center"):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "topleft":
        text_rect.topleft = (x, y)
    screen.blit(text_obj, text_rect)

def trigger_jumpscare():
    global jumpscare_active, sound_started, game_over
    if not jumpscare_active and not sound_started:
        jumpscare_active = True
        sound_started = True
        if jumpscare_sound:  # Verifica se o som foi carregado corretamente
            jumpscare_sound.play()
        else:
            print("Erro: Som não carregado")

def reset_game():
    global score, game_over, jumpscare_active, sound_started
    score = 0
    game_over = False
    jumpscare_active = False
    sound_started = False
    generate_question()

# Loop principal do jogo
while True:
    screen.fill((0, 0, 0))  # Fundo preto

    if menu:
        # Exibe a imagem de fundo do menu
        screen.blit(menu_background, (0, 0))

        # Desenha os botões do menu inicial (mais para baixo)
        pygame.draw.rect(screen, (0, 255, 0), easy_button)
        pygame.draw.rect(screen, (255, 255, 0), medium_button)
        pygame.draw.rect(screen, (255, 0, 0), hard_button)
        draw_text("Fácil", font_medium, (0, 0, 0), easy_button.centerx, easy_button.centery)
        draw_text("Médio", font_medium, (0, 0, 0), medium_button.centerx, medium_button.centery)
        draw_text("Difícil", font_medium, (0, 0, 0), hard_button.centerx, hard_button.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    difficulty = "easy"
                    menu = False
                    reset_game()
                elif medium_button.collidepoint(event.pos):
                    difficulty = "medium"
                    menu = False
                    reset_game()
                elif hard_button.collidepoint(event.pos):
                    difficulty = "hard"
                    menu = False
                    reset_game()
    else:
        # Jogo principal
        mic_volume = random.uniform(0, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button_rect.collidepoint(event.pos) and not game_over:
                    reset_game()
                elif menu_button_rect.collidepoint(event.pos):  # Retorna ao menu inicial
                    menu = True
                    game_over = False
                    reset_game()
                elif not game_over:
                    for i, option in enumerate(options):
                        if pygame.Rect(325, 250 + i * 60, 150, 40).collidepoint(event.pos):
                            if option == correct_answer:
                                score += 10  # Aumenta a pontuação ao responder corretamente
                                generate_question()
                            else:
                                trigger_jumpscare()

        # Checa se o som terminou
        if sound_started and not pygame.mixer.get_busy():
            jumpscare_active = False
            game_over = True
            sound_started = False

        # Exibe o jogo ou a pontuação final
        if jumpscare_active:
            # Exibe a imagem de jumpscare
            screen.blit(pygame.transform.scale(jumpscare_image, (800, 600)), (0, 0))
            draw_text("GAME OVER", font_large, (255, 0, 0), 400, 300)
        elif game_over:
            # Exibe a pontuação final em tamanho grande
            draw_text(f"Pontuação Final: {score}", font_score_large, (255, 255, 255), 400, 300)
        else:
            # Exibe o jogo normal
            draw_text(f"Volume: {mic_volume:.2f}", font_small, (255, 255, 255), 10, 10, "topleft")
            draw_text(f"Score: {score}", font_small, (255, 255, 255), 10, 40, "topleft")

            if not game_over:
                draw_text(question, font_large, (255, 255, 255), 400, 100)
                for i, option in enumerate(options):
                    pygame.draw.rect(screen, (0, 255, 0), (325, 250 + i * 60, 150, 40))
                    draw_text(str(option), font_medium, (0, 0, 0), 400, 270 + i * 60)

        # Botão de reset e menu
        pygame.draw.rect(screen, (255, 255, 255), reset_button_rect)
        draw_text("Reset", font_medium, (0, 0, 0), reset_button_rect.centerx, reset_button_rect.centery)

        pygame.draw.rect(screen, (255, 255, 255), menu_button_rect)  # Botão de menu
        draw_text("Menu", font_medium, (0, 0, 0), menu_button_rect.centerx, menu_button_rect.centery)

    pygame.display.flip()
    pygame.time.delay(100)
