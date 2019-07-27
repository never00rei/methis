import logging
import yaml
import math
from base64 import b64encode, b64decode
import hashlib


"""
The purpose of this script is to take a peice of data: 
    1. split it into equal chunks,
    2. convert each chunk into binary "010010",
    3. base64 encode each new binary chunk,
    4. generate an md5 checksum for each new binary chunk
    5. randomly assign an md5 checksum as the password for part 2.
    6. dump the output as yaml to be loaded into the API.
"""

class Obscure():
    """
    The purpose of this class is to Obscure some data
    """

    def __init__(self, data=None, chunk_size=24):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        if data:
            self.data = data
        else:
            self.data = None

        self.chunk_size = chunk_size


    def process_data(self):
        """
        Process data passed through this function
        """
        
        self.logger.info('Processing data.')
        list_object = self._split_data_object()
        binary = self._convert_to_binary(input=list_object)
        base64 = self._base64_encode_binary(input=binary)
        checksums = self._generate_md5_checksum(input=base64)
        api_object = self._build_config_object(
            encoded_data=base64, 
            checksums=checksums)

        with open('data.yml', 'w') as outfile:
            yaml.dump(api_object, outfile, default_flow_style=False)


    def _split_data_object(self):
        """
        This function takes the 'self.data' object and splits it into
        equal chunks defined by the 'self.chunk_size' variable.
        """   

        size, remainder = divmod(len(self.data), self.chunk_size)
        chunks_sizes = [size + 1] * remainder + [size] * (self.chunk_size - remainder)
        offsets = [sum(chunks_sizes[:i]) for i in range(len(chunks_sizes))]

        return [self.data[o:o+s] for o, s in zip(offsets, chunks_sizes)]
    
    def _convert_to_binary(self, input):
        """
        This function takes the list object and converts it to binary.
        """
        try:
            binary_list = []
            for item in input:
                binary_list.append(" ".join(f"{ord(i):08b}" for i in item))
        except Exception as e:
            self.logger.error(f'Could not convert input to binary: {e}')
            raise 'Could not convert input to binary'

        return binary_list
    
    def _base64_encode_binary(self, input):
        """
        This function takes a list of binary and base64 encodes it
        """
        try:
            encoded_data = []
            for item in input:
                encoded_data.append(b64encode(item.encode('ascii')).decode('utf8'))
        except Exception as e:
            self.logger.error(f'Could not convert input to base64: {e}')
            raise 'Could not convert input to base64'

        return encoded_data

    def _generate_md5_checksum(self, input):
        """
        This function takes a base64 snippet and generates a corresponding 
        md5 checksum.
        """
        try:
            checksum_list = []
            for item in input:
                lookup = {}
                checksum = hashlib.md5(item.encode('ascii')).hexdigest()
                lookup[item.strip('=')] = dict(md5=checksum)
                checksum_list.append(lookup)
        except Exception as e:
            self.logger.error(f'Could not generate md5 checksum: {e}')
            raise 'Could not generate md5 checksum'

        return checksum_list

    def _build_config_object(self, encoded_data, checksums):
        """
        This function spits out a yaml object with 24 different hours worth of payload and checksums.
        """

        hour = 0
        api_config = {}
        for item in encoded_data:
            if hour <= 9:
                h = f'0{str(hour)}'
            else: 
                h = str(hour)
            for checksum in checksums:
                if item.strip('=') in checksum:
                    md5 = checksum[item.strip('=')]['md5']
            api_config[h] = dict(payload = item, checksum = md5)
            hour += 1

        return api_config
