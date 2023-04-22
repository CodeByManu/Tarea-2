import pandas as pd

file = open("nfae1.txt", 'r')
inputs = {"Estados": {"Inicial" : [], "Transitorio" : [], "Final" : []}, "Alfabeto" : [], "Transiciones" : {"Normales": [], "Epsilon": []},"EpsilonClausura":{}}
titulos = ["Estados\n", "Alfabeto\n", "Transiciones\n"]
rows = []
cols = []
fin = []

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
            rows.append(line[1])
            
        elif line[0] == '*':
            inputs["Estados"]["Final"].append(line[1])
            rows.append(line[1])
            fin.append(line[1])
            
        else:
            inputs["Estados"]["Transitorio"].append(line[0])
            rows.append(line[0])
            

    elif aux == titulos[1]:
        if line == aux:
            continue
        inputs["Alfabeto"].append(line[0])
        cols.append(line[0])

    else:
        if line == aux:
            continue
        if line[2] == "e":
            inputs["Transiciones"]["Epsilon"].append([line[0], "Epsilon", line[13]])
        else:
            inputs["Transiciones"]["Normales"].append([line[0], line[2], line[7]])


file.close()


#Colocamos el mismo elemento a si mismo
for i in rows:
    inputs["EpsilonClausura"][i] = [i]

#Colocamos el destino de cada transicion epsilon 
for i in range(len(inputs["Transiciones"]["Epsilon"])):
    origen = inputs["Transiciones"]["Epsilon"][i][0]
    destino = inputs["Transiciones"]["Epsilon"][i][2]
    inputs["EpsilonClausura"][origen].append(destino)
    
#Comprobamos si las transiciones estan conectadas entre ellas para asignar mas elementos a Epsilon Clausura
for estado in rows:
    for i in inputs["EpsilonClausura"][estado]:
        if i != estado:
            for k in inputs["EpsilonClausura"][i]:
                if k not in inputs["EpsilonClausura"][estado]: inputs["EpsilonClausura"][estado].append(k)




outputs = pd.DataFrame(None, rows, cols)

for element in inputs['EpsilonClausura']:
    for c in cols:
        aux = []
        for x in inputs['EpsilonClausura'][element]:
            for n in range(len(inputs['Transiciones']['Normales'])):
                if inputs['Transiciones']['Normales'][n][0] == x and inputs['Transiciones']['Normales'][n][1] == c and inputs['Transiciones']['Normales'][n][2] not in aux:
                    aux.append(inputs['Transiciones']['Normales'][n][2])
        if len(aux) > 1:
            for i in aux:
                for j in inputs['EpsilonClausura'][i]:
                    if j not in aux: aux.append(j)
            outputs.loc[element][c] = aux
        else: outputs.loc[element][c] = aux

ffin = fin
for estado in rows:
    for i in range(len(fin)):
        if fin[i] in inputs["EpsilonClausura"][estado] and fin[i] != estado and estado not in ffin:
            ffin.append(estado)

fout = open("nfae_output.txt", "w")

for header in titulos:
    fout.write(header)
    if header == titulos[0]:
        for state in inputs['Estados']:
            if state == 'Inicial':
                for element in inputs['Estados'][state]:
                    if element in ffin:
                        fout.write(f'>*{{{",".join(element)}}}\n')
                    else: fout.write(f'>{{{",".join(element)}}}\n')
            elif state == 'Transitorio':
                for element in rows:
                    if element not in ffin and element not in inputs['Estados']['Inicial']:
                        fout.write(f'{{{",".join(element)}}}\n')
            elif state == 'Final':
                for element in ffin:
                    if element not in inputs['Estados']['Inicial']:
                        fout.write(f'*{{{",".join(element)}}}\n')

    elif header == titulos[1]:
        for key in inputs['Alfabeto']:
            fout.write(', '.join(key))
            fout.write('\n')

    elif header == titulos[2]:
        for i in rows:
            for j in cols:
                for k in outputs.loc[i][j]:
                    fout.write(f'{{{i}}} {j} -> {{{k}}}\n')

fout.close()
