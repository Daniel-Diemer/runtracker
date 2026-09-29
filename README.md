# RunTracker

RunTracker é uma aplicação web desenvolvida com Flask e PostgreSQL para registrar treinos de corrida e caminhada, acompanhar histórico e visualizar métricas de desempenho.

O objetivo do projeto é aplicar conceitos de desenvolvimento web, autenticação, banco de dados relacional, sessões, validações e organização de uma aplicação Flask.

## Funcionalidades

- Cadastro de usuário
- Login e logout com sessão
- Senha protegida com hash
- Registro de treinos
- Edição de treinos
- Exclusão de treinos
- Histórico de atividades
- Dashboard com métricas gerais
- Cálculo de distância total
- Cálculo de tempo total
- Cálculo de pace médio
- Máscara para distância em km
- Máscara para tempo no formato HH:MM:SS
- Mensagens de feedback com categorias
- Layout responsivo

## Tecnologias utilizadas

- Python
- Flask
- PostgreSQL
- HTML
- CSS
- JavaScript
- Jinja2
- Werkzeug Security
- python-dotenv
- psycopg2

## Estrutura do projeto

```text
runtracker/
│
├── app.py
├── database.py
├── utils.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── cadastro.html
│   ├── dashboard.html
│   ├── novo_treino.html
│   ├── historico.html
│   └── editar_treino.html
│
└── static/
    └── css/
        └── style.css
```

## Aprendizados aplicados

Neste projeto foram aplicados conceitos como:

- Rotas com Flask
- Templates com Jinja2
- Autenticação de usuários
- Sessões
- Hash de senhas
- Integração com PostgreSQL
- CRUD completo
- Validação de formulários
- Organização de funções auxiliares
- Uso de variáveis de ambiente
- Versionamento com Git e GitHub
- Separação entre lógica, banco de dados e interface

## Status do projeto

Versão inicial finalizada.

Próximas melhorias possíveis:

- Adicionar gráficos de evolução
- Criar filtros por data e tipo de treino
- Criar tela de perfil do usuário
- Melhorar o dashboard com estatísticas avançadas
- Fazer deploy da aplicação
- Adicionar testes automatizados

## Autor

Desenvolvido por Daniel Diemer Alves.

GitHub: [Daniel-Diemer](https://github.com/Daniel-Diemer)