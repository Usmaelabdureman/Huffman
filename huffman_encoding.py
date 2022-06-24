import sys
from  queues import Queue

def Compress(data):
    if data == '':
        return None, ''
    tree = build_tree(data)
    dict = get_codes(tree.root)
    codes = ''
    for char in data:
        codes += dict[char]
    return tree, codes

# The function traverses over the encoded data and checks if a certain piece of binary code could actually be a letter
def Decompress(data, tree):
    if data == '':
        return ''
    dict = get_codes(tree.root)
    reversed_dict = {}
    for value, key in dict.items():
        reversed_dict[key] = value
    start_index = 0
    end_index = 1
    max_index = len(data)
    plaintext = ''

    while start_index != max_index:
        if data[start_index : end_index] in reversed_dict:
            plaintext += reversed_dict[data[start_index : end_index]]
            start_index = end_index
        end_index += 1

    return plaintext

class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_left_child(self, left):
        self.left = left

    def set_right_child(self, right):
        self.right = right

    def get_left_child(self):
        return self.left

    def get_right_child(self):
        return self.right

    def has_left_child(self):
        return self.left != None

    def has_right_child(self):
        return self.right != None

    def __repr__(self):
        return f"Node({self.get_value()})"

    def __str__(self):
        return f"Node({self.get_value()})"

class Tree:
    def __init__(self):
        self.root = None

    def set_root(self, value):
        self.root = Node(value)

    def get_root(self):
        return self.root
    def __repr__(self):
        level = 0
        q = Queue()
        visit_order = list()
        node = self.get_root()
        q.enq((node, level))
        while (len(q) > 0):
            node, level = q.deq()
            if node == None:
                visit_order.append(("<empty>", level))
                continue
            visit_order.append((node, level))
            if node.has_left_child():
                q.enq((node.get_left_child(), level + 1))
            else:
                q.enq((None, level + 1))
            if node.has_right_child():
                q.enq((node.get_right_child(), level + 1))
            else:
                q.enq((None, level + 1))
        s = "Tree\n"
        previous_level = -1
        for i in range(len(visit_order)):
            node, level = visit_order[i]
            if level == previous_level:
                s += " | " + str(node)
            else:
                s += "\n" + str(node)
                previous_level = level

        return s
def return_frequency(data):
    # Take a string and determine the relevant frequencies of the characters
    frequency = {}
    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    lst = [(v, k) for k, v in frequency.items()]
    lst.sort(reverse=True)
    return lst

# A helper function to the build_tree()
def Sort_tree(nodes_list, node):
    node_value, char1 = node.value
    index = 0
    max_index = len(nodes_list)

    while True:
        if index == max_index:
            nodes_list.append(node)
            return
        current_val, char2 = nodes_list[index].value
        if current_val <= node_value:
            nodes_list.insert(index, node)
            return
        index += 1
# Build a Huffman Tree: nodes are stored in list with their values (frequencies) in descending order.
# Two nodes with the lowest frequencies form a tree node. That node gets pushed back into the list and the process repeats
def build_tree(data):
    lst = return_frequency(data)
    nodes_list = []
    for node_value in lst:
        node = Node(node_value)
        nodes_list.append(node)

    while len(nodes_list) != 1:
        first_node = nodes_list.pop()
        second_node = nodes_list.pop()
        val1, char1 = first_node.value
        val2, char2 = second_node.value
        node = Node((val1 + val2, char1 + char2))
        node.set_left_child(second_node)
        node.set_right_child(first_node)
        Sort_tree(nodes_list, node)

    root = nodes_list[0]
    tree = Tree()
    tree.root = root
    return tree

# the function traverses over the huffman tree and returns a dictionary with letter as keys and binary value and value.
# function get_codes() is for encoding purposes
def get_codes(root):
    if root is None:
        return {}
    frequency, characters = root.value
    char_dict = dict([(i, '') for i in list(characters)])

    left_child = get_codes(root.get_left_child())

    for key, value in left_child.items():
        char_dict[key] += '0' + left_child[key]
    right_child = get_codes(root.get_right_child())
    for key, value in right_child.items():
        char_dict[key] += '1' + right_child[key]
    return char_dict

def test():
    # fileName=input("Enter the name of the file")
    sentences_file = open("data.txt", "r")
    sentences = sentences_file.readlines()

    for number, senctence in enumerate(sentences, 1):
        print("*"*30)
        print("* Test {} \n".format(str(number)))
        print("*"*30)


        print("The size of the data Before Encoded is: {}".format(sys.getsizeof(senctence)))
        print("The content of the data is: [{}]\n".format(senctence))
        print("Encoding process Begins Here:\n")


        tree, encoded_data = Compress(senctence)
        print("The size of the encoded data After Encoded is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
        print("The content of the encoded data is: [ {} ]\n".format(encoded_data))


        print("\nDecoding Begins Here::")
        decoded_data = Decompress(encoded_data, tree)
        print("\nThe size of data after decoded is: {}".format(sys.getsizeof(decoded_data)))
        print("\nThe content of the decoded data is: [ {} ] ".format(decoded_data))
    sentences_file.close()
if __name__=="__main__":
    test()