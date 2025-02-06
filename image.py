from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import random
from PIL import Image  # For displaying images

class ImageCrypto:
    def __init__(self):
        self.key = None

    def generate_key(self):
        self.key = get_random_bytes(32)

    def save_key(self, key_path):
        with open(key_path, 'wb') as file:
            file.write(self.key)

    def load_key(self, key_path):
        with open(key_path, 'rb') as file:
            self.key = file.read()

    def encrypt_image(self, input_path, output_path):
        try:
            with open(input_path, 'rb') as file:
                image_data = file.read()

            # Generate a random IV (Initialization Vector)
            iv = get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padded_data = pad(image_data, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)

            # Combine IV and encrypted data for saving
            encrypted_file_data = iv + encrypted_data

            # Save the encrypted file
            with open(output_path, 'wb') as file:
                file.write(encrypted_file_data)

            print(f"Image encrypted successfully! Saved to {output_path}")
        except Exception as e:
            print(f"Encryption error: {str(e)}")

    def decrypt_image(self, encrypted_path, output_path):
        try:
            with open(encrypted_path, 'rb') as file:
                encrypted_data = file.read()

            # Extract the IV and the encrypted image data
            iv = encrypted_data[:16]
            encrypted_image_data = encrypted_data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(encrypted_image_data)
            unpadded_data = unpad(decrypted_data, AES.block_size)

            # Write the decrypted data to output file
            with open(output_path, 'wb') as file:
                file.write(unpadded_data)

            print(f"Image decrypted successfully! Saved to {output_path}")
        except Exception as e:
            print(f"Decryption error: {str(e)}")

    def get_random_image(self, images_directory):
        """Select a random image from a given directory."""
        images = [img for img in os.listdir(images_directory) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if images:
            return os.path.join(images_directory, random.choice(images))
        else:
            print("No valid images found in the specified directory.")
            return None

    def display_image(self, image_path):
        """Display the image."""
        try:
            img = Image.open(image_path)
            img.show()  # This will open the image in the default image viewer
        except Exception as e:
            print(f"Error displaying image: {str(e)}")

if __name__ == "__main__":
    crypto = ImageCrypto()
    images_directory = "images"  # Folder where images are stored
    encrypted_image = "encrypted_image.bin"
    decrypted_image = "decrypted_image.jpg"
    key_file = "aes_key.bin"

    # Generate and save key if it doesn't exist
    if not os.path.exists(key_file):
        crypto.generate_key()
        crypto.save_key(key_file)
    else:
        crypto.load_key(key_file)

    # Get a random image from the directory
    random_image = crypto.get_random_image(images_directory)
    if random_image:
        print(f"Selected image for encryption: {random_image}")

        # Display the original image
        print("Displaying original image:")
        crypto.display_image(random_image)

        # Encrypt the image
        crypto.encrypt_image(random_image, encrypted_image)

        # Display message about encrypted image (binary format can't be displayed as image)
        print("Encrypted image is saved, but cannot be displayed as an image.")

        # Decrypt the image
        crypto.decrypt_image(encrypted_image, decrypted_image)

        # Display the decrypted image
        print("Displaying decrypted image:")
        crypto.display_image(decrypted_image)

    else:
        print("No images available for encryption.")
