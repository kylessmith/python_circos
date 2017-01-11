from . import main
import argparse

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

