# Quadtree

A Quad Tree is a spatial partitioning data structure to efficiently store clusters
of points on a 2D plane. It works by partitioning the plane into sub-planes recursively and
stores the points belonging to a cluster wtihin those regions, to efficiently index points for
operations such as quantization or collision detection.

This is a python implementation of a 2D Point - Region (PR) Quad Tree
https://en.wikipedia.org/wiki/Quadtree

## How to use:
- Initialize the Quad tree by creating an object of Quad
- configure max_points and max_depth as required <br>
(Only do this on the root node as dynamic depth/point capacity is untested on child nodes)
- create an object of the Item class to use as a container or use a child class of your own 
- Insert points into the item quad tree using the insert function

## Requirements:
Python ```3.8.5``` or higher <br>
pygame ```2.0``` or higher  (_only for running the visualization script_)

## Visualization: 
Run quad_tree.py to view the interactive Visualization <br>
```LMB``` Add few points <br>
```RMB``` Add point of interest for points to gravitate towards 

## Todo:
- Implement neighbour finding algorithm for more efficient insertion <br>
	https://geidav.wordpress.com/2017/12/02/advanced-octrees-4-finding-neighbor-nodes/
- implement async highlight function

