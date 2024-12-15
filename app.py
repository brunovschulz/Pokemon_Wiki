from flask import Flask, render_template, request, jsonify
import pymysql
from queries import *

app = Flask(__name__)

@app.route('/pokemon/<int:pokemon_id>')
def pokemon_page(pokemon_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    #pokemon - informacoes gerais
    cursor.execute(qr_poke(), (pokemon_id))
    pokemon = cursor.fetchone()

    #ovos
    ovos = [pokemon[10]]
    if pokemon[11]:
        ovos.append(pokemon[11])

    #elementos
    cursor.execute(qr_el(), (pokemon[7], pokemon[8]))
    elementos = cursor.fetchall()

    #habilidades
    cursor.execute(qr_hab(), (pokemon_id))
    habilidades = cursor.fetchall()
    habilidades = list(habilidades)
    habilidades_secretas = []

    #separando habilidades normais das secretas
    for habilidade in habilidades:
        if int(habilidade[1]) == 1:
            habilidades_secretas.append(habilidade)
            habilidades.remove(habilidade)


    #multiplicadores
    cursor.execute(qr_mult(), (pokemon_id))
    multiplicadores = cursor.fetchall()

    #evolucoes
    cursor.execute(qr_evol(), (pokemon[1]))
    evolucoes = cursor.fetchall()
    evolucoes = list(evolucoes) #era tupla
    evolucoes.pop(0) #retirando o próprio pokémon

    #lista de atributos
    atrib = [
        ("HP", pokemon[18]),
        ("Ataque", pokemon[19]),
        ("Defesa", pokemon[20]),
        ("Especial Ataque", pokemon[21]),
        ("Especial Defesa", pokemon[22]),
        ("Velocidade", pokemon[23]),
        ("Total de Pontos", pokemon[17]),
    ]

    #debug
    print(pokemon)
    print(elementos)
    print(evolucoes)
    print(habilidades)
    print(habilidades_secretas)
    print(multiplicadores)

    conn.close()

    if not pokemon:
        return "Pokémon não encontrado", 404

    #17-23 -> atributos de combate
    return render_template('pokemon.html', 
    pokemon=pokemon, elementos=elementos, evolucoes=evolucoes, habilidades = habilidades, 
    habilidades_secretas = habilidades_secretas, multiplicadores = multiplicadores, atrib = atrib, ovos = ovos)

#@app.route('/pokedex') #troquei rota com pokedex para facilitar
#def home():
#    return render_template('home.html')

@app.route('/')
def pokedex():
    conn = get_db_connection()
    cursor = conn.cursor()

    #lista pokémon
    cursor.execute(qr_pokedex())
    pokemons = cursor.fetchall()
    conn.close()
    return render_template('pokedex.html', pokemons=pokemons)

@app.route('/top-pokemons')
def top_pokemons():
    conn = get_db_connection()
    cursor = conn.cursor()

    #lendarios
    cursor.execute(qr_lendario())
    lendarios = cursor.fetchall()

    #top Pokémon por elemento
    cursor.execute(qr_topEl())
    pokeTopEle = cursor.fetchall()

    conn.close()

    print(lendarios)
    print(pokeTopEle)

    return render_template('top_pokemons.html', lendarios= lendarios,
    pokeTopEle = pokeTopEle) 

#lista os tipos de ovo
@app.route('/ovos')
def ovos():
    conn = get_db_connection()
    cursor = conn.cursor()

    #lista de tipos de ovo
    cursor.execute(qr_ovos())
    ovos = cursor.fetchall()

    #print(ovos)
    conn.close()
    return render_template('tipos_ovo.html', ovos = ovos) 

#lista os pokémons de um tipo de ovo
@app.route('/ovos/<string:tipo_ovo>')
def ovo(tipo_ovo):
    conn = get_db_connection()
    cursor = conn.cursor()

    #pokemons do tipo_ovo
    cursor.execute(qr_ovo_poke(), (tipo_ovo, tipo_ovo))
    pokemon_ovo = cursor.fetchall()

    print(pokemon_ovo)
    conn.close()
    return render_template('ovo.html', pokemon_ovo = pokemon_ovo, nome_ovo = tipo_ovo) 

@app.route('/habilidades_secretas')
def hab_sec():
    conn = get_db_connection()
    cursor = conn.cursor()

    #Pokémons e suas habilidades secretas
    cursor.execute(qr_habSec())
    habSecPoke = cursor.fetchall()

    print(habSecPoke)

    conn.close()
    return render_template('hab_sec.html', habSecPoke = habSecPoke)

#consulta dinâmica
@app.route('/get_attribute', methods=['GET'])
def get_attribute():
    # Obtém o parâmetro 'generation' da solicitação
    attribute = request.args.get('attribute')

    print(attribute)

    # Conexão com o banco de dados
    connection = get_db_connection()
    cursor = connection.cursor()

    # Consulta dinâmica
    query = f"""
    select numero_pokedex, nome, {attribute}, "{attribute}" from status_combate natural join pokemon where {attribute} = (select max({attribute}) from status_combate);
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print(results)

    # Fecha conexão
    cursor.close()
    connection.close()

    # Converte resultados para JSON

    pokemons = []

    for r in results:
        aux = ""
        if r[3] == 'vida':
            aux = 'Hp'
        elif r[3] == 'ataque':
            aux = 'Ataque'
        elif r[3] == 'defesa':
            aux = 'Defesa'
        elif r[3] == 'esp_ataque':
            aux = 'Ataque Especial'
        elif r[3] == 'esp_defesa':
            aux = 'Defesa Especial'
        elif r[3] == 'velocidade':
            aux = 'Velocidade'
        else:
            aux = 'Pontuação Total'
        pokemons.append({'id': r[0], 'name': r[1], 'attribute': r[2], 'att_name': aux})

    return jsonify(pokemons)

