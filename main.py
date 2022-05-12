from ete3 import Tree
import time


THRESHOLD = 0.15
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
        if i in Nodes:
            # print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
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
        # print("BR:", BR, "BL:", BL, "WR:", WR, "WL:", WL, "BR + WR:", BR + WR, "BL + WL:", BL + WL)
        if (BR + WR + BL + WL) > THRESHOLD:
            if (BL + WL) <= (BR + WR):
                # for i in NodesForDetach:
                    # print(i)
                    # D = Tree.search_nodes(name = i.name)[0]
                    # D.detach()
                # NodesForDetach.append(Tree.children[0])
                Tree.children[0].detach()
                NodesForDetach.append(Tree.children[0])
                ClusterDiversity.append(μ_tree_distance(Tree))
                BU = BL + WL
                global PARTS
                PARTS = PARTS + 1
                print(PARTS)
            else:
                # for i in NodesForDetach:
                    # print(i)
                    # D = Tree.search_nodes(name=i.name)[0]
                    # D.detach()
                # NodesForDetach.append(Tree.children[1])
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
        # print("##################### ", PARTS, BU, " #####################")

start = time.time()
Max_diameter_min_cut_partitioning(Tree)
end = time.time()
print("##################### Result #####################")
print(PARTS)
print(len(Leaves))
print("------------------------------------------")
print(ClusterDiversity)
print("------------------------------------------")
print(sum(ClusterDiversity))
print("Result for the plot:", sum(ClusterDiversity)/len(ClusterDiversity))
time_of_running = end-start
print("Time of running:", time_of_running)

# Results
# For Deepika to run
# 0.005 :
# 0.010 :
# 0.015 :
# 0.020 :
# 0.025 :
# 0.030 :
# 0.035 :
# 0.040 :
# 0.045 :
# 0.050 :
# 0.055 :
# 0.060 :
# 0.065 :
# 0.070 :
# 0.075 :

# For Ardavan to run
# 0.080 :
# 0.085 :
# 0.090 :
# 0.095 :
# 0.100 :
# 0.105 :
# 0.110 :
# 0.115 :
# 0.120 :
# 0.125 :
# 0.130 :
# 0.135 :
# 0.140 :
# 0.145 :
# 0.150 :
