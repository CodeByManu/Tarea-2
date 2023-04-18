
file = open("nfae1.txt", 'r')
inputs = {"Estados": {"Inicial" : [], "Transitorio" : [], "Final" : []}, "Alfabeto" : [], "Transiciones" : {"Normales": [], "Epsilon": []}}
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

print(inputs)
print(X,Y)

for i in inputs["Transiciones"]["Epsilon"]:
    print(i[0] + " e " + i[2])
            
    