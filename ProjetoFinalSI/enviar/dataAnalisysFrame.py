## Gabriel Conte, João Carvalho, Maria Pedroso
# Código usado para validar o modelo Knn frame a frame

import matplotlib.pyplot as pt
from knnAlgorithmFrame import *
import seaborn as sn
import pandas as pd


def main():
    # abre o arquivo do dataser
    dataset = open("Dataset.txt", "r")

    #cria o objeto com o algoritmo do knn
    knn_algorithm = knnAlgorithm()

    # lê a primeira linha e atribui os valores
    line = dataset.readline()
    components = line.split("#")
    angle = [abs(float(components[0]))] 
    velocity = [float(components[1])]  
    dist = [float(components[2])]
    count = 0

    # lê o arquivo inteiro pegando todos os valores
    while line != "":
        line = line.replace('\n','')
        components = line.split("#")
        angle.append(abs(float(components[0])))
        velocity.append(float(components[1]))
        dist.append(float(components[2]))
        count +=1
        line = dataset.readline()
    
    # separa entre abaixar e cair para fazer análise gráfica
    angleAbaixar = angle[0:143]
    angleCair = angle[144:]
    distAbaixar = dist[0:143]
    distCair = dist[144:]

    # gera um gráfico para análise
    pt.plot(angleAbaixar, distAbaixar, 'ro')
    pt.plot(angleCair,distCair,'bo')
    pt.title("Comparacao de valores de distancia e angulo")
    pt.ylabel("Distancia")
    pt.xlabel("Angulo")
    pt.show()

    # separa entre modelo e teste (100-43 em cada categoria)
    model = []
    test = []
    for i in range(0,100):
        model.append([angle[i], dist[i], "Abaixar"])

    for i in range(143,243):
        model.append([angle[i], dist[i], "Cair"])
    
    for i in range(100,143):
        test.append([angle[i], dist[i], "Abaixar"])

    for i in range(243,286):
        test.append([angle[i], dist[i], "Cair"])

    # aplica o modelo em cada elemento do teste analisando se está certo ou não para fazer a matriz de confusao
    matrixConf = [[0,0],[0,0]]
    for elemento in test:
        prediction = knn_algorithm.getKNN(elemento, model, 3)
        if prediction == elemento[2]:
            if elemento[2] == "Abaixar":
                matrixConf[0][0] += 1
            else:
                matrixConf[1][1] += 1
        else:
            if elemento[2] == "Abaixar":
                matrixConf[0][1] += 1
            else:
                matrixConf[1][0] += 1

    # plota a matrix de confusao
    df_cm = pd.DataFrame(matrixConf, range(2), range(2))
    # plt.figure(figsize=(10,7))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size

    pt.show()
    print(knn_algorithm.getKNN([88.10445216003234,423.2316150761897],model,3))
    
    print(matrixConf)

    dataset.close()


if __name__ == "__main__":
    main()
