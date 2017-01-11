import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from collections import OrderedDict


def get_polar(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)


def get_cartesian(r, theta):
    x = r*np.sin(theta)
    y = r*np.cos(theta)

    return x, y


class node(object):
    
    def __init__(self, name, radius, theta_start=None, theta_end=None, cartesian_start=None, cartesian_end=None,
                 cartesian_total_length=None, color=None, linewidth=10, fontsize=8, rotation="vertical"):
        self.name = name
        self.radius = radius
        self.color = color
        self.linewidth = 10
        
        if theta_start == None and cartesian_start != None:
            self.cartesian_start = cartesian_start
            self.cartesian_end = cartesian_end
            self.cartesian_length = cartesian_end - cartesian_start
            self.cartesian_total_length = cartesian_total_length
            self.cartesian_init()
            
        else:        
            self.theta_start = theta_start
            self.theta_end = theta_end
            self.polar_length = theta_end - theta_start
            self.thetas = np.linspace(theta_start, theta_end, 30)
            self.cartesian_start = cartesian_start
            self.cartesian_end = cartesian_end
            self.cartesian_length = cartesian_end - cartesian_start
            self.cartesian_total_length = cartesian_total_length
        
            self.cartesian_middle = get_cartesian(radius, ((theta_end-theta_start)/2.0)+theta_start)
            self.label_position = get_cartesian(self.radius*1.04, ((self.theta_end-self.theta_start)/2.0)+self.theta_start)
        
        self.polar_coordinates = np.zeros((len(self.thetas), 2))
        self.polar_coordinates[:,0] = self.thetas
        self.polar_coordinates[:,1] = radius
        self.cartesian_coordinates = np.array(get_cartesian(self.polar_coordinates[:,1], self.polar_coordinates[:,0]))
        self.set_label_props(fontsize, rotation)
            
    
    def cartesian_init(self):
        self.theta_start = (self.cartesian_start / float(self.cartesian_total_length)) * (2*np.pi)
        self.theta_end = (self.cartesian_end / float(self.cartesian_total_length)) * (2*np.pi)
        self.polar_length = self.theta_end - self.theta_start
        self.thetas = np.linspace(self.theta_start, self.theta_end, 30)
        self.cartesian_middle = get_cartesian(self.radius, ((self.theta_end-self.theta_start)/2.0)+self.theta_start)
        self.label_position = get_cartesian(self.radius*1.04, ((self.theta_end-self.theta_start)/2.0)+self.theta_start)
        
    
    def set_label_props(self, fontsize, rotation):
        degrees = (((self.theta_end-self.theta_start)/2.0)+self.theta_start)*57.29577951308232 #convert radians to degrees
        if degrees >= 0 and degrees <= 90:
            degrees = 90-degrees
            if rotation == "vertical":
                self.degrees = degrees
            else:
                self.degrees = degrees+270
            self.ha = "left"
            self.va = "bottom"
            self.fontsize = fontsize
        elif degrees > 90 and degrees <= 180:
            degrees = 360+90-degrees
            if rotation == "vertical":
                self.degrees = degrees
            else:
                self.degrees = degrees+90
            self.ha = "left"
            self.va = "top"
            self.fontsize = fontsize
        elif degrees > 180 and degrees <=270:
            degrees = 270 - degrees
            if rotation == "vertical":
                self.degrees = degrees
            else:
                self.degrees = degrees+270
            self.ha = "right"
            self.va = "top"
            self.fontsize = fontsize
        elif degrees > 270 and degrees < 360:
            degrees = 360+270-degrees
            if rotation == "vertical":
                self.degrees = degrees
            else:
                self.degrees = degrees+90
            self.ha = "right"
            self.va = "bottom"
            self.fontsize = fontsize
                
        
    def node_position(self, position, polar=False):
        """
        Given cartesian position on node
        Return polar position in graph
        """
        node_pos = None
        graph_pos = None
        if polar: #check if position in polar
            node_pos = positon
            graph_pos = theta_start + position
        elif self.cartesian_total_length != None:
            node_pos = (position / float(self.cartesian_length)) * self.polar_length
            graph_pos = ((self.cartesian_start / self.cartesian_total_length) * (2*np.pi)) + node_pos
        else:
            print "requires node atrribute cartesian_total_length to be set"
            
        return node_pos, graph_pos
        
        
        
        
