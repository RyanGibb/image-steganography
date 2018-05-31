import cv2


def conceal_text_in_img(input_path, output_path, text, color_bits_changed=1):
    list_binary = get_binary_from_text(text)
    img = cv2.imread(input_path)
    img = conceal_binary_in_image(img, list_binary, color_bits_changed)
    cv2.imwrite(output_path, img)


def get_binary_from_text(text):
    print("Number of characters: " + str(len(text)))
    array_of_char_binary_values = [bin(ord(c))[2:] for c in text]
    bits_per_char = len(max(array_of_char_binary_values, key=len))
    print("Bits per character: " + str(bits_per_char))
    binary = "".join([b.zfill(bits_per_char) for b in array_of_char_binary_values])
    return binary


def conceal_binary_in_image(img, binary, color_bits_changed):
    binary_index = 0
    binary_list = list(binary)
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    for y in range(height):
        for x in range(width):
            for channel in range(channels):
                # color is a list of binary digits
                color = list(bin(img.item(y, x, channel))[2:].zfill(color_bits_changed))
                color[-color_bits_changed:] = binary_list[binary_index:binary_index + color_bits_changed]
                new_color = int("".join(color), 2)
                img.itemset(y, x, channel, new_color)
                binary_index += color_bits_changed
                if binary_index >= len(binary_list):
                    return img
    return img


def unconceal_text_in_image(input_path, chars_to_look_for=0, bits_per_char=8, color_bits_changed=1):
    img = cv2.imread(input_path)
    binary = unconceal_binary_in_image(img, chars_to_look_for * bits_per_char)
    print(get_text_from_binary(binary, bits_per_char))


def unconceal_binary_in_image(img, binary_values_to_look_for=0, color_bits_changed=1):
    # Starts at 1 so if binary_values_to_look_for=0, all the values are found
    values_found = 1
    binary_list = []
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    for y in range(height):
        for x in range(width):
            for channel in range(channels):
                color = list(bin(img.item(y, x, channel))[2:].zfill(color_bits_changed))
                #################
                binary_list.append("".join(color[-color_bits_changed:]))
                if values_found == binary_values_to_look_for:
                    return "".join(binary_list)
                values_found += 1
    return "".join(binary_list)


def get_text_from_binary(binary, bits_per_char):
    char_binary_values = [binary[i:i+bits_per_char] for i in range(0, len(binary), bits_per_char)]
    chars = [chr(int(b, 2)) for b in char_binary_values]
    text = "".join(chars)
    return text


if __name__ == "__main__":
    conceal_text_in_img("download.jpeg", "download.png", "William Shakespeare was an English poet, playwright and "
                                                         "actor, widely regarded as both the greatest writer in the "
                                                         "English language, and the world's pre-eminent dramatist. "
                                                         "He is often called England's national poet, and the Bard of "
                                                         "Avon.")
    unconceal_text_in_image("download.png", 100, 7)

