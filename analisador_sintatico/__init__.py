from analisador_lexico import AnalisadorLexico
import pdb

class AnalisadorSintatico():
    def __init__(self, lex : AnalisadorLexico, verbose: bool = False):
        self.lex = lex
        self.lexema_corrente = self.lex.proximo_token()
        self.verbose = verbose
    def __avancar(self):
        self.lexema_corrente = self.lex.proximo_token()
    def __comer(self, tipo_token : AnalisadorLexico.TipoToken):
        if self.verbose:
            print('Token Esperado (..., {}), encontrado: (\'{}\', {}'.format(
                tipo_token,
                self.lexema_corrente[0],
                self.lexema_corrente[1]
                )
            )
            if (tipo_token == self.lexema_corrente[1]):
                self.__avancar()
            else:
                self.__propagar_erro()
    def __propagar_erro(self):
        mensagem_erro = '{:02d}: '.format(self.lex.linhas)
        match self.lexema_corrente[1]:
            case self.lex.TipoToken.INVALID_TOKEN:
                mensagem_erro += 'Lexema Inválido [{}]\n'.format(self.lexema_corrente[0])
            case self.lex.TipoToken.UNEXPECTED_EOF | self.lex.TipoToken.END_OF_FILE:
                mensagem_erro += 'Fim de arquivo inesperado \n'
            case _:
                mensagem_erro += 'Lexema não esperado [{}]\n'.format(self.lexema_corrente[0])
        raise Exception(mensagem_erro)

    def __raiz(self): # comeca pelo simbolo inicial da nossa arvore de derivacao
        # esperamos construir uma arvore de derivacao que tenha o simbolo
        # terminal program na raiz
        self.__processar_program() 
        # esperamos que após gerar uma arvore de derivacao valida
        # consumamos por fim, um token de fim de arquivo
        self.__comer(self.lex.TipoToken.END_OF_FILE)

    # Na gramática EBNF de tiny, o método processar_program equivale à regra
    # <program> ::= program <cmdlist>
    def __processar_program(self):
        # queremos processar (comer) um token correspondente à palavra reservada processar_program
        self.__comer(self.lex.TipoToken.PROGRAM)
        # se recebemos o token correto, queremos consumir a lista de comandos que um program possui
        self.__processar_cmdlist()

    # Na gramática EBNF de tiny, o método processar_cmdlist equivale à regra
    # <cmdlist> ::= <cmd> { <cmd> }
    def __processar_cmdlist(self):
        pass

    # Na gramática EBNF de tiny, o método processar_cmd equivale à regra
    # <cmd> ::= (<assign> | <output> | <if> | <while>);
    def __processar_cmd(self):
        pass

    # Na gramática EBNF de tiny, o método processar_cmd_atribuicao equivale à regra
    # <assign> ::= <var> = <intexpr>
    def __processar_cmd_atribuicao(self):
        pass

    # Na gramática EBNF de tiny, o método processar_cmd_saida equivale à regra
    # <output> ::= output <intexpr>
    def __processar_cmd_saida(self):
        pass

    # Na gramática EBNF de tiny, o método processar_cmd_se equivale à regra
    # <if> ::= if <boolexpr> then <cmdlist> [ else <cmdlist> ] done
    def __processar_cmd_se(self):
        pass


    # Na gramática EBNF de tiny, o método processar_cmd_se equivale à regra
    # <while> ::= while <boolexpr> do <cmdlist> done
    def __processar_cmd_repeticao(self):
        pass

    # Na gramática EBNF de tiny, o método processar_expressao_booleana equivale à regra
    # <boolexpr>  ::= false | true |
    #                 not <boolexpr> |
    #                 <intterm> (== | != | < | > | <= | >=) <intterm>

    def __processar_expressao_booleana(self):
        pass

    # Na gramática EBNF de tiny, o método processar_expressao_inteiros equivale à regra
    # <intexpr>   ::= [ + | - ] <intterm> [ (+ | - | * | / | %) <intterm> ]
    def __processar_expressao_inteiros(self):
        pass

    # Na gramática EBNF de tiny, o método processar_termo_inteiro equivale à regra
    # <intterm> ::= <var> | <const> | read
    def __processar_termo_inteiro(self):
        pass

    # Na gramática EBNF de tiny, o método processar_var equivale à regra
    # <var> ::= id
    def __processar_var(self):
        pass

    # Na gramática EBNF de tiny, o método processar_constante equivale à regra
    # <const> ::= number
    def __processar_constante(self):
        pass

    def analisar(self):
        self.__raiz()
