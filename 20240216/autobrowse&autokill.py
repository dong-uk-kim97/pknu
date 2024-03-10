import cv2

image = cv2.imread("C:\\study\\20240216\\moon.jpg", cv2.IMREAD_ANYCOLOR)
height, width, channel = image.shape

print(height, width, channel)
cv2.imshow("Moon", image)
cv2.waitKey()
cv2.destroyAllWindows()