class edge(object):
    
    def __init__(self, node1, node2, position1=None, position2=None, radius=10, color="black", weight=1, polar=False):
        self.edgeprops = {}
        self.edgeprops["facecolor"] = "none"
        self.edgeprops["edgecolor"] = color
        
        self.node1 = node1.name
        self.node2 = node2.name
        self.position1 = position1
        self.position2 = position2
        self.radius = radius
        
        node_pos1, graph_pos1 = node1.node_position(position1, polar)
        node_pos2, graph_pos2 = node2.node_position(position2, polar)
        
        self.start_theta = graph_pos1
        self.end_theta = graph_pos2
        
        verts = [get_cartesian(self.radius, self.start_theta),
                 (0, 0),
                 get_cartesian(self.radius, self.end_theta)]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

        self.path = Path(verts, codes)
        self.patch = patches.PathPatch(self.path, lw=weight, **self.edgeprops)
        
        


class CircosObject(object):
    
    def __init__(self, nodes, edges, radius):
        """
        nodes: list of tuples [(name, length)...]
        edges: list of tuples [(node1, position1, node2, position2)]
        """
        
        self.radius = radius
        self.nodes = self.fill_nodes(nodes)
        self.edges = self.fill_edges(edges)
        
        self.fig = plt.figure()
        
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-radius*1.05, radius*1.05)
        self.ax.set_ylim(-radius*1.05, radius*1.05)
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        for k in self.ax.spines.keys():
            self.ax.spines[k].set_visible(False)
            
    
    def fill_nodes(self, nodes):
        new_nodes = OrderedDict()
        
        if type(nodes[0]) == tuple:
            lengths = np.array([i[1] for i in nodes])
            cumsum_lengths = np.append(0.0, np.cumsum(lengths))
            total_length = cumsum_lengths[-1]
            for i in xrange(len(nodes)):
                name = nodes[i][0]
                start = cumsum_lengths[i]
                end = cumsum_lengths[i+1]
                
                try:
                    color = nodes[i][2]
                except IndexError:
                    color = None
                
                new_node = node(name, self.radius, cartesian_start=start, cartesian_end=end,
                                cartesian_total_length=total_length, color=color)
                new_nodes[name] = new_node
            
        else:
            lengths = np.repeat((2*np.pi)/len(nodes), len(nodes))
            cumsum_lengths = np.append(np.cumsum(lengths), 0.0)
            for i in xrange(len(nodes)):
                name = nodes[i][0]
                start = cumsum_lengths[i]
                end = cumsum_lengths[i+1]
                
                try:
                    color = nodes[i][2]
                except IndexError:
                    color = None
                
                new_node = node(name, self.radius, polar_start=start, polar_end=end, color=color)
                new_nodes[name] = new_node
                
        return new_nodes
                
    
    def fill_edges(self, edges):
        new_edges = []
        
        if type(edges[0][1])==int or type(edges[0][1])==float:
            for e in edges:
                node1  = self.nodes[e[0]]
                position1 = e[1]
                node2 = self.nodes[e[2]]
                position2 = e[3]
                
                try:
                    color = e[4]
                except IndexError:
                    color = "black"
                try:
                    weight = int(e[5])
                except IndexError:
                    weight = 1
            
                new_edge = edge(node1=node1, position1=position1, node2=node2, position2=position2,
                                radius=self.radius, polar=False, color=color, weight=weight)
                new_edges.append(new_edge)
        else:
            for e in edges:
                node1  = self.nodes[e[0]]
                node2 = self.nodes[e[2]]
                
                try:
                    color = e[3]
                except IndexError:
                    color = "black"
                try:
                    weight = int(e[4])
                except IndexError:
                    weight = 1
                
                new_edge = edge(node1=node1, node2=node2, radius=self.radius, polar=True, color=color,
                                weight=weight)
                new_edges.append(new_edge)
            
        return new_edges
        
    
    def draw(self):
        self.add_nodes()
        self.add_edges()
        
    
    def add_nodes(self):
        for n in self.nodes:
            if self.nodes[n].color == None:
                self.ax.plot(self.nodes[n].cartesian_coordinates[0], self.nodes[n].cartesian_coordinates[1],
                             linewidth=self.nodes[n].linewidth, solid_capstyle="butt")
            else:
                self.ax.plot(self.nodes[n].cartesian_coordinates[0], self.nodes[n].cartesian_coordinates[1],
                             linewidth=self.nodes[n].linewidth, solid_capstyle="butt", color=self.nodes[n].color)
                             
            self.ax.text(self.nodes[n].label_position[0], self.nodes[n].label_position[1],
                         self.nodes[n].name, rotation=int(self.nodes[n].degrees), ha=self.nodes[n].ha,
                         va=self.nodes[n].va, fontsize=self.nodes[n].fontsize, color="black")
       
                         
    def add_edges(self):
        for e in self.edges:
            self.ax.add_patch(e.patch)