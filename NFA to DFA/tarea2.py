import pandas as pd

file = open("nfa4.txt", 'r')
inputs = {"Estados": {"Inicial" : [], "Transitorio" : [], "Final" : []}, "Alfabeto" : [], "Transiciones" : []}
titulos = ["Estados\n", "Alfabeto\n", "Transiciones\n"]

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
        elif line[0] == '*':
            inputs["Estados"]["Final"].append(line[1])
        else:
            inputs["Estados"]["Transitorio"].append(line[0])

    elif aux == titulos[1]:
        if line == aux:
            continue
        inputs["Alfabeto"].append(line[0])
        
    else:
        if line == aux:
            continue
        inputs["Transiciones"].append([line[0], line[2], line[7]])
    
# print(inputs)

states = []

for i in inputs["Estados"]["Inicial"]:
    if i not in states:
        states.append(i)
for i in inputs["Estados"]["Transitorio"]:
    if i not in states:
        states.append(i)
for i in inputs["Estados"]["Final"]:
    if i not in states:
        states.append(i)

print(states)

transitions = inputs["Transiciones"]
transition_table = pd.DataFrame(None, (states), inputs["Alfabeto"])

for i in range(len(states)):
    for j in range(len(inputs["Alfabeto"])):
        transition_table.iloc[i][j] = []
        
for t in transitions:
    i = states.index(t[0])
    j = inputs["Alfabeto"].index(t[1])
    transition_table.iloc[i][j].append(t[2]) 

# initial_states.append(transition_table["Estado inicial"])

# print(initial_states)
print(states)
print(inputs["Alfabeto"])
# print(states)
print(transition_table)