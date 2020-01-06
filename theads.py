import threading
import cv2
import numpy as np


def get_menu():
    menu = "\n"
    menu += "1. Run\n"
    menu += "2. Change number of threads\n"
    menu += "3. Change kernel size\n"
    menu += "0. Exit\n"
    return menu


class FilterThread(threading.Thread):
    def __init__(self, thread_id, start_index):
        threading.Thread.__init__(self)
        self.__thread_id = thread_id
        self.__start_index = start_index

    def run(self):
        row = self.__start_index // width
        col = self.__start_index % width

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

            result[row, col] = [blue_sum, green_sum, red_sum]

            # move to the next pixel
            col += 1
            if col == width:
                col = 0
                row += 1

        print("Exit thread " + str(self.__thread_id))


img = cv2.imread("images/source/kids.bmp", cv2.IMREAD_COLOR)
height, width = img.shape[:2]
result = np.zeros((height, width, 3), np.uint8)
img_size = height * width


nr_threads = 10
kernel_size = 5
menu = get_menu()
run = True
while run:
    print("\nCurrent number of threads: " + str(nr_threads))
    print("Current kernel size: " + str(kernel_size))
    print(menu)

    command = input("Give command: ")

    if command == "2":
        nr_threads = int(input("Give the number of threads: "))

    elif command == "3":
        kernel_size = int(input("Give the kernel size: "))

    elif command == "0":
        run = False

    elif command == "1":
        threads = []
        master_size = img_size % (nr_threads - 1)
        slave_size = img_size // (nr_threads - 1)
        half_size = kernel_size // 2

        for i in range(nr_threads - 1):
            thread = FilterThread(i, i * slave_size)
            thread.start()
            threads.append(thread)

        # master computation
        start_index = (nr_threads - 1) * slave_size
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

        for t in threads:
            t.join()

        cv2.imshow("Source image", img)
        cv2.imshow("Blurred image", result)
        cv2.waitKey(0)

        print("Exit main thread")

    else:
        print("Invalid command")
