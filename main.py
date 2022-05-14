from ete3 import Tree
import time


THRESHOLD = 0.10
global PARTS
PARTS = 1
global Leaves
Leaves = []
ClusterDiversity = []
global NodesForDetach
NodesForDetach = []


FILE = open("99_otus_unannotated.tree", "r")
TreeNewickString = str(FILE.read())
Tree = Tree(TreeNewickString)
Tree.delete()
print(len(Tree.get_leaves()))


def μ_tree_distance(Tree):
    Nodes = Tree.get_leaves()
    k = len(Nodes)
    if k <= 1:
        return 0
    Sum = 0
    NodesForDetach2 = []
    for i in NodesForDetach:
        NodesForDetach2.append(i)
        NodesForDetach2 = NodesForDetach2 + i.get_leaves()
    NodesForDetach2 = list(dict.fromkeys(NodesForDetach2))
    print("--------------------------")
    print(len(NodesForDetach2))
    print("Before", k)
    for i in NodesForDetach2:
        if len(Nodes) == 0:
            break
        if i in Nodes:
            Nodes.remove(i)
    N = len(Nodes)
    if N <= 1:
        return 0
    print(k - N)
    print("after", N)
    for i in range(0, N):
        for j in range(i + 1, N):
            Sum = Sum + Nodes[i].get_distance(Nodes[j])/len(Nodes)
    return Sum


def Max_diameter_min_cut_partitioning(Tree):
    if not Tree.is_leaf():
        Max_diameter_min_cut_partitioning(Tree.children[0])
        Max_diameter_min_cut_partitioning(Tree.children[1])
        BR = Tree.children[0].get_farthest_leaf()[1]
        BL = Tree.children[1].get_farthest_leaf()[1]
        WR = Tree.get_distance(Tree.children[0])
        WL = Tree.get_distance(Tree.children[1])
        if (BR + WR + BL + WL) > THRESHOLD:
            if (BL + WL) <= (BR + WR):
                Tree.children[0].detach()
                NodesForDetach.append(Tree.children[0])
                ClusterDiversity.append(μ_tree_distance(Tree))
                BU = BL + WL
                global PARTS
                PARTS = PARTS + 1
                print(PARTS)
            else:
                Tree.children[1].detach()
                try:
                    NodesForDetach.append(Tree.children[1])
                except:
                    pass
                ClusterDiversity.append(μ_tree_distance(Tree))
                BU = BR + WR
                PARTS = PARTS + 1
                print(PARTS)
        else:
            BU = max([BL + WL, BR + WR])
        Leaves.append(Tree.get_leaves())

start = time.time()
Max_diameter_min_cut_partitioning(Tree)
end = time.time()
print("##################### Result #####################")
print(PARTS)
print("------------------------------------------")
print(ClusterDiversity)
print("------------------------------------------")
print(sum(ClusterDiversity))
print("Number of clusters", PARTS)
print("Result for the plot:", sum(ClusterDiversity)/len(ClusterDiversity))
time_of_running = end-start
print("Time of running:", time_of_running)

# Results
# For Deepika to run (please report result, number of clusters and time for each)
# Report in this format: result     time    Number of clusters
# 0.005 :
#
#
#

# 0.010 :
#
#
#

# 0.015 :
#
#
#

# 0.020 :
#
#
#

# 0.025 :
#
#
#

# 0.030 :
#
#
#

# 0.035 :
#
#
#

# 0.040 :
#
#
#

# 0.045 :
#
#
#

# 0.050 :
#
#
#

# 0.055 :
#
#
#

# 0.060 :
#
#
#

# 0.065 :
#
#
#

# 0.070 :
#
#
#

# 0.075 :
#
#
#

# For Ardavan to run
# 0.080 :
#
#
#

# 0.085 :
#
#
#

# 0.090 :
#
#
#

# 0.095 :
#
#
#

# 0.100 :
#
#
#

# 0.105 :
#
#
#

# 0.110 :
#   0.05058216984000356
#   16406.564623117447
#   17373

# 0.115 :
#   0.05595412738337391
#   12967.376780033112
#   16164

# 0.120 :
#   0.0628157484693781
#   12293.710629224777
#   15052

# 0.125 :
#   0.06866318803955122
#   10746.403151750565
#   14044

# 0.130 :
#   0.07475133658379958
#   8780.454730987549
#   13089

# 0.135 :
#   0.0861362623387877
#   8119.411988973618
#   12271

# 0.140 :
#   0.09566889546855913
#   8512.706733226776
#   11510

# 0.145 :
#   0.10828192145116002
#   6610.039298057556
#   10769

# 0.150 :
#   0.118549667375214
#   6037.745747089386s
#   10112
