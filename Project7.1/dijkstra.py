import sys
import json
import math  # If you want to use math.inf for infinity

def ipv4_to_value(ipv4_addr):

    decs = ipv4_addr.split(".")

    string = ''

    for i in decs:
        string += format(int(i), '08b')

    return string


def get_subnet_mask_value(slash):
    n = slash.find("/")

    mask = int(slash[n+1:])

    string = ''

    for i in range(32):
        if i < mask:
            string += '1'
        else:
            string += '0'
    
    return string

def ips_same_subnet(ip1, ip2, slash):
    mask = get_subnet_mask_value(slash)

    ip1 = ipv4_to_value(ip1)
    ip2 = ipv4_to_value(ip2)

    for i in range(32):
        if mask[i] == '1':
            if ip1[i] != ip2[i]:
                return False

    return True

def find_router_for_ip(routers, ip):
    #for each router, if ips_same_subnet is true, return the router
    for i in routers:
        if ips_same_subnet(i, ip, routers[i]['netmask']):
            return i
    
    return None

def minQ(q, d):
    min = math.inf
    minQ = None

    for i in q:
        if d[i] < min:
            min = d[i]
            minQ = i

    return minQ

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.

    1  function Dijkstra(Graph, source):
    2
    3      for each vertex v in Graph.Vertices:
    4          dist[v] ← INFINITY
    5          prev[v] ← UNDEFINED
    6          add v to Q
    7      dist[source] ← 0
    8
    9      while Q is not empty:
    10          u ← vertex in Q with min dist[u]
    11          remove u from Q
    12
    13          for each connection v of u still in Q:
    14              alt ← dist[u] + Graph.Edges(u, v)
    15              if alt < dist[v]:
    16                  dist[v] ← alt
    17                  prev[v] ← u
    18
    19      return dist[], prev[]

    """
    dist = {}
    prev = {}
    q = []


    for v in routers:
        dist[v] = math.inf
        prev[v] = None
        q.append(v)

    sr = find_router_for_ip(routers, src_ip)
    
    dist[sr] = 0

    i = 0

    while q:
        i += 1
        
        u = minQ(q, dist)     

        r = find_router_for_ip(routers, u)

        q.remove(r)

        for v in routers[r]['connections']:

            alt = dist[r] + routers[r]['connections'][v]['ad']

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = r

    
    c = find_router_for_ip(routers, dest_ip)

    path = []

    while c != sr:
        path.append(c)
        c = prev[c]

    if path:
        path.append(sr)

    return list(reversed(path))

    

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
