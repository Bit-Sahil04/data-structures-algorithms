# Quadtree

Point-region (PR) quadtree Data structure implementation in python and its visualisation

requires pygame 2

## Todo:
- Design a point or node class and operate on those objects instead of pure coordinates (WIP)
- Design a collision system with efficient use of quad tree (WIP)
- Fix collision bug between points of diff radius in point.update() function (WIP)
- optimize point removal and subtree clearing algorithms Fn:{Pop, Truncate, DFS}
- Restructure Quad.py to put core functions first followed by utility functions
- Implement neighbour finding algorithm for more efficient insertion <br>
	https://geidav.wordpress.com/2017/12/02/advanced-octrees-4-finding-neighbor-nodes/
- implement async highlight function

### Optimization candidates
Profiler report. Execution time: 52.3 seconds
<table>
 <tr>
  <th>ncalls</th>
  <th>tottime</th>
  <th>percall</th>
  <th>cumtime</th>
  <th>percall</th>
  <th>filename:lineno(function)</th>
 </tr>
  <tr>
  <th>102870/78361</th>
  <th>0.096</th>
  <th>0.000</th>
  <th>40.000</th>
  <th>0.001</th>
  <th>Quad.py:118(pop)</th>
 </tr>
  <tr>
  <th>91807206/102870</th>
  <th>36.328</th>
  <th>0.000</th>
  <th>39.788</th>
  <th>0.000</th>
  <th>filename:lineno(function)</th>
 </tr>
  <tr>
  <th>493331</th>
  <th>0.681</th>
  <th>0.000</th>
  <th>43.055</th>
  <th>0.000</th>
  <th>quad_tree.py:89(update)</th>
 </tr> </tr>
  <tr>
  <th>102870</th>
  <th>0.082</th>
  <th>0.000</th>
  <th>39.869</th>
  <th>0.000</th>
  <th>Quad.py:137(truncate_tree)</th>
 </tr>
 </table>
