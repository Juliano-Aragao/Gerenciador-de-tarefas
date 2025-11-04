import os
import time
import json
import sys
import termios
import tty

# Configuração de cores
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
AZUL = "\033[94m"
RESET = "\033[0m"

# Arquivo para salvar tarefas
ARQUIVO_TAREFAS = "tarefas.json"

# Listas iniciais
tarefas = []
tarefas_concluidas = []

# ---------------- Funções de persistência ----------------

def salvar_tarefas():
    # Se o arquivo não existir, cria um vazio antes de salvar
    if not os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
            json.dump({"pendentes": [], "concluidas": []}, f, indent=4, ensure_ascii=False)

    # Estrutura dos dados atuais
    dados = {
        "pendentes": tarefas,
        "concluidas": tarefas_concluidas
    }

    # Salva (ou sobrescreve) o conteúdo atualizado
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def carregar_tarefas():
    global tarefas, tarefas_concluidas
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            tarefas = dados.get("pendentes", [])
            tarefas_concluidas = dados.get("concluidas", [])

# ---------------- Funções do menu ----------------
def limpar():
    os.system('clear')

def menu():
    try:
        limpar()
        print(f"""
        {VERDE}================================
                    MENU
        ================================{RESET}
        {VERMELHO} 1  -{RESET} {AZUL} Listar tarefas {RESET}
        {VERMELHO} 2  -{RESET} {AZUL} Criar tarefa {RESET}
        {VERMELHO} 3  -{RESET} {AZUL} Marcar tarefa como concluída {RESET}
        {VERMELHO} 4  -{RESET} {AZUL} Deletar tarefa {RESET}
        {VERMELHO} 5  -{RESET} {AZUL} Sair {RESET}
        """)
        escolha = int(input(f"{VERDE}Digite sua opção: {RESET}"))

        if escolha == 1:
            limpar()
            listar_tarefas()
            listar_tarefas_concluidas()
            voltar_menu()
        elif escolha == 2:
            criar_tarefa()
        elif escolha == 3:
            concluir_tarefa()
        elif escolha == 4:
            titulo_login()
        elif escolha == 5:
            sair()
        else:
            input(f"{VERMELHO}Opção inválida. Pressione Enter para tentar novamente.{RESET}")
            menu()
    except ValueError:
        input(f"{VERMELHO}Entrada inválida. Pressione Enter para tentar novamente.{RESET}")
        menu()

# ---------------- Funções de tarefas ----------------
def listar_tarefas():
    print(f"\n{VERDE}******** Tarefas Pendentes ********{RESET}")
    if not tarefas:
        print(f"{AMARELO}Nenhuma tarefa pendente.{RESET}")
    else:
        for i, t in enumerate(tarefas, start=1):
            print(f"{i}. {t}")

def listar_tarefas_concluidas():
    print(f"\n{VERMELHO}******** Tarefas Concluídas ********{RESET}")
    if not tarefas_concluidas:
        print(f"{AMARELO}Nenhuma tarefa concluída ainda.{RESET}")
    else:
        for i, t in enumerate(tarefas_concluidas, start=1):
            print(f"{i}. {t}")

def criar_tarefa():
    nova_tarefa = input("\nDigite sua nova tarefa: ").upper().strip()

    if not nova_tarefa:
        input(f"{VERMELHO}A tarefa não pode estar vazia. Pressione Enter para voltar ao menu.{RESET}")
        menu()

    if nova_tarefa in tarefas:
        input(f"{AMARELO}Essa tarefa já existe. Pressione Enter para voltar ao menu.{RESET}")
        menu()
    else:
        tarefas.append(nova_tarefa)
        salvar_tarefas()
        limpar()
        print(f"\n✅ Tarefa '{nova_tarefa}' adicionada com sucesso!\n")
        listar_tarefas()
        input(f"{VERDE}Pressione Enter para voltar ao menu.{RESET}")
        menu()

