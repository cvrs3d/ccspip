# Number 1: Write yet another function that solves for element n of the Fibonacci sequence,
#  using a technique of your own design. Write unit tests that evaluate its correct
# ness and performance relative to the other versions in this chapter.
import math
from typing import Generator, Generic, TypeVar, List, Tuple
import numpy as np
import random
from PIL import Image


def ex_fibonacci(n: int) -> int:
    value = (1 + math.sqrt(5)) / 2
    return round((value ** n) / math.sqrt(5))


# Number 2:  You saw how the simple int type in Python can be used to represent a bit string.
#  Write an ergonomic wrapper around int that can be used generically as a
#  sequence of bits (make it iterable and implement __getitem__()). Reimple
# ment CompressedGene, using the wrapper.

class BitArray:
    def __init__(self, bit_string: int = 0) -> None:
        self.bit_string = bit_string

    def __getitem__(self, index: int) -> int:
        """This function return the bit at given index"""
        if index < 0 or index >= self.bit_length():
            raise IndexError("Bit index out of range")
        return (self.bit_string >> index) & 1

    def __iter__(self):
        """Allow this class to be iterable"""
        for i in range(self.bit_length()):
            yield self[i]

    def bit_length(self) -> int:
        """Returns a bit length of bitstring"""
        return self.bit_string.bit_length()

    def __str__(self) -> str:
        """Return bit string as a binary without 0b"""
        return bin(self.bit_string)[2:]


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_array = BitArray(1)  # Start with sentinel bit 1
        for nucleotide in gene.upper():
            self.bit_array.bit_string <<= 2  # Shift left 2 bits
            if nucleotide == 'A':
                self.bit_array.bit_string |= 0b00  # Set last two bits
            elif nucleotide == 'C':
                self.bit_array.bit_string |= 0b01
            elif nucleotide == 'G':
                self.bit_array.bit_string |= 0b10
            elif nucleotide == 'T':
                self.bit_array.bit_string |= 0b11
            else:
                raise ValueError(f"Invalid nucleotide: {nucleotide}")

    def decompress(self) -> str:
        gene: str = ""
        # Skip the sentinel bit
        for i in range(0, self.bit_array.bit_length() - 1, 2):
            bits: int = (self.bit_array.bit_string >> i) & 0b11  # Get 2 bits
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError(f"Invalid bits: {bits}")
        return gene[::-1]  # Reverse the string to get the original order

    def __str__(self) -> str:
        return self.decompress()


# Number 3:  Write a solver for The Towers of Hanoi that works for any number of towers

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

    def isempty(self) -> bool:
        value = None
        try:
            value = self._container.pop()
        except IndexError:
            return True
        finally:
            if value:
                self._container.append(value)
                return False


def towers_of_hanoi(n: int, source: Stack[int], target: Stack[int], auxiliary_towers: List[Stack[int]]) -> None:
    num_towers: int = len(auxiliary_towers) + 2
    if n == 0:
        return

    if num_towers == 3:
        if n == 1:
            target.push(source.pop())
        else:
            temp = auxiliary_towers[0]
            towers_of_hanoi(n - 1, source, temp, [target])
            target.push(source.pop())
            towers_of_hanoi(n - 1, temp, target, [source])
    else:
        k = n - 1
        new_auxiliary = auxiliary_towers[:-1]
        intermediate = auxiliary_towers[-1]
        towers_of_hanoi(k, source, intermediate, new_auxiliary + [target])
        target.push(source.pop())
        towers_of_hanoi(k, intermediate, target, new_auxiliary + [source])


# Number 4: Use a one-time pad to encrypt and decrypt images.

def random_key(length: int) -> int:
    key = random.getrandbits(length * 8)
    return key


def encrypt_image(image_path: str) -> Tuple[int, int, Tuple[int, int], str]:
    """This function using PIL or Pillow library with context manager to open an image
        It is more useful to use PIL because it allows to perform various operations on images
        Function uses so called OTP to encrypt a bit-sequence, which requires a key and a string
        Output will contain a dummy data and our string
        The random key (dummy) must be kept secure and never reused for another encryption.
         The one-time pad is theoretically unbreakable if the key is truly random,
          used only once, and kept secret.
          Basically we are doing simple XOR a^b operation here
    """
    with Image.open(image_path) as img:
        img_bytes = np.array(img).tobytes()
        img_size = img.size  # (width, height)
        img_mode = img.mode  # Image mode, e.g., "RGB"

    dummy: int = random_key(len(img_bytes))
    image_key: int = int.from_bytes(img_bytes, "big")
    encrypted: int = image_key ^ dummy
    return dummy, encrypted, img_size, img_mode


def decrypt_image(dummy: int, encrypted: int, output_path: str, image_size: Tuple[int, int], image_mode: str) -> None:
    # Decrypt the image using XOR
    decrypted: int = dummy ^ encrypted

    # Calculate the expected number of bytes based on image mode
    expected_size = image_size[0] * image_size[1]
    if image_mode != 'L':  # Non-grayscale images
        expected_size *= len(image_mode)

    # Convert the decrypted int back to bytes
    decrypted_bytes: bytes = decrypted.to_bytes(expected_size, "big")

    # Convert bytes back to the original image format
    if image_mode == 'L':  # Grayscale image
        img_array = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(image_size[1], image_size[0])
    else:  # Color image
        img_array = np.frombuffer(decrypted_bytes, dtype=np.uint8).reshape(image_size[1], image_size[0],
                                                                           len(image_mode))

    # Create an image from the array and save it
    img = Image.fromarray(img_array, image_mode)
    img.save(output_path)


dummy_key, encrypted_image, img_size, img_mode = encrypt_image('input_image.png')

# Decrypt the image
decrypt_image(dummy_key, encrypted_image, 'output_image.png', image_size=img_size, image_mode="RGB")
