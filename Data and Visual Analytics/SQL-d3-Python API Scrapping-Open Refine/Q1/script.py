import http.client
import json
import time
import timeit
import sys
import collections
from pygexf.gexf import *
import urllib
import urllib.request



#
# implement your data retrieval code here
#

#headers = {
#  "Accept": "application/json"
#}

#key = "2909b95f0537f1f20c8e38853f661175"
key = str(sys.argv)[15:-2]
r = urllib.request.urlopen("https://rebrickable.com/api/v3/lego/sets/?key="+key+"&page_size=300&ordering=-num_parts").read()
data = json.loads(r.decode())
sets_sorted_300 = data['results']
a_sets = []

for set in sets_sorted_300:
    temp_dict = {key:set[key] for key in ['set_num', 'name']}
    a_sets.append(temp_dict)


# complete auto grader functions for Q1.1.b,d
def min_parts():
    """
    Returns an integer value
    """
    # you must replace this with your own value
    return 1094

def lego_sets():
    """
    return a list of lego sets.
    this may be a list of any type of values
    but each value should represent one set
    [set_names for set_names in ]

    e.g.,
    biggest_lego_sets = lego_sets()
    print(len(biggest_lego_sets))
    > 280
    e.g., len(my_sets)
    """
    #[a_sets[i]['name'] for i in range(len(a_sets))]
    # you must replace this line and return your own list
    return [a_sets[i]['set_num'] for i in range(len(a_sets))]

lego_sets_1 = lego_sets()
num_part_dict = {}
n = 0
for sets in lego_sets_1:
    print(str(sets) + " "+ str(n))
    n = n + 1
    l = urllib.request.urlopen("https://rebrickable.com/api/v3/lego/sets/" + sets + "/parts/?key="+key+"&page_size=1000").read()
    parts = json.loads(l.decode())["results"]
    parts_dicts = sorted(parts, key = lambda i:i['quantity'],reverse=True)[0:20]
    parts_dicts_revised = []
    for dicts in parts_dicts:
        temp_dict = {key:dicts[key] for key in ['quantity']}
        temp_dict['color'] = dicts['color']['rgb']
        for x in ['name', 'part_num'] : temp_dict[x]=dicts['part'][x]
        temp_dict['id'] = temp_dict['part_num'] + "_" + temp_dict['color']
#        temp_dict = {key:temp_dict['part'][key] for key in ['name', 'part_num']}
        parts_dicts_revised.append(temp_dict)
    num_part_dict[sets]=parts_dicts_revised


def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     return list(int(hex[i:i+2], 16) for i in (0, 2, 4))

def gexf_graph():
    """
    return the completed Gexf graph object
    """
    # you must replace these lines and supply your own graph
    gexf = Gexf("Rishi", "Lego Land 2")
    graph = gexf.addGraph("undirected", "static", "I'm sleepy")
    graph.addNodeAttribute("type", type='string', force_id = "type")
    graph_id = 0
    for sets in a_sets:
        node = graph.addNode(sets['set_num'],sets['name'], r='0',b='0',g='0')
        node.addAttribute("type", "set")
        for parts in num_part_dict[sets['set_num']]:
            if (not(graph.nodeExists(parts['id']))):
                rgb_list = hex_to_rgb(parts['color'])
                node = graph.addNode(parts['id'],parts['name'], r=str(rgb_list[0]),b=str(rgb_list[2]),g=str(rgb_list[1]))
                node.addAttribute("type", "part")
            graph.addEdge(graph_id,sets['set_num'],parts['id'],weight=parts['quantity'])
            graph_id = graph_id + 1
    
    output_file=open("bricks_graph.gexf","wb")
    gexf.write(output_file)
    
    return gexf.graphs[0]

# complete auto-grader functions for Q1.2.d

def avg_node_degree():
    """
    hardcode and return the average node degree
    (run the function called “Average Degree”) within Gephi
    """
    # you must replace this value with the avg node degree
    return 5.577

def graph_diameter():
    """
    hardcode and return the diameter of the graph
    (run the function called “Network Diameter”) within Gephi
    """
    # you must replace this value with the graph diameter
    return 8

def avg_path_length():
    """
    hardcode and return the average path length
    (run the function called “Avg. Path Length”) within Gephi
    :return:
    """
    # you must replace this value with the avg path length
    return 4.395