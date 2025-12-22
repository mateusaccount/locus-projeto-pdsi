# Plataforma de Gestão de Ideias e Problemas

## Sobre o projeto
Sistema web colaborativo desenvolvido em Django que permite aos usuários relatar problemas e sugerir ideias de melhoria. A plataforma fomenta o engajamento comunitário através de funcionalidades de votação (upvote/downvote), comentários em tempo real e um sistema de gamificação que classifica os usuários em níveis (de "Iniciante" a "Líder Comunitário") com base em sua participação.

## Tecnologias Utilizadas
- Python 3.13.5
- Django 5.2.6
- Banco de dados: SQLite
- Outras bibliotecas:
    - **Pillow 12.0.0**: Gerenciamento de upload de imagens (para evidências de problemas/ideias).
    - **zabbix-utils & psutil**: (Dependências instaladas no ambiente).
    - **Unidecode**: Tratamento de strings para busca.
    - **Asgiref & Sqlparse**: Dependências do core do Django.

## Pré-requisitos
- Python 3.8 ou superior
- Git
- Navegador Web moderno (para funcionalidades AJAX/JS)

## Instalação e Configuração

### 1. Clone o repositório
```bash
git clone (https://github.com/mateusaccount/locus-projeto-pdsi)
cd projeto
```

### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
Este comando irá instalar todas as bibliotecas necessárias listadas no arquivo `requirements.txt`.

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

### 5. Execute as migrações do banco de dados

```bash
python manage.py migrate
```

### 6. (Opcional) Crie um superusuário

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

### 7. Execute o servidor
```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## Estrutura do Projeto

```
LOCUS-PROJETO-PDSI/
│
├── manage.py                   # Script de gerenciamento do Django
├── requirements.txt            # Lista de dependências
├── .gitignore                  # Arquivos ignorados pelo Git
├── README.md                   # Documentação do projeto
│
├── config/                     # Configurações do projeto
│
├── app/                        # Aplicação Principal
│   ├── migrations/             # Histórico de banco de dados
│   ├── static/
│   │   └── images/             # Arquivos de imagem estáticos
│   │
│   ├── templates/              # Arquivos HTML
│   │   ├── gestao/
│   │   │   ├── lista.html      # Listagem administrativa
│   │   │   └── painel.html     # Dashboard do admin
│   │   │
│   │   ├── ideias/
│   │   │   ├── detalhe.html    # Visualização única de ideia
│   │   │   ├── form.html       # Formulário de criação
│   │   │   └── lista.html      # Feed de ideias
│   │   │
│   │   ├── problemas/
│   │   │   ├── detalhe.html
│   │   │   ├── form.html
│   │   │   └── lista.html
│   │   │
│   │   ├── registration/       # Autenticação
│   │   │   ├── cadastro.html
│   │   │   ├── login.html
│   │   │   └── ... (arquivos de reset de senha)
│   │   │
│   │   ├── usuarios/
│   │   │   ├── editar.html
│   │   │   └── perfil.html
│   │   │
│   │   ├── base.html           # Template base (navbar/footer)
│   │   ├── dashboard.html      # Página inicial
│   │   └── pesquisa.html       # Resultados de busca
│   │
│   ├── admin.py                # Configuração do Django Admin
│   ├── apps.py                 # Config do App
│   ├── forms.py                # Formulários
│   ├── models.py               # Banco de Dados
│   ├── tests.py                # Testes
│   ├── urls.py                 # Rotas
│   └── views.py                # Lógica (Controllers)
│
└── Docs/
    └── manual/                 # Documentação

```

---

## Funcionalidades

- Autenticação de usuários (registro, login, logout)
- Sistema de Gamificação (cálculo de engajamento e níveis de usuário)
- Gestão de Ideias (submissão, votação upvote/downvote e comentários)
- Relato de Problemas (categorização por área e vínculo com soluções)
- Busca Inteligente (pesquisa instantânea "Live Search" e filtros)
- Painel administrativo

**Para instruções detalhadas**, consulte o [Manual do Usuário](docs/manual/index.html)

## Autores
- Mateus Cosme dos Anjos Lira e Elias Renner Carvalho Damascena
- Orientador: Diego Cirilo