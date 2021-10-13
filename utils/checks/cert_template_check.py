import os

from error_lib import *


class CertTemplateCheck:
    """Add checks as private methods and call them in begin() method."""

    def __init__(self, template_dir):
        self.template_dir = template_dir

    def __template_dir_check(self):
        if not os.path.isfile(os.path.join(self.template_dir)):
            raise GeneralError(f"Template Directory {self.template_dir} doesn't exist.")

    # TODO: add check for template to be used in current execution

    def begin(self):
        self.__template_dir_check()
