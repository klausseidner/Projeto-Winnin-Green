# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela criptografia de senhas
############################################################################################################

############################################################################################################
# Importações necessárias
############################################################################################################
import os # Utilizado para gerar um salt
import hashlib # Utilizado para gerar o hash
import binascii # Utilizado para converter bytes para hexadecimal

############################################################################################################
# Função responsável por gerar o hash da senha
############################################################################################################
def hash_pass(password):
    """Hash de senha para senha forte."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii') # Gerar o salt
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000) # Gerar o hash da senha
    pwdhash = binascii.hexlify(pwdhash) # Convertendo o hash para hexadecimal
    return (salt + pwdhash)  # return bytes

############################################################################################################
# Função responsável por verificar se a senha está correta
############################################################################################################
def verify_pass(provided_password, stored_password):
    """Verifique uma senha armazenada em relação a uma fornecida pelo usuário"""
    stored_password = stored_password.decode('ascii') # Convertendo o hash para hexadecimal e decodificando
    salt = stored_password[:64] # Pegando o salt
    stored_password = stored_password[64:] # Pegando o hash da senha
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000) # Gerando o hash da senha
    pwdhash = binascii.hexlify(pwdhash).decode('ascii') # Convertendo o hash para hexadecimal e decodificando
    return pwdhash == stored_password # Retornando True se a senha for correta, senão retornando False

############################################################################################################