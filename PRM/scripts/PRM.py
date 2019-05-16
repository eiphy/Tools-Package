# import environment_2d
import numpy as np
import math
import pylab as pl

# Generalized functions
def cross_mul(px, py, qx, qy):
    '''
    This function is used to calculate a 'cross multiplication'
    --------------------
    px, py: vector P
    qx, qy: vector Q
    '''
    return px*qy - py*qx



class node():
    '''
    The basic class for node
    -----------------
    x, y: the coordinate
    dis: The heuristic (distance from goal point)
    costc: The cummulated cost
    '''
    def __init__(self, x, y, dis=0, costc=0):
        self.x = x
        self.y = y

        # conne is the connected node set and cost is the corresponding cost set
        self.conne = []
        self.cost = []

        # These are the values used in the path searching
        self.dis = dis                       
        self.costc = costc                    
        self.oscore = self.dis + self.costc     # Overall score: costc + dis        
        self.previous = self                    # Previous node, used to trace back the path

    def add_conne(self, node_next, cost_next):
        '''
        This function is used to add connective node into current node object.
        '''
        self.conne.append(node_next)
        self.conne.append(cost_next)

    def del_conne(self, node_del):
        '''
        This function is used to delete nodes from the conne list. If the nodes don't exist in the list, an error message will be sent out.
        '''
        try:
            index = self.conne.index(node_del)
        except:
            print("Given node is not in conne of current node")
            return

        del self.conne[index]
        del self.cost[index]

    def dis_calc(self, x, y):
        '''
        This function is used to calculate distance from this node to a point
        '''
        return math.sqrt((self.x-x)**2 + (self.y-y)**2)

