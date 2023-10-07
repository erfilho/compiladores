# Configurando as importações

import ply.lex as lex
import gradio as gr
import re

# Lista com nomes de tokens
tokens = (
   'NUMERO',
   'OPERADOR',
   'IGUALDADE',
   'VARIAVEL',
)

# Regex para cada token
def t_VARIAVEL(t):
    r'[a-zA-Z_][a-zA-Z_]*'
    t.value = str(t.value)
    return t

def t_IGUALDADE(t):
    r'\='
    t.value = 'IGUALDADE'
    return t

def t_OPERADOR(t):
    r'\+|\-|\*|\/'
    if t.value == '+':
        t.value = 'SOMA'
    elif t.value == '-':
        t.value = 'SUBTRAÇAO'
    elif t.value == '*':
        t.value = 'MULTIPLICAÇAO'
    elif t.value == '/':
        t.value = 'DIVISAO'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = str(t.value)    
    return t

# Definindo uma regra para calcular os números das linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# String padrão com caracteres ignorados
t_ignore  = ' \t'

# Erro de caractere não reconhecido
def t_error(t):
    print("Caractere inválido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construindo o lexer
lexer = lex.lex()

# Definindo uma função para testar o input se realmente é uma equação de segundo grau
def input_test(text):
    eq = re.compile(r'(^[0-9]*[\*][a-zA-Z_]*[\+|\-|\*|\/][0-9]*[\=][0-9]*$)')
    if(eq.search(text) == None):
        return False
    else:
        return True

# Função para analisar o input
def input(text):
    # Verifica se o texto do input passa no teste, ou não
    if(input_test(text) == False):
        # Mostra um erro na tela
        raise gr.Error("Equação inválida!")
    # Passa o texto do input no lexer
    lexer.input(text)
    tokens = []
    # Registra os tokens em uma lista
    while True:
        tok = lexer.token()
        if not tok: 
            # Ao acabar inputs, retorna lista de tokens
            break
        if tok.type == "NUMERO":
            tokens.append([tok.value, tok.type, tok.value])
        elif tok.type == "VARIAVEL":
            tokens.append([tok.value, tok.type, tok.value])
        else:
            tokens.append([text[tok.lexpos], tok.type, tok.value])
    return tokens

# Configuração da interface no gradio
with gr.Blocks() as demo:
    # Configurando o input de texto
    equacao = gr.Textbox(
        label="Digite uma equação de primeiro grau:",
        lines=1,
        placeholder="Ex: 5*a+10=0")
    # Configurando a tabela de resultado
    saida = gr.Dataframe(
        headers=["Token", "Tipo", "Valor"],
        datatype=["str", "str", "str"],
        label="Tokens")
    # Configurando o botão
    analisa_botao = gr.Button("Analisar léxicamente")
    #Configurando a função do botão
    analisa_botao.click(fn=input, inputs=[equacao], outputs=[saida])

# Lancando a interface
demo.launch(inline=False, share=True)