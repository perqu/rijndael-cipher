"""
# ---------------------------------------------------------------
# Program:    cipher.py
# Version:    0.0.1 - 2021 April 11
# Author:    Pawel Perenc
# Released on:    Github
# Purpose:    Recruitment task / Learning
#
# Description:
# Advanced Encryption Standard (AES)
# This program is an implementation of a FIPS 197 standard
# that specifies the Rijndael algorithm, a symmetric block
# cipher that can process data blocks of 128 bits, using
# cipher keys with lengths of 128 bits
# ---------------------------------------------------------------
"""
import random
import os


def read_sbox(size):
    """
    Reads inside key (sbox) from file: "sbox.txt" \n
    if such a file does not exist, the generate_inside_key function generates this file.

    Args:
        size - amount of columns/rows - number of type int

    Returns:
        sbox values - List of type int
    """

    if not os.path.exists("data/sbox.txt"):
        generate_inside_key(size)

    sbox = []
    with open("data/sbox.txt", "r") as file:
        fields = file.read().strip().split(" ")
        for number in fields:
            sbox.append(int(number, 0))

    return sbox


def read_inv_sbox(size):
    """
    Reads inverted key (inv_sbox) from file: "inv_sbox.txt" \n
    if such a file does not exist, the generate_inside_key function generates this file.

    Args:
        size - amount of columns/rows - number of type int

    Returns:
        inv_sbox values - List of type int
    """

    if not os.path.exists("data/inv_sbox.txt"):
        generate_inside_key(size)

    inv_sbox = []
    with open("data/inv_sbox.txt", "r") as file:
        fields = file.read().strip().split(" ")
        for number in fields:
            inv_sbox.append(int(number, 0))

    return inv_sbox


def generate_inside_key(size):
    """
    Generate inside key (sbox) and inverted key (inv_sbox) \n
    Saves values to files: "sbox.txt", "inv_sbox.txt"

    Args:
        size - amount of columns/rows - number of type int

    Returns:
        None
    """

    list_xy = []
    sbox = []
    inv_sbox = []
    for i in range(size**2):
        list_xy.append(i)

    for i in range(size**2):
        inv_sbox.append(None)

    for i in range(size**2):
        rand_num = random.randrange(0, len(list_xy))
        rand_element = list_xy[rand_num]
        inv_sbox[rand_element] = i
        sbox.append(list_xy.pop(rand_num))

    with open("data/sbox.txt", "w") as file:
        for counter, item in enumerate(sbox, 1):
            file.write("0x{:02x} ".format(item))
            if counter % 16 == 0:
                file.write("\n")

    with open("data/inv_sbox.txt", "w") as file:
        for counter, item in enumerate(inv_sbox, 1):
            file.write("0x{:02x} ".format(item))
            if counter % 16 == 0:
                file.write("\n")


def read_user_key():
    """
    Reads user key (KEY) from file: "KEY.txt" \n

    Args:
        None

    Returns:
        KEY values - List of type int
    """

    key = []
    with open("data/key.txt", "r") as file:
        fields = file.read().strip().split(" ")
        for number in fields:
            key.append(int(number, 0))
    return key


def read_rcon(size):
    """
    Reads rcon values from file: "rcon.txt" \n
    if such a file does not exist, the generate_rcon function generates this file.

    Args:
        size - amount of columns/rows - number of type int

    Returns:
        rcon values - List of type int
    """

    if not os.path.exists("data/rcon.txt"):
        generate_rcon(size)
    rcon = []
    with open("data/rcon.txt", "r") as file:
        fields = file.read().strip().split(" ")
        for number in fields:
            rcon.append(int(number, 0))

    return rcon


def generate_rcon(size):
    """
    Generate rcon values \n
    Saves values to file: "rcon.txt"

    Args:
        size - amount of columns/rows - number of type int

    Returns:
        None
    """

    def generate_rcon_number(number):
        c = 1
        if number == 0:
            return 0
        elif number == 1:
            return c
        for i in range(number, 1, -1):
            b = c & 0x80
            c <<= 1
            if b == 0x80:
                c ^= 0x1B
        return c

    with open("data/rcon.txt", "w") as file:
        for i in range(size**2):
            file.write("0x" + ("{:02x}".format(generate_rcon_number(i))[-2:]) + " ")
            if i % 16 == 15:
                file.write("\n")


