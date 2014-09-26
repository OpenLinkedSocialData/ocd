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
* É bom verificar se há URLs padrão para as postagens e para os usuários. Registrar isso talvez como a própria URI.
* Análises informativas com as tags usadas. Confrontar com as palavras mais usadas no texto produzido.
* Usuários não possuem relação de amizade, mas se relacionam pelos seguintes modos:
    * Seguem postagens iguais
    * Usam tags iguais
    * Usam palavras iguais
    * Fizeram participação no mesmo período de tempo
    * Responderam à postagens uns dos outros
    * Comentaram as mesmas postagens
    * Vale triplificar regioes (estados, cidades e bairros) e entender como se relaciona com o resto do portal
    * Pq os observatórios tem tags? Do que se tratam?
    * Não há info de latitude e longitude em lugar algum, confirmam?
    * Do que se tratam os observatórios?
