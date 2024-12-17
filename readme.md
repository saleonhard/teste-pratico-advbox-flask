# Ferramenta de Migração - Teste Prático para Seleção ADVBOX

Este projeto foi desenvolvido como parte de um **teste prático para seleção** para a vaga de **Analista Python Júnior** na **ADVBOX**. O objetivo deste projeto é demonstrar habilidades no desenvolvimento de soluções com **Python (Flask)**, **HTML**, **CSS**, **Bootstrap**, e **JavaScript**, com foco em automação, integração de sistemas e análise de dados.

A ferramenta permite ao usuário carregar diretórios, visualizar e fazer o download de tabelas encontradas, e também gerenciar os dados carregados (excluir dados).

## Funcionalidades

- **Carregar Tabelas**: Permite ao usuário selecionar um diretório do sistema local, que será analisado em busca de tabelas.
- **Exibição de Tabelas**: Após carregar o diretório, as tabelas encontradas são exibidas para o usuário.
- **Download de Tabelas**: O usuário pode fazer o download das tabelas processadas.
- **Apagar Dados**: O usuário pode apagar os dados carregados diretamente pela interface.

## Tecnologias Utilizadas

- **HTML**: Estruturação da interface web.
- **CSS**: Estilos personalizados para melhorar a experiência do usuário.
- **Bootstrap 5**: Framework CSS para design responsivo e componentes prontos.
- **Python (Flask)**: Framework Python utilizado para o backend da aplicação.
- **JavaScript**: Interatividade da interface, como exibição de mensagens e carregamento dinâmico.

## Como Usar

### Requisitos

- Python 3.x
- Flask (Framework para o backend)
- Dependências listadas no arquivo `requirements.txt`

### Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/SEU-USUARIO/ferramenta-migracao.git
   cd ferramenta-migracao

## Criar e Ativar um Ambiente Virtual

1. Crie o ambiente virtual:
    ```bash
    python3 -m venv venv
    ```

2. Ative o ambiente virtual:
    - Para Linux/Mac:
        ```bash
        source venv/bin/activate
        ```
    - Para Windows:
        ```bash
        venv\Scripts\activate
        ```

## Instalar as Dependências Necessárias

Instale as dependências do projeto:
    ```bash
    pip install -r requirements.txt
    ```

## Executando o Projeto

Inicie o servidor Flask:
    ```bash
    python app.py
    ```

Abra o navegador e vá para [http://localhost:5000](http://localhost:5000) para acessar a ferramenta.

## Estrutura de Diretórios

- `app.py`: Lógica do servidor Flask, responsável por gerenciar as requisições e processar os diretórios.
 - `utils/`: Contém funções auxiliares responsáveis pelo processamento e formatação de dados
- `templates/`: Contém os arquivos HTML, incluindo o template principal.
- `static/`: Arquivos estáticos, como imagens, folhas de estilo (CSS) e JavaScript.

## Fluxo de Funcionamento

1. O usuário insere o caminho de um diretório no formulário e clica em "Carregar Tabelas".
2. O sistema processa o diretório e exibe as tabelas encontradas na interface.
3. O usuário pode realizar o download das tabelas clicando no botão "Download Processado".
4. Caso queira apagar os dados carregados, o usuário pode clicar no botão "Apagar Dados Carregados".