def create_blocks(message, size, calling_function):
    """
    Creates blocks (size x size) of ASCII values from string

    Args:
        message - text containing ASCII codes or letters of type string
        size - amount of columns/rows - number of type int
        calling_function - type string ('decoder' or 'encoder')

    Returns:
        Values of ASCII representation from delivered string - List of lists (blocks)
    """

    if calling_function == "decoder":
        blocks = []
        message = list(map(int, message.strip().split(" ")))
        while len(message) > 0:
            message_block = message[:size]
            while len(message) < size:
                message_block.append(3)
            message = message[size:]
            blocks.append(message_block)
        return blocks
    elif calling_function == "encoder":
        blocks = []
        while len(message) > 0:
            message_block = []
            while len(message) < size:
                message += chr(3)
            for i in range(size):
                message_block.append(ord(message[i]))
            message = message[size:]
            blocks.append(message_block)
        return blocks
    return 0


def sub_bytes(block, size, sbox):
    """
    Translating all block values by byte substitution table (sbox)

    Args:
        block - an list to translate of numbers of type int
        size - amount of columns/rows - number of type int
        sbox - byte substition table - a list of type int

    Returns:
        block - translated by sbox values - List of type int
    """

    for i in range(size):
        block[i] = sbox[block[i]]
    return block


def inv_sub_bytes(block, size, inv_sbox):
    """
    Translating all block values by inverted byte substitution table (inv_sbox)

    Args:
        block - an list to translate of numbers of type int
        size - amount of columns/rows - number of type int
        inv_sbox - inverted byte substition table - a list of type int

    Returns:
        block - translated by inv_sbox values - List of type int
    """

    for i in range(size):
        block[i] = inv_sbox[block[i]]
    return block


def rotate_rows(block, rows_rotates):
    """
    Rotating over rows_rotates values, ex.  \n

    rows_rotates = (0,1,2,3)                \n
    n0 n1 n2 n3   -->   n0 n1 n2 n3         \n
    n4 n5 n6 n7   -->   n5 n6 n7 n4         \n
    n8 n9 na nb   -->   na nb n8 n9         \n
    nc nd ne nf   -->   nf nc nd ne         \n

    Args:
        block - an list to rotate of numbers of type int
        rows_rotates - numbers of rotates (1st row, 2nd row, 3rd row, 4th row)

    Returns:
        block - list after rotates - List of type int
    """

    for row, row_rotates in enumerate(rows_rotates):
        for i in range(row_rotates):
            temp = block[row * 4]
            block[row * 4] = block[row * 4 + 1]
            block[row * 4 + 1] = block[row * 4 + 2]
            block[row * 4 + 2] = block[row * 4 + 3]
            block[row * 4 + 3] = temp
    return block


def inv_rotate_rows(block, rows_rotates):
    """
    Rotating over rows_rotates values in reverse direction, ex.  \n

    rows_rotates = (0,1,2,3)                \n
    n0 n1 n2 n3   -->   n0 n1 n2 n3         \n
    n5 n6 n7 n4   -->   n4 n5 n6 n7         \n
    na nb n8 n9   -->   n8 n9 na nb         \n
    nf nc nd ne   -->   nc nd ne nf         \n

    Args:
        block - an list to rotate of numbers of type int
        rows_rotates - numbers of rotates (1st row, 2nd row, 3rd row, 4th row)

    Returns:
        block - list after rotates - List of type int
    """

    for row, row_rotates in enumerate(rows_rotates):
        for i in range(row_rotates):
            temp = block[row * 4 + 3]
            block[row * 4 + 3] = block[row * 4 + 2]
            block[row * 4 + 2] = block[row * 4 + 1]
            block[row * 4 + 1] = block[row * 4]
            block[row * 4] = temp
    return block


def GF(numb_1, numb_2):
    """
    Interpretation of Galois multiplication of 2 numbers a and b

    Args:
        a - first value of type int
        b - second value of type int

    Returns:
        result of GF(2) multiplication
    """
    result = 0
    for i in range(8):
        if (numb_2 & 1) == 1:
            result = result ^ numb_1
        if result > 0x100:
            result = result ^ 0x100
        bit_set = numb_1 & 0x80
        numb_1 = numb_1 << 1
        if numb_1 > 0x100:
            numb_1 = numb_1 ^ 0x100
        if bit_set == 0x80:
            numb_1 = numb_1 ^ 0x1B
        if numb_1 > 0x100:
            numb_1 = numb_1 ^ 0x100
        numb_2 = numb_2 >> 1
        if numb_2 > 0x100:
            numb_2 = numb_2 ^ 0x100
    return result


