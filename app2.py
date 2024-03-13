import json
import streamlit as st
st.set_page_config(layout="wide")
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
# Carregar o JSON
with open("data/todos.json", "r") as f:
    data = json.load(f)

nodes = []
edges = []

# nó raiz
root_node = Node(id="Comic", label="Comic")
nodes.append(root_node)
i = 1
# categorias (Marvel e DC)
for universe in data["children"]:
    universe_node = Node(id=universe["name"], label=universe["name"], shape="circle")
    nodes.append(universe_node)

    # aresta da raiz para Marvel ou DC
    edge = Edge(source=root_node.id, target=universe_node.id)
    edges.append(edge)

    # personagens heróis, vilões e times dentro da categoria
    for category in universe["children"]:
        i+=1
        category_node = Node(id=f'{category["name"]}_category_{universe["name"]}', label=category["name"], shape="circle")
        nodes.append(category_node)

        # aresta da categoria para o personagem
        edge = Edge(source=universe_node.id, target=category_node.id)
        edges.append(edge)

        # heróis/vilões dentro da categoria
        for character in category["children"]:
            character_node = Node(id=character.get("hero", character.get("villain", character.get("team"))), 
                                  label=character.get("hero", character.get("villain", character.get("team"))), 
                                  shape="circularImage", 
                                  image=character["img"])
            nodes.append(character_node)
            
            character_edge = Edge(source=category_node.id, target=character_node.id)
            edges.append(character_edge)

# Construir a configuração
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# Salvar a configuração em um arquivo JSON
config.save("config.json")

# Renderizar o grafo
agraph(nodes, edges, config)