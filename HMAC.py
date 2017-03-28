#!/usr/bin/python
# -*- coding: utf-8 -*-
from hashlib import md5
import os
from re import compile
import sys


trans_5C = "".join(chr(x ^ 0x5c) for x in xrange(256))
trans_36 = "".join(chr(x ^ 0x36) for x in xrange(256))
blocksize = md5().block_size

## 	@brief 	 Função hmac_md5()
#	@details Função para gerar o hash do hmac
#	@param 	 key 	- chave usada para gerar o hash do hmac
#	@param 	 msg 		- conteúdo que gerará a hash
#	@return  retorna a hash
def hmac_md5(key, msg):
    if len(key) > blocksize:
        key = md5(key).digest()
    key += chr(0) * (blocksize - len(key))
    o_key_pad = key.translate(trans_5C)
    i_key_pad = key.translate(trans_36)
    hash = md5(o_key_pad + md5(i_key_pad + msg).digest()).hexdigest()
    return (hash)

## 	@brief 	 Função find()
#	@details Busca todos os arquivos recursivamente em todos os subdiretórios
#	@param 	 path 	- caminho onde fará a busca
#	@return  Retorna uma lista com o caminho de todos os arquivos encontrados
def find(path='.'):
    try:
        listdir = os.listdir(path)
    except Exception:
        listdir = []
    for item in listdir:
        fn = os.path.normpath(os.path.join(path, item))
        if os.path.isdir(fn):
            for f in find(fn):
                yield f
        else:
            yield fn

## 	@brief 	 Função salva_Hash()
#	@details Função salva o hash de cada arquivo em um arquivo guarda.txt para ser comparado posteriomente
#	@param 	 tmp 	- valor a ser validado e formatado
def salva_Hash(path):
    texto = ''
    for fn in find(path):
        arquivo = open(fn, 'r')
        x = arquivo.read()
        y = open(path+"guarda", "w")
        z = hmac_md5("teste", fn+x)
        texto += str(fn) + " --> " + str(z) + "\n"
        y.writelines(texto)

    arquivo.close()
    y.close()

## 	@brief 	 Função compara()
#	@details A função compara os hash e nomes de arquivos, procurando por arquivos deletados, criados ou alterados
#	@param 	 path   - Caminho onde está o arquivo guarda.txt para ser comparado
#	@return  Mostra as situções dos arquivos

def compara(path):
    x = []
    flag = False
    arquivos = open(path+"guarda", 'r')
    files = arquivos.read()
    x = str(files).split('\n')
    for fn in find(path):
        if(not(searchstring(str(fn),path + "guarda"))):
            print (fn + " Arquivo novo")

    for value in x:
        if (value == ''):
            break;

        flag = False
        for fn in find(path):
            if (fn == str(value).split(' --> ')[0]):
                flag = True
                arquivo = open(str(fn), 'r')
                file = arquivo.read()
                hash_old = (str(value).split(' --> ')[1])
                hash_new = hmac_md5("teste", fn+file)
                arquivo.close()
                if (hash_new == hash_old):
                    print (fn + "\t" + "não mudou")
                else:
                    print(fn + "\t" + "mudou")
                #print ("old " + hash_old + "\t" + str(value).split(' --> ')[0])
                #print ("new " + hash_new + "\t" + fn)
        if(not flag):
            print (value + " arquivo deletado")

def searchstring(String, File):
    FileSearch = open(File, 'r')
    ReadingFile = FileSearch.read()
    ReadingFile = ReadingFile.split('n')
    StringSearching = compile(String)
    for Line in ReadingFile:
        FoundString = StringSearching.search(Line)
        if (FoundString):
            return True
    FileSearch.close()
    return False

if __name__ == "__main__":
    action = str(sys.argv[1])
    path = str(sys.argv[2])
    if (action == '-i'):
        salva_Hash(path)
    elif (action == '-t'):
        try:
            os.path.isfile(path + "guarda")
            compara(path)
        except IOError:
            print u'Arquivo não encontrado!'
    elif (action == '-x'):
        os.system("rm " + path + "guarda")
        print ("Guarda removida")
