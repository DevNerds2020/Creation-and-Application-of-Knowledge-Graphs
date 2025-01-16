import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph

def visualize_rdf_graph(rdf_file, summarize=False):
    """
    This function takes an RDF file (in Turtle format) as input, parses it, and visualizes the knowledge graph.
    If summarize is True, the function will display only the last part of the URL (after the last '/').

    Parameters:
    rdf_file (str): Path to the RDF file in Turtle format.
    summarize (bool): If True, display only the last part of the URL for subject and object.

    Returns:
    None
    """
    # Load the RDF graph using rdflib
    g = Graph()
    g.parse(rdf_file, format="ttl")

    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Add RDF triples as edges in the graph (subject-predicate-object)
    for s, p, o in g:
        # Extract the last part of the URI (if summarize is True)
        if summarize:
            s = str(s).split("/")[-1]  # Take the part after the last "/"
            p = str(p).split("/")[-1]  # Take the part after the last "/"
            o = str(o).split("/")[-1]  # Take the part after the last "/"

            # if the characters are more than 10, then take the first 10 characters
            if len(s) > 10:
                s = s[:10] + "..."
            if len(p) > 10:
                p = p[:10] + "..."
            if len(o) > 10:
                o = o[:10] + "..."
        else:
            s = str(s)  # Keep full URI
            p = str(p)  # Keep full URI
            o = str(o)  # Keep full URI

        # Add subject and object as nodes
        G.add_node(s, label=s)
        G.add_node(o, label=o)

        # Add the predicate as an edge label
        G.add_edge(s, o, label=str(p))

    # Generate a layout for the graph
    pos = nx.spring_layout(G, seed=42)  # Set a seed for consistent layout
    plt.figure(figsize=(12, 12))

    # Draw the graph with labels
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Display the graph
    plt.title("RDF Knowledge Graph")
    plt.show()