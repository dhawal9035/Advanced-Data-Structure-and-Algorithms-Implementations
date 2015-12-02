"TODO: Get rid of all flake8 warnings -- that means adding docstrings"
#      to the file, classes, and methods.
import doctest


class SinglyLinkedNode(object):

    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class SinglyLinkedList(object):

    def __init__(self, head=None):
        super(SinglyLinkedList, self).__init__()
        self.head = head
        pass

    def __len__(self):
        current_node = self.head
        count = 0
        while current_node:
            current_node = current_node.next
            count += 1
        return count
        pass

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            yield current_node.item
            current_node = current_node.next
        pass

    def __contains__(self, item):
        flag = 0
        current_node = self.head
        while current_node and flag == 0:
            if current_node.item == item:
                flag = 1
            else:
                current_node = current_node.next
        if flag == 1:
            return True
        else:
            return False
        pass

    def remove(self, item):
        current_node = self.head
        previous_node = None
        flag = 0
        while current_node and flag is 0:
            if current_node.item == item:
                flag = 1
            else:
                previous_node = current_node
                current_node = current_node.next
        if current_node is None:
            print "Node not found in the list"
        if previous_node is None:
            self.head = current_node.next
        else:
            previous_node._next = current_node._next
        pass

    def prepend(self, item):
        new_node = SinglyLinkedNode(item)
        new_node._next = self.head
        self.head = new_node
        pass

    def __repr__(self):
        s = "List:" + "->".join([str(item) for item in self])
        return s

sll = SinglyLinkedList()
sll.prepend(1)
sll.prepend(2)
sll.prepend(3)
sll.prepend(4)
sll.prepend(5)

print sll.__repr__()
print "Check and remove the element if it is present in the linked list"
sll.remove(2)
print sll.__repr__()


class ChainedHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()
        self.bincount = bin_count
        self.load_fac = max_load
        self.size = 0
        self.non_null = 0
        self.table = [{} for i in range(bin_count)]

    @property
    def load_factor(self):
        return self.size/self.bincount
        pass

    @property
    def bin_count(self):
        return self.bincount
        pass

    def rebuild(self, bincount):
        a = [{} for i in range(bin_count)]
        for i in range(bincount):
            if self.table[i] is not None and self.hash_table[i] is not False:
                hashval = self.hash(self.table[i],bincount)
                a[hashval] = self.table[i]
        self.non_null = self.size
        self.bincount = bincount
        self.table = a

    def __getitem__(self, key):
        hashval = hash(key, self.bincount)
        table = self.table[hashval]
        if table.has_key(key):
            return table[key]
        else:
            return None

    def __setitem__(self, key, value):
        hashval = hash(key, self.bincount)
        if 2*(self.non_null+1) > (self.bincount):
            print self.non_null
            self.rebuild(2*self.bincount)
            return
        table = self.table[hashval]
        table[key] = value

    def __delitem__(self, key):
        hashval = hash(key, self.bincount)
        table = self.table[hashval]
        if table.has_key(key):
            del table[key]
        else:
            return None

    def __contains__(self, key):
        hashval = hash(key, self.bincount)
        table = self.table[hashval]
        if table.has_key(key):
            return table.has_key(key)
        else:
            return None

    def __len__(self):
        count = 0
        for i, val in enumerate(self.table):
            count += len(val)
        return count
        pass

    def display(self):
        for i in range(self.bincount):
            print "Bin ", i, ":", self.table[i]
        pass


def hash(x, size):
    return x % size

c = ChainedHashDict()
c[40] = 'a'
c[20] = 'b'
c[25] = 'c'
c[4] = 'd'
c[42] = 'e'


print "Chained Hash Dictionary"
c.display()


class OpenAddressHashDict(object):

    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()
        self.bincount = bin_count
        self.load_fac = max_load
        self.slot = [None for i in range(self.bincount)]
        self.value = [None for i in range(self.bincount)]
        pass

    @property
    def load_factor(self):
        return self.size/self.bincount
        pass

    @property
    def bin_count(self):
        return self.bincount
        pass

    def rebuild(self, bincount):
        self.slot = [None for i in range(self.bincount)]
        self.value = [None for i in range(self.bincount)]
        pass

    def __getitem__(self, key):
        flag = False
        search_stop = False
        hashval = hash(key, self.bincount)
        temp = hashval
        value = None
        while not search_stop and not flag and self.slot[temp] is not None:
            if self.slot[temp] == key:
                flag = True
                value = self.value[temp]
            else:
                temp = self.rehash(temp, self.bincount)
                if hashval == temp:
                    search_stop = True
        return value
        pass

    def __setitem__(self, key, value):
        hashval = hash(key, self.bincount)
        if self.slot[hashval] is None:
            self.slot[hashval] = key
            self.value[hashval] = value
        elif self.slot[hashval] == key:
            self.value[hashval] = value
        else:
            new_slot = self.rehash(hashval, self.bincount)
            while self.slot[new_slot] is not None and self.slot[new_slot] != key:
                new_slot = self.rehash(new_slot,self.bincount)
            if self.slot[new_slot] is None:
                self.slot[new_slot] = key
                self.value[new_slot] = value
            else:
                self.value[new_slot] = value
        pass

    def __delitem__(self, key):
        hashval = hash(key, self.bincount)
        while self.slot[hashval] and self.value[hashval]:
            if self.slot[hashval] == key:
                self.slot[hashval] = None
                self.value[hashval] = None
            else:
                return None

    def __contains__(self, key):
        flag = False
        search_stop = False
        hashval = hash(key, self.bincount)
        temp = hashval
        value = None
        while not search_stop and not flag and self.slot[temp] is not None:
            if self.slot[temp] == key:
                flag = True
                value = self.value[temp]
            else:
                temp = self.rehash(temp, self.bincount)
                if hashval == temp:
                    search_stop = True
        if flag:
            return True
        else:
            return False

    def __len__(self):
        count = 0
        for i in range(self.bincount):
            if self.slot[i] is not None:
                count += 1
            else:
                pass
        return count

    def display(self):
        for i in range(self.bincount):
            print "Bin ", i, ":", "{", self.slot[i], ":", self.value[i], "}"

    def rehash(self, hash_val, size):
        return (hash_val+1) % size


