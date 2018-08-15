import cv2


def conceal_text_in_image(input_path, output_path, text, color_bits_changed=1):
    binary = get_binary_from_text(text)
    print("Text size: " + bit_format(len(binary)))
    img = cv2.imread(input_path)
    print("Image capacity: " + bit_format(get_image_capcity(img, color_bits_changed)))
    img = conceal_binary_in_image(img, binary, color_bits_changed)
    cv2.imwrite(output_path, img)


def unconceal_text_in_image(input_path, chars_to_look_for=0, bits_per_char=8, color_bits_changed=1):
    img = cv2.imread(input_path)
    number_of_bits = chars_to_look_for * bits_per_char
    binary = unconceal_binary_in_image(img, number_of_bits, color_bits_changed)
    text = get_text_from_binary(binary, bits_per_char)
    # replaces carriage returns with newlines for printing
    text = text.replace('\r', '\n')
    print(text)


def conceal_file_in_image(input_path, output_path, file_path, color_bits_changed=1):
    binary = get_binary_from_file(file_path)
    print("\tSize: " + bit_format(len(binary)))
    img = cv2.imread(input_path)
    print("Image capacity: " + bit_format(get_image_capcity(img, color_bits_changed)))
    img = conceal_binary_in_image(img, binary, color_bits_changed)
    cv2.imwrite(output_path, img)


def unconceal_file_in_image(input_path, output_path, number_of_bits, color_bits_changed=1):
    img = cv2.imread(input_path)
    binary = unconceal_binary_in_image(img, number_of_bits, color_bits_changed)
    get_file_from_binary(binary, output_path)


def conceal_binary_in_image(img, binary, color_bits_changed):
    binary_index = 0
    binary_list = list(binary)
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    for y in range(height):
        for x in range(width):
            for channel in range(channels):
                # Color is a list of binary digits
                #   [2:] removes the leaving "0b", as all values will be positive
                #   zfill adds the required amount of leading 0's, so color[-color_bits_changed:] works
                color = list(bin(img.item(y, x, channel))[2:].zfill(color_bits_changed))
                # Changes the last number of binary digits of color to a section of the binary_list
                color[-color_bits_changed:] = binary_list[binary_index:binary_index + color_bits_changed]
                # Calculates the new integer color value
                new_color = int("".join(color), 2)
                img.itemset(y, x, channel, new_color)
                binary_index += color_bits_changed
                if binary_index > len(binary_list):
                    image_capacity_left = (((height - y) * width - (x + 1)) * channels + (channel + 1)) * color_bits_changed
                    print("Space left in image: " + bit_format(image_capacity_left))
                    return img
    bits_left = len(binary_list) - (binary_index + 1)
    if bits_left == 0:
        print("No space left in image")
    else:
        print("Not enough space in image. Discarded: " + bit_format(bits_left))
    return img


def unconceal_binary_in_image(img, binary_values_to_look_for=0, color_bits_changed=1):
    # Starts at 1 so if binary_values_to_look_for=0 (the default) all the binary values are returned
    values_found = 1
    binary_list = []
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    for y in range(height):
        for x in range(width):
            for channel in range(channels):
                # Color is a list of binary digits. bin gets the number as a binary string
                #   [2:] removes the leaving "0b", as all values will be positive
                #   zfill adds the required amount of leading 0's, so color[-color_bits_changed:] works
                color = list(bin(img.item(y, x, channel))[2:].zfill(color_bits_changed))
                # Appends the binary_list with the bits stored in the color value
                binary_list.append("".join(color[-color_bits_changed:]))
                if values_found == binary_values_to_look_for:
                    return "".join(binary_list)
                values_found += 1
    return "".join(binary_list)


def get_binary_from_file(path):
    with open(path, "rb") as f:
        bytes = f.read()
    binary_array = [bin(i)[2:].zfill(8) for i in bytes]
    binary = "".join(binary_array)
    return binary


def get_file_from_binary(binary, path):
    bits_per_byte = 8
    binary_array = [binary[i:i+bits_per_byte] for i in range(0, len(binary), bits_per_byte)]
    int_array = [int(b, 2) for b in binary_array]
    bytes = bytearray(int_array)
    with open(path, "wb") as f:
        f.write(bytes)


def get_binary_from_text(text):
    print("Number of characters: " + str(len(text)))
    # Converts the text into a list of binary values. ord gets the unicode value, bin gets the number as a binary string
    #   [2:] removes the "0b" from the start of the number, which is done as all of the numbers will be positive
    array_of_char_binary_values = [bin(ord(c))[2:] for c in text]
    # Sets the number of bits per character to the length of the longest binary number
    bits_per_char = len(max(array_of_char_binary_values, key=len))
    print("Bits per character: " + str(bits_per_char))
    # zfill adds leading zeros if the binary number is the wrong length, and they are joined to give a continuous string
    binary = "".join([b.zfill(bits_per_char) for b in array_of_char_binary_values])
    text_size = len(text) * bits_per_char
    return binary


def get_text_from_binary(binary, bits_per_char):
    # Gets the character binary values in a list
    char_binary_values = [binary[i:i + bits_per_char] for i in range(0, len(binary), bits_per_char)]
    # Converts the binary values to base 10 integers, and then to characters
    chars = [chr(int(b, 2)) for b in char_binary_values]
    # Joins characters and returns them as the text
    text = "".join(chars)
    return text


def get_image_capcity(img, color_bits_changed=1):
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    capacity = height * width * channels * color_bits_changed
    return capacity


# Source: https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def bit_format(bits):
    num_bytes = bits / 8.0
    suffix = 'B'
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num_bytes) < 1024.0:
            return "%3.1f%s%s (%s bits)" % (num_bytes, unit, suffix, bits)
        num_bytes /= 1024.0
    return "%.1f%s%s (%s bits)" % (num_bytes, 'Yi', suffix, bits)

if __name__ == "__main__":
    test_conceal_text_in_image()
    test_conceal_image_in_image()


