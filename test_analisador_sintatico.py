from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
import sys

a_lex = AnalisadorLexico(sys.argv[1])
a_sn = AnalisadorSintatico(a_lex, True)
a_sn.analisar()
