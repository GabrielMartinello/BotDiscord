O Projeto foi desenvolvido com Python 3.11.5.

Bibliotecas utilizadas:
* discord - Biblioteca para enviar/ler comandos do discord
* os, dotenv - Pegar valores do .env
* firebase_admin - Para persistir dados em nuvem
* datetime - Para manipular datas

Este projeto foi desenvolvido com intuito de ajudar um grupo de amigos a controlar a frequência mensal em que praticam exercícios físicos. Para isso desenvolvi um bot para o discord que vai controlar para eles e salvar os dados no Firebase.

#

### Contagem de presenças
Para que o bot registre sua presença, você precisa enviar uma foto e na mensagem desta foto colocar a tag #euFui, ele irá verificar se teve uma foto e se a foto possui esta mensagem, consequentemente irá salvar no banco de dados do firebase

![Alt text](/src/bancoDeDadosFirebase.jpg?raw=true "Banco de Dados")


### Mostrar vencedor
Todo início de mês (Dia primeiro) ele irá executar uma task para verificar quem foi o vencedor do mês, fazendo um count de registros e retornando um top 3 em forma de mensagem no discord, ele irá fazer isto de forma automática sem precisar rodar comandos. No exemplo abaixo só tinha dois participantes no mês anterior

![Alt text](/src/vencedorBot.jpg?raw=true "Vencedor")
