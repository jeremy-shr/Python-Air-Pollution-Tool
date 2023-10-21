from matplotlib import pyplot as mat_plot
import numpy as np


def find_red_pixels(path, *args, **kwargs):
    '''
    Reads a city map and outputs a binary image of all its RED pixels saved as map-red-pixels.jpg

    @param: path --> Relative path to the image file of the map

    @return: binary array (black and white) with all the red pixels of the image. 
    '''
    arr = mat_plot.imread(path)
    out = ((arr.copy())*255).astype('i')

    for row in range(len(out)):
        for col in range(len(out[0])):
            if out[row][col][0] > 100 and out[row][col][1] < 50 and out[row][col][2] < 50:
                out[row][col] = 255, 255, 255, 255
            else:
                out[row][col] = 0, 0, 0, 255
    out = out.astype('uint8')
    mat_plot.imsave('map-red-pixels.jpg', out)
    return out


def find_cyan_pixels(path, *args, **kwargs):
    '''
    Reads a city map and outputs a binary image of all its CYAN pixels saved as map-cyan-pixels.jpg

    @param: path --> Relative path to the image file of the map

    @return: binary array (black and white) with all the cyan pixels of the image. 
    '''
    arr = mat_plot.imread(path)
    out = ((arr.copy())*255).astype('i')
    for row in range(len(out)):
        for col in range(len(out[0])):
            if out[row][col][0] < 50 and out[row][col][2] > 100 and out[row][col][1] > 100:
                out[row][col] = 255, 255, 255, 255
            else:
                out[row][col] = 0, 0, 0, 255
    out = out.astype('uint8')
    mat_plot.imsave('map-cyan-pixels.jpg', out)
    return out


def detect_connected_components(image='map-red-pixels.jpg', *args, **kwargs):
    '''
    Connected component detection algorithm.
    This implementation uses an empty placeholder matrix to which is written white pixels when a pavement is detected in the original image. It is optimised to be composed of boolean values only. 
    It uses counters to keep track of regions of connected components and the number of pixels they have. 

    @param: image --> path to the red pixel binary map.

    @return: mark --> array with all pavements marked as visited
    @return: data_for_sort --> used as input in the sorted function. Composed of a dictionary with each region of connected components mapped to the number of pixels it contains. Also, there is a list of coords for all pixels belonging to that region. 
    '''
    arr = mat_plot.imread(image) / 255
    Q = np.array([[0, 0]])
    components = []
    height = len(arr)
    width = len(arr[0])
    mark = [[False for _ in range(width)] for _ in range(height)]

    f = open('cc-output-2a.txt', 'w+')
    region = 0
    data_for_sort = [{}, []]

    for row in range(height):
        for col in range(width):
            if sum(arr[row][col][:2]) > 1 and not mark[row][col]:

                Q = np.concatenate([Q, np.array([[row, col]])])
                component = []
                region += 1
                region_size = 0
                data_for_sort[1].append([])
                while Q.size != 0:

                    m, n = Q[0]
                    Q = np.delete(Q, 0, axis=0)
                    component.append((m, n))

                    neighbours = [(m-1, n-1), (m-1, n), (m-1, n+1),
                                  (m, n-1), (m, n+1),
                                  (m+1, n-1), (m+1, n), (m+1, n+1)]
                    for s, t in neighbours:
                        if s < height and t < width:
                            if sum(arr[s][t][:2]) > 1 and not mark[s][t]:
                                mark[s][t] = True
                                Q = np.concatenate([Q, np.array([[s, t]])])
                                data_for_sort[1][region-1].append((s, t))
                                region_size += 1
                f.write(
                    f'Connected component {region}, number of pixels = {region_size}\n')
                components.append(component)
                data_for_sort[0][region] = region_size
    f.write(f'Total number of connected components = {region}')
    f.close()
    return mark, data_for_sort


def detect_connected_components_sorted(*args, **kwargs):
    '''
    Sorts regions of connected components using an implementation of quick sort and outputs an image showing the two largest ones. 
    Writes to a .txt file the outcome of the sorting. 

    @return: array of all the connected components belonging to the two largest regions. 
    '''
    data, lst_of_coords = detect_connected_components('map-red-pixels.jpg')[1]
    out = list(data.items())
    quick_sort(out, 0, len(out) - 1)
    with open('cc-output-2b.txt', 'w+') as f:
        for region, pixels in out:
            f.write(
                f'Connected component {region}, number of pixels = {pixels}\n')
        f.write(f'Total number of connected components = {len(out)}')

    largest, second_largest = out[0][0], out[1][0]
    arr = np.zeros((1140, 1053, 3))
    for y, x in (lst_of_coords[largest-1] + lst_of_coords[second_largest - 1]):
        arr[y][x] = (1, 1, 1)
    mat_plot.imsave('cc-top-2.jpg', arr)

    return out


def partition(items, low, high):
    '''
    Used in the quick sort function below
    '''
    pivot = items[high][1]
    i = low
    for j in range(low, high):
        if items[j][1] > pivot:
            items[i], items[j] = items[j], items[i]
            i += 1
    items[i], items[high] = items[high], items[i]
    return i


def quick_sort(items, low, high):
    if low < high:
        pivot_index = partition(items, low, high)
        quick_sort(items, low, pivot_index - 1)
        quick_sort(items, pivot_index + 1, high)
