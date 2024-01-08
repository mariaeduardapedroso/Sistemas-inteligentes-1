## Gabriel Conte, João Carvalho, Maria Pedroso
# Código usado para validação do modelo em tempo real
# Código original: https://github.com/opencv/opencv/blob/master/samples/dnn/openpose.py


import cv2 as cv
import numpy as np
import argparse
from knnAlgorithmConj import *

# argumentos do openpose (usado vídeos gravados previamente)
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')
parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')
parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')

args = parser.parse_args()

# Declaração das partes do esqueleto
BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = args.width
inHeight = args.height

# Lê a rede fo tensor flow (Openpose)
net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

# Abre um vido ou dispositivo de video
cap = cv.VideoCapture(args.input if args.input else 0)

#inicia a classe com o modelo
knn_algorithm = knnAlgorithm()

posNeck = [0,0]
oldNeck = [0,0]
posLHip = [0,0]
oldLHip = [0,0]
posRHip = [0,0]
oldRHip = [0,0]
middle = [0,0]
window = []
a = 0
b = 0
model = []

# Abre o arquivo com o dataset
dataset = open("ModeloConj.txt","r")

# lê a primeira linha e atribui os valores
line = dataset.readline()
realData = []
components = line.split("#")
dados = []
dados.append([abs(float(components[0])), float(components[2])])
count = 0

# lê o arquivo inteiro pegando todos os valores
while line != "":
    line = line.replace('\n','')
    if line == "-----------":
        realData.append([dados,str(components[3])])
        dados = []
        line = dataset.readline()
        line.replace('\n','')
        if line == '':
            break


    components = line.split("#")
    dados.append([abs(float(components[0])), float(components[2])])
    count +=1
    line = dataset.readline()




#enquanto não apertar esq
while cv.waitKey(1) < 0:
    #captura o frame
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    # pega os valores do tamanho da imagem
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    #Define a input do modelo
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    # Pega os pontos do corpo
    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    # a cada ponto pega as coordenadas X Y
    for i in range(len(BODY_PARTS)):
        heatMap = out[0, i, :, :]

        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        points.append((int(x), int(y)) if conf > args.thr else None)

    #Cria as linhas de conecção entre os pontos
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000

    # pega a posição do pescoço, quadril direito e quadril esquerdo se forem lidos
    if points[1] != None and points[8] != None and points[11] != None:
        posNeck = [points[1][0],points[1][1]]
        posRHip = [points[8][0],points[8][1]]
        posLHip = [points[11][0],points[11][1]]

    # Estima a posição baseada na variação e na taxa de amostragem
    if points[1] == None and posNeck[0] != 0 and posNeck[1] != 0:
        a = ((posNeck[0]-oldNeck[0])/0.033)
        posNeck[0] = posNeck[0] + a*0.033
        a = ((posNeck[1]-oldNeck[1])/0.033)
        posNeck[1] = posNeck[1] + a*0.033

    if points[11] == None and posLHip[0] != 0 and posLHip[1] != 0:
        a = ((posLHip[0]-oldLHip[0])/0.033)
        posLHip[0] = posLHip[0] + a*0.033
        a = ((posLHip[1]-oldLHip[1])/0.033)
        posLHip[1] = posLHip[1] + a*0.033

    if points[8] == None and posRHip[0] != 0 and posRHip[1] != 0:
        a = ((posRHip[0]-oldRHip[0])/0.033)
        posRHip[0] = posRHip[0] + a*0.033
        a = ((posRHip[1]-oldRHip[1])/0.033)
        posRHip[1] = posRHip[1] + a*0.033
    
    # acha o ponto que fica na metade dos quadris
    middle[0] = (int(posRHip[0])+int(posLHip[0]))/2
    middle[1] = (int(posRHip[1])+int(posLHip[1]))/2

    # calcula o ângulo entre o centro do quadril e o pescoço
    if(int(posNeck[0]) - middle[0]) != 0:
        angle = np.arctan((int(posNeck[1]) - middle[1])/ (int(posNeck[0]) - middle[0]))*180/3.14159
    else:
        angle = 90
    
    # Encontra a velocidade (Não usado)
    velocity = (float(posNeck[1]) - float(oldNeck[1]))/0.033
    # Encontra a distância entre o quadril e o pescoço
    distNH = np.sqrt((posNeck[0]-middle[0])**2 + (posNeck[1]-middle[1])**2)

    # Mensagem default se ainda não conseguiu um conjunto de 60 valores
    msg = "Ainda nao foi 60"

    # Se tiver tiver mais de 60
    if len(window) >= 60:
        # Exclui o mais antigo e agrega o mais novo
        window.pop(0)
        window.append([angle,distNH])
        # Aplica o algoritmo do Knn para fazer a previsão
        msg = str(knn_algorithm.getKNN(window,realData,3))
    else:
        # Adiciona até 60
        window.append([angle,distNH])
    
    
    # Atualiza os valores antigos
    oldNeck = posNeck
    oldLHip = posLHip
    oldRHip = posRHip

    # Exibe a mensagem com a predição
    cv.putText(frame, "Predicao: " + msg, (500, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (1, 1, 1))
    # Exibe o video
    cv.imshow('OpenPose using OpenCV', frame)