
import base64
from datetime import datetime
import random

def generate_id():
    # Obtén el tiempo actual en milisegundos desde la época
    current_time_ms = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
    current_time_ms = str(current_time_ms)

    # Convierte el tiempo actual a una cadena en base 32
    time_str_base32 = base64.b64encode(bytearray(current_time_ms, 'ascii')).decode('utf-8')

    # Genera un número aleatorio y conviértelo a una cadena en base 32
    random_number = str(random.random())
    random_str_base32 = base64.b64encode(bytearray(random_number,'ascii')).decode('utf-8')

    # Combina las dos cadenas generadas
    result = time_str_base32 + random_str_base32

    return result