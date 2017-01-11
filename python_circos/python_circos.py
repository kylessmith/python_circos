import numpy as np
import matplotlib.pyplot as plt
from genome_plot import CircosObject
import argparse

def parse_nodes(nodes_fn):
    nodes = []
    for line in open(nodes_fn,"r"):
        fields = line.strip().split("\t")
        name = fields[0]
        length = float(fields[1])
        
        try:
            color = fields[2]
        except IndexError:
            color = None
        nodes.append((name, length, color))
    
    return nodes


def parse_edges(edges_fn):
    edges = []
    for line in open(edges_fn,"r"):
        fields = line.strip().split("\t")
        node1 = fields[0]
        position1 = float(fields[1])
        node2 = fields[2]
        position2 = float(fields[3])
        color = fields[4]
        weight = fields[5]
        
        edges.append((node1, position1, node2, position2, color, weight))
        
    return edges
    
    
def main(nodes_fn, edges_fn, out_fn, radius):
    nodes = parse_nodes(nodes_fn)
    edges = parse_edges(edges_fn)
    
    c = CircosObject(nodes, edges, radius)

    c.draw()
    c.fig.savefig(out_fn, transparent=True)

    
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('--nodes', help='nodes file name', required=True)
    parser.add_argument('--edges', help='edges file name', required=True)
    parser.add_argument('--o', help='output file name', required=True)
    parser.add_argument('--radius', help='radius to use', type=int, default=10)
    args=parser.parse_args()
    
    nodes_fn = args.nodes
    edges_fn = args.edges
    out_fn = args.o
    radius = args.radius
    
    main(nodes_fn, edges_fn, out_fn, radius)