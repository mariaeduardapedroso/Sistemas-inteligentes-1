## Gabriel Conte, João Carvalho, Maria Pedroso
# Código usado para validar o modelo Knn em conjunto

import matplotlib.pyplot as pt
from knnAlgorithmConj import *
import seaborn as sn
import pandas as pd


def main():
    # abre o arquivo do dataser
    dataset = open("Dataset1.txt", "r")

    #cria o objeto com o algoritmo do knn
    knn_algorithm = knnAlgorithm()

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
            realData.append(dados)
            print(len(dados))
            dados = []
            line = dataset.readline()
            line.replace('\n','')
            if line == '':
                break


        components = line.split("#")
        dados.append([abs(float(components[0])), float(components[2])])
        count +=1
        line = dataset.readline()

    
    # separa entre abaixar e cair para fazer análise gráfica
    abaixar = realData[0:6]
    cair = realData[6:12]
    ax = pt.figure().add_subplot(projection='3d')

    for j in range(0,6):
        abaixarAngle = []
        abaixarDist = []

        cairAngle = []
        cairDist = []

        time = range(0,60)

        for i in range(0,60):
            abaixarAngle.append(abaixar[j][i][0])
            abaixarDist.append(abaixar[j][i][1])
            cairAngle.append(cair[j][i][0])
            cairDist.append(cair[j][i][1])

        # gera um gráfico para análise
        ax.plot(time, abaixarDist, abaixarAngle, 'r')
        ax.plot(time, cairDist, cairAngle, 'k')

    pt.show()

    # separa entre modelo e teste (4-2 em cada categoria)
    model = []
    modelAux = []
    test = []
    testAux = []

    #Adiciona os valores de interesse em uma lista auxiliar e adiciona essa lista em outra lista
    for i in range(0,4):
        for j in range(0,60):
            modelAux.append([realData[i][j][0], realData[i][j][1]])
        model.append([modelAux,"Abaixar"])
        modelAux = []

    for i in range(4,6):
        for j in range(0,60):
            testAux.append([realData[i][j][0], realData[i][j][1]])
        test.append([testAux,"Abaixar"])
        testAux = []

    for i in range(6,10):
        for j in range(0,60):
            modelAux.append([realData[i][j][0], realData[i][j][1]])
        model.append([modelAux,"Cair"])
        modelAux = []

    for i in range(10,12):
        for j in range(0,60):
            testAux.append([realData[i][j][0], realData[i][j][1]])
        test.append([testAux,"Cair"])
        testAux = []

    # Consegue a matriz de confusao aplicando o modelo do Knn
    matrixConf = [[0,0],[0,0]]
    for elemento in test:
        prediction = knn_algorithm.getKNN(elemento, model, 3)
        if prediction == elemento[1]:
            if elemento[1] == "Abaixar":
                matrixConf[0][0] += 1
            else:
                matrixConf[1][1] += 1
        else:
            if elemento[1] == "Abaixar":
                matrixConf[0][1] += 1
            else:
                matrixConf[1][0] += 1

    # plota a matrix de confusao
    df_cm = pd.DataFrame(matrixConf, range(2), range(2))
    # plt.figure(figsize=(10,7))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}) # font size

    pt.show()


    dataset.close()


if __name__ == "__main__":
    main()
