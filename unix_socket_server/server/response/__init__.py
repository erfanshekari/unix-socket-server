from io import BytesIO
from typing import Union, BinaryIO
from ._exceptions import (
    ResponseIsNotChunked,
     InputIsNotReadable, 
     UnableToHandleInput
)

class Response:
    def __init__(self, input: Union[bytes, BinaryIO], buff_size: int=4096) -> None:
        self.buff_size = buff_size
        self.input = input
        self.io = None
        if not type(self.input) is bytes:
            if not hasattr(self.input, 'read') or not hasattr(self.input, 'readable'):
                raise UnableToHandleInput()
            if not self.input.readable():
                raise InputIsNotReadable()
            self.io = BytesIO(input.read())
        else:
            self.io = BytesIO(input)

        self.total_len = self.io.getbuffer().nbytes

        if self.is_chunked:
            self.total_parts = int(self.total_len / self.buff_size)

    @property
    def is_chunked(self) -> bool:
        return self.total_len > self.buff_size
    
    @property
    def chunked_response(self):
        if not hasattr(self, 'total_parts'):
            raise ResponseIsNotChunked()
        current_part_index = 0
        while current_part_index <= self.total_parts:
            start = current_part_index * self.buff_size
            end = start + self.buff_size
            yield self.response[start:end]
            current_part_index += 1
    
    @property
    def response(self) -> bytes:
        return self.io.getvalue()
    
        
        
        
