from flask import Flask, render_template
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='123', database='pokemonbd')

@app.route('/pokemon/<int:pokemon_id>')
def pokemon_page(pokemon_id):

    querry_evol = """
    WITH RECURSIVE EvolucaoPokemon AS (
    SELECT numero_pokedex, nome, subevolucao
    FROM pokemon
    WHERE nome = %s

    UNION ALL

    SELECT p.numero_pokedex, p.nome, p.subevolucao
    FROM pokemon p
    INNER JOIN EvolucaoPokemon ep ON p.subevolucao = ep.nome
    ) SELECT * FROM EvolucaoPokemon
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("select * from (((pokemon natural join ovo) natural join treinamento) natural join status_combate) where numero_pokedex = %s", (pokemon_id,))
    pokemon = cursor.fetchone()

    
    cursor.execute("select * from elemento where ID_elemento = %s or ID_elemento = %s", (pokemon[7], pokemon[8]))
    elementos = cursor.fetchall()


    cursor.execute(querry_evol, (pokemon[1]))
    evolucoes = cursor.fetchall()
    evolucoes = list(evolucoes) #era tupla
    evolucoes.pop(0) #retirando o próprio pokémon

    print(pokemon)
    print(elementos)
    print(evolucoes)
    conn.close()
    if not pokemon:
        return "Pokémon não encontrado", 404
    return render_template('pokemon.html', pokemon=pokemon, elementos=elementos, evolucoes=evolucoes)

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT numero_pokedex, nome FROM pokemon order by numero_pokedex")
    pokemons = cursor.fetchall()
    conn.close()
    return render_template('home.html', pokemons=pokemons)

