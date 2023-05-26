import numpy as np
from collections import defaultdict

_size_data = 0
_dim = 0

def generate_codebook(data, size_codebook, epsilon=0.00005):
    global _size_data, _dim

    _size_data = len(data)
    _dim = len(data[0])

    codebook = []
    # get the initial codevector by taking the average vector of whole input data
    c0 = avg_all_vectors(data, _dim, _size_data)
    codebook.append(c0)

    # initial average distortion
    avg_dist = initial_avg_distortion(c0, data)

    # splitting process until we have exactly same number of codevector with the size of codebook.
    while len(codebook) < size_codebook:
        codebook = split_codebook(data, codebook, epsilon, avg_dist)
    #return the result
    return codebook

def split_codebook(data, codebook, epsilon, initial_avg_dist):
    # split into 2
    new_cv = []
    for c in codebook:
        # plus and minus epsilon for the new codebook
        c1 = new_codevector(c, epsilon)
        c2 = new_codevector(c, -epsilon)
        new_cv.extend((c1, c2))

    codebook = new_cv
    len_codebook = len(codebook)

    # Get the best centroid by taking average distortion as cost function. This problems mimic K-Means.
    avg_dist = 0
    err = epsilon + 1
    num_iter = 0
    while err > epsilon:
        # Get nearest codevector.
        closest_c_list = [None] * _size_data    # nearest codevector
        vecs_near_c = defaultdict(list)         # input data vector mapping
        vec_idxs_near_c = defaultdict(list)     # input data index mapping
        for i, vec in enumerate(data):  # for each input vector
            min_dist = None
            closest_c_index = None
            for i_c, c in enumerate(codebook):
                d = get_mse(vec, c)
                # Get the nearest ones.
                if min_dist is None or d < min_dist:
                    min_dist = d
                    closest_c_list[i] = c
                    closest_c_index = i_c
            vecs_near_c[closest_c_index].append(vec)
            vec_idxs_near_c[closest_c_index].append(i)

        # Update the codebook
        for i_c in range(len_codebook):
            vecs = vecs_near_c.get(i_c) or []
            num_vecs_near_c = len(vecs)
            if num_vecs_near_c > 0:
                # assign as new center
                new_c = avg_all_vectors(vecs, _dim)
                codebook[i_c] = new_c
                for i in vec_idxs_near_c[i_c]:
                    closest_c_list[i] = new_c

        # Recalculate average distortion
        prev_avg_dist = avg_dist if avg_dist > 0 else initial_avg_dist
        avg_dist = avg_codevector_dist(closest_c_list, data)

        # Recalculate the new error value
        err = (prev_avg_dist - avg_dist) / prev_avg_dist
        num_iter += 1

    return codebook

def avg_all_vectors(vecs, dim=None, size=None):
    size = size or len(vecs)
    nvec = np.array(vecs)
    nvec = nvec / size
    navg = np.sum(nvec, axis=0)
    return navg.tolist()

def new_codevector(c, e):
    nc = np.array(c)
    return (nc * (1.0 + e)).tolist()

def initial_avg_distortion(c0, data, size=None):
    size = size or _size_data
    nc = np.array(c0)
    nd = np.array(data)
    f = np.sum(((nc-nd)**2)/size)
    return f

def avg_codevector_dist(c_list, data, size=None):
    size = size or _size_data
    nc = np.array(c_list)
    nd = np.array(data)
    f = np.sum(((nc-nd)**2)/size)
    return f

def get_mse(a, b):
    na = np.array(a)
    nb = np.array(b)
    return np.sum((na-nb)**2)

def generate_training(img, block):
    train_vec = []
    x = block[0]
    y = block[1]
    for i in range(0, img.shape[0], y):
        for j in range(0, img.shape[1], x):
            train_vec.append(img[i:i + y, j:j + x].reshape((x * y * block[2])))
    return (np.array(train_vec))

def distance(a, b):
    return np.mean((np.subtract(a, b) ** 2))

def closest_match(src, cb):
    c = np.zeros((cb.shape[0],))
    for i in range(0, cb.shape[0]):
        c[i] = distance(src, cb[i])
    minimum = np.argmin(c, axis=0)
    return minimum

def encode_image(img, cb, block):
    x = block[0]
    y = block[1]
    compressed = np.zeros((img.shape[0] // y, img.shape[1] // x))
    ix = 0
    for i in range(0, img.shape[0], y):
        iy = 0
        for j in range(0, img.shape[1], x):
            src = img[i:i + y, j:j + x].reshape((x * y * block[2])).copy()
            k = closest_match(src, cb)
            compressed[ix, iy] = k
            iy += 1
        ix += 1
    return compressed


def decode_image(cb, compressed, block):
    x = block[0]
    y = block[1]
    original = np.zeros((compressed.shape[0] * y, compressed.shape[1] * x, block[2]))
    iy = 0
    for i in range(0, compressed.shape[0]):
        ix = 0
        for j in range(0, compressed.shape[1]):
            original[iy:iy + y, ix:ix + x] = cb[int(compressed[i, j])].reshape(block[1], block[0], block[2])
            ix += x
        iy += y
    return original

def Vector_quantization(img, cb_size, epsilon, block):
    for i in range (img.shape[0] - img.shape[0]%block[1], img.shape[0]):
        img = np.delete(img, img.shape[0]-1, 0)
    for i in range (img.shape[1] - img.shape[1]%block[0], img.shape[1]):
        img = np.delete(img, img.shape[1]-1, 1)

    train_X = generate_training(img, block)
    cb = generate_codebook(train_X, cb_size, epsilon)
    cb_n = np.array(cb)
    result = encode_image(img, cb_n, block)
    final_result = decode_image(cb_n, result, block)
    final_result = np.array(final_result, dtype=np.uint8)
    return final_result