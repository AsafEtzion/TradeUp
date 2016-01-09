import networkx as nx
import csv


# parses the csv file and returns the data which is a list of lists
def parse_data(csv_file):
    with open(csv_file) as f:
        csv_f = csv.reader(f)

        data = []

        for row in csv_f:
            item = []
            for col in row:
                item.append(col)
            data.append(item)

    return data


# calculates the weight for the inputted edge.
def calc_weight(G, a, b):
    if G.node[a]["Country"] == G.node[b]["Country"]:
        if G.node[a]["State"] == G.node[b]["State"]:
            if G.node[a]["City"] == G.node[b]["City"]:
                return 1
            else:
                return 2
        else:
            return 4
    else:
        return 9


# adds vertices from the data to the graph
def add_vertices(G, data):
    for i in range(len(data)):
        G.add_node(int(data[i][0]), Country=data[i][1], State=data[i][2],
                   City=data[i][3], Name=data[i][4], Offering=data[i][5],
                   #OfferingCategory=data[i][6] ,
                   Seeking=data[i][6],
                   #SeekingCategory=data[i][8],
                   URL=data[i][7])


# adds edges from the data to the graph
def add_edges(G):
    for offering_node in G.node:
        for seeking_node in G.node:
            if (offering_node != seeking_node) and (
                        G.node[offering_node]['Offering'] in G.node[seeking_node]['Seeking']):
                G.add_edge(offering_node, seeking_node, weight=calc_weight(G, offering_node, seeking_node))


# def category_heuristic(a, b):
#     if G.node[a]["OfferingCategory"] == G.node[b]["OfferingCategory"]:
#         return 1
#     else:
#         return 3

# creates two lists seekingList, offeringList for checking if an item exists in the graph
def create_items_lists(data):
    seekingList = []
    offeringList = []
    for i in range(len(data)):
        offeringList.append(data[i][5])
        seekingList.append(data[i][6])
    return seekingList, offeringList


# runs the parse method and lists method. then creates the graph
def parse_and_init(csv_file):
    data = parse_data(csv_file)

    seekingList, offeringList = create_items_lists(data)

    G = nx.DiGraph()
    add_vertices(G, data)
    add_edges(G)

    return G, seekingList, offeringList

def find_index_matches(word, lst):
    indexes = []
    for i in range(len(lst)):
        if word == lst[i]:
            indexes.append(i)
    return indexes

# first checks if the items exists and then searches for the shortest path
def search_match(graph, seekingList, offeringList, seeking_product, offering_product):
    seekingIdxOccurrence = find_index_matches(seeking_product, seekingList)
    if len(seekingIdxOccurrence) == 0:
        return "noSeek"

    offeringIdxOccurrence = find_index_matches(offering_product, offeringList)
    if len(offeringIdxOccurrence) == 0:
        return "noHave"

    try:
        path = nx.astar_path(graph, seekingIdxOccurrence[0], offeringIdxOccurrence[0])  # TODO add more A* iterations
        items_list = []
        url_list = []
        for node in path:
            items_list.append(graph.node[node]["Offering"])
            url_list.append(graph.node[node]["URL"])
        return {"items": items_list, "link": url_list}
    except nx.NetworkXNoPath:
        return "noPath"


# G, seekingList, offeringList = parse_and_init('Products List for demo.csv')

# nx.write_graphml(G, "plot1.graphml")

# print(nx.astar_path(G, 6, 2, category_heuristic))