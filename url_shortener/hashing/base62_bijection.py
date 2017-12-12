# -*- coding: utf-8 -*-
import string

from .base import BaseHasher


class Base62_Hasher(BaseHasher):

    """
    Class that provides methods to encode natural numbers to ascii string and string to previously encoded number. It's based on a bijective function that uses a 62-character alphabet. 

    Algorithm: when encoding the number is converted from base 10 to length-of-alpahbet-base (base 62 in this case) by factorizing it using that base. The resulting factors are then mapped to characters in the alphabet. The result of concatenating all the characters mapped in previous step is the hashed number.
    When decoding the string the characters forming it are individually converted from base 62 to base 10 based on their position in the string summing up each of resulting values. The result of that sum is the decoded number.

    """

    _base_62_alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    _alphabet_length = len(_base_62_alphabet)

    def encode(self, number):
        """
        :param number: non-zero positive number
        :returns: string
        :raises ValueError
        """
        if not isinstance(number, int) and number <= 0:
            raise ValueError('Input must be non-zero and positive number')
        string_ = ''
        digits = []
        while(number > 0):
            string_ += self._base_62_alphabet[number % self._alphabet_length]
            number //= self._alphabet_length
        return string_

    def decode(self, string_):
        """
        :param number: string
        :returns: non-zero positive number
        :raises TypeError
        """
        if not isinstance(string_, str):
            raise TypeError('Input must be an string')
        decoded = 0
        for digit, char in enumerate(string_):
            alphabet_index = self._base_62_alphabet.index(char)
            decoded += alphabet_index * self._alphabet_length ** digit
        return decoded
