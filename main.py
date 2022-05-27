# Adding the ete3 library for working with the newick format tree
from ete3 import Tree
# Adding the time library for checking the time complexity
import time

# THRESHOLD is a global variable and the threshold mentioned in the paper
THRESHOLD = 0.15
# PARTS is a global variable for counting the number of clusters
global PARTS
PARTS = 1
# ClusterDiversity is a global variable for calculating μ
ClusterDiversity = []
# NodesForDetach is a global variable that is used for saving the detached node for each step
global NodesForDetach
NodesForDetach = []
# NodesForDetach2 is a global variable that is used for saving all the detached nodes
global NodesForDetach2
NodesForDetach2 = []

# Opening the file of the tree
FILE = open("99_otus_unannotated.tree", "r")
# Read from the file
TreeNewickString = str(FILE.read())
# Have the root node in Tree
Tree = Tree(TreeNewickString)

# Calculating the μ for each cluster for having the final result at the end of the program
def μ_tree_distance(Tree):
    # Nodes that the input node has
    Nodes = Tree.get_leaves()
    # First optimization
    # Just checking if the node has 1 or less child then the result is simply 0 so we dont
    # need to go through the function
    k = len(Nodes)
    if k <= 1:
        return 0
    Sum = 0
    # Saving the detached nodes and their children (append) for checking
    global NodesForDetach2
    for i in NodesForDetach:
        NodesForDetach2.append(i)
        NodesForDetach2 = NodesForDetach2 + i.get_leaves()
    NodesForDetach2 = list(dict.fromkeys(NodesForDetach2))
    print("--------------------------")
    print(len(NodesForDetach2))
    print("Before", k)
    # Removing the nodes that were saved as detached
    for i in NodesForDetach2:
        if i in Nodes:
            Nodes.remove(i)
    N = len(Nodes)
    # Checking the number of leafs again so if it is 1 or less we dont bother to check the
    # number and just return 0
    # Second optimization
    if N <= 1:
        return 0
    print(k - N)
    print("after", N)
    # Calculate the formula in paper
    for i in range(0, N):
        for j in range(i + 1, N):
            Sum = Sum + Nodes[i].get_distance(Nodes[j])/len(Nodes)
    return Sum

# This is the main function in our program that is an implementation of max diameter min cut partitioning
def Max_diameter_min_cut_partitioning(Tree):
    # Using the global NodesForDetach
    global NodesForDetach
    # Checking if the node that we are in it is not a leaf
    if not Tree.is_leaf():
        # Recall the function for the recursion for the right child and left child
        Max_diameter_min_cut_partitioning(Tree.children[0])
        Max_diameter_min_cut_partitioning(Tree.children[1])
        # BR is the distance of the right child of the node to the farthest leaf
        BR = Tree.children[0].get_farthest_leaf()[1]
        # BL is the distance of the left child of the node to the farthest leaf
        BL = Tree.children[1].get_farthest_leaf()[1]
        # WR is the distance of the node to its own right child
        WR = Tree.get_distance(Tree.children[0])
        # WL is the distance of the node to its own right child
        WL = Tree.get_distance(Tree.children[1])
        # The condition in the paper
        if (BR + WR + BL + WL) > THRESHOLD:
            # The condition in the paper
            if (BL + WL) <= (BR + WR):
                # This is just for clarification and because the algorithm is recursive it doesnt do anything
                Tree.children[0].detach()
                # The main optimization
                # Here is the actual place that we save the detach node and then use it in μ_tree_distance for 
                # calculating Cluster Diversity that is mentiond in the paper as μ
                NodesForDetach = Tree.children[0]
                # Saving the Cluster Diversity for one cluster for calculating the final μ at the end
                ClusterDiversity.append(μ_tree_distance(Tree))
                # This is also extra because with our approach we dont need BU anymore to make the tree ready 
                # for the next step
                BU = BL + WL
                # Adding one to PARTS for detecting a new cluster
                global PARTS
                PARTS = PARTS + 1
            # The condition in the paper
            else:
                # Same as the is statement
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
        # The condition in the paper
        else:
            # Detecting no Cluster and doing nothing
            BU = max([BL + WL, BR + WR])
        Leaves.append(Tree.get_leaves())

# Calculating the running time
start = time.time()
# Calling the algorithm in the function
Max_diameter_min_cut_partitioning(Tree)
end = time.time()

# Display the result
print("##################### Result #####################")
print(PARTS)
print("------------------------------------------")
print(ClusterDiversity)
print("------------------------------------------")
print(sum(ClusterDiversity))
print("Number of clusters", PARTS)
# We nud to sum up the ClusterDiversity array and div it on number of clusters based on the 
# formula in paper
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
