#Copy and paste this code into whatver, to simulate a successful reading of
#mlx90640. That is, it will be a list 768 elements, with random floats
#mlx will read from -40C to 85C the data will not be re-oriented

import random
frame = list()
for i in range (0,768):
    frame.append(random.randint(-45,85))
