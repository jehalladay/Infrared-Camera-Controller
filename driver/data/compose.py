
# Check out:
# https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv#comment63502914_14102014 for offsetting
# https://imagekit.io/blog/image-resizing-in-python/ for padding
# https://pythonexamples.org/python-opencv-add-blend-two-images/ for blending
# https://www.geeksforgeeks.org/python-pil-image-resize-method/

from PIL import Image
# Opening the primary image (used in background)
img1 = Image.open('./Once_2022_10_30/02_15_41/mp.png')
# Opening the secondary image (overlay image)
img2 = Image.open('./here/frame_0.png')
img2.resize((3,3))
img2.putalpha(150)
  
# Pasting img2 image on top of img1 
# starting at coordinates (0, 0)
img1.paste(img2, (0,0), mask = img2)
  
# Displaying the image
img1.show()