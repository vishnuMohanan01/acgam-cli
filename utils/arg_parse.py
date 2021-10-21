import argparse


def init_arg_parser():
    arg_parser = argparse.ArgumentParser(prog='acgam-cli',
                                         usage='python3 main.py [options] [value]',
                                         description='generates certificates for given recipients and mails them')
    arg_parser.add_argument('-t',
                            '--template',
                            action='store',
                            required=True,
                            choices=["comsoc", "cs", "ias", "sb", "wie"],
                            help='specify the name of the certificate template to be used')
    arg_parser.add_argument('-z',
                            '--zone-name',
                            action='store',
                            required=True,
                            help='Takes in name of the zone.')

    return arg_parser

