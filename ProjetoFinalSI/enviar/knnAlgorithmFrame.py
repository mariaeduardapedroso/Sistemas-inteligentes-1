import statistics

class knnAlgorithm:

    def __init__(self):
        print("Implementação pelo Método Knn")

    def getKNN(self, example, model, k):
        #calcula a distancia de cada elemento
        distancias = []

        for elemento in model:
            distancia = ((example[0]-elemento[0])**2 + (example[1]-elemento[1])**2)**(1/2)
            distancias.append([distancia, elemento[2]])

        # ordena as distancias e pega as 3 mais próximas
        knnNeighbors = sorted(distancias, key=lambda x :x[0])[1:k+1]

        # pega as predições
        predictionLabels = [element[1] for element in knnNeighbors]

        # pega a moda de predição
        prediction = statistics.mode(predictionLabels)

        # retorna a predição
        return prediction

        
