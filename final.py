import spidev
import time
import csv
import joblib
import numpy as np
import socket
import json

BLENDER_HOST="XXX.XX.XXX.XXX" #Replace with your Blender server IP
BLENDER_PORT=9999


def send_shape(shape_type,dimensions):
	shape = (shape_type,dimensions)
	msg=json.dumps(shape).encode('utf-8')
	
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		s.connect((BLENDER_HOST,BLENDER_PORT))
		s.sendall(msg)
		print(f"Sent to Blender: {shape}")



spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000 

modelc = joblib.load("models/shapeClassifier.pkl")
modelr = joblib.load("models/cylinderRadiusPredictor.pkl")
models = joblib.load("models/sideLength.pkl")
modelspr= joblib.load("models/sphereRadiusPredictor.pkl")
scaler1 = joblib.load("models/classificationScaler.pkl")
scaler2 = joblib.load("models/cylinderScaler.pkl")
scaler3 = joblib.load("models/cuboidScaler.pkl")
scaler4 = joblib.load("models/sphereScaler.pkl")

print(1)


def read_adc(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")
    
    spi.xfer2([1, (8 + channel) << 4, 0])
    time.sleep(0.001)  # Settling time
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    print(1)
    return data



def predict_radius(flex_values):
    flex_scaled = scaler2.transform([flex_values])  
    predicted_radius = modelr.predict(flex_scaled)  
    print(1)
    return predicted_radius[0]

def predict_sradius(flex_values):
    flex_scaled = scaler4.transform([flex_values])  
    predicted_radius = modelspr.predict(flex_scaled)  
    print(1)
    return predicted_radius[0]

def predict_sidelength(flex_values):
    flex_scaled = scaler3.transform([flex_values])  
    predicted_radius = models.predict(flex_scaled)  
    print(1)
    return predicted_radius[0] 

def predict_shape(flex_values):
    flex_scaled = scaler1.transform([flex_values])  
    predicted_radius = modelc.predict(flex_scaled)  
    print(1)
    return predicted_radius[0] 

try:
    while True:
        flex_values = [read_adc(channel) for channel in range(5)]  
        print(f"Flex Sensor Values: {flex_values}")

        if any(num < 20 for num in flex_values):
            print("1")  
        else:
            estimated_shape = predict_shape(flex_values)
            print(estimated_shape)
            if estimated_shape=="cylinder":
                estimated_radius=predict_radius(flex_values)
                print(f"Predicted Radius: {estimated_radius:.2f} cm")
                send_shape('cylinder',[estimated_radius,7])
                if(flex_values[1]>100 and flex_values[2]>250 and flex_values[3] >255):
                    print(total)
                    break
                elif(flex_values[1]>100 or flex_values[2]>250 or flex_values[3] >255):
                    if(flex_values[3]>255):
                        print(total)
                        break
                    elif(flex_values[1]>100 and flex_values[2]<250):
                        height=5.5
                        total+=height
                    elif(flex_values[2]>250 and flex_values[1]>100):
                        height=3.5
                        total+=height
                    print(total)
                    send_shape('cylinder',[estimated_radius,height])
                    break 
                else:
                    estimated_radius = predict_radius(flex_values)
                    radius=estimated_radius
                    print(f"Predicted Radius: {estimated_radius:.2f} cm")
                    total+=7
                    send_shape('cylinder',[estimated_radius,7])
                time.sleep(5)
            
         
            elif(estimated_shape=="cuboid"):
                time.sleep(2)
                length=0
                breath=0
                height=0
                tlength=0
                count=0
                while True:
                    flex_values = [read_adc(channel) for channel in range(5)]
                    print(f"Flex Sensor Values: {flex_values}")
                    if any(num < 20 for num in flex_values[1:]):
                        print("1")
                    else:
                        elength = predict_sidelength(flex_values[1:])
                        print(f"Predicted Radius: {elength:.2f} cm")
                        if elength < 5:
                            tlength += elength
                            print(tlength)
                            if(count==0):
                                print("length")
                                count+=1
                                length=tlength
                                tlength=0
                            elif(count==1):
                                print("breath")
                                count+=1
                                breath=tlength
                                tlength=0
                            else:
                                print("height")
                                count+=1
                                height=tlength
                                tlength=0
                                break
                        else:
                            tlength+=elength
                    time.sleep(5)
                send_shape('cuboid',[length,breath,height])
                    
            elif(estimated_shape=="sphere"):
                estimated_radius=predict_sradius(flex_values)
                print(f"Predicted Radius: {estimated_radius:.2f} cm")
                send_shape('sphere',[estimated_radius])
                break
				

        time.sleep(1)  

except KeyboardInterrupt:
    print("Exiting...")
    spi.close()
