<h1 align="center">Gerador de Apostas</h1>

## Descrição do Projeto
<p align="center">Este é um programa que gera números aleatórios para realizar apostas na Mega-Sena, consulta qual foi o ultimo resultado do sorteio, e confere quantos numeros você acertou da última aposta realizada.</p>



<h4 align="center"> 
	🚧   🚀 Em construção...  🚧
</h4>

### Features

- [x] Cadastro de usuário
- [x] Edição de usuário
- [x] Remover usuário
- [x] Criar nojo jogo aleatório
- [x] Resultado da Mega-Sena
- [x] Consultar número de acertos
- [ ] Autenticação

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas: [Python 3.9](https://www.python.org/),
[Git](https://git-scm.com), [Mysql](https://www.mysql.com/) e [Mysql Workbench](https://www.mysql.com/products/workbench/)
Além disto é bom ter um editor para trabalhar com o código como [Pycharm](https://www.jetbrains.com/pt-br/pycharm/) ou [VSCode](https://code.visualstudio.com/)

### 🎲 Rodando o Back End (servidor)

```bash
# Clone este repositório
$ git clone <https://github.com/ericfp87/Teste_Python.git>

# Acesse a pasta do projeto no terminal/cmd
$ cd Teste_Python

# Instale as dependências
$ pip install -r requirements.txt

# Crie um banco de dados no Mysql
- Nome da Database: users
- usuário de login: admin
- senha: admin

# Execute a aplicação em modo de desenvolvimento
$ python main.py runserver



# O servidor inciará na porta:5000 - acesse <http://127.0.0.1:5000>
```

### 🛠 Tecnologias

As seguintes ferramentas foram usadas na construção do projeto:

- [Python 3.9](https://www.python.org/)
- [Mysql](https://www.mysql.com/)


##Obervações:
#### A Autenticação JWT ainda não foi concluida, mas os códigos de sua criação ainda estão no arquivo main.py. A declaração do Decorator @jwt_required está comentado em todas as rotas que necessitam de acesso autorizado.