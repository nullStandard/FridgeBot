# Darknet with NNPACK
NNPACK was used to optimize [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet) without using a GPU. It is useful for embedded devices using ARM CPUs.

## Build from Raspberry Pi 4
Log in to Raspberry Pi using SSH.<br/>
Install [PeachPy](https://github.com/Maratyszcza/PeachPy) and [confu](https://github.com/Maratyszcza/confu)
```
sudo pip install --upgrade git+https://github.com/Maratyszcza/PeachPy
sudo pip install --upgrade git+https://github.com/Maratyszcza/confu
```
Install [Ninja](https://ninja-build.org/)
```
git clone https://github.com/ninja-build/ninja.git
cd ninja
git checkout release
./configure.py --bootstrap
export NINJA_PATH=$PWD
```
Install clang
```
sudo apt-get install clang
```
Install [NNPACK-darknet](https://github.com/digitalbrain79/NNPACK-darknet.git)
```
git clone https://github.com/digitalbrain79/NNPACK-darknet.git
cd NNPACK-darknet
confu setup
python ./configure.py --backend auto
$NINJA_PATH/ninja
sudo cp -a lib/* /usr/lib/
sudo cp include/nnpack.h /usr/include/
sudo cp deps/pthreadpool/include/pthreadpool.h /usr/include/
```
Build darknet-nnpack
```
git clone https://github.com/digitalbrain79/darknet-nnpack.git
cd darknet-nnpack
make
```

## Test
The weight files can be downloaded from the [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet).
```
YOLOv3-tiny
./darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg yolov3-tiny.weights data/person.jpg
```
```
YOLOv3-tiny-prn
./darknet detector test cfg/coco.data cfg/yolov3-tiny-prn.cfg yolov3-tiny-prn.weights data/person.jpg
```
## Result
cfg | Build Options | Prediction Time (seconds)
:-:|:-:|:-:
yolov3-tiny-voc.cfg | NNPACK=1 | 1.0
yolov3-tiny-voc.cfg | NNPACK=0 | 14.0
yolov3-tiny-prn-voc.cfg | NNPACK=1 | 0.77
yolov3-tiny-prn-voc.cfg | NNPACK=0 | 8.9
Gaussian_yolov3-tiny-voc.cfg | NNPACK=1 | 1.0