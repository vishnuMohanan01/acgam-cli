import os

from error_lib import *


class OtherCheck:
    """Add checks as private methods and call them in begin() method."""

    def __init__(self, gen_certs_dir):
        self.gen_certs_dir = gen_certs_dir

    def __gen_certs_dir_check(self):
        if not os.path.isfile(os.path.join(self.gen_certs_dir)):
            raise GeneralError(f"Directory {self.gen_certs_dir} doesn't exist.")

    def begin(self):
        self.__gen_certs_dir_check()
