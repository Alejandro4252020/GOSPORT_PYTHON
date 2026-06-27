import re
from django.core.exceptions import ValidationError

def validar_seguridad_contrasena(password):
    if not password:
        raise ValidationError('La contraseña no puede estar vacía.')
    
    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
        
    if not password[0].isupper():
        raise ValidationError('La primera letra de la contraseña debe ser mayúscula.')
        
    if not any(char.isdigit() for char in password):
        raise ValidationError('La contraseña debe contener al menos un número.')
        
    # Requerir al menos un carácter especial (no alfanumérico)
    if not re.search(r'[^a-zA-Z0-9]', password):
        raise ValidationError('La contraseña debe contener al menos un carácter especial (ej. !, @, #, $, etc.).')
