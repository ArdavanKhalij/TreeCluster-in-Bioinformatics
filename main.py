from ete3 import Tree


THRESHOLD = 0.005
global PARTS
PARTS = 1
global Leaves
Leaves = []


FILE = open("99_otus_unannotated.tree", "r")
TreeNewickString = str(FILE.read())
Tree = Tree(TreeNewickString)


def Max_diameter_min_cut_partitioning(Tree):
    if not Tree.is_leaf():
        Max_diameter_min_cut_partitioning(Tree.children[0])
        Max_diameter_min_cut_partitioning(Tree.children[1])
        BR = Tree.children[0].get_farthest_leaf()[1]
        BL = Tree.children[1].get_farthest_leaf()[1]
        WR = Tree.get_distance(Tree.children[0])
        WL = Tree.get_distance(Tree.children[1])
        print("BR:", BR, "BL:", BL, "WR:", WR, "WL:", WL, "BR + WR:", BR + WR, "BL + WL:", BL + WL)
        if (BR + WR + BL + WL) > THRESHOLD:
            if (BL + WL) <= (BR + WR):
                Tree.children[0].detach()
                BU = BL + WL
                global PARTS
                PARTS = PARTS + 1
            else:
                Tree.children[1].detach()
                BU = BR + WR
                PARTS = PARTS + 1
        else:
            BU = max([BL + WL, BR + WR])
        Leaves.append(Tree.get_leaves())
        print("##################### "+ str(PARTS) +" #####################")


Max_diameter_min_cut_partitioning(Tree)
print("##################### Result #####################")
print(PARTS)