def concluir_tarefa():
    limpar()
    print(f"\n{VERDE}***** Concluir Tarefa *****{RESET}\n")

    if not tarefas:
        input(f"{AMARELO}Nenhuma tarefa disponível para concluir. Pressione Enter para voltar ao menu.{RESET}")
        menu()

    listar_tarefas()

    while True:
        try:
            escolha = int(input("\nQual tarefa foi concluída? (Digite o número) \n=> "))
            if 1 <= escolha <= len(tarefas):
                break
            else:
                print(f"{VERMELHO}Número inválido. Escolha uma tarefa existente.{RESET}")
        except ValueError:
            print(f"{VERMELHO}Entrada inválida. Digite apenas números.{RESET}")

    concluida = tarefas.pop(escolha - 1)
    tarefas_concluidas.append(concluida)
    salvar_tarefas()
    limpar()
    print(f"\n✅ Tarefa '{concluida}' marcada como concluída!\n")
    listar_tarefas()
    listar_tarefas_concluidas()
    input(f"{VERDE}Pressione Enter para voltar ao menu.{RESET}")
    menu()

# ---------------- Funções administrativas ----------------
def titulo_login():
    limpar()
    print(f"""
        ****************************************
        {VERMELHO}Atenção: apenas administradores podem excluir tarefas.{RESET}
        ****************************************
        """)
    
    escolha = input("Pressione 1 para prosseguir ou qualquer tecla para voltar: ")
    if escolha == '1':
        login_adm()
    else:
        menu()


def login_adm():
    limpar()
    senha_correta = "777"  # senha armazenada de forma oculta
    tentativas = 3

    while tentativas > 0:
        print(f"{AZUL}Digite a senha de administrador:{RESET} ", end="", flush=True)
        senha_digitada = ""
        
        # Desativa o "eco" do terminal (modo silencioso)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch == "\n" or ch == "\r":  # Enter
                    print()
                    break
                elif ch == "\x7f":  # Backspace
                    if len(senha_digitada) > 0:
                        senha_digitada = senha_digitada[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    senha_digitada += ch
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # Verificação da senha
        if senha_digitada == senha_correta:
            print(f"\n{VERDE}✅ Acesso permitido!{RESET}")
            time.sleep(1)
            deletar_tarefa()
            return
        else:
            tentativas -= 1
            if tentativas > 0:
                print(f"\n{VERMELHO}❌ Senha incorreta. Você tem mais {tentativas} tentativa(s).{RESET}")
                time.sleep(1)
                limpar()
            else:
                print(f"\n{VERMELHO}⚠️  Número máximo de tentativas atingido. Acesso bloqueado!{RESET}")
                time.sleep(2)
                sair()



def deletar_tarefa():
    limpar()
    try:
        escolha = int(input(f"""
        {AMARELO}===== Deletar Tarefa ====={RESET}
        1 - Deletar tarefa pendente
        2 - Deletar tarefa concluída
        Escolha uma opção: """))

        if escolha == 1:
            limpar()
            listar_tarefas()
            if not tarefas:
                input(f"{AMARELO}Nenhuma tarefa para excluir. Pressione Enter para voltar.{RESET}")
                menu()
            num = int(input("\nDigite o número da tarefa a ser excluída: "))
            excluida = tarefas.pop(num - 1)
            salvar_tarefas()
            print(f"\n🗑️ Tarefa '{excluida}' excluída com sucesso!")
            input(f"{VERDE}Pressione Enter para voltar ao menu.{RESET}")
            menu()

        elif escolha == 2:
            limpar()
            listar_tarefas_concluidas()
            if not tarefas_concluidas:
                input(f"{AMARELO}Nenhuma tarefa concluída para excluir. Pressione Enter para voltar.{RESET}")
                menu()
            num = int(input("\nDigite o número da tarefa a ser excluída: "))
            excluida = tarefas_concluidas.pop(num - 1)
            salvar_tarefas()
            print(f"\n🗑️ Tarefa '{excluida}' excluída com sucesso!")
            input(f"{VERDE}Pressione Enter para voltar ao menu.{RESET}")
            menu()

        else:
            input(f"{VERMELHO}Opção inválida. Pressione Enter para voltar ao menu.{RESET}")
            menu()

    except (ValueError, IndexError):
        input(f"{VERMELHO}Entrada inválida. Pressione Enter para voltar ao menu.{RESET}")
        menu()

def voltar_menu():
    input(f"{VERDE}Pressione Enter para voltar ao menu.{RESET}")
    menu()
    
def sair():
    limpar()
    print(f"\n{VERDE}Obrigado por usar o gerenciador de tarefas!{RESET}")
    print(f"{VERMELHO}*** Volte sempre para acompanhar seu progresso! ***{RESET}\n")
    exit()    

# ---------------- Início do programa ----------------
carregar_tarefas()
menu()
