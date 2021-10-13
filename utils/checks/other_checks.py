import os

from ..error_lib import *


class OtherCheck:
    """Add checks as private methods and call them in begin() method."""

    def __init__(self, certs_store_dir):
        self.certs_store_dir = certs_store_dir

    def __gen_certs_dir_check(self):
        if not os.path.isfile(os.path.join(self.certs_store_dir)):
            raise GeneralError(f"Directory {self.certs_store_dir} not created.")

    def begin(self):
        self.__gen_certs_dir_check()
