import glob, os, re, json, shutil
from collections import defaultdict
from graphviz import Digraph

pattern = re.compile(r'Et0/[0-4]$')   # local interfaces to include
files = sorted(glob.glob("./tmp/*.txt"))

output_dir = "./output"
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

def load_lines(file):
    with open(file) as f:
        text = f.read()
    return text.splitlines()

def parse_lldp_output(file):
    # Return (device_name, [neighbor, ...]) for one file.
    base = os.path.splitext(os.path.basename(file))[0]
    device = re.sub(r'_lldp_output$', '', base, flags=re.IGNORECASE)

    neighbors = []
    in_table = False
    for line in load_lines(file):
        line = line.rstrip()
        if line.startswith("Device ID"):
            in_table = True
            continue
        if not in_table or not line.strip():
            continue
        if line.startswith("Total entries"):
            break
        parts = line.split()
        if len(parts) < 4:
            continue
        remote = parts[0].split(".")[0]      # SW2.lab.test -> SW2
        local_intf = parts[1]
        if pattern.match(local_intf) and remote not in neighbors:
            neighbors.append(remote)
    return device, neighbors

results = defaultdict(list)
for file in files:
    device, neighbors = parse_lldp_output(file)
    results[device].extend(n for n in neighbors if n not in results[device])

known = set(results)

def canonical(name):
    # Map a short neighbor name (r5) onto the full device name (r5-tor).
    if name in known:
        return name
    matches = [d for d in known if d.split("-")[0].lower() == name.lower()]
    return matches[0] if len(matches) == 1 else name

def is_switch(name):
    return bool(re.match(r'(sw|switch)', name, re.IGNORECASE))

my_graph = Digraph(comment="Automatic Topology Diagram", engine="dot")

edges = set()
nodes = set()
for device, neighbors in results.items():
    print(f"device: {device}")
    nodes.add(device)
    for n in neighbors:
        n = canonical(n)
        nodes.add(n)
        edges.add(tuple(sorted((device, n))))
        print(f"neighbors: {n}")

for n in sorted(nodes):
    if is_switch(n):
        my_graph.node(n, shape="box")
    else:
        my_graph.node(n, shape="circle")

for a, b in sorted(edges):
    my_graph.edge(a, b)

print(my_graph.source)
my_graph.render("output/AutomaticGraph.gv")