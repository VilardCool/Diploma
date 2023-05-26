import numpy as np

num_colors = 255

def get_region_index(color_value, num_regions):
    region_value = num_colors/num_regions
    for index in range(num_regions):
        if color_value >= index*region_value and color_value <= (index+1)*region_value:
            return index

def Uniform_quantization(img, num_regions):
    r_region_mappings = [[] for i in range(num_regions)]
    g_region_mappings = [[] for i in range(num_regions)]
    b_region_mappings = [[] for i in range(num_regions)]

    # loop through all pixels and the put the colors into the respective color regions
    for rows in img:
        for pixel in rows:
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            #find the index where the color is supposed to go and add it
            r_region_mappings[get_region_index(red, num_regions)].append(red)
            g_region_mappings[get_region_index(green, num_regions)].append(green)
            b_region_mappings[get_region_index(blue, num_regions)].append(blue)
            
    # find the color that represents each region
    r_representative_color_per_region = [0 for i in range(num_regions)]
    g_representative_color_per_region = [0 for i in range(num_regions)]
    b_representative_color_per_region = [0 for i in range(num_regions)]

    # find the average of all colors in the regions to find the representative color
    for index in range(num_regions):
        r_representative_color_per_region[index] = np.mean(r_region_mappings[index]).astype(int)
        g_representative_color_per_region[index] = np.mean(g_region_mappings[index]).astype(int)
        b_representative_color_per_region[index] = np.mean(b_region_mappings[index]).astype(int)

    # now replace all colors in the image with their uniform quantized representative colors
    new_img = np.copy(img)
    for rindex, rows in enumerate(img):
        for cindex, pixel in enumerate(rows):
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            new_img[rindex, cindex][0] = r_representative_color_per_region[get_region_index(red, num_regions)]
            new_img[rindex, cindex][1] = g_representative_color_per_region[get_region_index(green, num_regions)]
            new_img[rindex, cindex][2] = b_representative_color_per_region[get_region_index(blue, num_regions)]

    return new_img