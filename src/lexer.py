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

# --- 3. Definição das Regras de Expressão Regular (Regex) ---

# Operadores e Símbolos
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
t_PONTO = r'\.' # Necessário para acessar as Propriedades

# --- 4. Regras Complexas com Funções (Ordem de Leitura) ---

# NÚMEROS (Laranja Claro)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    # Aceita inteiros e flutuantes
    t.value = float(t.value)
    return t

# STRINGS (Texto - Verde Claro)
def t_TEXTO(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # Remove as aspas. A lógica do Parser garantirá que esta string
    # seja tratada como um Literal de texto.
    t.value = t.value[1:-1]
    return t

# COMENTÁRIOS (Cinza)
# Comentários de linha única (//...)
def t_COMENTARIO(t):
    r'//.*'
    pass  # Ignora e não retorna um token

# IDENTIFICADORES E PALAVRAS-CHAVE
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verifica no dicionário `keywords` se é uma palavra reservada
    t.type = keywords.get(t.value, 'IDENTIFICADOR')
    return t

# PROPRIEDADES (Azul Claro) - Este token é mais complexo, pois pode ser parte de um IDENTIFICADOR
# Vamos tratar o '.' como um token separado (t_PONTO) e deixar o Parser
# juntar `IDENTIFICADOR` + `PONTO` + `IDENTIFICADOR` (a propriedade)
# No entanto, se quisermos que o Lexer já identifique a propriedade em si (ex: ".Name"),
# podemos usar uma regex com lookbehind negativo, mas é mais simples para o PLY
# deixar o Parser lidar com a sequência `IDENTIFICADOR` + `PONTO` + `PROPRIEDADE`.
# Por enquanto, PROPRIEDADE será um tipo de IDENTIFICADOR.
# O parser será quem definirá que "Pos" após um "." é uma Propriedade.

# --- 5. Tratamento de Espaços em Branco e Erros ---

t_ignore = ' \t' # Ignora espaços e tabs

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

if __name__ == '__main__':
    codigo_csscript_teste = """
    local MySprite = Add("Sprite");
    MySprite.Name = "Nave01";

    function Mover() {
        if MySprite.Collide {
            while true do
                MySprite.Pos.move(10, 0);
                printinConsole("Movendo!");
            }
        } elseif MySprite.Type == "Player" {
            // Este é um comentário
            Angle.rotate(45);
        } else {
            MySprite.Size.scale(1.5, 1.5);
        }
    }
    """
    lexer.input(codigo_csscript_teste)
    print("--- Tokens Gerados (CSScript) ---")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Tipo: {tok.type:<20} Valor: {repr(tok.value):<15} Linha: {tok.lineno}")