class Roadmap():
    '''
    The map class, containning most method to solve a planning problem
    -----------------
    env: the environment object
    r: max connectable distance between two points
    dense: density of node w.r.t the map size i.e number of node/ area of map.
    cp_mode=1: =1: plot the connection. Be aware that plotting connection is very inefficient in this version.
    '''
    def __init__(self, env, r, dense, cp_mode=1):
        self.env = env
        self.nodels = []
        self.cp_mode = cp_mode
        self.dense = 0
        self.mapsize = env.size_x * env.size_y

        # section initilization
        nx = math.floor(env.size_x / r)
        ny = math.floor(env.size_y / r)

        if env.size_x % r:
            nx = nx + 1
        if env.size_y % r:
            ny = ny + 1

        self.section = [[ [] for j in range(nx) ] for i in range(ny)]

        # nodels generate/sample map
        self.node_density_modifier(dense, r)
        self.node_connectivity_modifer(r)

    def path_calc(self, s_x, s_y, g_x, g_y, r):
        '''
        This function is used to get the shortest path by A* method
        ---------------------
        s_x, s_y: coordinate of start point
        g_x, g_y: coordinate of goal point
        r: max connectable distance
        '''
        # Initialize the starting and goal nodes
        node_g = node(g_x, g_y)
        node_s = node(s_x, s_y, node_g.dis_calc(s_x, s_y))

        # Configure the connectivity
        self.nodels.append(node_s)
        self.nodels.append(node_g)

        xsec = math.floor(s_x / r)
        ysec = math.floor(s_y / r)
        testset = []
        testset.extend(self.section[ysec][xsec])
        self.nearby_testset_gen(ysec, xsec, testset)

        for node_test in testset:
            self.node_connectivity_add(node_s, node_test, r, 0)

        xsec = math.floor(g_x / r)
        ysec = math.floor(g_y / r)
        testset = []
        testset.extend(self.section[ysec][xsec])
        self.nearby_testset_gen(ysec, xsec, testset)

        for node_test in testset:
            self.node_connectivity_add(node_g, node_test, r, 0)

        # Start search
        openset = [node_s]
        closedset = []

        while len(openset):
            # Sort the open node w.r.t overall score
            sortedopen = sorted(openset, key=lambda c:c.oscore)
            current_node = sortedopen[0]

            if current_node == node_g:
                i = node_g.previous.conne.index(node_g)
                node_g.costc = node_g.previous.costc + node_g.previous.cost[i]
                break

            openset.remove(current_node)
            closedset.append(current_node)

            # Configure connected_node from current_node
            for connected_node in current_node.conne:
                if connected_node in closedset:
                    continue
                
                i = current_node.conne.index(connected_node)
                cost_temp = current_node.costc + current_node.cost[i]

                if not connected_node in openset:
                    openset.append(connected_node)
                else:
                    if cost_temp >= connected_node.costc:
                        continue

                connected_node.costc = cost_temp
                connected_node.dis = connected_node.dis_calc(node_g.x, node_g.y)
                connected_node.oscore = connected_node.dis + cost_temp
                connected_node.previous = current_node

        if current_node != node_g:
            print('No solution for current parameters')
            return -1

        # Plot the search path
        pl.pause(0.001)
        xls = []
        yls = []
        xls.append(node_g.x)
        yls.append(node_g.y)
        trace_node = node_g.previous
        while trace_node != node_s:
            xls.append(trace_node.x)
            yls.append(trace_node.y)

            trace_node = trace_node.previous

        xls.append(node_s.x)
        yls.append(node_s.y)
        pl.plot(xls, yls, 'g')

        return node_g.costc


    def node_density_modifier(self, dense, r):
        '''
        This function together with other two functions are used to modify the node density of PRM & and seperate the new added nodes to different sections.
        ---------------------
        dense: density of node w.r.t the map size i.e number of node/ area of map. Currently, this value should be bigger than current density.
        r: max radius that can connect two node
        '''
        if dense > self.dense:
            self.node_density_increase(dense, r)
        else:
            self.node_density_decrease(dense, r)


    def node_density_increase(self, dense, r):
        '''
        This function is used to increase the node density
        '''
        # As the starting and goal point is continues added to the list
        n0 = math.ceil(dense * self.mapsize)
        n = n0 - len(self.nodels)

        while n > 0:
            x_temp = np.random.rand(n) * self.env.size_x
            y_temp = np.random.rand(n) * self.env.size_y

            for i in range(len(x_temp)):
                if not self.env.check_collision(x_temp[i], y_temp[i]):
                    self.nodels.append(node(x_temp[i], y_temp[i]))
                    # to desireable section
                    xsec = math.floor(x_temp[i] / r)
                    ysec = math.floor(y_temp[i] / r)
                    self.section[ysec][xsec].append(self.nodels[-1])
            n = n0 - len(self.nodels)

        self.node_dense_plot()


    def node_density_decrease(self, dense, r):
        '''
        This function is used to decrease the onde density
        The later joined start points and end points may be removed during the decreasing
        '''
        n0 = math.ceil(dense * self.mapsize)
        n = len(self.nodels) - n0

        if n == 0:
            return
        else:
            index = np.random.randint(0, len(self.nodels)-1, n)

        del_nodels = [node for node in self.nodels if self.nodels.index(node) in index]
        self.nodels = [node for node in self.nodels if self.nodels.index(node) not in del_nodels]

        for node in self.nodels:
            map(node.del_conne, del_nodels)


    def node_dense_plot(self):
        '''
        This function is used to plot the scattered node
        '''
        xls = []
        yls = []

        for node in self.nodels:
            xls.append(node.x)
            yls.append(node.y)
        pl.scatter(xls, yls, 10, 'b')
        pl.pause(0.0001)


    def node_connectivity_modifer(self, r):
        '''
        This function is used to modify the nodes' connectivity property w.r.t current node list and max
        connectable distance
        ---------------------
        r: max connectable distance
        '''
        edset = []
        for i in range(len(self.section)):
            for j in range(len(self.section[0])):
                for node in self.section[i][j]:
                    # Generate testset
                    current_ind = self.section[i][j].index(node)
                    testset = []
                    testset.extend(self.section[i][j][current_ind+1:-1])
                    self.nearby_testset_gen(i, j, testset)

                    # Modify connectivity
                    for node_test in testset:
                        if node_test in edset:
                            continue

                        if node_test in node.conne:
                            continue
                        
                        self.node_connectivity_add(node, node_test, r, self.cp_mode)
                    
                    edset.append(node)


    def nearby_testset_gen(self, i, j, testset):
        '''
        This function is used to generate the test set component near current section used to determine the connectivity
        ---------------------
        i, j: section index (ith col & jth row) of tested node
        '''
        if i == 0:
            y_bias = [0, 1]
        else:
            if i == len(self.section) - 1:
                y_bias = [-1, 0]
            else:
                y_bias = [-1, 0, 1]

        if j == 0:
            x_bias = [0, 1]
        else:
            if j == len(self.section[i]) - 1:
                x_bias = [-1, 0]
            else:
                x_bias = [-1, 0, 1]

        for xb in x_bias:
            for yb in y_bias:
                if xb == 0 and yb == 0:
                    continue
                testset.extend(self.section[i+yb][j+xb])
        
        # return testset


    def node_connectivity_add(self, node, node_test, r, cp_mode):
        '''
        This function is used to check if the two nodes should be conncted
        ---------------------
        param: node: current node obj
        param: node_test: tested node obj
        param: r: max connectable distance
        param: cp_mode: =0: don't plot the connection
        '''

        if self.check_conflict(node.x, node.y, node_test.x, node_test.y):
            return

        dis = node.dis_calc(node_test.x, node_test.y)
        if dis <= r:
            node.conne.append(node_test)
            node_test.conne.append(node)
            node.cost.append(dis)
            node_test.cost.append(dis)

            if cp_mode == 1:
                pl.plot([node.x,node_test.x], [node.y,node_test.y], 'b', linewidth = 1)


    def check_conflict(self, x1, y1, x2, y2):
        '''
        This function is used to check if the connection violent the obstacles.
        Be aware if the obstacle is not triangle, the algorithm may fail to observe the violence, due to very narrow obstacle shape.
        ---------------------
        x1, y1: the coordinate of one endpoint
        x2, y2: the coordinate of another endpoint
        '''            
        for obs in self.env.obs:
            d1 = cross_mul(x2-x1, y2-y1, obs.x0-x1, obs.y0-y1)
            d2 = cross_mul(x2-x1, y2-y1, obs.x1-x1, obs.y1-y1)
            d3 = cross_mul(obs.x1-obs.x0, obs.y1-obs.y0, x1-obs.x0, y1-obs.y0)
            d4 = cross_mul(obs.x1-obs.x0, obs.y1-obs.y0, x2-obs.x0, y2-obs.y0)

            if d1 * d2 < 0 and d3 * d4 < 0:
                return True

            d1 = cross_mul(x2-x1, y2-y1, obs.x1-x1, obs.y1-y1)
            d2 = cross_mul(x2-x1, y2-y1, obs.x2-x1, obs.y2-y1)
            d3 = cross_mul(obs.x2-obs.x1, obs.y2-obs.y1, x1-obs.x1, y1-obs.y1)
            d4 = cross_mul(obs.x2-obs.x1, obs.y2-obs.y1, x2-obs.x1, y2-obs.y1)

            if d1 * d2 < 0 and d3 * d4 < 0:
                return True

            d1 = cross_mul(x2-x1, y2-y1, obs.x2-x1, obs.y2-y1)
            d2 = cross_mul(x2-x1, y2-y1, obs.x0-x1, obs.y0-y1)
            d3 = cross_mul(obs.x0-obs.x2, obs.y0-obs.y2, x1-obs.x2, y1-obs.y2)
            d4 = cross_mul(obs.x0-obs.x2, obs.y0-obs.y2, x2-obs.x2, y2-obs.y2)

            if d1 * d2 < 0 and d3 * d4 < 0:
                return True

        return False       

