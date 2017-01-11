python_circos is a python package to visualize the genome and links
between regions. (Only basic implementation, so far!)

Data Format
===========

Edge input files must be in tab delimited format (node1, position1, node2, position2, color, width)::

	chr1	200000000	chr2	100	grey	1
	chr1	200000000	chr3	30000000	grey	2

Simple Example:

    https://raw.githubusercontent.com/kylessmith/python_circos/master/example/test_edges.txt
	
Node input files must be in tab delimited format (node, length, color)::

	chr1	249250621	darkgrey
	chr2	243199373	black
	chr3	198022430	darkgrey
	chr4	191154276	black

Simple Example:

    https://raw.githubusercontent.com/kylessmith/python_circos/master/example/test_nodes.txt

Invocation
==========

Running the following command will result in a more detailed help message::

    $ python -m genome_plot -h

Gives::

	--nodes NODES    nodes file name
	--edges EDGES    edges file name
	--o O            output file name
	--radius RADIUS  radius to use

QuickStart
==========
::

	$ python -m python_circos \
	  --nodes example/test_nodes.txt\
	  --edges example/test_edges.txt\
	  --o example/test.png

The output will be shown in the following files::

	example/test.png
	
Importation
===========
::

	>>> import python_circos
	>>> edges = python_circos.parse_edges("test_edges.txt") #returns list of tuples
	>>> nodes = python_circos.parse_nodes("test_nodes.txt") #returns list of tuples
	>>> radius = 10
	>>> c = python_circos.genome_plot.CircosObject(nodes, edges, radius) #create CircosObject
	>>> c.draw()
	>>> c.fig.savefig("test.png", transparent=True)

Installation
============

If you dont already have numpy and matplotlib installed, it is best to download
`Anaconda`, a python distribution that has them included.  

    https://continuum.io/downloads

Dependencies can be installed by::

    pip install -r requirements.txt

License
=======
python_circos is freely available under the MIT License