o = OpenAddressHashDict()
o[14] = 'a'
o[16] = 'b'
o[13] = 'c'
o[17] = 'd'
o[37] = 'e'

print "Open Address Hash Dictionary"
o.display()


class CalcKeyVal:

    def __init__(self, key, value):
        self.key = key
        self.value = value


class BinaryTreeNode(object):
    def __init__(self, data, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = CalcKeyVal(data.key, data.value)
        self.left = left
        self.right = right
        self.parent = parent

    @property
    def key(self):
        return self.data.key

    @property
    def value(self):
        return self.data.value

    def put(self, data):
        if self.data.key == data.key:
            self.data.key = data.key
        if self.data.key > data.key:
            if self.left is None:
                self.left = BinaryTreeNode(data, None, None, None)
                self.left.parent = self
            else:
                self.left.put(data)
        else:
            if self.right is None:
                self.right = BinaryTreeNode(data, None, None, None)
                self.right.parent = self
            else:
                self.right.put(data)

    def delete(self, key):
        if self.key > key:
            if self.left is None:
                self.left = self.left.delete(key)
        elif self.key < key:
            if self.right is None:
                self.right = self.right.delete(key)
        else:
            if self.left is None and self.right is None:
                return None
            elif self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            else:
                while self.left.right is not None:
                    self.left = self.left.right
                self.key = self.left.key
                self.left = self.left.delete(self.left.key)
        return self

    def get(self, key):
        if self.key == key:
            return self.data.value
        if self.key > key:
            if self.left is None:
                return None
            else:
                return self.left.get(key)
        else:
            if self.right is None:
                return None
            else:
                return self.right.get(key)

    def inorder_node(self, root):
        if root.left:
            for node_element in self.inorder_node(root.left):
                yield node_element
        yield root
        if root.right:
            for node_element in self.inorder_node(root.right):
                yield node_element

    def postorder_node(self,root):
        if root.left:
            for node_element in self.postorder_node(root.left):
                yield node_element
        if root.right:
            for node_element in self.postorder_node(root.right):
                yield node_element
        yield root

    def preorder_node(self,root):
        yield root
        if root.left:
            for node_element in self.preorder_node(root.left):
                yield node_element
        if root.right:
            for node_element in self.preorder_node(root.right):
                yield node_element

    def traverse(self):
        if self.left is not None:
            max_left = 1 + self.left.traverse()
        else:
            return 0
        if self.right is not None:
            max_right = 1 + self.left.traverse()
        else:
            return 0

        return max(1+max_left, 1+max_right)


class BinarySearchTreeDict(object):

    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.root = None
        self.size = 0
        pass

    @property
    def height(self):
        print self.root.traverse()

    def inorder_keys(self):
        inorder = "Inorder:" + "->".join([str(i.data.key) for i in self.root.inorder_node(self.root)])
        print inorder

    def postorder_keys(self):
        postorder = "Postorder:" + "->".join([str(i.data.key) for i in self.root.postorder_node(self.root)])
        print postorder

    def preorder_keys(self):
        preorder = "Preorder:" + "->".join([str(i.data.key) for i in self.root.preorder_node(self.root)])
        print preorder

    def items(self):
        for i in self.root.inorder_node(self.root):
            print i.data.key

    def __getitem__(self, key):
        if self.root:
            print self.root.get(key)
        else:
            return None
        pass

    def __setitem__(self, key, value):
        data = CalcKeyVal(key,value)
        if self.root is None:
            self.root = BinaryTreeNode(data, None, None, None)
        else:
            self.root.put(data)
        self.size += 1

    def __delitem__(self, key):
        if self.root:
            self.root = self.root.delete(key)
        else:
            return None

    def __contains__(self, key):
        if self.root.get(key):
            return True
        else:
            return False

    def __len__(self):
        return self.size

    def display(self):
        self.inorder_keys()
        self.postorder_keys()


bst = BinarySearchTreeDict()

bst.__setitem__(4, 4)
bst.__setitem__(3, 3)
bst.__setitem__(1, 1)
bst.__setitem__(2, 2)
bst.__setitem__(6, 6)

bst.display()
print "Size is as below:"
bst.height

def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """
    def hashfunc(item):
        return bin
    return hashfunc


def main():
    doctest.testmod()
    # Thoroughly test your program and produce useful out.
    #
    # Do at least these kinds of tests:
    #  (1)  Check the boundary conditions (empty containers,
    #       full containers, etc)
    #  (2)  Test your hash tables for terrible hash functions
    #       that map to keys in the middle or ends of your
    #       table
    #  (3)  Check your table on 100s or randomly generated
    #       sets of keys to make sure they function
    #
    #  (4)  Make sure that no keys / items are lost, especially
    #       as a result of deleting another key
    pass


if __name__ == '__main__':
    main()
