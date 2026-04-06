1 - criação da tabela em "schema.sql"
2 - coração do banco de dados e seu funcionamento (conexão com o banco)
3 - inicialização do banco 
4 - CRUD
    4.1 - cria o comando de create (inserir novos dados)
    4.2 - cria o comando de listar
    4.3 - cria o comando de buscar
    4.4 - cria o comando update
    4.5 - cria o comando delete

5 - cria o arquivo teste_db.py para testar o comando create do CRUD e verificar o funcionamento do banco de dados com dados imaginários

6 - criar API REST com FLASK
    6.1 - estrutura base
    6.2 - cria ROTA: GET / (PAINEL PRINCIPAL)
    6.3 - GET /leituras (LISTAR TODAS)
    6.4 - POST /leituras - essa é a rota que o Arduino vai usar
    6.5 - GET /leituras/<id>
    6.6 - PUT /leituras/<id>
    6.7 - DELETE /leituras/<id>
    6.8 - GET /api/estatisticas
    6.9 - cria comando para rodar o servidor