def mix_columns(block):
    """
    All block numbers are modulo multiplied       \n
    in Rijndael's Galois Field by a given matrix. \n
    To mix values the below matrix was used:      \n
    02 03 01 01                                   \n
    01 02 03 01                                   \n
    01 01 02 03                                   \n
    03 01 01 02                                   \n

    Args:
        block - an list to be multiplied of numbers of type int

    Returns:
        new_block - list after multiplication - List of type int
    """

    new_block = []
    for i in range(0, 16, 4):
        new_block.append(
            GF(2, block[i])
            ^ GF(3, block[i + 1])
            ^ GF(1, block[i + 2])
            ^ GF(1, block[i + 3])
        )
        new_block.append(
            GF(1, block[i])
            ^ GF(2, block[i + 1])
            ^ GF(3, block[i + 2])
            ^ GF(1, block[i + 3])
        )
        new_block.append(
            GF(1, block[i])
            ^ GF(1, block[i + 1])
            ^ GF(2, block[i + 2])
            ^ GF(3, block[i + 3])
        )
        new_block.append(
            GF(3, block[i])
            ^ GF(1, block[i + 1])
            ^ GF(1, block[i + 2])
            ^ GF(2, block[i + 3])
        )
    return new_block


def inv_mix_columns(block):
    """
    All block numbers are modulo multiplied       \n
    in Rijndael's Galois Field by a given matrix. \n
    To mix values the below matrix was used:      \n
    14 11 13 09                                   \n
    09 14 11 13                                   \n
    13 09 14 11                                   \n
    11 13 09 14                                   \n

    Args:
        block - an list to be multiplied of numbers of type int

    Returns:
        new_block - list after multiplication - List of type int
    """

    new_block = []
    for i in range(0, 16, 4):
        new_block.append(
            GF(14, block[i])
            ^ GF(11, block[i + 1])
            ^ GF(13, block[i + 2])
            ^ GF(9, block[i + 3])
        )
        new_block.append(
            GF(9, block[i])
            ^ GF(14, block[i + 1])
            ^ GF(11, block[i + 2])
            ^ GF(13, block[i + 3])
        )
        new_block.append(
            GF(13, block[i])
            ^ GF(9, block[i + 1])
            ^ GF(14, block[i + 2])
            ^ GF(11, block[i + 3])
        )
        new_block.append(
            GF(11, block[i])
            ^ GF(13, block[i + 1])
            ^ GF(9, block[i + 2])
            ^ GF(14, block[i + 3])
        )
    return new_block


def key_schedule(key, rcon, sbox):
    """
    Generates a key schedule from a user-supplied key

    Args:
        key - key provided by user - list of type int
        rcon - list with rcon codes generated by other function
        sbox - byte substition table - a list of type int

    Returns:
        round_keys - all keys prepared for each round stored in matrixs - list of lists of type int
    """

    def rotate_key(key):
        """
        Rotates the values ​​contained in the key by 90* to make the algorithm easier to implement
                                                \n
        n0 n1 n2 n3   -->   n3 n7 nb nf         \n
        n4 n5 n6 n7   -->   n2 n6 na ne         \n
        n8 n9 na nb   -->   n1 n5 n9 nd         \n
        nc nd ne nf   -->   n0 n4 n8 nc         \n

        Args:
            key - key provided by user - list of type int

        Returns:
            key - rotated key values by 90* - list of type int
        """

        new_key = []
        i = 0
        while len(new_key) < len(key):
            new_key.append(key[12 + i])
            new_key.append(key[8 + i])
            new_key.append(key[4 + i])
            new_key.append(key[0 + i])
            i += 1
        return new_key

    key = rotate_key(key)
    i = 1
    while len(key) < 11 * 16:
        length = len(key)
        key.append(key[length - 16] ^ sbox[key[length - 1]] ^ 0)
        key.append(key[length - 15] ^ sbox[key[length - 4]] ^ 0)
        key.append(key[length - 14] ^ sbox[key[length - 3]] ^ 0)
        key.append(key[length - 13] ^ sbox[key[length - 2]] ^ rcon[i])

        for j in range(3):
            length = len(key)
            key.append(key[length - 16] ^ key[length - 4])
            key.append(key[length - 15] ^ key[length - 3])
            key.append(key[length - 14] ^ key[length - 2])
            key.append(key[length - 13] ^ key[length - 1])

        i += 1

    round_keys = []
    while len(key) > 0:
        round_keys.append(key[:16])
        key = key[16:]
    return round_keys


def add_round_key(block, round_key, size):
    """
    Processes all values ​​in the block using "bitwise \n
    exclusive or" with values ​​of the round key

    Args:
        block - an list to rotate of numbers of type int
        round_key - key generated by key_schedule for existing round - list of type int
        size - amount of columns/rows - number of type int

    Returns:
        block - values after including round_key - List of type int
    """

    for i in range(size):
        block[i] = block[i] ^ round_key[i]
    return block


