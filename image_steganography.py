import numpy
import itertools
import cv2


def encrypt(input_path, output_path, message, color_bits_changed=1):
    array_of_char_binary_values = [get_binary_list(ord(c)) for c in message]
    char_binary_values = list(itertools.chain.from_iterable(array_of_char_binary_values))
    img = cv2.imread(input_path)
    img = modify_image(img, char_binary_values, color_bits_changed)
    cv2.imwrite(output_path, img)


def modify_image(img, char_binary_values, color_bits_changed):
    char_index = 0
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    for y in range(height):
        for x in range(width):
            for channel_index in range(channels):
                new_color_binary_array = [binary_digit for binary_digit in get_binary_list(img.item(y, x, channel_index), color_bits_changed)]

                new_color_binary_array[-color_bits_changed:] = char_binary_values[
                                                               char_index:char_index + color_bits_changed]
                new_color_integer = int("".join(new_color_binary_array))
                img.itemset(y, x, channel_index, new_color_integer)
                char_index += color_bits_changed
                if char_index >= len(char_binary_values):
                    return img
    return img


def decrypt(input_path, characters_to_look_for=-1, bytes_per_character=1, color_bits_changed=1):
    bits_per_character = bytes_per_character * 8
    img = cv2.imread(input_path)
    char_binary_value = []
    char_index = 0
    chars_found = 0
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    for y in range(height):
        for x in range(width):
            for channel_index in range(channels):
                color_binary_array = get_binary_list(img.item(y, x, channel_index))
                char_binary_value += color_binary_array[-color_bits_changed:]
                # char_binary_value.append(color_binary_array[-color_bits_changed:])
                char_index += 1
                if char_index % bits_per_character == 0:
                    chars_found += 1
                    char_int = to_integer(char_binary_value)
                    char = chr(char_int)
                    # deal with carriage returns ect
                    print(char, end='')
                    char_binary_value = []
                if chars_found == characters_to_look_for:
                    return


def get_binary_list(integer, length=8):
    binary_list = to_binary(integer)
    if len(binary_list) < length:
        zeros_to_insert = length - len(binary_list)
        for i in range(zeros_to_insert):
            binary_list.insert(0, "0")
    return binary_list


def to_binary(integer):
    binary_base = 2
    if integer < binary_base:
        return [str(integer)]
    quotient = integer // binary_base
    remainder = integer % binary_base
    binary_list = to_binary(quotient)
    binary_list.append(str(remainder))
    return binary_list


def to_integer(binary_array):
    binary_string = "".join(binary_array)
    integer = int(binary_string, 2)
    return integer


if __name__ == "__main__":
    encrypt("kingfishers.jpg", "kingfishers-output.png", "test")
    decrypt("kingfishers-output.png", 45)
    # parse command line arguments, and call appropriate method with parameters

