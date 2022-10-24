from board import I2C
from time import sleep
from adafruit_as726x import AS726x_I2C

spectro_address = 0x49



if __name__ == '__main__':


    print("MLX addr detected on I2C")
    print([hex(i) for i in mlx.serial_number])

    # get todays date
    date = time.strftime("%Y_%m_%d")

    file_name = f'./readingsCSV/infrared_{date}.csv'
    height = 24
    width = 32
    channels = 1
    verbose = False

    if len(sys.argv) > 1:
        file_name = sys.argv[1] 
    if len(sys.argv) > 2:
        width = int(sys.argv[2])
    if len(sys.argv) > 3:
        height = int(sys.argv[3])
    if len(sys.argv) > 4:
        verbose = bool(int(sys.argv[4]))

    main(
        file_name = file_name, 
        width = width, 
        height = height, 
        verbose = verbose
    )