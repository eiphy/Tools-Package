import numpy as np
import pylab as pl
import sys
from scripts import environment_2d
from scripts import PRM
import datetime
# sys.path.append('./scripts')

# sample parameters
dense = 10
r = 1

pl.ion()
pl.clf()
np.random.seed()

# generate environment & first query
env = environment_2d.Environment(10, 6, 5)
env.plot()
q = env.random_query()
if q is not None:
  x_start, y_start, x_goal, y_goal = q
  env.plot_query(x_start, y_start, x_goal, y_goal)

np.random.seed()
start = datetime.datetime.now()

# generate roadmap
map = PRM.Roadmap(env, r, dense, 0)

path = map.path_calc(x_start, y_start, x_goal, y_goal, 1)

# if cannot find path, denser the node and increase the r
if path == -1:
  dense = dense * 1.2
  r = r * 1.2
  wait = input('The program will denser the map, press Enter to continue')
  map.node_density_modifier(dense, r)
  map.node_connectivity_modifer(r)

  path = map.path_calc(x_start, y_start, x_goal, y_goal, r)
  if path == -1:
      wait = ''
      while path == -1:
        if wait == '':
          break
        wait = input('No solutions are available.\n The goal may not be reachable.\n press Enter to abandon this query or "dense_pval r_pval" to continue the process (Please be aware the dense should be no smaller than current one and pval stands for the increase percentage, 1 for do not change)\n')
        para = wait.split()
        dense = dense * float(para[0].strip())
        r = r * float(para[1].strip())

        map.node_density_modifier(dense, r)
        map.node_connectivity_modifer(r)
        path = map.path_calc(x_start, y_start, x_goal, y_goal, r)

end = datetime.datetime.now()
print('Planning time is ', (end-start), ' seconds\n','Path length is ',path)

np.random.seed()

# randomly generate queries. for test purpose
while 1:

  q = None
  while q is None:
    q = env.random_query()
    if q is not None:
      x_start, y_start, x_goal, y_goal = q
      env.plot_query(x_start, y_start, x_goal, y_goal)
      pl.pause(0.001)
  start = datetime.datetime.now()
  path = map.path_calc(x_start, y_start, x_goal, y_goal, 1)
  if path == -1:
    dense = dense * 1.2
    r = r * 1.2
    wait = input('The program will denser the map, press Enter to continue')
    map.node_density_modifier(dense, r)
    map.node_connectivity_modifer(r)

    path = map.path_calc(x_start, y_start, x_goal, y_goal, r)
    if path == -1:
      wait = ''
      while path == -1:
        wait = input('No solutions are available.\n The goal may not be reachable.\n press Enter to abandon this query or "dense_pval r_pval" to continue the process (Please be aware the dense should be no smaller than current one and pval stands for the increase percentage, 1 for do not change)\n')
        if wait == '':
          break
        para = wait.split()
        dense = dense * float(para[0].strip())
        r = r * float(para[1].strip())

        map.node_density_modifier(dense, r)
        map.node_connectivity_modifer(r)
        path = map.path_calc(x_start, y_start, x_goal, y_goal, r)

  end = datetime.datetime.now()
  print('Planning time is ', (end-start), ' seconds\n','Path length is ',path)
  pl.pause(0.001)


pl.ioff()
pl.show()