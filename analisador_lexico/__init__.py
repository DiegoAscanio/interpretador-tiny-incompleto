import pdb
from enum import Enum

class AnalisadorLexico:
    TipoToken = Enum(
       'TipoToken', [
        # Specials
        'UNEXPECTED_EOF',
        'INVALID_TOKEN',
        'END_OF_FILE',

        # Symbols
        'SEMICOLON',     # ;
        'ASSIGN',        # =

        # Logic operators
        'EQUAL',         # ==
        'NOT_EQUAL',     # !=
        'LOWER',         # <
        'LOWER_EQUAL',   # <=
        'GREATER',       # >
        'GREATER_EQUAL', # >=

        # Arithmetic operators
        'ADD',           # +
        'SUB',           # -
        'MUL',           # *
        'DIV',           # /
        'MOD',           # %

        # Keywords
        'PROGRAM',       # program
        'WHILE',         # while
        'DO',            # do
        'DONE',          # done
        'IF',            # if
        'THEN',          # then
        'ELSE',          # else
        'OUTPUT',        # output
        'TRUE',          # true
        'FALSE',         # false
        'READ',          # read
        'NOT',           # not

        # Others
        'NUMBER',        # number
        'VAR'            # variable
    ])
    tabela_simbolos = {
        # simbolos
        ';': TipoToken.SEMICOLON,
        '=': TipoToken.ASSIGN,
    
        # operadores logicos
        '==': TipoToken.EQUAL,
        '!=': TipoToken.NOT_EQUAL,
        '<':  TipoToken.LOWER,
        '<=': TipoToken.LOWER_EQUAL,
        '>':  TipoToken.GREATER,
        '>=': TipoToken.GREATER_EQUAL,
    
        # operadores aritmeticos
        '+': TipoToken.ADD,
        '-': TipoToken.SUB,
        '*': TipoToken.MUL,
        '/': TipoToken.DIV,
        '%': TipoToken.MOD,
    
        # palavras-chave
        'program': TipoToken.PROGRAM,
        'while': TipoToken.WHILE,
        'do': TipoToken.DO,
        'done': TipoToken.DONE,
        'if': TipoToken.IF,
        'then': TipoToken.THEN,
        'else': TipoToken.ELSE,
        'output': TipoToken.OUTPUT,
        'true': TipoToken.TRUE,
        'false': TipoToken.FALSE,
        'read': TipoToken.READ,
        'not': TipoToken.NOT,
    }
    # estados do automato de leitura de tokens
    # explicito é melhor que implicito!
    estados = Enum('estados', [
        'inicial', # 1 - o estado onde o automato começa e se mantem ao ler espaços em branco e novas linhas
        'ler_comentarios', # 2 - o estado que representa a leitura de comentarios, o automato continua nele até ler uma nova linhas
        'ler_atribuicao_comparacao_ou_igualdade', # 3 - o estado que representa a leitura de uma atribuicao (=) ou comparacao (>, <, >=, <=, ==)
        'ler_nao_igual', # 4 - o estado subsequente à leitura da exclamação (!) que só possui transição válida para um caractere igual
        'ler_variavel', # 5 o estado para o qual o automato transita (a partir de 1) quando le uma letra ou underscore
        'ler_digito', # o estado para o qual o automato transita (à partir de 1) quando le um digito
        'criar_token_reservado_ou_variavel', # no estado 7, deve ser realizada uma consulta a tabela de simbolos para, depois da extração do lexema, verificar se ele é uma palavra reservada da linguagem ou uma variável, aqui a tupla (token, tipotoken) é criada, sendo uma variável (TipoToken.VAR) ou uma palavra reservada da linguagem
        'criar_token_numerico', # o estado 8 vem de uma transição do estado 6, onde ocorre a leitura de digitos, neste estado, quando ocorre a finalização da leitura de digitos, é criado uma tupla (token, TipoToken.NUM).
        'criar_token_fim_de_arquivo_nao_esperado', # qualquer estado pode transitar para este quando encontra um fim de arquivo nao esperado
        'criar_token_invalido', # qualquer estado pode transitar para este quando processa algum lexema inválido
        'criar_token_fim_de_arquivo', # se o estado pode __processar um fim de arquivo valido, então, transita para cá
        ]
    )

    def __init__(self, caminho_arquivo: str):
        self.AFD = {
            self.estados.inicial: self.__processar_estado_1,
            self.estados.ler_comentarios: self.__processar_estado_2,
            self.estados.ler_atribuicao_comparacao_ou_igualdade: self.__processar_estado_3,
            self.estados.ler_nao_igual: self.__processar_estado_4,
            self.estados.ler_variavel: self.__processar_estado_5,
            self.estados.ler_digito: self.__processar_estado_6,
            self.estados.criar_token_reservado_ou_variavel: self.__processar_estado_7,
            self.estados.criar_token_numerico: self.__processar_estado_8,
            self.estados.criar_token_fim_de_arquivo_nao_esperado: self.__processar_estado_9,
            self.estados.criar_token_invalido: self.__processar_estado_10,
            self.estados.criar_token_fim_de_arquivo: self.__processar_estado_11
        }
        try:
            self.__ler_programa(caminho_arquivo)
        except FileNotFoundError as fe:
            raise fe
        self.cabecote = 0
        self.simbolo_terminal = ''
        self.linhas = 0

    def __ler_programa(self, caminho_arquivo: str):
        try:
            with open(caminho_arquivo, 'r') as f:
                self.programa = f.read()
        except FileNotFoundError as fe:
            raise Exception('O arquivo {} não foi encontrado!'.format(caminho_arquivo))

    def __avancar(self) -> str:
        try:
            caractere = self.programa[self.cabecote]
            self.cabecote += 1
        except IndexError as ie: # chegou ao caractere final do programa, portanto, caractere deve ser vazio
            caractere = ''
        return caractere

    def __retroceder(self, c):
        if c != '':
            self.cabecote -= 1

    def __processar_estado_1(self, c):
        if c == ' ' or c == '\r' or c == '\t':
            return self.estados.inicial
        elif c == '\n':
            self.linhas += 1
            return self.estados.inicial
        elif c == '#':
            return self.estados.ler_comentarios
        elif c == '=' or c == '<' or c == '>':
            self.simbolo_terminal += c
            return self.estados.ler_atribuicao_comparacao_ou_igualdade
        elif c == '!':
            self.simbolo_terminal += c
            return self.estados.ler_nao_igual
        elif c == ';' or c == '+' or c == '-' or c == '*' or c == '/' or c == '%':
            self.simbolo_terminal += c
            return self.estados.criar_token_reservado_ou_variavel
        elif c.isalpha() or c == '_':
            self.simbolo_terminal += c
            return self.estados.ler_variavel
        elif c.isdigit():
            self.simbolo_terminal += c
            return self.estados.ler_digito
        elif c == '':
            return self.estados.criar_token_fim_de_arquivo
        else:
            self.simbolo_terminal += c
            return self.estados.criar_token_invalido

    def __processar_estado_2(self, c):
        pass

    def __processar_estado_3(self, c):
        pass

    def __processar_estado_4(self, c):
        pass
    
    def __processar_estado_5(self, c):
        pass
    
    def __processar_estado_6(self, c):
        pass
    
    def __processar_estado_7(self):
        pass
    
    def __processar_estado_8(self):
        pass
    
    def __processar_estado_9(self):
        return (self.simbolo_terminal, self.TipoToken.UNEXPECTED_EOF)
    
    def __processar_estado_10(self):
        return (self.simbolo_terminal, self.TipoToken.INVALID_TOKEN)
    
    def __processar_estado_11(self):
        return (self.simbolo_terminal, self.TipoToken.END_OF_FILE)


    def proximo_token(self) -> tuple[str, TipoToken]:
        self.simbolo_terminal = ''
        estado = self.estados.inicial
        while estado != self.estados.criar_token_reservado_ou_variavel and estado != self.estados.criar_token_numerico and estado != self.estados.criar_token_fim_de_arquivo_nao_esperado and estado != self.estados.criar_token_invalido and estado != self.estados.criar_token_fim_de_arquivo:
            # proximo caractere
            c = self.__avancar()
            # explicito é melhor do que implicito
            # meu AFD é um dicionario que mapeia funcoes (valores)
            # a estados (chaves) onde, ao acessar o AFD[estado], eu obtenho
            # a funcao que processa o estado corrente. Ela deve receber por paremetro
            # o caractere c lido por __avancar e retorna o proximo estado que depende
            # da transicao realizada pela funcao de processamento de estado
            estado = self.AFD[estado](c)
        lexema = self.AFD[estado]()
        return lexema

    def todos_os_tokens(self) -> str:
        tokenlist = []
        token, tipo = self.proximo_token()
        while tipo != self.TipoToken.END_OF_FILE and tipo != self.TipoToken.INVALID_TOKEN and tipo != self.TipoToken.UNEXPECTED_EOF:
            tokenlist.append((token, tipo))
            token, tipo = self.proximo_token()
        if tipo == self.TipoToken.END_OF_FILE:
            tokenlist.append((token, tipo))
        elif tipo == self.TipoToken.INVALID_TOKEN:
            tokenlist.append('Linha {:02d} Lexema Inválido {}'.format(self.linhas, token))
        elif tipo == self.TipoToken.UNEXPECTED_EOF:
            tokenlist.append('Linha {:02d} Fim de arquivo inesperado'.format(self.linhas))
        return '\n'.join([str(x) for x in tokenlist])
