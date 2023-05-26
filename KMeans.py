import numpy as np
import random

def initialize_K_centroids(X, K):
    C = []
    for i in range(K):
        C.append(random.choice(X))
    return C

def find_closest_centroids(X, centroids):
    m = len(X)
    c = [0]*len(X)

    for i in range(m):
        # Find distances
        distances = []
        distance = 0
        for j in range(len(centroids)):
            for k in range(len(centroids[j])):
                distance += (X[i][k] - centroids[j][k])**2
            distances.append(distance)
            distance = 0

        # Assign closest cluster to c[i]
        c[i] = distances.index(min(distances))
    
    return c

def compute_means(X, idx, K):
    centroids = []
    examples = []
    mean = [0] * len(X[0])

    for k in range(K):
        examples = []
        for i in range(len(X[0])):
            mean[i] = 0

        for i in range(len(X)):
            if (idx[i] == k):
                examples.append(X[i])

        for i in range(len(examples)):
            for j in range(len(X[0])):
                mean[j] += examples[i][j]

        for i in range(len(X[0])):
            mean[i] /= len(examples)

        centroids.append(mean[:])

    return centroids

def get_centroids(img, K, max_iters):
    centroids = initialize_K_centroids(img, K)
    previous_centroids = centroids
    for _ in range(max_iters):
        idx = find_closest_centroids(img, centroids)
        centroids = compute_means(img, idx, K)
        for i in range(len(centroids)):
            for j in range(len(centroids[i])):
                if (previous_centroids[i][j]==centroids[i][j]):
                    # The centroids aren't moving anymore.
                    return centroids

        previous_centroids = centroids

    return centroids

def KMeans(img, K, max_iters):
    w,h,d = img.shape
    img = img/255
    img = img.reshape(w*h,d)

    colors = get_centroids(img, K, max_iters)

    # Indexes for color for each pixel
    idx = find_closest_centroids(img, colors)

    # Reconstruct the image
    res = []
    for i in range(len(idx)):
        for k in range(K):
            if (idx[i] == k):
                res.append(colors[k])
                break

    res = np.array(res)*255
    res = np.array(res, dtype=np.uint8)
    recolored_img = res.reshape(w,h,d)

    return recolored_img