import time
import cv2
import numpy as np

import HandTrackingModule as htm
import pyautogui

pyautogui.FAILSAFE = False

############
wCam, hCam = 640, 480
frameR = 100 # redução do quadro
suavizar = 4
############

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0,0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam) # width = 3
cap.set(4, hCam) # higth



detector = htm.handDetector(maxHands=1)
wScreen, hScreen = pyautogui.size()
print(wScreen, hScreen)

while True:
    check, img = cap.read()

# 1. Encontrar marcações das mãos
    img = detector.findHands(img)

# 2. Pegue a ponta dos dedos indicador e médio
    lmList, bbox = detector.findPosition(img)
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:] # dedo indicador
        x2, y2 = lmList[12][1:] # dedo médio
        # print(x1, y1, x2, y2) posições dos dedos indicador e médio

# 3. Verifique quais dedos estão levantados
        fingers = detector.fingersUp()
        # print(fingers) # quais dedos estão levantados
        # redução da área de contato
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
# 4. Apenas dedo indicador
        if fingers[1]==1 and fingers[2]==0: # dedo indicador levantado e médio, baixo
            #print("Largura img: ", wCam, "Altura img: ", hCam)
            #cv2.line(img, (x1, y1), (wCam//2,0), (255, 0, 255), 2)
            #cv2.line(img, (x1, y1), (0, hCam//2), (255, 0, 255), 2)
            #cv2.line(img, (x1, y1), (wCam, hCam // 2), (255, 0, 255), 2)
            #cv2.line(img, (x1, y1), (wCam//2, hCam), (255, 0, 255), 2)
            #print("Largura tela pc:", wScreen, "Altura tela pc:", hScreen)

# 5. Converter coordenadas
            x3 = np.interp(x1, (frameR,wCam-frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))

# 6. Suavizar valores/movimentação
            clocX = plocX + (x3 - plocX) / suavizar
            clocY = plocY + (y3 - plocY) / suavizar
            # pyautogui.moveTo(wScreen - clocX, clocY) com suavização
# 7. Mover mouse
            pyautogui.moveTo(x3, y3)
            cv2.circle(img, (x1, y1), 30, (0, 255, 0), 2)
            plocX, plocY = clocX, clocY
# 8. Ambos os dedos indicador e médio estão para cima: clicar com o mouse
        if fingers[1] == 1 and fingers[2] == 1:
# 9. Encontrar distâncias entre os dedos
            length, img, lineInfo = detector.findDistance(8, 12, img)
            xEntre = lineInfo[4]
            yEntre = lineInfo[5]
            # print(length)
# 10. Clicar com o mouse a distância for menor que a desejada
            if length < 32:
                cv2.circle(img, (xEntre, yEntre), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

# 11. Taxa de quadros
    cTime = time.time() # current time
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0),2)

# 12. Exibir
    cv2.imshow("Janela", img)
    cv2.waitKey(1)