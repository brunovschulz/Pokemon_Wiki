import pymysql

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='123', database='pokemonbd')


#QUERRY PAG POKEDEX

def qr_pokedex():
    return (
        "select numero_pokedex, nome from pokemon order by numero_pokedex"
    )


#QUERRYS PARA POKEMON

def qr_poke():
    return (
        "select * from (((pokemon natural join ovo) natural join treinamento) natural join status_combate) where numero_pokedex = %s"
    )

#FALTA COLOCAR ESSA CONSULTA NA DOCUMENTAÇÃO
def qr_el():
    return (
        "select * from elemento where ID_elemento = %s or ID_elemento = %s"
    )

def qr_evol():
    return (
        """
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
    )

def qr_mult():
    return (
        "select nome_elemento, multiplicador from tem_efetividade natural join elemento where numero_pokedex = %s"
    )

def qr_hab():
    return (
        "select nome_habilidade, habilidade_secreta from possui_habilidade natural join habilidade where numero_pokedex = %s"
    )


#QUERRYS PARA OVOS

#FALTA ALTERAR ESSA CONSULTA NA DOCUMENTAÇÃO
def qr_ovos():
    return (
        """
        select * from ((select ovo_tipo1 as tipo_ovo from ovo) union 
        (select ovo_tipo2 as tipo_ovo from ovo where ovo_tipo2 is not NULL)) as tabela_tipo_ovo order by tipo_ovo
        """
    )

def qr_ovo_poke():
    return(
        """
        select numero_pokedex, nome, outro_tipo from 
        ((select numero_pokedex, nome, ovo_tipo2 as outro_tipo from Pokemon natural join ovo where ovo_tipo1 = %s) 
        union (select numero_pokedex, nome, ovo_tipo1 as outro_tipo from Pokemon natural join ovo where ovo_tipo2 = %s)) as tabela_ovo
        """
    )

#QUERRYS PARA TOP POKÉMONS
#PRECISA ALTERAR NA DOCUMENTAÇÃO
def qr_lendario():
    return (
    """
    select numero_pokedex, nome, raridade from Pokemon where raridade != 'Normal';
    """
    )

#PRECISA ALTERAR NA DOCUMENTAÇÃO
def qr_topEl():
    return (
    """
    select numero_pokedex, nome, nome_elemento, total_pontos 
    from (Pokemon natural join Status_Combate) join Elemento on ID_elemento_primario = ID_elemento or ID_elemento_secundario = ID_elemento 
    where (nome_elemento, total_pontos) in 
    (select nome_elemento, MAX(total_pontos) 
    from (Pokemon natural join Status_Combate) join Elemento on ID_elemento_primario = ID_elemento or ID_elemento_secundario  = ID_elemento 
    group by nome_elemento); 
    """
    )

#QUERRY PARA ABA HABILIDADES SECRETAS

def qr_habSec():
    return (
    """
    select nome, nome_habilidade 
    from Pokemon left join (select numero_pokedex, nome_habilidade from possui_habilidade natural join habilidade where habilidade_secreta = 1)
     as poke_hab_sec on Pokemon.numero_pokedex = poke_hab_sec.numero_pokedex;
    """
    )
