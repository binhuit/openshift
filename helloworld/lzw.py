import os
import pickle

# init ascii dictionary
# the larger range, the exactly encode (but it make slower)
range_ascii = 256

def init_dict():
    ascii_dict = dict()
    ascii_in_number = range(1,range_ascii)
    for each_char in ascii_in_number:
        ascii_dict[each_char] = chr(int(hex(each_char),16))
    print("Status: Initialized ascii table.")
    dictionary = ascii_dict
    return(dictionary)

def compress(source_path):
    source = open(source_path,"r",encoding='utf-8')
    dictionary = init_dict()
    source_content = source.read()
    lists = list(source_content)
    id = 0
    s = lists[0]
    output_code = list()
    article_name = source.name[:-4]
    output_decimal = open(os.path.join(article_name + "-decimal.txt"),"w",encoding="utf-8")
    output_binary = open(os.path.join(article_name + "-binary.txt"),"w",encoding="utf-8")

    content_len = len(lists)
    dictionary_len = len(dictionary)
    while (id < content_len-1):
        c = lists[id+1]
        print("== check ",id, " {",s,";",c,"}")
        print(s+"\t"+c)
        join = s + c
        if join in dictionary.values():
            s = join
            #step = len(join)+1
            print("s + c {"+join+"} founded")
        else:
            dictionary_len = dictionary_len + 1
            code = next((key for key, value in dictionary.items() if value == s), 63)
            output_code.append(code)
            dictionary.update({dictionary_len:join})
            print("== dictionary update : ",{dictionary_len:join})
            s = c
        code = next((key for key, value in dictionary.items() if value == s), 63)
        #output_code.append(code)
        id = id + 1
        if id+1 == len(lists):
            c = "EOF"
            code = next((key for key, value in dictionary.items() if value == s), 63)
            output_code.append(code)
            break
    # output return table

    sorted(dictionary.items(), key = lambda x:x[1])


    # output return decimal, binary
    for code in output_code:
        output_decimal.write(str(code)+" ")
        print(code)
        print(bin(code))
        output_binary.write(str(bin(code))+" ")
    output_decimal.close()
    output_binary.close()

    # calculate code length
    code_length = len(bin(len(dictionary)))-2
    bin_code = ""
    for c in output_code:
        bin_code += convert_decimal_to_bin(c,code_length)
    redurant_bit = 8 - len(bin_code)%8
    for i in range(redurant_bit):
        bin_code = "0" + bin_code
    length_code_bin = "{0:08b}".format(code_length)
    redurent_bit_bin = "{0:08b}".format(redurant_bit)
    bin_code = length_code_bin + redurent_bit_bin + bin_code
    # print(bin_code)
    # convert bin_code to byte
    bin_code = convert_bin_to_byte(bin_code)
    filename = os.path.split(source.name)[-1][:-4]+"-lzw.bin"
    pickle.dump(bin_code, open(os.path.join('media','result',filename),'wb'))
    print(filename)
    return filename

def decompress(code_path):
    code = open(code_path,"rb")
    print(code.name)
    article_name = os.path.split(code.name)[-1][:-4]
    output_string = list()
    dictionary = init_dict()
    lists = []
    # recover bin_code
    bin_code = pickle.load(code)
    code_length = bin_code[0]
    redurant_bit = bin_code[1]
    code = ""
    for i in bin_code[2:]:
        bi = "{0:08b}".format(i)
        code += bi
    code = code[redurant_bit:]
    for i in range(0, len(code), code_length):
        index_b = code[i:i+code_length]
        index = int(index_b,2)
        lists.append(index)

    filename = article_name+"-decoded.txt"
    dictionary_len = len(dictionary)
    output_decode = open(os.path.join('media','result',filename),"w",encoding="utf-8")
    code_len = len(lists)
    s = None
    id = -1
    while (id < len(lists)-1):
        k = lists[id+1]
        if k == '':
            break
        if int(k) <= dictionary_len:
            entry = dictionary[int(k)]
        else:
            entry = None
        print(k," : ",entry)
        if entry == None:
            if s != None:
                entry = s + s[0]
                print(entry)
            #else:
            #    entry = s

        output_string.append(entry)
        if (s != None):
            dictionary_len = dictionary_len + 1
            print("dictionary update: ",{dictionary_len:s+entry[0]})
            dictionary.update({dictionary_len:s+entry[0]})
        s = entry
        id = id + 1
    sorted(dictionary.items(), key = lambda x:x[1])


    print(output_string)
    print(dictionary)
    print(filename)
    for string in output_string:
        output_decode.write(string)
    output_decode.close()
    return filename

def convert_decimal_to_bin(number, length):
    bi = "{0:012b}".format(number)
    return(bi)

def convert_bin_to_byte(content):
    b = bytearray()
    for i in range(0, len(content), 8):
        byte = content[i:i + 8]
        b.append(int(byte, 2))
    return b
