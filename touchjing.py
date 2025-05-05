
import cv2
import os

images = os.listdir(r"C:\YAD\YADP\Python\tof\images")

print(images)
img_path =(r"C:\YAD\YADP\Python\tof\images")

for img_name in images:
# Read an image
    img = cv2.imread(img_path+"\\"+img_name)

    # Display the image
    cv2.imshow('Image Window', img)
    cv2.waitKey(0)  # Wait for any key press
cv2.destroyAllWindows()

#     # Load image
# screenshot = cv2.imread(r"C:\YAD\YADP\Python\tof\images\ss3.png")  # The window/screen image
# template = cv2.imread(r"C:\YAD\YADP\Python\tof\images\ss.png")     # The image you're looking for

# # Template matching
# result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

# # Find best match location
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# # For TM_CCOEFF_NORMED, the best match is at max_loc
# # max_val is the confidence score (0-1)

# # If confidence is high enough, we found a match
# if max_val > 0.8:  # Threshold value
#     # The match was found at max_loc
#     top_left = max_loc

#     print(
#         max_val, max_loc

#         , template.shape
#     )

# else:
#     print("Not same")