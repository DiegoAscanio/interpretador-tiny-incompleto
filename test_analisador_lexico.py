from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
import sys

a_lex = AnalisadorLexico(sys.argv[1])
token, tipo = a_lex.proximo_token()

while tipo != a_lex.TipoToken.END_OF_FILE and tipo != a_lex.TipoToken.INVALID_TOKEN and tipo != a_lex.TipoToken.UNEXPECTED_EOF:
    print((token, tipo))
    token, tipo = a_lex.proximo_token()
if tipo == a_lex.TipoToken.END_OF_FILE:
    print((token, tipo))
elif tipo == a_lex.TipoToken.INVALID_TOKEN:
    print('Linha {:02d} Lexema Inválido {}'.format(a_lex.linhas, token))
elif tipo == a_lex.TipoToken.UNEXPECTED_EOF:
    print('Linha {:02d} Fim de arquivo inesperado'.format(a_lex.linhas))
