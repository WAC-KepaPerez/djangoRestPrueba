import datetime
import time

def countNumer(num,text_data):
    time.sleep(3)
    if(num+int(text_data) % 2) == 0:
        return num+text_data
    else:
        return "Number no valid"