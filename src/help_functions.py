import os
import json


def write_to_file(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()


def write_to_bin_file(filepath, content):
    f = open(filepath, 'wb')
    f.write(content)
    f.close()


def read_file(filepath):
    with open(filepath) as f:
        content = f.readlines()
        return content


def read_bin_file(filepath):
    with open(filepath, "rb") as f:
        B = []
        byte = f.read(1)
        B.append(byte)
        while byte != b"":
            byte = f.read(1)
            B.append(byte)
        return b''.join(B)


def byte_2_hex(byteStr):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    a = ''.join(["%02X " % ord(x) for x in byteStr]).strip()
    print(a)

    return [chr(int(num, 16)) for num in a.split(' ') if (num is not '78' and num is not '5C')]


def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length]) * length
    return data


def unpad(data):
    return data[:-data[-1]]


def get_random_bytes(length):
    return os.urandom(length)


def bytes_2_string(B):
    return B.decode("latin-1")


def string_2_bytes(s, encoding):
    return bytes(s, encoding)


def write_keys_to_file(keys, filepaths, bin=False):
    if (len(keys) != len(filepaths)):
        raise SyntaxError('Keys and filepaths lists must have same length.')
    for i in range(len(keys)):
        if (bin):
            write_to_bin_file(filepaths[i], keys[i])
        else:
            write_to_file(filepaths[i], keys[i])


def write_obj_to_json_file(obj, filepath):
    with open(filepath, 'w') as outfile:
        json.dump(obj, outfile)


def read_json_file(filepath):
    with open(filepath) as data_file:
        return json.load(data_file)



def files_in_dir(path):
    files = os.listdir(path)

    try:
        curr_json = read_json_file('../Private/document_index.json')
    except IOError:
        print('Cannot open file at: ../Private/document_index.json')
        return False

    # -1 because of 'current_value' key
    if (len(files) == len(curr_json)-1):
        print('Document index is already up to date.')
        return [curr_json, []]

    # update json file
    changed_ids = []
    current_value = curr_json['current_value'] if 'current_value' in curr_json else 0
    if (len(files) > len(curr_json)-1):
        for i in range(len(files)):
            if (files[i] not in curr_json):
                curr_json[files[i]] = current_value
                changed_ids.append(current_value)
                current_value += 1
        curr_json['current_value'] = current_value
    else:
        delete_keys = []
        for key, value in curr_json.items():
            if (key not in files and key != 'current_value'):
                delete_keys.append(key)
                changed_ids.append(value)

        for del_key in delete_keys:
            curr_json.pop(del_key, None)

    # save updated version
    write_obj_to_json_file(curr_json, '../Private/document_index.json')

    return [curr_json, changed_ids]



