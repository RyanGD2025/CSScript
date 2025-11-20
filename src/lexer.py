# Arquivo: src/lexer.py

from ply import lex

# --- 1. Definição das Palavras-Chave (Keywords) ---
keywords = {
    # Keywords
    'while': 'WHILE', 'do': 'DO', 'function': 'FUNCTION', 'local': 'LOCAL', 
    'class': 'CLASS', 'if': 'IF', 'else': 'ELSE', 'elseif': 'ELSEIF', 
    'extents': 'EXTENTS', 'var': 'VAR', 'retornar': 'RETORNAR',

    # Literais Booleanos
    'true': 'TRUE', 'false': 'FALSE',

    # Funções Built-in (Simplificadas)
    'printinConsole': 'PRINTINCONSOLE', 'Add': 'ADD', 'Vector': 'VECTOR', 
    'Angle': 'ANGLE', 'GetChildren': 'GETCHILDREN', 'GetParent': 'GETPARENT', 
    'Destroy': 'DESTROY', 'Duplicate': 'DUPLICATE',
    
    # Propriedades de uso comum que queremos tokenizar como ID
    'Name': 'IDENTIFICADOR', 'Type': 'IDENTIFICADOR', 'Pos': 'IDENTIFICADOR', 
    'Size': 'IDENTIFICADOR', 'Angle': 'IDENTIFICADOR', 'Color': 'IDENTIFICADOR', 
    'Collide': 'IDENTIFICADOR', 'Touch': 'IDENTIFICADOR', 'Text': 'IDENTIFICADOR', 
    'Image': 'IDENTIFICADOR'
}

# --- 2. Lista de Nomes de Tokens ---
tokens = [
    'NUMERO', 'TEXTO', 'IDENTIFICADOR',
    # Operadores
    'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'ATRIBUICAO', 'IGUAL',
    # Delimitadores
    'PARENTESE_ESQ', 'PARENTESE_DIR', 'CHAVE_ESQ', 'CHAVE_DIR',
    'PONTO_VIRGULA', 'VIRGULA', 'PONTO', 'E_COMERCIAL', # Incluindo o '&'
] + list(keywords.values())

# --- 3. Definição das Regras de Expressão Regular (Regex) ---

# Tokens Simples
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_IGUAL = r'=='
t_ATRIBUICAO = r'='
t_PARENTESE_ESQ = r'\('
t_PARENTESE_DIR = r'\)'
t_CHAVE_ESQ = r'{'
t_CHAVE_DIR = r'}'
t_VIRGULA = r','
t_PONTO_VIRGULA = r';'
t_PONTO = r'\.'
t_E_COMERCIAL = r'&'

# Números (Inteiros ou flutuantes)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Strings (Texto)
def t_TEXTO(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1] # Remove as aspas
    return t

# Comentários (Ignorados)
def t_COMENTARIO(t):
    r'//.*'
    pass

# Identificadores e Palavras-Chave
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verifica se o token é uma palavra-chave (ex: 'extents')
    t.type = keywords.get(t.value, 'IDENTIFICADOR')
    return t

# Espaços em branco e novas linhas (Ignorados)
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erro de caractere ilegal
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()
