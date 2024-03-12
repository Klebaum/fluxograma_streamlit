import json
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
# Carregar o JSON
with open("data/marvel.json", "r") as f:
    data = json.load(f)

nodes = []
edges = []

# nó raiz
root_node = Node(id="Marvel", label="Marvel", image='http://marvel-force-chart.surge.sh/marvel_force_chart_img/marvel.png')
nodes.append(root_node)

for category in data["children"]:
    category_node = Node(id=category["name"], label=category["name"])
    
    nodes.append(category_node)

    # Adiciona a aresta da raiz para a categoria
    edge = Edge(source=root_node.id, target=category_node.id)
    edges.append(edge)

    for character in category["children"]:
        character_node = Node(id=character["hero"], 
                              label=character["hero"], 
                              shape="circularImage", 
                              image=character["img"])  
        nodes.append(character_node)

        # Adiciona a aresta da categoria para o herói/vilão
        edge = Edge(source=category_node.id, target=character_node.id)
        edges.append(edge)

# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# 2. If your done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")

st.title('Fluxograma de teste Marvel')
agraph(nodes=nodes, edges=edges, config=config)