# Ontologia do cidade democrática e triplificação dos dados

Este repositório é dedicado aos roteiros de disponibilização
de conteúdo semanticamente enriquecido do Cidade Democrática através.
Os recursos disponibilizados são, principalmente:
* Script para triplificação dos dados do Cidade Democrática: triplificaCD.py
* Script para síntese da ontologia do Cidade Democrática: OCD.py
* Dados triplificados do portal: dadosCD.rdf
* Ontologia do portal: OCD.owl

## Anotações
* Há dois ids no user\_dados que não encontramos users: '168', '16657'
* Datas de criação e update não batem do users e do user\_dados. Usado do users
* A URI dada ao Participante é feita com a ID da tabela users. Uma slug seria melhor, mas não parece ser usada para usuario na plataforma.
* É bom verificar se há URLs padrão para as postagens e para os usuários. Registrar isso talvez como a URI.
