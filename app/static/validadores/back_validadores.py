#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from requests import get


class Validadores(object):

    def __init__(self):
        pass

    def validar_cpf(self, cpf):
        '''
        Valida CPFs, retornando apenas a string de números válida.

        # CPFs errados
        validar_cpf('abcdefghijk')
            False
        validar_cpf('123')
            False
        validar_cpf('')
            False
        validar_cpf(None)
            False
        validar_cpf('12345678900')
            False

        # CPFs corretos
        validar_cpf('95524361503')
            True
        validar_cpf('955.243.615-03')
            True
        validar_cpf('  955 243 615 03  ')
            True
        '''

        cpf = ''.join(re.findall('\d', str(cpf)))

        if (not cpf) or (len(cpf) < 11):
            return False

        # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
        inteiros = map(int, cpf)
        novo = inteiros[:9]

        while len(novo) < 11:
            r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)

        # Se o número gerado coincidir com o número original, é válido
        if novo == inteiros:
            return True
        return False

    def validar_cnpj(self, cnpj):
        """
        Valida CNPJs, retornando apenas a string de números válida.

        # CNPJs errados
         validar_cnpj('abcdefghijklmn')
        False
         validar_cnpj('123')
        False
         validar_cnpj('')
        False
         validar_cnpj(None)
        False
         validar_cnpj('12345678901234')
        False
         validar_cnpj('11222333000100')
        False

        # CNPJs corretos
         validar_cnpj('11222333000181')
        '11222333000181'
         validar_cnpj('11.222.333/0001-81')
        '11222333000181'
         validar_cnpj('  11 222 333 0001 81  ')
        '11222333000181'
        """
        cnpj = ''.join(re.findall('\d', str(cnpj)))

        if (not cnpj) or (len(cnpj) < 14):
            return False

        # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
        inteiros = list(map(int, cnpj))
        novo = inteiros[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
            prod.insert(0, 6)

        # Se o número gerado coincidir com o número original, é válido

        if novo == inteiros:
            return True
        return False


    def valida_cnae(self, link, cnae1, cnae2):
        '''
        Método que verifica se uma cnae é válida
        Retorna 1 ou 2 significa que uma das cnae é inválida
        Caso não exista a cnae2, verifica só a cnae1
        '''
        print(cnae1)
        print(cnae2)
        cnae1 = cnae1.replace("-", "")
        cnae1 = cnae1.replace("/", "")
        cnae1 = get(link + cnae1)
        cnae1.raise_for_status()
        cnae1 = cnae1.json()
        if cnae2 != None:
            cnae2 = cnae2.replace("-", "")
            cnae2 = cnae2.replace("/", "")
            cnae2 = get(link + cnae2)
            cnae2.raise_for_status()
            cnae2 = cnae2.json()

        else:
            #Não existe a cnae 2 para ser validada
            cnae2 = 0

        if cnae2 != 0:
            if cnae1 and cnae2:
                return (7)

            elif cnae2:
                return (2)

            elif cnae1:
                return (1)

        elif cnae2 == 0:
            if cnae1:
                return (7)
            else:
                return (1)
