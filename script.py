import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuración inicial
ds = "OSnaALIWUkpOziVAMycaZQ=="  # Uso el valor real de "ds"
algorithm = "AES"  # Cmbio al algoritmo utilizado por la app (e.g., AES)
expected_decrypted_text = "master_on"  # Texto esperado después de desencriptar

def generate_key(static_key: int) -> bytes:
    """
    Genera una clave de 16 bytes a partir del PIN.
    """
    key_bytes = bytearray(16)
    static_key_bytes = str(static_key).encode("utf-8")
    key_bytes[:len(static_key_bytes)] = static_key_bytes[:16]
    return bytes(key_bytes)

def decrypt(ds2: str, key: int) -> str:
    """
    Desencripta el texto cifrado con la clave generada.
    """
    secret_key = generate_key(key)
    cipher = AES.new(secret_key, AES.MODE_ECB)  # Modo ECB con PKCS5 Padding
    encrypted_bytes = base64.b64decode(ds2)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    return unpad(decrypted_bytes, AES.block_size).decode("utf-8")

# Fuerza bruta para encontrar el PIN
def brute_force(ds: str, expected_text: str, max_attempts: int = 999):
    for key in range(max_attempts + 1):  # De 0 a 999
        try:
            result = decrypt(ds, key)
            if result == expected_text:
                print(f"Bien!!! El PIN es: {key:03d}")
                return key
        except Exception:
            # Ignorar errores de desencriptación
            continue
    print("No se pudo encontrar el PIN")
    return None

# Ejecutar fuerza bruta
if __name__ == "__main__":
    brute_force(ds, expected_decrypted_text)
