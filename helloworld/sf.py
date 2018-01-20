import os
import pickle


def init_stat_table(source_content_list):
    """
    :param source_content:
    :return:
    probability table stored like this..
    symbol  count
    """
    prob_table = {}
    # count
    for each_char in source_content_list:
        meet_char = next((key for key, value in prob_table.items() if key == each_char), None)
        if meet_char != None:
            prob_table[each_char] = prob_table[each_char] + 1
        else:
            prob_table.update({each_char:1})
    # calculate prob
    for each_symbol in prob_table:
        prob_table[each_symbol] = prob_table[each_symbol]/len(source_content_list)
    return prob_table

def make_approx(input_dict):
    sorted_dict = dict(sorted(input_dict.items(), key = lambda x:x[1]))
    new_list = [0 for x in range(len(sorted_dict))]
    flag = 0
    id = 0
    left_dict = dict()
    right_dict = dict()
    for each_key in sorted_dict.keys():
        if flag == 0:
            new_list[id] = each_key
            left_dict.update({new_list[id]:sorted_dict[new_list[id]]})
            flag = 1
        else:
            new_list[len(new_list)-id-1] = each_key
            right_dict.update({new_list[len(new_list)-id-1]:sorted_dict[new_list[len(new_list)-id-1]]})
            flag = 0
            id += 1
    return left_dict, right_dict

def sf_recursive(dict_table, string_list, root_code):
    size = len(string_list)
    if size <= 1:
        dict_table[list(string_list)[0]] = root_code
        #print("symbol",list(string_list)[0],"prob:",list(string_list.values())[0],"; code:",root_code)
    else:
        string_list_left, string_list_right = make_approx(string_list)
        sf_recursive(dict_table,string_list_left, root_code + "1")
        sf_recursive(dict_table,string_list_right, root_code + "0")

def compress(source_path):
    source = open(source_path,'r')
    dict_table = {}
    source_content = source.read()
    article_name = source.name[:-4]
    source_content_list = list(source_content)
    sf_recursive(dict_table,init_stat_table(source_content_list), "")

    output_code = list()
    bin_code = ""
    for each_char in source_content_list:
        code = dict_table[each_char]
        output_code.append(code)
        bin_code += code
    redurant_bit = 8 - len(bin_code)% 8
    for i in range(redurant_bit):
        bin_code = '0' + bin_code
    redurant_bit_bin = "{0:08b}".format(redurant_bit)
    bin_code = redurant_bit_bin + bin_code
    bin_code = convert_bin_to_byte(bin_code)
    file_name = os.path.split(source_path)[-1][:-4] + '-sf.bin'
    pickle.dump((dict_table, bin_code),open(os.path.join('media','result', file_name),'wb'))
    return file_name


def convert_bin_to_byte(content):
    b = bytearray()
    for i in range(0, len(content), 8):
        byte = content[i:i + 8]
        b.append(int(byte, 2))
    return b




def decompress(file_path):
    dic, bin_code = pickle.load(open(file_path,'rb'))
    recover_code = ""
    for byte in bin_code:
        recover_code += "{0:08b}".format(byte)
    redurant_bit = int(recover_code[:8],2)
    recover_code = recover_code[8+redurant_bit:]
    dic_reverse = {}
    for key in dic.keys():
        dic_reverse[dic[key]] = key

    current_code = ""
    decoded_text = ""
    for bit in recover_code:
        current_code += bit
        if (current_code in dic_reverse):
            character = dic_reverse[current_code]
            decoded_text += str(character)
            current_code = ""
    file_name = os.path.split(file_path)[-1][:-4]+"-decoded.txt"
    print(file_name)
    with open(os.path.join('media','result',file_name),'w') as f:
        f.write(decoded_text)
    # print(decoded_text)
    return file_name

