class Node:
    def __init__(self, is_leaf):
        self.leaf = is_leaf
        self.keys = []       # sorted keys
        self.values = []     # only meaningful for leaf nodes
        self.child = []      # child pointers (internal node er jonno)
        self.next = None     # leaf-level linked list pointer


class BPlusTree:
    def __init__(self, order=3):
        self.root = None
        self.order = order               # max children per internal node
        self.max_keys = order - 1        # max keys in any node

    #SEARCH
    def search(self, key):
        cur = self.root
        while cur:
            i = 0
            #Leaf node exact match
            if cur.leaf:
                while i < len(cur.keys) and key > cur.keys[i]:
                    i += 1
                if i < len(cur.keys) and cur.keys[i] == key:
                    return cur.values[i]
                return -1  #NOT FOUND

            # Internal node search
            while i < len(cur.keys) and key >= cur.keys[i]:
                i += 1
            cur = cur.child[i]
        return -1

    #COUNT LEAVES
    def count_leaves(self):
        if not self.root:
            print("Total Leaves: 0")
            return
            
        temp = self.root
        while not temp.leaf:
            temp = temp.child[0]
            
        leaf_count = 0
        while temp:
            leaf_count += 1
            temp = temp.next
        print(f"Total Leaves: {leaf_count}")

    #RANGE SEARCH
    def range_search(self, low, high):
        if not self.root:
            return

        cur = self.root
        while not cur.leaf:
            i = 0
            while i < len(cur.keys) and low >= cur.keys[i]:
                i += 1
            cur = cur.child[i]

        # leaf list traversing
        output = []
        while cur:
            for i in range(len(cur.keys)):
                if cur.keys[i] >= low and cur.keys[i] <= high:
                    output.append(f"({cur.keys[i]},{cur.values[i]})")

                if cur.keys[i] > high:
                    print(" ".join(output))
                    return
            cur = cur.next
        print(" ".join(output))

    #INSERT
    def insert(self, key, value):
        if not self.root:
            self.root = Node(True)
            self.root.keys.append(key)
            self.root.values.append(value)
            return


        if len(self.root.keys) == self.max_keys:
            new_root = Node(False)
            new_root.child.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key, value)

    #INSERT NON-FULL
    def _insert_non_full(self, node, key, value):
        if node.leaf:
            # Sorted insertion position searching
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
            node.values.insert(i, value)
            return

        # Internal node
        i = 0
        while i < len(node.keys) and key >= node.keys[i]:
            i += 1

        if len(node.child[i].keys) == self.max_keys:
            self._split_child(node, i)
            if key > node.keys[i]:
                i += 1

        self._insert_non_full(node.child[i], key, value)

    #SPLIT CHILD
    def _split_child(self, parent, idx):
        child = parent.child[idx]
        sibling = Node(child.leaf)
        mid = len(child.keys) // 2

        if child.leaf:
            #Leaf split
            sibling.keys = child.keys[mid:]
            child.keys = child.keys[:mid]

            sibling.values = child.values[mid:]
            child.values = child.values[:mid]

            # Linked list
            sibling.next = child.next
            child.next = sibling

            parent.keys.insert(idx, sibling.keys[0])
        else:
            #Internal split: PUSH-UP
            promo = child.keys[mid]

            sibling.keys = child.keys[mid + 1:]
            child.keys = child.keys[:mid]

            sibling.child = child.child[mid + 1:]
            child.child = child.child[:mid + 1]

            parent.keys.insert(idx, promo)

        # Parent er child list e sibling node ke insert kora
        parent.child.insert(idx + 1, sibling)

    # PRINT (level-order) 
    def print_tree(self):
        if not self.root:
            print("(empty)")
            return

        level = [self.root]
        j = 0

        while level:
            print(j, end="")
            j += 1
            next_level = []
            for n in level:
                print("[", end="")
                print(" ".join(map(str, n.keys)), end="")
                print("] ", end="")

                if not n.leaf:
                    for c in n.child:
                        next_level.append(c)
            print()
            level = next_level

    #PRINT LEAF LINKED LIST
    def print_leaves(self):
        p = self.root
        while p and not p.leaf:
            p = p.child[0]

        output = []
        while p:
            for i in range(len(p.keys)):
                output.append(f"({p.keys[i]},{p.values[i]})")
            p = p.next
        print(" ".join(output))


#Main
if __name__ == "__main__":
    tree = BPlusTree(4) 

    seq = [10, 20, 5, 6, 12, 30, 7, 17, 1, 100, 250, 3]
    for k in seq:
        tree.insert(k, k * 10)

    print("Level-order view:")
    tree.print_tree()

    print("\nLeaf list (key,value):")
    tree.print_leaves()

    tree.count_leaves()

    q = 12
    print(f"\nSearch {q} -> {tree.search(q)}")

    print("\nRange Query:")
    tree.range_search(1, 30)