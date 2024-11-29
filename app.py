from flask import Flask, render_template
import pymysql
from querrys import *

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
    print(multiplicadores)

    conn.close()

    if not pokemon:
        return "Pokémon não encontrado", 404

    #17-23 -> atributos de combate
    return render_template('pokemon.html', 
    pokemon=pokemon, elementos=elementos, evolucoes=evolucoes, habilidades = habilidades, 
    multiplicadores = multiplicadores, atrib = atrib, ovos = ovos)

@app.route('/pokedex') #troquei rota com pokedex para facilitar
def home():
    return render_template('home.html')

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
    return render_template('top_pokemons.html') 

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