def encoder(string_text, size, rotate_rows_schema, sbox, round_keys):
    """
    Recreates the entire Rijndael encryption scheme

    Args:
        string_text - delivered by user text to be encrypted of type string
        size - amount of columns/rows - number of type int
        rotate_rows_schema - four digit one for each row in a tuple ex. (0,1,2,3)
        sbox - byte substition table - a list of type int
        round_keys - keys generated by key_schedule for all rounds - list of lists of type int

    Returns:
        output - encrypted text of type string
    """

    blocks = create_blocks(string_text, size, "encoder")
    actual_round = 0
    for block in blocks:
        block = add_round_key(block, round_keys[0], size)

    actual_round += 1
    for i in range(9):
        for block in blocks:
            block = sub_bytes(block, size, sbox)

        for block in blocks:
            block = rotate_rows(block, rotate_rows_schema)

        temp = []
        for block in blocks:
            temp.append(mix_columns(block))
        blocks = temp

        for block in blocks:
            block = add_round_key(block, round_keys[actual_round], size)
        actual_round += 1

    for block in blocks:
        block = sub_bytes(block, size, sbox)

    for block in blocks:
        block = rotate_rows(block, rotate_rows_schema)

    for block in blocks:
        block = add_round_key(block, round_keys[actual_round], size)

    output = ""
    for block in blocks:
        for char in block:
            output += str(char) + " "

    return output.strip()


def decoder(string_text, size, rotate_rows_schema, inv_sbox, round_keys):
    """
    Recreates the entire Rijndael decryption scheme

    Args:
        string_text - delivered by user text to be decrypted of type string
        size - amount of columns/rows - number of type int
        rotate_rows_schema - four digit one for each row in a tuple ex. (0,1,2,3)
        inv_sbox - inversed byte substition table - a list of type int
        round_keys - keys generated by key_schedule for all rounds - list of lists of type int

    Returns:
        output - decrypted text of type string
    """

    blocks = create_blocks(string_text, size, "decoder")
    actual_round = 10
    for block in blocks:
        block = add_round_key(block, round_keys[actual_round], size)

    for block in blocks:
        block = inv_rotate_rows(block, rotate_rows_schema)
    ## tu wypada
    for block in blocks:
        block = inv_sub_bytes(block, size, inv_sbox)

    actual_round -= 1

    for i in range(9):
        for block in blocks:
            block = add_round_key(block, round_keys[actual_round], size)

        for j in range(1):
            temp = []
            for block in blocks:
                temp.append(inv_mix_columns(block))
            blocks = temp

        for block in blocks:
            block = inv_rotate_rows(block, rotate_rows_schema)

        for block in blocks:
            block = inv_sub_bytes(block, size, inv_sbox)
        actual_round -= 1

    for block in blocks:
        block = add_round_key(block, round_keys[actual_round], size)

    output = ""
    for block in blocks:
        for char in block:
            if char != 3:
                output += chr(char)

    return output


def encode_message(message):
    """
    Preparing all needed data and run function that \n
    recreate the entire Rijndael encryption scheme
    Args:
        message - delivered by user text to be encrypted of type string
    Returns:
        output - encrypted text of type string
    """

    if not os.path.exists("data/key.txt"):
        return None

    size = 16
    rotate_rows_schema = (0, 1, 2, 3)

    rcon = read_rcon(size)
    sbox = read_sbox(size)

    round_keys = key_schedule(read_user_key(), rcon, sbox)

    encoded_message = encoder(message, size, rotate_rows_schema, sbox, round_keys)

    if os.path.exists("data/key.txt"):
        os.remove("data/key.txt")

    return encoded_message


def decode_message(message):
    """
    Preparing all needed data and run function that \n
    recreate the entire Rijndael decryption scheme
    Args:
        message - delivered by user text to be decrypted of type string
    Returns:
        output - decrypted text of type string
    """

    if not os.path.exists("data/key.txt"):
        return None

    size = 16
    rotate_rows_schema = (0, 1, 2, 3)

    rcon = read_rcon(size)
    sbox = read_sbox(size)
    inv_sbox = read_inv_sbox(size)
    round_keys = key_schedule(read_user_key(), rcon, sbox)

    decoded_message = decoder(message, size, rotate_rows_schema, inv_sbox, round_keys)

    if os.path.exists("data/key.txt"):
        os.remove("data/key.txt")

    return decoded_message


def add_key(provided_key):
    """
    Save key provided by user to file "KEY.txt". \n
    Key would be ready for next operation, after \n
    will be deleted

    Args:
        key - key provided by user - list of type int

    Returns:
        output - True if key was suitable, otherwise False
    """
    if len(provided_key) == 16:
        with open("data/key.txt", "w") as file:
            for counter, char in enumerate(provided_key, 1):
                file.write("0x{:02x} ".format(ord(char)))
                if counter % 4 == 0:
                    file.write("\n")
        return True
    return False
