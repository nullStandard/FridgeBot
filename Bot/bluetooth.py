import serial
from PIL import Image
import io

_BT_serial = serial.Serial('/dev/rfcomm0', 9600, timeout=1)

def getPhoto():
    #if not _BT_serial.is_open:
       # _BT_serial.open()
        
    _BT_serial.write(b'!')
    _BT_serial.flush()
    image_array = bytearray()
    while True:
        arr_from_buf = _BT_serial.readline()
        image_array.extend(arr_from_buf)
        if _BT_serial.in_waiting == 0:
            break
    print(image_array)

    image = Image.open(io.BytesIO(image_array))
    #image.save("test.jpg")
    #_BT_serial.close()
    return image
    
if __name__ == "__main__":
    getPhoto().save("taken_image.jpg")