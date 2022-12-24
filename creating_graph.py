import networkx as nx
import json
import numpy as np
import pickle
from multiprocessing import Pool
import itertools
from time import sleep

data = {}
G = nx.Graph()

def make_edges(start):
    global data, G
    res = []
    for end in set(data.keys()) - {start}:
        inter = np.intersect1d(data[start].items(), data[end].items())
        if len(inter) > 0:
            res.append((start, end))
            for el in inter[0]:
                if el[1] != []:
                    write_connection(start, end, el)
    return res

def write_connection(start, end, value):
    global hnd_connections
    hnd_connections.write(f'{start}\t{end}\t{value}\n')

def main():
    global data, G, hnd_connections
    with open('out/out.json', 'r') as f:
        data = f.read()
    data = json.loads(data)

    G.add_nodes_from(data.keys())

    with open('out/connections.csv', 'w') as f:
        f.write(f'node1\tnode2\tvalue\n')
    
    hnd_connections = open('out/connections.csv', 'a')

    for el in data.keys():
        G.add_edges_from(make_edges(el))

    # with Pool(8) as p:
    #     out_arr = p.map(make_edges, data.keys())

    # while len(out_arr) < len(data.keys()):
    #     pass

    # sleep(15)
    
    # G.add_edges_from(list(itertools.chain(*out_arr)))

    print(G.number_of_edges(), G.number_of_nodes())
    with open('out/graph.pickle', 'wb') as f:
        pickle.dump(G, f)
    
    hnd_connections.close()


if __name__ == '__main__':
    main()
