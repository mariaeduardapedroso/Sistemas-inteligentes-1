import numpy as np

def main():
    # abrir o arquivo
    file = open("PosCair1.txt","r")
    dataset = open("Dataset1.txt","a")

    #ler uma linha
    line = file.readline()
    line = line.replace('\n','')

    #separar componentes da linha
    components = line.split("#")
    posNeck = str(components[0]).split(",")
    posRHip = str(components[1]).split(",")
    posLHip = str(components[2]).split(",")
    middle = [0,0]
    ultimo_point = posNeck

    middle[0] = (int(posRHip[0])+int(posLHip[0]))/2
    middle[1] = (int(posRHip[1])+int(posLHip[1]))/2
    
    if(int(posNeck[0]) - middle[0]) != 0:
        angle = np.arctan((int(posNeck[1]) - middle[1])/ (int(posNeck[0]) - middle[0]))*180/3.14159
    else:
        angle = 90
    
    velocity = (float(posNeck[1]) - float(ultimo_point[1]))/0.033
    distNH = np.sqrt((int(posNeck[0])-(int(posRHip[0]) + int(posLHip[0]))/2)**2 + (int(posNeck[1])-(int(posRHip[1]) + int(posLHip[1]))/2)**2)

    print(angle, velocity, distNH)
    text = str(angle) + "#" + str(velocity) + "#" + str(distNH) + "#cair\n"
    dataset.write(text)

    while(line != ""):
        line = line.replace('\n','')

        #separar componentes da linha
        components = line.split("#")
        posNeck = str(components[0]).split(",")
        posRHip = str(components[1]).split(",")
        posLHip = str(components[2]).split(",")

        middle[0] = (int(posRHip[0])+int(posLHip[0]))/2
        middle[1] = (int(posRHip[1])+int(posLHip[1]))/2
        
        if(int(posNeck[0]) - middle[0]) != 0:
            angle = np.arctan((int(posNeck[1]) - middle[1])/ (int(posNeck[0]) - middle[0]))*180/3.14159
        else:
            angle = 90
        velocity = (float(posNeck[1]) - float(ultimo_point[1]))/0.033
        distNH = np.sqrt((int(posNeck[0])-(int(posRHip[0]) + int(posLHip[0]))/2)**2 + (int(posNeck[1])-(int(posRHip[1]) + int(posLHip[1]))/2)**2)

        print(angle, velocity, distNH)
        text = str(angle) + "#" + str(velocity) + "#" + str(distNH) + "#cair\n"
        dataset.write(text)
        line = file.readline()
        ultimo_point = posNeck

    dataset.write("-----------\n")
    file.close()
    dataset.close()


if __name__ == "__main__":
    main()