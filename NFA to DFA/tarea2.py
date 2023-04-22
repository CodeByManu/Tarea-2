import pandas as pd

file = open("nfa4.txt", 'r')
inputs = {"Estados": {"Inicial" : [], "Transitorio" : [], "Final" : []}, "Alfabeto" : [], "Transiciones" : []}
titulos = ["Estados\n", "Alfabeto\n", "Transiciones\n"]
states = []

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
        x = line.split()
        x = [elem.replace('>', '') for elem in x]
        x = [elem.replace('*', '') for elem in x]
        if line[0] == '>':
            inputs["Estados"]["Inicial"].append(x[0])
        elif line[0] == '*':
            inputs["Estados"]["Final"].append(x[0])
        else:
            inputs["Estados"]["Transitorio"].append(x[0])

    elif aux == titulos[1]:
        if line == aux:
            continue
        inputs["Alfabeto"].append(line[0])
        
    else:
        if line == aux:
            continue
        x = line.split()
        x.pop(2)
        inputs["Transiciones"].append(x)
    
file.close()

for i in inputs["Estados"]["Inicial"]:
    if i not in states:
        states.append(i)
for i in inputs["Estados"]["Transitorio"]:
    if i not in states:
        states.append(i)
for i in inputs["Estados"]["Final"]:
    if i not in states:
        states.append(i)

transitions = inputs["Transiciones"]
transition_table = pd.DataFrame(None, states, inputs["Alfabeto"])
subsets = pd.DataFrame(None, None, inputs["Alfabeto"])
subsets_states = []

for i in range(len(states)):
    for j in range(len(inputs["Alfabeto"])):
        transition_table.iloc[i][j] = []
        
for t in transitions:
    i = states.index(t[0])
    j = inputs["Alfabeto"].index(t[1])
    transition_table.iloc[i][j].append(t[2])

for i in range(len(inputs["Estados"]["Inicial"])):
    subsets.loc[inputs["Estados"]["Inicial"][i]] = transition_table.loc[inputs["Estados"]["Inicial"][i]]

for n in range(len(inputs["Alfabeto"])):
    x = (subsets.loc[states[0]][n])
    subsets_states.append(x)

for s in subsets_states:
    if tuple(s) not in subsets.index:
        aux = []
        for j in inputs["Alfabeto"]:
            auxil = []
            for i in s:
                for k in transition_table.loc[i][j]:
                    if k not in aux:
                        if k in auxil:
                            break
                        auxil.append(k)
            aux.append(auxil)  
            if len(aux) == len(inputs["Alfabeto"]):
                subsets.loc[str(s)] = aux
                for i in aux:
                    if i not in subsets_states:
                        subsets_states.append(i)
    if s in subsets_states:
        pass

subsets = subsets.drop(subsets.index[0])

outputs = {"Estados": {"Inicial" : [], "Transitorio" : [], "Final" : []}, "Alfabeto" : inputs["Alfabeto"], "Transiciones" : []}

for s in subsets_states:
    for i in inputs["Estados"]["Inicial"]:
        if s == list(i):
            outputs["Estados"]["Inicial"].append(s)
    
    for i in inputs["Estados"]["Final"]:
        if i in s and s not in outputs['Estados']['Final']:
            outputs["Estados"]["Final"].append(s)
    if s not in outputs["Estados"]["Inicial"] and s not in outputs["Estados"]["Final"]:
        outputs["Estados"]["Transitorio"].append(s)

for s in subsets_states:
    # print('\n', subsets_states[n])
    for i in range(len(inputs["Alfabeto"])):
        if subsets.loc[str(s)][i] != []:
            outputs["Transiciones"].append([s, inputs["Alfabeto"][i], subsets.loc[str(s)][i]])

fout = open("dfa_output.txt", "w")

for line in outputs.keys():
    if line == 'Estados':
        aux = 'Estados'
    elif line == 'Alfabeto':
        aux = 'Alfabeto'
    elif line == 'Transiciones':
        aux = 'Transiciones'
    
    fout.write(f'{line}\n')
    if titulos[0].strip() == aux:
        for state in outputs['Estados']:
            if state == 'Inicial':
                for element in outputs['Estados'][state]:
                    fout.write(f'>{{{",".join(element)}}}\n')
            elif state == 'Transitorio':
                for element in outputs['Estados'][state]:
                    fout.write(f'{{{",".join(element)}}}\n')
            elif state == 'Final':
                for element in outputs['Estados'][state]:
                    fout.write(f'*{{{",".join(element)}}}\n')
    
    elif titulos[1].strip() == aux:
        for key in outputs['Alfabeto']:
            fout.write(', '.join(key))
            fout.write('\n')

    elif titulos[2].strip() == aux:
        for transition in outputs['Transiciones']:
            for n, x in enumerate(transition):
                if n == 0:
                    fout.write('{')
                    for c in x:
                        if c == x[-1]:
                            fout.write(c)
                        else:
                            fout.write(f'{c},')
                    fout.write('} ')
                
                if n == 1:
                    fout.write(f'{x} -> ')

                if n == 2:
                    fout.write('{')
                    for c in x:
                        if c == x[-1]:
                            fout.write(c)
                        else:
                            fout.write(f'{c},')
                    fout.write('}')
            fout.write('\n')

fout.close()
