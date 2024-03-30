strArr = [['abcde'], ['grtlw'], ['dergh']]
vogais = ['a', 'b', 'c', 'd', 'e', 'i', 'o', 'u']

rows = len(strArr)
columns = len(strArr[0][0])

print(rows, columns)

posicoes_vogais = []
quadrados_vogais = []

for i in range(len(strArr)):
    for j in range(len(strArr[i][0])):
        if strArr[i][0][j] in vogais:
            posicoes_vogais.append([i, j])

print(posicoes_vogais)

for i in range(len(strArr)): 
    for j in range(len(strArr[i][0])):
        if [i, j] in posicoes_vogais:
            print("OutPut: ", strArr[i][0][j])
        else: print("OutPut not found :() ")    