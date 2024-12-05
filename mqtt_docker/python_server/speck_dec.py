from speck import SpeckCipher

# Define the 128-bit key used in Arduino code
key = 0x0f0e0d0c0b0a09080706050403020100  # Convert the key to a 16-byte integer

# Cipher text (in hexadecimal format) from ESP32 monitor
cipher_hex = "90 1f ac de 9e ce 66 3e 74 6d 67 18 06 61 ef a5 8a 0d 18 38 97 8c b3 6e 9e 75 18 44 50 a7 2a f8 "

# Convert hex string to bytes
cipher_text = bytes(int(x, 16) for x in cipher_hex.split())

# Initialize the SpeckCipher object
speck = SpeckCipher(key, key_size=128, block_size=128)

# Decrypt function
def decrypt_speck(speck, cipher_text):
    block_size = 16  # Speck128 block size in bytes
    plain_text = b""

    # Decrypt each block
    for i in range(0, len(cipher_text), block_size):
        block = cipher_text[i:i + block_size]
        # Convert block to integer for decryption
        block_int = int.from_bytes(block, byteorder="big")
        decrypted_block_int = speck.decrypt(block_int)
        # Convert decrypted integer block back to bytes
        decrypted_block = decrypted_block_int.to_bytes(block_size, byteorder="big")
        plain_text += decrypted_block

    return plain_text

def remove_padding(data):
    # Remove trailing zeros added as padding
    return data.rstrip(b'\x00').decode('utf-8')  # Decode only after padding removal

# Perform decryption
plain_text = decrypt_speck(speck, cipher_text)

# Print decrypted text before and after removing padding
print("Decrypted Text (raw bytes):", plain_text)

# Remove padding and decode to string
decrypted_text = remove_padding(plain_text)
print("Decrypted Text (decoded):", decrypted_text)
