from mpi4py import MPI
import cv2
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = comm.Get_size()

img = cv2.imread("images/source/kids.bmp", cv2.IMREAD_COLOR)
kernel_size = 5
half_size = kernel_size // 2
height, width = img.shape[:2]

img_size = height * width
master_size = img_size % (world_size - 1)
slave_size = img_size // (world_size - 1)

if rank == 0:
    # send data to slaves
    for i in range(world_size - 1):
        start_index = i * slave_size
        comm.send(start_index, dest=i + 1)

    result = np.zeros((height, width, 3), np.uint8)

    # master computation
    start_index = (world_size - 1) * slave_size
    row = start_index // width
    col = start_index % width

    for i in range(master_size):
        # compute the mean value for current pixel
        red_sum = 0
        green_sum = 0
        blue_sum = 0

        for k in range(-half_size, half_size + 1):
            for l in range(-half_size, half_size + 1):
                if (0 <= row + k < height) and (0 <= col + l < width):
                    red_sum += img[row + k, col + l, 2]
                    green_sum += img[row + k, col + l, 1]
                    blue_sum += img[row + k, col + l, 0]

        red_sum //= kernel_size * kernel_size
        green_sum //= kernel_size * kernel_size
        blue_sum //= kernel_size * kernel_size

        result[row, col] = [blue_sum, green_sum, red_sum]

        # move to the next pixel
        col += 1
        if col == width:
            col = 0
            row += 1

    # collect data from slaves
    for i in range(world_size - 1):
        slave_data = comm.recv(source=i + 1)
        start_index = i * slave_size
        row = start_index // width
        col = start_index % width

        for j in range(slave_size):
            result[row, col] = slave_data[j]
            col += 1
            if col == width:
                col = 0
                row += 1

    cv2.imshow("Source image", img)
    cv2.imshow("Blurred image", result)
    cv2.waitKey(0)

else:
    start_index = comm.recv(source=0)
    row = start_index // width
    col = start_index % width

    data = []

    for i in range(slave_size):
        # compute the mean value for current pixel
        red_sum = 0
        green_sum = 0
        blue_sum = 0

        for k in range(-half_size, half_size + 1):
            for l in range(-half_size, half_size + 1):
                if (0 <= row + k < height) and (0 <= col + l < width):
                    red_sum += img[row + k, col + l, 2]
                    green_sum += img[row + k, col + l, 1]
                    blue_sum += img[row + k, col + l, 0]

        red_sum //= kernel_size * kernel_size
        green_sum //= kernel_size * kernel_size
        blue_sum //= kernel_size * kernel_size

        data.append([blue_sum, green_sum, red_sum])

        # move to the next pixel
        col += 1
        if col == width:
            col = 0
            row += 1

    comm.send(data, dest=0)
