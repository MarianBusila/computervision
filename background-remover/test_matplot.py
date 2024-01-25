import cv2
import matplotlib.pyplot as plt
from background_remover import remove_background

# load image and select x, y coordinates of the test object to keep
image_path = './test.jpg'
x = 528
y = 606

image = cv2.imread(image_path)

result_image = remove_background(image, x, y)

plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGRA2RGBA))
plt.show()
