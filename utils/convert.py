convert_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def dec_2_62(id):
    id = int(id)
    index_list = []
    append = index_list.append
    base = convert_table.__len__()

    while id > 0:
        remainder = id % 62
        append(remainder - 1)
        id = id // base
    return index_list


def get_code(id):
    index_list = dec_2_62(id)
    code = ''
    for i in range(len(index_list)):
        code += convert_table[index_list[i]]
    fill_length = 6 - code.__len__()
    code += 'a' * fill_length
    return code


if __name__ == '__main__':
    code = get_code()
    print(code)
