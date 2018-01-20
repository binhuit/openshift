import heapq
import operator
import os
from bitstring import BitArray
import json
import pickle
import codecs

DIR_DATA = "media/"
DIR_HUFFMAN = DIR_DATA
#using to save dictionary
temp_reverse = {}
#init a seperate sympol as Node of Huffman Tree with value = frequency
class Node:
    #build a class node with sympol, frequency, left node, right node
    def __init__(self,sympol=None,frequency=None,left_node=None,right_node=None):
        self.sympol = sympol
        self.frequency = frequency
        self.left_node = left_node
        self.right_node = right_node
    # defining comparators less_than
    def __lt__(self, other):
        return self.frequency < other.frequency
#init table frequency of all seperate sympols in text
def count_frequency(content):
    table_frequency = {}
    for sym in content:
        if not sym in table_frequency:
            table_frequency[sym] = 0;
        table_frequency[sym] +=1
    return table_frequency
#sort table frequency min - max
def sort_table_frequency(table_frequency):
    sorted_table_frequency = sorted(table_frequency.items(), key=operator.itemgetter(1))
    sorted_table_frequency = dict(sorted_table_frequency)
    return sorted_table_frequency
#make a Huffman tree with min heap
def tree_maker(tree,table_frequency):
    #init sympol is a Node
    for each_sym in table_frequency:
        node = Node(each_sym,table_frequency[each_sym])
        heapq.heappush(tree,node)
    #add node into tree until having a node with weight max
    while (len(tree)>1):
        #take 2 node having min frequency and add to tree
        nodel = heapq.heappop(tree)
        noder = heapq.heappop(tree)
        #create an internal node with frequency = sum of 2 node above
        internal_weight = nodel.frequency + noder.frequency
        internal_node = Node(None,internal_weight,nodel,noder)
        heapq.heappush(tree,internal_node)
    return tree
#creat path to all sympols by reverse tree
def encode_reverse(encoded_sympol,temp_reverse,parent, temp_way):
    if (parent == None ):
        return
    if (parent.sympol != None):
        encoded_sympol[parent.sympol] = temp_way
        temp_reverse[temp_way] = parent.sympol
        return
    #recursion to find paths
    encode_reverse(encoded_sympol,temp_reverse,parent.left_node,temp_way + "0")
    encode_reverse(encoded_sympol,temp_reverse,parent.right_node,temp_way + "1")
#create dictionary with sympol and code
def encoded(encoded_sympol,temp_reverse,tree):
    parent = heapq.heappop(tree)
    temp_path = ""
    encode_reverse(encoded_sympol,temp_reverse,parent,temp_path)
#encode text to code
def convert_text_to_code(encoded_sympol,content):
    encoded_content = ""
    for sym in content:
        encoded_content = encoded_content + encoded_sympol[sym]
    #print (encoded_content)
    return encoded_content
#convert bin to byte,must len(code)%8 = 0, add k "0" into code and convert k to bin and save code together
def prepare_to_convert_bin_to_byte(content):
    added_code = 8 - len(content) % 8
    for i in range(added_code):
        content = "0" + content
    encoded_added_code = "{0:08b}".format(added_code)
    content = encoded_added_code + content
    return content
#convert bin to byte
def convert_bin_to_byte(content):
    b = bytearray()
    for i in range(0, len(content), 8):
        byte = content[i:i + 8]
        b.append(int(byte, 2))
    return b
#compress
def compress(path):
    temp_reverse = {}
    tree = []
    encoded_sympol = {}
    tempname, _ = os.path.splitext(path)
    filename = tempname.split("/")
    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()
        frequency = count_frequency(content)
        table_frequency = sort_table_frequency(frequency)
        tree = tree_maker(tree,table_frequency)
        encoded_tree = encoded(encoded_sympol,temp_reverse,tree)
        file_dict = os.path.join(DIR_HUFFMAN,filename[-1] + ".dict")
        encoded_content = convert_text_to_code(encoded_sympol,content)
        new_content = prepare_to_convert_bin_to_byte(encoded_content)
        byte_content = convert_bin_to_byte(new_content)

    file_com = os.path.join(DIR_HUFFMAN,"result", filename[-1] + ".bin")
    pickle.dump((temp_reverse, byte_content), open(file_com,'wb'))
    print ("Completely compressed")
    return file_com
#decode code
def decode(new_content):
    temp = new_content.bin
    added_num_info = temp[:8]
    added_num = int(added_num_info, 2)
    temp = temp[8:]
    return temp[added_num:]
#decompress
def decompress(path):
    pack = pickle.load(open(path,'rb'))
    temp_reverse = pack[0]
    content = pack[1]
    new_content = BitArray(bytes = content)
    new_content = decode(new_content)
    current_code = ""
    decoded_text = ""
    for bit in new_content:
        current_code += bit
        if (current_code in temp_reverse):
            character = temp_reverse[current_code]
            decoded_text += character
            current_code = ""
    temp_reverse.clear()
    tempname, _ = os.path.splitext(path)
    filename = tempname.split("/")
    file_decom = "media/result/" + filename[-1] + "-decoded" + ".txt"
    with codecs.open(file_decom, "w+", encoding='utf-8') as o:
        o.write(decoded_text)
    print("Completely decompressed")
    return filename[-1] + "-decoded" + ".txt"
