# 🗂️ Gerenciador de Tarefas

**Aplicativo desenvolvido por Juliano Aragão** para organizar tarefas do dia a dia, com interface de terminal e suporte a salvamento automático em arquivo JSON.

---

## 🚀 Funcionalidades

* 📋 **Listar tarefas pendentes e concluídas**
* ✍️ **Adicionar novas tarefas**
* ✅ **Marcar tarefas como concluídas**
* 🗑️ **Excluir tarefas (somente administrador)**
* 💾 **Salvamento automático em `tarefas.json`**
* 🔐 **Proteção com senha de administrador**
* 🧠 **Interface simples e colorida no terminal**

---

## ⚙️ Requisitos

O programa roda em **qualquer sistema com Python 3 instalado**.

Instale as dependências com:

```bash
pip install -r requirements.txt
```

> No momento, este projeto usa apenas bibliotecas padrão do Python,
> então o arquivo `requirements.txt` é apenas para referência.

---

## ▶️ Como executar

### Opção 1 — Rodar o script Python

```bash
python3 agenda_tarefas.py
```

### Opção 2 — Usar o executável

Se estiver usando Linux (como Pop!_OS ou Ubuntu):

```bash
cd dist
./agenda_tarefas
```

---

## 🔒 Acesso de Administrador

Para excluir tarefas é necessário inserir a senha de administrador.
Durante a digitação, a senha **não é exibida na tela** por segurança.

---

## 💡 Estrutura do Projeto

```
Gerenciador-de-Tarefas/
├── agenda_tarefas.py       # Código principal da aplicação
├── tarefas.json             # Banco de dados simples com as tarefas
├── icone_tarefas.png        # Ícone do aplicativo
├── requirements.txt
└── dist/
    └── agenda_tarefas       # Executável gerado com PyInstaller
```

---

## 🧩 Como gerar o executável

Se quiser gerar o executável novamente, use:

```bash
pyinstaller --onefile --icon=icone_tarefas.png agenda_tarefas.py
```

O arquivo será criado dentro da pasta `dist/`.

---

## 👨‍💻 Autor

**Juliano Aragão**
Desenvolvedor Python | Automação & IA
📧 [juliano.aragao.dev@gmail.com](mailto:juliano.aragao.dev@gmail.com) *(adicione se quiser)*
🌐 [GitHub: Juliano-Aragao](https://github.com/Juliano-Aragao)

---

⭐ *Se este projeto foi útil, deixe uma estrela no repositório!*
