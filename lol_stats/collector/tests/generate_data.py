import random
import string

class GenarateData:

    def get_random_string(length):
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str