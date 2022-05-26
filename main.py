from ete3 import Tree
import time


THRESHOLD = 0.105
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
Tree.delete()
print(len(Tree.get_leaves()))


def μ_tree_distance(Tree):
    Nodes = Tree.get_leaves()
    # First optimization
    k = len(Nodes)
    if k <= 1:
        return 0
    Sum = 0
    global NodesForDetach2
    for i in NodesForDetach:
        NodesForDetach2.append(i)
        NodesForDetach2 = NodesForDetach2 + i.get_leaves()
    NodesForDetach2 = list(dict.fromkeys(NodesForDetach2))
    print("--------------------------")
    print(len(NodesForDetach2))
    print("Before", k)
    for i in NodesForDetach2:
        if i in Nodes:
            Nodes.remove(i)
    N = len(Nodes)
    # Second optimization
    if N <= 1:
        return 0
    print(k - N)
    print("after", N)
    for i in range(0, N):
        for j in range(i + 1, N):
            Sum = Sum + Nodes[i].get_distance(Nodes[j])/len(Nodes)
    return Sum


def Max_diameter_min_cut_partitioning(Tree):
    global NodesForDetach
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
                # The main optimization
                NodesForDetach = Tree.children[0]
                ClusterDiversity.append(μ_tree_distance(Tree))
                BU = BL + WL
                global PARTS
                PARTS = PARTS + 1
                print(PARTS)
            else:
                Tree.children[1].detach()
                try:
                    # The main optimization
                    NodesForDetach = Tree.children[1]
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
#####################################################
# 0.005 :
#   0.00004963416381852437
#   149.32807683944702
#   181573

# 0.010 :
#   0.00025166146892214436
#   317.25540804862976
#   150063

# 0.015 :
#   0.0006531960084677711
#   468.319837808609
#   123460

# 0.020 :
#   0.0012037491555914883
#   556.6031062602997
#   103768

# 0.025 :
#   0.001922258632878354
#   495.05629110336304
#   88723

# 0.030 :
#   0.0028022701523227242
#   613.4455859661102
#   77266

# 0.035 :
#   0.0038788127500481205
#   484.11643981933594
#   68006

# 0.040 :
#   0.0049186568683535
#   620.2524716854095
#   60555

# 0.045 :
#   0.006551723126441533
#   151621.34584784508
#   54071

# 0.050 :
#   0.008326191589860863
#   483.2067520618439
#   48692

# 0.055 :
#   0.009890008116802266
#   483.49843525886536
#   43972

# 0.060 :
#   0.01200361906106457
#   667.2666728496552
#   39811

# 0.065 :
#   0.014452139670171879
#   512.7458958625793
#   36265

# 0.070 :
#   0.01678221639957774
#   714.725035905838
#   33191

# 0.075 :
#   0.020579979771172447
#   495.85116505622864
#   30338

# For Ardavan to run
# 0.080 :
#   0.02431905118924475
#   33455.75756812096
#   27809

# 0.085:
#   0.027485665960935882
#   859.633740901947
#   25628

# 0.090 :
#   0.031432243351193996
#   1388.7801098823547
#   23631

# 0.095 :
#   0.03573863866271736
#   1002.0514023303986
#   21869

# 0.100 :
#   0.0386100788506496
#   20247.943447113037
#   20256

# 0.105 :
#   0.03573863866271736
#   1002.0514023303986
#   18740

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
