# generated by maixhub, tested on maixpy3 v0.4.8
# copy files to TF card and plug into board and power on
import sensor, image, lcd, time
import KPU as kpu
import gc, sys
from Maix import GPIO
from board import board_info
from fpioa_manager import fm
import utime
input_size = (224, 224)
labels = ['3', '5', '7', '1', '2', '6', '9', '4', '0', '8']
anchors = [4.25, 4.22, 2.94, 3.09, 5.09, 5.16, 3.78, 3.44, 3.31, 4.44]
fm.register(11, fm.fpioa.GPIO0)
fm.register(12, fm.fpioa.GPIO1)
fm.register(13, fm.fpioa.GPIO2)
fm.register(14, fm.fpioa.GPIO3)
pin0 =  GPIO(GPIO.GPIO0, GPIO.OUT)
pin1 =  GPIO(GPIO.GPIO1, GPIO.OUT)
pin4 =  GPIO(GPIO.GPIO2, GPIO.OUT)
pin5 =  GPIO(GPIO.GPIO3, GPIO.OUT)

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=input_size)
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

def main(anchors, labels = None, model_addr="/sd/m.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(1)
    sensor.set_vflip(1)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels:
        with open('labels.txt','r') as f:
            exec(f.read())
    if not labels:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    try:
        task = None
        task = kpu.load(model_addr)
        kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 0, 0))
					n=labels[obj.classid()]
					pin0.value(1)
                    pin1.value(0)
                    pin4.value(0)
                    pin5.value(0)
					utime.sleep(10)
					if (n=='0'):
                        pin0.value(1)
                        pin1.value(0)
                        pin4.value(0)
                        pin5.value(0)
                    if (n=='1'):
                        pin0.value(0)
                        pin1.value(1)
                        pin4.value(0)
                        pin5.value(0)
                    if (n=='2'):
                        pin0.value(1)
                        pin1.value(1)
                        pin4.value(0)
                        pin5.value(0)
                    if (n=='3'):
                        pin0.value(1)
                        pin1.value(1)
                        pin4.value(1)
                        pin5.value(0)
                    if (n=='4'):
                        pin0.value(0)
                        pin1.value(0)
                        pin4.value(1)
                        pin5.value(0)
                    if (n=='5'):
                        pin0.value(0)
                        pin1.value(0)
                        pin4.value(0)
                        pin5.value(1)
                    if (n=='6'):
                        pin0.value(1)
                        pin1.value(0)
                        pin4.value(0)
                        pin5.value(1)
                    if (n=='7'):
                        pin0.value(1)
                        pin1.value(0)
                        pin4.value(1)
                        pin5.value(1)
                    if (n=='8'):
                        pin0.value(1)
                        pin1.value(1)
                        pin4.value(0)
                        pin5.value(1)
                    if (n=='9'):
                        pin0.value(1)
                        pin1.value(1)
                        pin4.value(1)
                        pin5.value(1)
            img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
            lcd.display(img)
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


if __name__ == "__main__":
    try:
        # main(anchors = anchors, labels=labels, model_addr=0x300000, lcd_rotation=0)
        main(anchors = anchors, labels=labels, model_addr="/sd/model-37027.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
