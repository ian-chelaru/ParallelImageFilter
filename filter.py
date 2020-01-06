import cv2
import numpy as np


def sequential_blur_filter(filename, kernel_size):
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    height, width = img.shape[:2]
    result = np.zeros((height, width, 3), np.uint8)
    half_size = kernel_size // 2

    for i in range(half_size, height - half_size):
        for j in range(half_size, width - half_size):
            red_sum = 0
            green_sum = 0
            blue_sum = 0

            for k in range(-half_size, half_size + 1):
                for l in range(-half_size, half_size + 1):
                    red_sum += img[i + k, j + l, 2]
                    green_sum += img[i + k, j + l, 1]
                    blue_sum += img[i + k, j + l, 0]

            red_sum //= kernel_size * kernel_size
            green_sum //= kernel_size * kernel_size
            blue_sum //= kernel_size * kernel_size

            result[i, j, 2] = red_sum
            result[i, j, 1] = green_sum
            result[i, j, 0] = blue_sum

    cv2.imshow("Source image", img)
    cv2.imshow("Blurred image", result)
    cv2.waitKey(0)


sequential_blur_filter("images/source/kids.bmp", 5)
