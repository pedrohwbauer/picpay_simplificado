from django.core.exceptions import ValidationError

def validate_cpf(value):
    # Remove qualquer caractere não numérico
    cpf = ''.join([char for char in value if char.isdigit()])

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        raise ValidationError('CPF inválido')

    # Verifica se todos os dígitos são iguais (caso especial inválido)
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido')

    # Calcula o primeiro dígito verificador
    sum = 0
    for i in range(9):
        sum += int(cpf[i]) * (10 - i)
    first_check_digit = (sum * 10 % 11) % 10

    # Calcula o segundo dígito verificador
    sum = 0
    for i in range(10):
        sum += int(cpf[i]) * (11 - i)
    second_check_digit = (sum * 10 % 11) % 10

    # Verifica se os dígitos verificadores estão corretos
    if first_check_digit != int(cpf[9]) or second_check_digit != int(cpf[10]):
        raise ValidationError('CPF inválido')        
