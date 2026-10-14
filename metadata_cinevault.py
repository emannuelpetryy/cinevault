# -*- coding: utf-8 -*-
import json
import re

METADATA = {
    # 1. PRIORITY (17 items)
    'p1': {'year': 2013, 'imdb': 8.1, 'rtCritics': 95, 'rtAudience': 90}, # 12 Anos de Escravidão
    'p2': {'year': 2017, 'imdb': 6.2, 'rtCritics': 92, 'rtAudience': 57}, # 1922
    'p3': {'year': 1999, 'imdb': 8.6, 'rtCritics': 79, 'rtAudience': 94}, # À Espera de um Milagre
    'p4': {'year': 2006, 'imdb': 8.0, 'rtCritics': 67, 'rtAudience': 87}, # À Procura da Felicidade
    'p5': {'year': 2009, 'imdb': 7.0, 'rtCritics': 59, 'rtAudience': 63}, # A Órfã
    'p6': {'year': 2016, 'imdb': 8.1, 'rtCritics': 84, 'rtAudience': 91}, # Até o Último Homem
    'p7': {'year': 1999, 'imdb': 8.8, 'rtCritics': 79, 'rtAudience': 96}, # Clube da Luta
    'p8': {'year': 2018, 'imdb': 7.4, 'rtCritics': 75, 'rtAudience': 84}, # Durante a Tormenta
    'p9': {'year': 2019, 'imdb': 5.8, 'rtCritics': 48, 'rtAudience': 43}, # Eli
    'p10': {'year': 2007, 'imdb': 7.2, 'rtCritics': 68, 'rtAudience': 68}, # Eu Sou a Lenda
    'p11': {'year': 2016, 'imdb': 7.3, 'rtCritics': 78, 'rtAudience': 79}, # Fragmentado
    'p12': {'year': 2001, 'imdb': 7.9, 'rtCritics': 85, 'rtAudience': 85}, # Harry Potter - Toda a Saga
    'p13': {'year': 2017, 'imdb': 6.5, 'rtCritics': 91, 'rtAudience': 70}, # Jogo Perigoso
    'p14': {'year': 2013, 'imdb': 7.2, 'rtCritics': 48, 'rtAudience': 67}, # O Grande Gatsby
    'p15': {'year': 1991, 'imdb': 8.6, 'rtCritics': 95, 'rtAudience': 95}, # O Silêncio dos Inocentes
    'p16': {'year': 1994, 'imdb': 9.3, 'rtCritics': 89, 'rtAudience': 98}, # Um Sonho de Liberdade
    'p17': {'year': 2005, 'imdb': 8.2, 'rtCritics': 73, 'rtAudience': 90}, # V de Vingança

    # 2. USER / MANU (37 items)
    'u1': {'year': 2020, 'imdb': 7.3, 'rtCritics': 99, 'rtAudience': 86}, # 2 Minutos Além do Infinito
    'u2': {'year': 2022, 'imdb': 7.7, 'rtCritics': 96, 'rtAudience': 82}, # Aftersun
    'u3': {'year': 1995, 'imdb': 8.1, 'rtCritics': 100, 'rtAudience': 93}, # Antes do Amanhecer
    'u4': {'year': 2022, 'imdb': 7.6, 'rtCritics': 96, 'rtAudience': 91}, # Argentina 1985
    'u5': {'year': 2012, 'imdb': 7.9, 'rtCritics': 85, 'rtAudience': 89}, # As Vantagens de Ser Invisível
    'u6': {'year': 2021, 'imdb': 6.8, 'rtCritics': 94, 'rtAudience': 76}, # Ataque dos Cães
    'u7': {'year': 2021, 'imdb': 7.3, 'rtCritics': 86, 'rtAudience': 92}, # Belfast
    'u8': {'year': 1985, 'imdb': 7.8, 'rtCritics': 89, 'rtAudience': 92}, # Clube dos Cinco
    'u9': {'year': 2017, 'imdb': 7.8, 'rtCritics': 98, 'rtAudience': 86}, # Corra!
    'u10': {'year': 2022, 'imdb': 7.3, 'rtCritics': 94, 'rtAudience': 85}, # Decisão de Partir
    'u11': {'year': 2016, 'imdb': 7.4, 'rtCritics': 91, 'rtAudience': 79}, # Dois Caras Legais
    'u12': {'year': 2011, 'imdb': 7.1, 'rtCritics': 54, 'rtAudience': 68}, # Dublê do Diabo
    'u13': {'year': 2019, 'imdb': 7.4, 'rtCritics': 91, 'rtAudience': 52}, # Joias Brutas
    'u14': {'year': 2000, 'imdb': 8.4, 'rtCritics': 93, 'rtAudience': 94}, # Memento / Amnésia
    'u15': {'year': 2022, 'imdb': 6.1, 'rtCritics': 69, 'rtAudience': 53}, # Men - Faces do Medo
    'u16': {'year': 2023, 'imdb': 7.1, 'rtCritics': 88, 'rtAudience': 90}, # Missing / Desaparecida
    'u17': {'year': 1997, 'imdb': 7.5, 'rtCritics': 63, 'rtAudience': 79}, # O Advogado do Diabo
    'u18': {'year': 2000, 'imdb': 8.6, 'rtCritics': 89, 'rtAudience': 96}, # O Auto da Compadecida
    'u19': {'year': 2004, 'imdb': 8.3, 'rtCritics': 92, 'rtAudience': 94}, # O Brilho Eterno de uma Mente sem Lembranças
    'u20': {'year': 2013, 'imdb': 6.8, 'rtCritics': 38, 'rtAudience': 65}, # O Estranho Thomas
    'u21': {'year': 2018, 'imdb': 6.7, 'rtCritics': 67, 'rtAudience': 74}, # O Fotógrafo de Mauthausen
    'u22': {'year': 2006, 'imdb': 8.5, 'rtCritics': 77, 'rtAudience': 92}, # O Grande Truque
    'u23': {'year': 2012, 'imdb': 7.8, 'rtCritics': 64, 'rtAudience': 83}, # O Hobbit - Trilogia
    'u24': {'year': 1980, 'imdb': 8.4, 'rtCritics': 83, 'rtAudience': 93}, # O Iluminado
    'u25': {'year': 1974, 'imdb': 9.0, 'rtCritics': 96, 'rtAudience': 97}, # O Poderoso Chefão 2
    'u26': {'year': 2001, 'imdb': 8.9, 'rtCritics': 93, 'rtAudience': 95}, # O Senhor dos Anéis - Trilogia
    'u27': {'year': 2003, 'imdb': 8.3, 'rtCritics': 82, 'rtAudience': 94}, # Oldboy
    'u28': {'year': 2021, 'imdb': 7.0, 'rtCritics': 85, 'rtAudience': 81}, # On the Count of Three
    'u29': {'year': 2006, 'imdb': 8.5, 'rtCritics': 91, 'rtAudience': 94}, # Os Infiltrados
    'u30': {'year': 2020, 'imdb': 7.7, 'rtCritics': 89, 'rtAudience': 91}, # Os Oito de Chicago
    'u31': {'year': 1992, 'imdb': 8.0, 'rtCritics': 85, 'rtAudience': 92}, # Perfume de Mulher
    'u32': {'year': 2015, 'imdb': 6.3, 'rtCritics': 37, 'rtAudience': 45}, # Projeto Almanaque
    'u33': {'year': 1994, 'imdb': 8.9, 'rtCritics': 92, 'rtAudience': 96}, # Pulp Fiction
    'u34': {'year': 1983, 'imdb': 8.3, 'rtCritics': 79, 'rtAudience': 93}, # Scarface
    'u35': {'year': 1995, 'imdb': 8.6, 'rtCritics': 83, 'rtAudience': 95}, # Seven: Os Sete Crimes Capitais
    'u36': {'year': 1996, 'imdb': 8.1, 'rtCritics': 90, 'rtAudience': 93}, # Trainspotting
    'u37': {'year': 2001, 'imdb': 8.2, 'rtCritics': 74, 'rtAudience': 93}, # Uma Mente Brilhante

    # 3. BROTHER (102 items)
    'b1': {'year': 2018, 'imdb': 6.8, 'rtCritics': 71, 'rtAudience': 73}, # 22 de Julho
    'b2': {'year': 2025, 'imdb': 6.7, 'rtCritics': 75, 'rtAudience': 72}, # A Acompanhante Perfeita
    'b3': {'year': 2016, 'imdb': 6.8, 'rtCritics': 86, 'rtAudience': 73}, # A Autópsia de Jane Doe
    'b4': {'year': 2023, 'imdb': 7.5, 'rtCritics': 96, 'rtAudience': 82}, # A Sala dos Professores
    'b5': {'year': 2023, 'imdb': 7.1, 'rtCritics': 96, 'rtAudience': 88}, # A Última Parada no Arizona
    'b6': {'year': 2005, 'imdb': 6.5, 'rtCritics': 37, 'rtAudience': 59}, # Chave Mestra
    'b7': {'year': 2023, 'imdb': 6.3, 'rtCritics': 80, 'rtAudience': 65}, # Frio nos Ossos
    'b8': {'year': 2020, 'imdb': 6.7, 'rtCritics': 89, 'rtAudience': 74}, # Fuja
    'b9': {'year': 2014, 'imdb': 8.1, 'rtCritics': 88, 'rtAudience': 87}, # Garota Exemplar
    'b10': {'year': 2024, 'imdb': 7.2, 'rtCritics': 92, 'rtAudience': 78}, # Herege
    'b11': {'year': 2024, 'imdb': 7.0, 'rtCritics': 93, 'rtAudience': 89}, # Jurado Nº 2
    'b12': {'year': 2014, 'imdb': 6.5, 'rtCritics': 77, 'rtAudience': 60}, # Lapso Temporal
    'b13': {'year': 1990, 'imdb': 7.8, 'rtCritics': 91, 'rtAudience': 90}, # Louca Obsessão
    'b14': {'year': 2022, 'imdb': 6.4, 'rtCritics': 93, 'rtAudience': 78}, # M3GAN
    'b15': {'year': 2003, 'imdb': 8.1, 'rtCritics': 95, 'rtAudience': 93}, # Memórias de um Assassino
    'b16': {'year': 2020, 'imdb': 6.5, 'rtCritics': 76, 'rtAudience': 68}, # Night Shift
    'b17': {'year': 2019, 'imdb': 6.8, 'rtCritics': 93, 'rtAudience': 60}, # Nós
    'b18': {'year': 2007, 'imdb': 6.4, 'rtCritics': 16, 'rtAudience': 57}, # Número 23
    'b19': {'year': 2022, 'imdb': 7.2, 'rtCritics': 85, 'rtAudience': 92}, # O Alfaiate
    'b20': {'year': 2023, 'imdb': 7.6, 'rtCritics': 93, 'rtAudience': 84}, # O Assassino da Lua das Flores
    'b21': {'year': 2020, 'imdb': 7.1, 'rtCritics': 64, 'rtAudience': 79}, # O Diabo de Cada Dia
    'b22': {'year': 2015, 'imdb': 7.0, 'rtCritics': 91, 'rtAudience': 74}, # O Presente
    'b23': {'year': 2022, 'imdb': 6.3, 'rtCritics': 88, 'rtAudience': 67}, # Observador
    'b24': {'year': 2018, 'imdb': 6.1, 'rtCritics': 61, 'rtAudience': 47}, # Obsessão
    'b25': {'year': 2007, 'imdb': 6.8, 'rtCritics': 69, 'rtAudience': 77}, # Paranoia
    'b26': {'year': 2025, 'imdb': 7.4, 'rtCritics': 85, 'rtAudience': 80}, # Pecadores
    'b27': {'year': 2000, 'imdb': 7.6, 'rtCritics': 68, 'rtAudience': 85}, # Psicopata Americano
    'b28': {'year': 2007, 'imdb': 6.8, 'rtCritics': 80, 'rtAudience': 64}, # Quarto 1408
    'b29': {'year': 2004, 'imdb': 6.2, 'rtCritics': 22, 'rtAudience': 53}, # Roubando Vidas
    'b30': {'year': 2023, 'imdb': 7.0, 'rtCritics': 71, 'rtAudience': 79}, # Saltburn
    'b31': {'year': 2021, 'imdb': 7.5, 'rtCritics': 93, 'rtAudience': 88}, # Socorro!
    'b32': {'year': 2024, 'imdb': 7.2, 'rtCritics': 95, 'rtAudience': 86}, # Strange Darling
    'b33': {'year': 2017, 'imdb': 7.7, 'rtCritics': 88, 'rtAudience': 89}, # Terra Selvagem
    'b34': {'year': 2017, 'imdb': 8.1, 'rtCritics': 90, 'rtAudience': 87}, # Três Anúncios Para Um Crime
    'b35': {'year': 2015, 'imdb': 6.3, 'rtCritics': 44, 'rtAudience': 41}, # True Story
    'b36': {'year': 2016, 'imdb': 8.0, 'rtCritics': 70, 'rtAudience': 87}, # Um Contratempo
    'b37': {'year': 2018, 'imdb': 7.4, 'rtCritics': 93, 'rtAudience': 91}, # Um Lugar Silencioso 1 e 2
    'b38': {'year': 2016, 'imdb': 6.2, 'rtCritics': 34, 'rtAudience': 46}, # Versões de um Crime
    'b39': {'year': 2015, 'imdb': 7.0, 'rtCritics': 91, 'rtAudience': 60}, # A Bruxa
    'b40': {'year': 2024, 'imdb': 7.5, 'rtCritics': 91, 'rtAudience': 73}, # A Substância
    'b41': {'year': 2015, 'imdb': 6.2, 'rtCritics': 68, 'rtAudience': 51}, # A Visita
    'b42': {'year': 2004, 'imdb': 7.0, 'rtCritics': 62, 'rtAudience': 76}, # Espíritos - A Morte Está ao Seu Lado
    'b43': {'year': 2002, 'imdb': 7.5, 'rtCritics': 87, 'rtAudience': 85}, # Extermínio
    'b44': {'year': 2023, 'imdb': 7.1, 'rtCritics': 95, 'rtAudience': 82}, # Fale Comigo
    'b45': {'year': 2022, 'imdb': 6.5, 'rtCritics': 75, 'rtAudience': 68}, # Hakum - O Pesadelo da Bruxa
    'b46': {'year': 2016, 'imdb': 6.3, 'rtCritics': 75, 'rtAudience': 61}, # Lights Out
    'b47': {'year': 2017, 'imdb': 6.6, 'rtCritics': 68, 'rtAudience': 51}, # Mãe!
    'b48': {'year': 2003, 'imdb': 5.8, 'rtCritics': 15, 'rtAudience': 44}, # Na Companhia do Medo
    'b49': {'year': 2021, 'imdb': 6.9, 'rtCritics': 81, 'rtAudience': 88}, # O Telefone Preto
    'b50': {'year': 2013, 'imdb': 6.5, 'rtCritics': 75, 'rtAudience': 53}, # Oculus
    'b51': {'year': 2024, 'imdb': 6.6, 'rtCritics': 88, 'rtAudience': 70}, # Presença
    'b52': {'year': 2007, 'imdb': 7.4, 'rtCritics': 90, 'rtAudience': 82}, # REC
    'b53': {'year': 2019, 'imdb': 6.0, 'rtCritics': 74, 'rtAudience': 51}, # The Lodge
    'b54': {'year': 2012, 'imdb': 8.3, 'rtCritics': 93, 'rtAudience': 93}, # A Caça
    'b55': {'year': 1997, 'imdb': 8.6, 'rtCritics': 80, 'rtAudience': 96}, # A Vida é Bela
    'b56': {'year': 2022, 'imdb': 7.3, 'rtCritics': 93, 'rtAudience': 93}, # Arremessando Alto
    'b57': {'year': 1999, 'imdb': 8.3, 'rtCritics': 87, 'rtAudience': 93}, # Beleza Americana
    'b58': {'year': 2023, 'imdb': 7.4, 'rtCritics': 98, 'rtAudience': 94}, # BlackBerry
    'b59': {'year': 2017, 'imdb': 6.3, 'rtCritics': 87, 'rtAudience': 65}, # Cargo
    'b60': {'year': 2002, 'imdb': 7.5, 'rtCritics': 72, 'rtAudience': 81}, # Gangues de Nova York
    'b61': {'year': 1997, 'imdb': 8.3, 'rtCritics': 97, 'rtAudience': 94}, # Gênio Indomável
    'b62': {'year': 2014, 'imdb': 7.2, 'rtCritics': 52, 'rtAudience': 70}, # Invencível
    'b63': {'year': 2004, 'imdb': 8.1, 'rtCritics': 90, 'rtAudience': 90}, # Menina de Ouro
    'b64': {'year': 2003, 'imdb': 6.9, 'rtCritics': 36, 'rtAudience': 84}, # Meu Nome é Rádio
    'b65': {'year': 2007, 'imdb': 8.1, 'rtCritics': 83, 'rtAudience': 89}, # Na Natureza Selvagem
    'b66': {'year': 2019, 'imdb': 7.8, 'rtCritics': 95, 'rtAudience': 86}, # O Irlandês
    'b67': {'year': 2014, 'imdb': 7.4, 'rtCritics': 48, 'rtAudience': 72}, # O Juiz
    'b68': {'year': 2023, 'imdb': 7.5, 'rtCritics': 83, 'rtAudience': 98}, # O Pacto
    'b69': {'year': 1994, 'imdb': 8.5, 'rtCritics': 74, 'rtAudience': 95}, # O Profissional
    'b70': {'year': 2015, 'imdb': 8.0, 'rtCritics': 78, 'rtAudience': 84}, # O Regresso
    'b71': {'year': 2019, 'imdb': 7.3, 'rtCritics': 71, 'rtAudience': 84}, # O Rei
    'b72': {'year': 2021, 'imdb': 7.4, 'rtCritics': 85, 'rtAudience': 81}, # O Último Duelo
    'b73': {'year': 2002, 'imdb': 7.0, 'rtCritics': 74, 'rtAudience': 78}, # Outra Beleza Americana
    'b74': {'year': 2019, 'imdb': 8.5, 'rtCritics': 99, 'rtAudience': 95}, # Parasita
    'b75': {'year': 2008, 'imdb': 8.0, 'rtCritics': 91, 'rtAudience': 90}, # Quem Quer Ser um Milionário?
    'b76': {'year': 1996, 'imdb': 7.6, 'rtCritics': 74, 'rtAudience': 85}, # Sleepers: A Vingança Adormecida
    'b77': {'year': 2003, 'imdb': 7.9, 'rtCritics': 88, 'rtAudience': 89}, # Sobre Meninos e Lobos
    'b78': {'year': 2001, 'imdb': 7.7, 'rtCritics': 35, 'rtAudience': 87}, # Uma Lição de Amor
    'b79': {'year': 2000, 'imdb': 6.6, 'rtCritics': 21, 'rtAudience': 57}, # A Praia
    'b80': {'year': 2006, 'imdb': 6.9, 'rtCritics': 54, 'rtAudience': 72}, # Alpha Dog
    'b81': {'year': 2000, 'imdb': 7.3, 'rtCritics': 70, 'rtAudience': 77}, # Corpo Fechado
    'b82': {'year': 2005, 'imdb': 6.5, 'rtCritics': 75, 'rtAudience': 42}, # Guerra dos Mundos
    'b83': {'year': 2019, 'imdb': 6.6, 'rtCritics': 29, 'rtAudience': 79}, # Missão no Mar Vermelho
    'b84': {'year': 2006, 'imdb': 7.6, 'rtCritics': 86, 'rtAudience': 85}, # O Plano Perfeito
    'b85': {'year': 2005, 'imdb': 7.6, 'rtCritics': 61, 'rtAudience': 84}, # O Senhor das Armas
    'b86': {'year': 2002, 'imdb': 8.1, 'rtCritics': 96, 'rtAudience': 89}, # Prenda-me se For Capaz
    'b87': {'year': 2011, 'imdb': 7.4, 'rtCritics': 69, 'rtAudience': 74}, # Sem Limites
    'b88': {'year': 2016, 'imdb': 7.3, 'rtCritics': 61, 'rtAudience': 70}, # Snowden: Herói ou Vilão
    'b89': {'year': 2023, 'imdb': 7.7, 'rtCritics': 57, 'rtAudience': 99}, # Som da Liberdade
    'b90': {'year': 2015, 'imdb': 6.7, 'rtCritics': 91, 'rtAudience': 74}, # Turbo Kid
    'b91': {'year': 2007, 'imdb': 7.3, 'rtCritics': 81, 'rtAudience': 84}, # A Garota Ideal
    'b92': {'year': 2023, 'imdb': 6.7, 'rtCritics': 77, 'rtAudience': 78}, # Dèdi / Daddio
    'b93': {'year': 2020, 'imdb': 6.3, 'rtCritics': 78, 'rtAudience': 35}, # Eu Me Importo
    'b94': {'year': 2024, 'imdb': 6.7, 'rtCritics': 81, 'rtAudience': 70}, # Identidades em Jogo
    'b95': {'year': 2001, 'imdb': 5.7, 'rtCritics': 30, 'rtAudience': 55}, # Não é Mais um Besteirol Americano
    'b96': {'year': 2001, 'imdb': 6.4, 'rtCritics': 65, 'rtAudience': 58}, # Novocaine
    'b97': {'year': 2020, 'imdb': 7.4, 'rtCritics': 95, 'rtAudience': 89}, # Palm Springs
    'b98': {'year': 2011, 'imdb': 5.8, 'rtCritics': 33, 'rtAudience': 43}, # Passe Livre
    'b99': {'year': 2005, 'imdb': 7.1, 'rtCritics': 75, 'rtAudience': 70}, # Penetras Bons de Bico
    'b100': {'year': 2014, 'imdb': 8.1, 'rtCritics': 94, 'rtAudience': 92}, # Relatos Selvagens
    'b101': {'year': 2017, 'imdb': 6.8, 'rtCritics': 78, 'rtAudience': 75}, # Toc Toc
    'b102': {'year': 2022, 'imdb': 7.3, 'rtCritics': 72, 'rtAudience': 70}, # Triângulo da Tristeza

    # 4. WATCHED (47 items)
    'w1': {'year': 2019, 'imdb': 6.8, 'rtCritics': 79, 'rtAudience': 74}, # À Espreita do Mal
    'w2': {'year': 2010, 'imdb': 8.2, 'rtCritics': 69, 'rtAudience': 77}, # A Ilha do Medo
    'w3': {'year': 1993, 'imdb': 9.0, 'rtCritics': 98, 'rtAudience': 95}, # A Lista de Schindler
    'w4': {'year': 2010, 'imdb': 8.8, 'rtCritics': 87, 'rtAudience': 91}, # A Origem
    'w5': {'year': 2022, 'imdb': 7.8, 'rtCritics': 85, 'rtAudience': 87}, # Batman
    'w6': {'year': 2016, 'imdb': 7.1, 'rtCritics': 61, 'rtAudience': 69}, # Cães de Guerra
    'w7': {'year': 2016, 'imdb': 7.8, 'rtCritics': 83, 'rtAudience': 85}, # Capitão Fantástico
    'w8': {'year': 2019, 'imdb': 6.9, 'rtCritics': 89, 'rtAudience': 78}, # Casamento Sangrento
    'w9': {'year': 2002, 'imdb': 8.6, 'rtCritics': 91, 'rtAudience': 97}, # Cidade de Deus
    'w10': {'year': 2019, 'imdb': 8.4, 'rtCritics': 68, 'rtAudience': 89}, # Coringa
    'w11': {'year': 2012, 'imdb': 8.5, 'rtCritics': 87, 'rtAudience': 92}, # Django Livre
    'w12': {'year': 2019, 'imdb': 7.3, 'rtCritics': 78, 'rtAudience': 89}, # Doutor Sono
    'w13': {'year': 2020, 'imdb': 7.7, 'rtCritics': 92, 'rtAudience': 90}, # Druk - Mais uma Rodada
    'w14': {'year': 2019, 'imdb': 7.6, 'rtCritics': 85, 'rtAudience': 70}, # Era Uma Vez em... Hollywood
    'w15': {'year': 1994, 'imdb': 8.8, 'rtCritics': 71, 'rtAudience': 95}, # Forrest Gump
    'w16': {'year': 2021, 'imdb': 7.1, 'rtCritics': 80, 'rtAudience': 94}, # Free Guy
    'w17': {'year': 2022, 'imdb': 7.9, 'rtCritics': 95, 'rtAudience': 94}, # Gato de Botas 2
    'w18': {'year': 2018, 'imdb': 8.2, 'rtCritics': 77, 'rtAudience': 91}, # Green Book
    'w19': {'year': 2018, 'imdb': 7.3, 'rtCritics': 90, 'rtAudience': 71}, # Hereditário
    'w20': {'year': 2016, 'imdb': 6.6, 'rtCritics': 91, 'rtAudience': 73}, # Hush - A Morte Ouve
    'w21': {'year': 2014, 'imdb': 8.7, 'rtCritics': 73, 'rtAudience': 86}, # Interestelar
    'w22': {'year': 2018, 'imdb': 7.4, 'rtCritics': 72, 'rtAudience': 77}, # Jogador Nº 1
    'w23': {'year': 2022, 'imdb': 7.8, 'rtCritics': 90, 'rtAudience': 90}, # Nada de Novo no Front
    'w24': {'year': 2014, 'imdb': 7.8, 'rtCritics': 95, 'rtAudience': 86}, # O Abutre
    'w25': {'year': 2002, 'imdb': 7.1, 'rtCritics': 71, 'rtAudience': 48}, # O Chamado 1 e 2
    'w26': {'year': 2017, 'imdb': 5.3, 'rtCritics': 54, 'rtAudience': 37}, # O Diabo e o Padre Amorth
    'w27': {'year': 2014, 'imdb': 8.1, 'rtCritics': 92, 'rtAudience': 86}, # O Grande Hotel Budapeste
    'w28': {'year': 2010, 'imdb': 6.8, 'rtCritics': 47, 'rtAudience': 64}, # O Livro de Eli
    'w29': {'year': 2013, 'imdb': 8.2, 'rtCritics': 80, 'rtAudience': 83}, # O Lobo de Wall Street
    'w30': {'year': 2019, 'imdb': 7.6, 'rtCritics': 86, 'rtAudience': 87}, # O Menino que Descobriu o Vento
    'w31': {'year': 2022, 'imdb': 7.2, 'rtCritics': 88, 'rtAudience': 76}, # O Menu
    'w32': {'year': 2002, 'imdb': 8.5, 'rtCritics': 95, 'rtAudience': 96}, # O Pianista
    'w33': {'year': 2022, 'imdb': 7.5, 'rtCritics': 70, 'rtAudience': 97}, # O Pior Vizinho do Mundo
    'w34': {'year': 1972, 'imdb': 9.2, 'rtCritics': 97, 'rtAudience': 98}, # O Poderoso Chefão 1
    'w35': {'year': 2014, 'imdb': 7.4, 'rtCritics': 84, 'rtAudience': 75}, # O Predestinado
    'w36': {'year': 1998, 'imdb': 8.2, 'rtCritics': 95, 'rtAudience': 89}, # O Show de Truman
    'w37': {'year': 2022, 'imdb': 7.7, 'rtCritics': 96, 'rtAudience': 75}, # Os Banshees de Inisherin
    'w38': {'year': 2022, 'imdb': 7.5, 'rtCritics': 92, 'rtAudience': 82}, # Os Fabelmans
    'w39': {'year': 2015, 'imdb': 7.8, 'rtCritics': 74, 'rtAudience': 76}, # Os Oito Odiados
    'w40': {'year': 2013, 'imdb': 8.2, 'rtCritics': 81, 'rtAudience': 87}, # Os Suspeitos
    'w41': {'year': 2013, 'imdb': 7.8, 'rtCritics': 70, 'rtAudience': 81}, # Questão de Tempo
    'w42': {'year': 2008, 'imdb': 7.6, 'rtCritics': 26, 'rtAudience': 75}, # Sete Vidas
    'w43': {'year': 2015, 'imdb': 8.1, 'rtCritics': 97, 'rtAudience': 93}, # Spotlight - Segredos Revelados
    'w44': {'year': 2007, 'imdb': 7.6, 'rtCritics': 88, 'rtAudience': 87}, # Superbad - É Hoje
    'w45': {'year': 2015, 'imdb': 7.1, 'rtCritics': 58, 'rtAudience': 74}, # Um Homem Entre Gigantes
    'w46': {'year': 2022, 'imdb': 7.2, 'rtCritics': 34, 'rtAudience': 96}, # Um Lugar Bem Longe Daqui
    'w47': {'year': 2014, 'imdb': 8.5, 'rtCritics': 94, 'rtAudience': 94}, # Whiplash

    # 5. SERIES & DOCS (14 items)
    's1': {'year': 2008, 'imdb': 9.5, 'rtCritics': 96, 'rtAudience': 97}, # Breaking Bad
    's2': {'year': 2010, 'imdb': 8.3, 'rtCritics': 82, 'rtAudience': 91}, # Blue Mountain State
    's3': {'year': 2019, 'imdb': 9.3, 'rtCritics': 95, 'rtAudience': 98}, # Chernobyl
    's4': {'year': 2018, 'imdb': 8.1, 'rtCritics': 97, 'rtAudience': 96}, # Free Solo
    's5': {'year': 2005, 'imdb': 8.3, 'rtCritics': 84, 'rtAudience': 82}, # How I Met Your Mother
    's6': {'year': 2023, 'imdb': 8.2, 'rtCritics': 82, 'rtAudience': 95}, # Na Mira do Júri
    's7': {'year': 2021, 'imdb': 8.0, 'rtCritics': 95, 'rtAudience': 84}, # Round 6
    's8': {'year': 2018, 'imdb': 8.9, 'rtCritics': 95, 'rtAudience': 91}, # Succession
    's9': {'year': 2007, 'imdb': 8.2, 'rtCritics': 81, 'rtAudience': 82}, # The Big Bang Theory
    's10': {'year': 2019, 'imdb': 8.7, 'rtCritics': 93, 'rtAudience': 84}, # The Boys + Gen V
    's11': {'year': 2005, 'imdb': 9.0, 'rtCritics': 81, 'rtAudience': 89}, # The Office
    's12': {'year': 2019, 'imdb': 8.0, 'rtCritics': 80, 'rtAudience': 75}, # The Witcher
    's13': {'year': 2019, 'imdb': 8.6, 'rtCritics': 97, 'rtAudience': 92}, # What We Do in the Shadows
    's14': {'year': 2011, 'imdb': 8.7, 'rtCritics': 83, 'rtAudience': 81}, # Black Mirror
}

print("Metadata loaded successfully. Total entries:", len(METADATA))
