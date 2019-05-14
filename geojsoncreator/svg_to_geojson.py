import xml.etree.ElementTree as ET
import numpy as np
import json
import networkx as nx
import pygraphviz as pgv

mappath="map.svg"
input_graph="k-neighbor_10000.dot"
G=nx.Graph(pgv.AGraph(input_graph))







clusteroutput="../cluster.geojson"
polylineoutput="../cluster_boundary.geojson"
edgesoutput="../edges.geojson"
nodesoutput="../nodes.geojson"

root = ET.parse(mappath).getroot()
n={}
n["type"]="Feature"
n["geometry"]={}
n["geometry"]["type"]=""
n["geometry"]["coordinates"]={}
n["properties"]={}

header='''{
  "type": "FeatureCollection",
    "crs": {
    "type": "name",
    "properties": {
      "name": "EPSG:3857"
    }
  },
  "features": [
  '''
footer= "\n]}"

def process_polygon(xml,id):
    polygon=n.copy()
    polygon["geometry"]["type"]="Polygon"
    polygon["id"]="cluster" + str(id)
    points=xml.attrib.pop('points')
    points_array=[[ float(p.split(",")[0]), float(p.split(",")[1])  ] for p in points.split(" ")]
    polygon["properties"]=xml.attrib
    polygon["properties"]["label"]=""
    polygon["geometry"]["coordinates"]=[points_array]
    return json.dumps(polygon, indent=2)



def process_polyline(xml):
    polygon=n.copy()
    polygon["geometry"]["type"]="LineString"
    points=xml.attrib.pop('points')
    #import pdb; pdb.set_trace()
    points_array=[[ float(p.split(",")[0]), float(p.split(",")[1])  ] for p in points.strip().split(" ")]
    polygon["properties"]=xml.attrib
    polygon["properties"]["label"]=""
    polygon["geometry"]["coordinates"]=points_array
    return json.dumps(polygon, indent=2)



def process_edge(xml,G,c):
    #import pdb; pdb.set_trace()
    edge=n.copy()
    edge["id"]="edge" + str(c)
    edge["geometry"]["type"]="LineString"
    points=xml[1].attrib.pop('d')
    points=points.replace("M"," ").replace("D"," ").replace("C"," ")
    #import pdb; pdb.set_trace()
    points_array=[[ float(p.split(",")[0]), float(p.split(",")[1])  ] for p in points.strip().split(" ")]
    edge["properties"]=xml[1].attrib
    n1=xml[0].text.split("--")[0]
    n2=xml[0].text.split("--")[1]
    edge["properties"]["src"]=n1
    edge["properties"]["dest"]=n2
    edge["properties"]["label"]=G.node[n1]["label"] + " -- " +  G.node[n2]["label"]
    edge["properties"]["weight"]=""
    edge["geometry"]["coordinates"]=points_array
    edge["properties"]["level"]="1"
    return json.dumps(edge, indent=2)





def process_node(xml,G):
    #import pdb; pdb.set_trace()
    node_g=xml[0].text
    node=n.copy()
    node["geometry"]["type"]="Point" #"Point"
    node["id"]="node" + node_g
    node["properties"]=G.node[node_g]
    x=float(xml[1].attrib.pop('x'))
    y=float(xml[1].attrib.pop('y'))
    #h= float(node["properties"]["height"]) * 1.10 * 72  # inch to pixel conversion
    #w=float(node["properties"]["width"]) * 1.10 * 72 # inch to pixel conversion
    #points_array=[[x-w/2,y-h/2], [x+w/2,y-h/2], [x+w/2,y+h/2], [x-w/2,y+h/2], [x-w/2,y-h/2]]

    node["properties"]["height"]="h"
    node["properties"]["width"]= "w"

    node["geometry"]["coordinates"]= [x,y] #[points_array] #//
    return json.dumps(node, indent=2)


def write_to_file(data,file):
    data=data[0:len(data)-3]
    data=header+ data+footer
    f=open(file,"w")
    f.write(data)
    f.close()




polygonCount=0
polylindCount=0
nodeCount=0
edgeCount=0
polygons=""
polylines=""
edges=""
nodes=""
for child in root.findall('*[@id="graph0"]/*'):
    if "polygon" in child.tag:
        if polygonCount!=0: #scape 1st rectangle
            polygons=polygons+ process_polygon(child,polygonCount) + ", \n"
        polygonCount=polygonCount+1
    if "polyline" in child.tag:
        polylines=polylines+ process_polyline(child) + ", \n"
    if "{http://www.w3.org/2000/svg}g"==child.tag:
        if child.attrib["class"]=="node":
            #print (child[0].text)
            #print(child[1].attrib)
            nodeCount=nodeCount+1
            nodes=nodes+ process_node(child,G)+ ", \n"
        if child.attrib["class"]=="edge":
            edges=edges+ process_edge(child,G,edgeCount)+ ", \n"
            edgeCount=edgeCount+1


print(polygonCount,polylindCount,nodeCount)

write_to_file(polygons,clusteroutput)
write_to_file(polylines,polylineoutput)
write_to_file(edges,edgesoutput)

write_to_file(nodes,nodesoutput)



'''
<g id="node2830" class="node">
<title>3506</title>
<text text-anchor="middle" x="23888.5" y="-6861.22" font-family="Helvetica,sans-Serif" font-weight="bold" font-size="15.00">block copolymers</text>
</g>
'''

'''

<g id="edge5238" class="edge">
<title>3324&#45;&#45;971</title>
<path fill="none" stroke="grey" d="M7023.05,-6911.53C7021.39,-6919.29 7019.08,-6930.12 7017.69,-6936.64"/>
</g>
'''
