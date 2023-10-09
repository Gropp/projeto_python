import string
from random import choice, shuffle

def gerar_senha_aleatoria(tamanho):
    # com a biblioteca string do python é possivel ter acesso a varios conjuntos de carateres alfanumericos
    caracteres_especiais = string.punctuation
    caracteres = string.ascii_letters
    numeros_list = string.digits

    # dividimos por inteiro o tamanho da senha por 3 para que cada parte da senha receba um tipo de string diferente
    # a ideia é dividir pelo tamanho da senha desejado, numeros iguais de caracteres especiais, numeros e caracteres normais
    qtd = tamanho // 3
    # pegamos o mod para ver se tem resto
    if not tamanho % 3 == 0:
        sobra = tamanho - (qtd * 3)
    
    letras = ''
    for i in range(0, qtd + sobra):
        letras += choice(caracteres)
    
    numeros = ''
    for i in range(0, qtd):
        numeros += choice(numeros_list)

    especiais = ''
    for i in range(0, qtd):
        especiais += choice(caracteres_especiais)
    
    senha = list(letras + numeros + especiais)
    # para embaralhar a senha usamos a função shuffle
    shuffle(senha)

    # precisamos retornar a lista como sendo um string
    return ''.join(senha)