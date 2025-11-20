# Arquivo: src/lexer.py

from ply import lex

# --- 1. Definição das Palavras-Chave e Tokens ---

# Palavras-chave (Rosa Claro) e Funções/Palavras Reservadas (Amarelo Claro)
# O valor do dicionário é o nome do TOKEN que o parser usará.
keywords = {
    # Keywords (Rosa Claro)
    'while': 'WHILE',
    'do': 'DO',
    'function': 'FUNCTION',
    'local': 'LOCAL',
    'class': 'CLASS',
    'if': 'IF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'extents': 'EXTENTS',  # Observação: 'extends' é mais comum, mas usaremos 'extents'

    # Literais Booleanos (Laranja Claro)
    'true': 'TRUE',
    'false': 'FALSE',

    # Funções (Amarelo Claro)
    'printinConsole': 'PRINTINCONSOLE',
    'Add': 'ADD',
    'Vector': 'VECTOR',
    'Angle': 'ANGLE',
    'GetChildren': 'GETCHILDREN',
    'GetParent': 'GETPARENT',
    'Destroy': 'DESTROY',
    'Duplicate': 'DUPLICATE',

    # Funções de Objeto (são tratadas como IDENTIFICADOR neste nível,
    # mas listamos aqui se você quiser tratá-las como Keywords:
    'move': 'MOVE',
    'rotate': 'ROTATE',
    'scale': 'SCALE'
}

# --- 2. Lista de Nomes de Tokens ---
tokens = [
    'NUMERO',          # Laranja Claro
    'TEXTO',           # Verde Claro
    'IDENTIFICADOR',   # Nomes de variáveis/funções definidas pelo usuário
    'PROPRIEDADE',     # Ex: .Name, .Pos, .Angle (Azul Claro)

    # Operadores
    'SOMA', 'SUBTRACAO', 'MULTIPLICACAO', 'DIVISAO', 'ATRIBUICAO', 'IGUAL',

    # Delimitadores
    'PARENTESE_ESQ', 'PARENTESE_DIR',
    'CHAVE_ESQ', 'CHAVE_DIR',
    'PONTO_VIRGULA', 'VIRGULA',
    'PONTO',          # Para acessar propriedades (Ex: Objeto.Name)

    # Comentário (o Lexer normalmente descarta, mas definimos para ignorar)
    # 'COMENTARIO',
] + list(keywords.values())
