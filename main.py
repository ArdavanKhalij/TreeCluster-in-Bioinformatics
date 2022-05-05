from ete3 import Tree


THRESHOLD = 0.15
global PARTS
PARTS = 1
global Leaves
Leaves = []
ClusterDiversity = []
global NodesForDetach
NodesForDetach = []
global NodesForDetach2
NodesForDetach2 = []


FILE = open("99_otus_unannotated.tree", "r")
TreeNewickString = str(FILE.read())
Tree = Tree(TreeNewickString)
print(len(Tree.get_leaves()))


def μ_tree_distance(Tree):
    # global NodesForDetach2
    # NodesForDetach2 = []
    # for i in NodesForDetach:
    #     NodesForDetach2.append(i)
    #     NodesForDetach2 = NodesForDetach2 + i.get_leaves()
    # NodesForDetach2 = list(dict.fromkeys(NodesForDetach2))
    Sum = 0
    # TREE = Tree
    # for i in NodesForDetach:
    #     TREE.detach()
    # print(NodesForDetach2)
    Nodes = Tree.get_leaves()
    # print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    # print(Nodes)
    print("--------------------------")
    # print(len(NodesForDetach2))
    k = len(Nodes)
    # print("Before", k)
    # for i in NodesForDetach2:
    #     if i in Nodes:
    #         print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    #         Nodes.remove(i)
    N = len(Nodes)
    # print(N - k)
    print("after", N)
    for i in range(0, N):
        for j in range(i + 1, N):
            # if i in NodesForDetach or j in NodesForDetach:
            #     pass
            # else:
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
                #     Tree.detach()
                NodesForDetach.append(Tree.children[0])
                Tree.children[0].detach()
                ClusterDiversity.append(μ_tree_distance(Tree))
                BU = BL + WL
                global PARTS
                PARTS = PARTS + 1
                print(PARTS)
            else:
                # for i in NodesForDetach:
                #     Tree.delete(i)
                NodesForDetach.append(Tree.children[1])
                Tree.children[1].detach()
                ClusterDiversity.append(μ_tree_distance(Tree))
                BU = BR + WR
                PARTS = PARTS + 1
                print(PARTS)
        else:
            BU = max([BL + WL, BR + WR])
        Leaves.append(Tree.get_leaves())
        # print("##################### ", PARTS, BU, " #####################")


Max_diameter_min_cut_partitioning(Tree)
print("##################### Result #####################")
print(PARTS)
print(len(Leaves))
print("------------------------------------------")
print(ClusterDiversity)
print("------------------------------------------")
print(sum(ClusterDiversity))
print(sum(ClusterDiversity)/len(ClusterDiversity))
