# Ontologia do cidade democrática e triplificação dos dados

Este repositório é dedicado aos roteiros de disponibilização
de conteúdo semanticamente enriquecido do Cidade Democrática através.
Os recursos disponibilizados são, principalmente:
* Script para triplificação dos dados do Cidade Democrática: triplificaCD.py
* Script para síntese da ontologia do Cidade Democrática: OCD.py
* Dados triplificados do portal: cdTriplestore.rdf
* Ontologia do portal: OCD.owl
Compactações nas triplas são feitas para estar de acordo com as normas do github.

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
* Pq os observatórios tem tags? Do que se tratam?
* Não há info de latitude e longitude em lugar algum, confirmam?
* Do que se tratam os observatórios?
* Adiantado das datas e horas, que são parseadas para não dar conflito com xsd:dateTime. Procurando motivo para usar literais tipados, mas deixando de fora enquanto isso por simplicidade.
* Adicionadas imagens como nomes, mas a imagem em si não está acessível. Ver se está disponivel online em uma URL ou se incluimos da triplificacao a imagem diretamente.
* A propriedade ocd:tagged é usada tanto no caso:
    * ocd:tag ocd:tagged ocd:obs, quanto:
    * ocd:tagging ocd:tagged ocd:topico
* userName é a propriedade name com a restricao de possuir domínio com a classe User. "Defined properties" neste formato de intersecção parece ainda não ser possível. Uma alternativa, caso isso seja desejado, é fazer a busca de todas as triplas { ?s ocd:name ?nome . ?s a ocd:User } e acrescentar na triplestore as triplas ?s ocd:userName ?nome. Além disso, é importante colocar na ontologia que ocd:userName rdfs:subPropertyOf ocd:name. Esta parte pode ser pulada para deixar mais leve e simples a ontologia e a triplificação. Para esta primeira versão, é o que foi feito.
* Usar ocd:body para ocd:text, usado somente em ocd:Tag ocd:text litera(string)?


