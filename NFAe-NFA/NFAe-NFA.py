
file = open("nfae1.txt", 'r')
inputs = {"Estados": {"Inicial" : [], "Transitorio" : [], "Final" : []}, "Alfabeto" : [], "Transiciones" : {"Normales": [], "Epsilon": []},"EpsilonClausura":{}}
titulos = ["Estados\n", "Alfabeto\n", "Transiciones\n"]
X = []
Y = []

aux = ''
for line in file:
    if line == titulos[0]:
        aux = titulos[0]
    elif line == titulos[1]:
        aux = titulos[1]
    elif line == titulos[2]:
        aux = titulos[2]
    

    if aux == titulos[0]:
        if line == aux:
            continue
        if line[0] == '>':
            inputs["Estados"]["Inicial"].append(line[1])
            X.append(line[1])
            
        elif line[0] == '*':
            inputs["Estados"]["Final"].append(line[1])
            X.append(line[1])
            
        else:
            inputs["Estados"]["Transitorio"].append(line[0])
            X.append(line[0])
            

    elif aux == titulos[1]:
        if line == aux:
            continue
        inputs["Alfabeto"].append(line[0])
        Y.append(line[0])

    else:
        if line == aux:
            continue
        if line[2] == "e":
            inputs["Transiciones"]["Epsilon"].append([line[0], "Epsilon", line[13]])
        else:
            inputs["Transiciones"]["Normales"].append([line[0], line[2], line[7]])



print(X)
print()
print(Y)
print()
file.close()


#Colocamos el mismo elemento a si mismo
for i in X:
    inputs["EpsilonClausura"][i] = [i]
print(inputs)
print()
#Colocamos el destino de cada transicion epsilon 
for i in range(len(inputs["Transiciones"]["Epsilon"])):
    origen = inputs["Transiciones"]["Epsilon"][i][0]
    destino = inputs["Transiciones"]["Epsilon"][i][2]
    inputs["EpsilonClausura"][origen].append(destino)
    
#Comprobamos si las transiciones estan conectadas entre ellas para asignar mas elementos a Epsilon Clausura
print(inputs["EpsilonClausura"][X[0]])
for estado in X:
    for i in range(len(inputs["EpsilonClausura"][estado])):
        c = inputs["EpsilonClausura"][estado][i]
        if c != estado:
            inputs["EpsilonClausura"][estado].extend(inputs["EpsilonClausura"][c])
            inputs["EpsilonClausura"][estado] = list(set(inputs["EpsilonClausura"][estado]))


print(inputs["EpsilonClausura"])
            
            
    