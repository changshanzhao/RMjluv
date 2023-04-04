import sensor,image,time
from image import SEARCH_EX, SEARCH_DS
from pyb import UART
from pyb import LED
from time import sleep
from pyb import Pin
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.LCD)
sensor.skip_frames(time = 2000)
clock = time.clock()
pin0 = Pin('B0', Pin.OUT_PP, Pin.PULL_DOWN)
pin1 = Pin('B1', Pin.OUT_PP, Pin.PULL_DOWN)
pin4 = Pin('B4', Pin.OUT_PP, Pin.PULL_DOWN)
pin5 = Pin('B5', Pin.OUT_PP, Pin.PULL_DOWN)

num_quantity=10  #目标数量
num_model=[]    #存储数字模型的图片列表
#循环将根目录下的F文件夹的数字图片载入
for n in range(0,num_quantity-1):
    num_model.append(image.Image("\F\%d.pgm"%n))
#声明小尺寸的画布，用于模板匹配
img_to_matching=sensor.alloc_extra_fb(32,32,sensor.GRAYSCALE)
#threshold=(0,70) #寻找色块的阈值
scale=1.0  #缩放比例变量
threshold  = [(0, 57, -44, 49, -46, 39),(25, 54, -33, 61, -29, 40)]  #可多取一些颜色阈值增加准确性
#uart = UART(1, 115200, timeout_char=1000)                         # i使用给定波特率初始化
#uart.init(115200, bits=8, parity=1, stop=1, timeout_char=1000) # 使用给定参数初始化
LED(1).on()
while(True):
    clock.tick() #帧率统计
    img=sensor.snapshot()
    blobs=img.find_blobs(threshold,area_threshold=100)  #寻找色块
	pin0.low()
	pin1.low()
	pin4.low()
	pin5.low()
    if blobs:
        for blob in blobs:
            if (blob.pixels()>100) and (blob.h()<90) and (blob.w()<50) : 
                #按坐标和比例提取出色块，注意坐标长宽都向外扩大4个像素，避免图像不全
                img.draw_rectangle(blob.rect()) # rect
                #按坐标和比例提取出色块，注意坐标长宽都向外扩大4个像素，避免图像不全
                error_s=int((blob.h()-blob.w())/2)  #目标位置，由于模板是正方形，这里做了目标扩展
                roi1=(blob.x()-error_s-2,blob.y()-2,blob.h()+4,blob.h()+4)
                print("roi1=",blob.h(),blob.w())
                scale=28.0/blob.h()  #缩放比例系数
                img2=img.copy(roi=roi1) #拷贝roi图像到缓存中
                img_to_matching.clear()
                img_to_matching.draw_image(img2,0,0,x_scale=scale,y_scale=scale)#将roi画到模板画布上
                del img2 #删除缓存，防止内存溢出
                for n in range(0,num_quantity-1):
                    #用所有数字模板和目标做匹配
                    r=img_to_matching.find_template(num_model[n],0.5,step=2,search=image.SEARCH_EX)
                    if r:
                        #在彩色画布上，用红色框绘制对应数字
                        #print(blob.rect())
                        img.draw_rectangle(blob.rect(),color=(255,0,0))
                        img.draw_string(blob.x()-8,blob.y()-8,str(n),scale=4,color=(255,0,0))
                        #uart.write(str(n))
                        if (n==0):
                            pin0.high()
                            pin1.low()
                            pin4.low()
                            pin5.low()
                        if (n==1):
                            pin0.low()
                            pin1.high()
                            pin4.low()
                            pin5.low()
                        if (n==2):
                            pin0.high()
                            pin1.high()
                            pin4.low()
                            pin5.low()
                        if (n==3):
                            pin0.high()
                            pin1.high()
                            pin4.high()
                            pin5.low()
                        if (n==4):
                            pin0.low()
                            pin1.low()
                            pin4.high()
                            pin5.low()
                        if (n==5):
                            pin0.low()
                            pin1.low()
                            pin4.low()
                            pin5.high()
                        if (n==6):
                            pin0.high()
                            pin1.low()
                            pin4.low()
                            pin5.high()
                        if (n==7):
                            pin0.high()
                            pin1.low()
                            pin4.high()
                            pin5.high()
                        if (n==8):
                            pin0.high()
                            pin1.high()
                            pin4.low()
                            pin5.high()
                        if (n==9):
                            pin0.high()
                            pin1.high()
                            pin4.high()
                            pin5.high()


                        LED(1).toggle()
                        sleep(100)
                        LED(1).off()
                        sleep(100)

