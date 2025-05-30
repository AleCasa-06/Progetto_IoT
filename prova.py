import cv2
import imutils
import numpy as np
import pytesseract
import RPi.GPIO as GPIO
import time
import re
from mysql.connector import connect
import datetime
import threading


connection = connect(host="localhost", user="admin", password="password", database="parcheggio")

cursor = connection.cursor()

def cam1():
    # Attiva webcam
    cap = cv2.VideoCapture("/dev/video0")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Errore nella lettura dalla webcam")
            break

        frame_resized = cv2.resize(frame, (800, 600))
        cv2.imshow("Immagine", frame_resized)

        img = frame_resized.copy()
        break

    cap.release()
    cv2.destroyAllWindows()

    # Preprocessing immagine
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 40, 40)
    edged = cv2.Canny(gray, 30, 200)

    # Trova contorni
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("Nessun contorno rilevato")
        text = ""
    else:
        # Crea maschera e ritaglia
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        # Threshold per migliorare OCR
        thresh = cv2.threshold(Cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.imshow("Ritaglio (Threshold)", thresh)

        # OCR
        raw_text = pytesseract.image_to_string(thresh, config='--psm 7')
        print("Raw OCR output:", repr(raw_text))

        # Pulizia finale
        text = raw_text.strip().replace("\n", "").replace("\f", "").replace(" ", "")
        print("Numero di targa rilevato:", text)

        # Disegna contorno e testo su immagine
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
        cv2.putText(img, text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostra immagini
        img = cv2.resize(img, (500, 300))
        Cropped = cv2.resize(Cropped, (400, 200))
        cv2.imshow('Auto', img)
        cv2.imshow('Targa Ritagliata', Cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Controllo targa
        text.replace(" ", "")
        text.replace("-", "")
        text.replace(":", "")
        text.replace(";", "")
        text.replace("/", "")
        x = re.findall(r"[A-Z]{2}\d{3}[A-Z]{2}", text)
        print(text)
        print(x)
        return x[0]


def cam2():

    # Attiva webcam
    cap = cv2.VideoCapture("/dev/video1")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Errore nella lettura dalla webcam")
            break

        frame_resized = cv2.resize(frame, (800, 600))
        cv2.imshow("Immagine", frame_resized)

        img = frame_resized.copy()
        break

    cap.release()
    cv2.destroyAllWindows()

    # Preprocessing immagine
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 40, 40)
    edged = cv2.Canny(gray, 30, 200)

    # Trova contorni
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("Nessun contorno rilevato")
        text = ""
    else:
        # Crea maschera e ritaglia
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        # Threshold per migliorare OCR
        thresh = cv2.threshold(Cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.imshow("Ritaglio (Threshold)", thresh)

        # OCR
        raw_text = pytesseract.image_to_string(thresh, config='--psm 7')
        print("Raw OCR output:", repr(raw_text))

        # Pulizia finale
        text = raw_text.strip().replace("\n", "").replace("\f", "").replace(" ", "")
        print("Numero di targa rilevato:", text)

        # Disegna contorno e testo su immagine
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
        cv2.putText(img, text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mostra immagini
        img = cv2.resize(img, (500, 300))
        Cropped = cv2.resize(Cropped, (400, 200))
        cv2.imshow('Auto', img)
        cv2.imshow('Targa Ritagliata', Cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Controllo targa
        text.replace(" ", "")
        text.replace("-", "")
        text.replace(":", "")
        text.replace(";", "")
        text.replace("/", "")
        x = re.findall(r"[A-Z]{2}\d{3}[A-Z]{2}", text)
        print(text)
        print(x)
        return x[0]


GPIO.setmode(GPIO.BCM)

def entra():

    TRIG = 23  
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


    while True:
        
        GPIO.output(TRIG, False)
        time.sleep(0.02)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start = 0
        pulse_end = 0

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()


        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)


        if distance < 7:
            query = "INSERT INTO automobili (targa, Data_ingresso) VALUES(%s, %s)"
            val = (cam1(), datetime.datetime.now())
            cursor.execute(query, val)
            connection.commit()

def esci():
    TRIG = 17  # pin del sensore
    ECHO = 27
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


    while True:

        GPIO.output(TRIG, False)

        time.sleep(0.02)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        pulse_start = 0
        pulse_end = 0

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance, 2)
        if distance < 7:
            targa = cam2()
            print(targa)
            auto = cursor.execute('SELECT * FROM automobili WHERE targa = %s', (targa, ))
            auto = cursor.fetchall()
            if auto == None:
                continue
            print(auto)
            query = "INSERT INTO auto_uscite (targa, Data_ingresso, Data_uscita) VALUES (%s, %s, %s)"
            val = (auto[0][0], auto[0][1], datetime.datetime.now())
            cursor.execute(query, val)
            print("jiyfckyfckyc")
            cursor.execute("DELETE FROM automobili WHERE targa = %s", (auto[0][0],))
            connection.commit()

th1 = threading.Thread(target= entra)
th2 = threading.Thread(target= esci)

th1.start()
th2.start()

th1.join()
th2.join()

GPIO.cleanup()