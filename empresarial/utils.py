import string
import os
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
from random import choice, shuffle
from weasyprint import HTML


def gerar_senha_aleatoria(tamanho):
    # com a biblioteca string do python é possivel ter acesso a varios conjuntos de carateres alfanumericos
    caracteres_especiais = string.punctuation
    caracteres = string.ascii_letters
    numeros_list = string.digits

    # dividimos por inteiro o tamanho da senha por 3 para que cada parte da senha receba um tipo de string diferente
    # a ideia é dividir pelo tamanho da senha desejado, numeros iguais de caracteres especiais, numeros e caracteres normais
    # inicializa a variavel
    sobra = 0

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

def gerar_pdf_exames(exame, paciente, senha):
    # salvar o caminho até o html padrao base para o PDF
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/senha_exame.html')
    # precisamos converte o html gerado pelo django, para um HTML puro para poder gerar o PDF sem lixo
    template_render = render_to_string(path_template, {'exame': exame, 'paciente':paciente, 'senha': senha})

    # HTML(string=template_render).write_pdf(os.path.join(settings.BASE_DIR, 'templates/partials/senha_exame.pdf'))
    # ao inves de jogar o arquivo pdf para um arquivo, vamos colocar ele em memoria, para usar e descartar

    # cria um espaco em memoria para "Salvar o arquivo"
    path_output = BytesIO()
    HTML(string=template_render).write_pdf(path_output)
    # volta o ponteiro para o inicio
    path_output.seek(0)

    return path_output

