import argparse
import os


class ArgParser:
    def __init__(self):
        self.program_name = os.environ["PROGRAM_NAME"]

    def __init_arg_parser(self):
        arg_parser = argparse.ArgumentParser(prog=self.program_name,
                                             usage='python3 main.py [options] [value]',
                                             description='Generates and mails certificates for given recipients.')
        # TODO: add this feature
        arg_parser.add_argument('-a',
                                '--add-event',
                                action='store',
                                # required=True,
                                help='To add an event  to DB. Specify the event name as value. Returns event ID.')
        arg_parser.add_argument('-d',
                                '--date',
                                action='store',
                                # required=True,
                                help='To specify the event date.')
        arg_parser.add_argument('-f',
                                '--file',
                                action='store',
                                # required=True,
                                help='To specify the CSV file path.')
        # TODO: add this feature
        arg_parser.add_argument('-g',
                                '--get-event-id',
                                action='store',
                                # required=True,
                                help='Specify the event name.')
        # TODO: Replace this feature with --event-id
        # Temp Feature
        arg_parser.add_argument('-e',
                                '--event-name',
                                action='store',
                                # required=True,
                                help='Specify the event id.')
        # TODO: add this feature
        arg_parser.add_argument('-E',
                                '--event-id',
                                action='store',
                                # required=True,
                                help='Specify the event id.')
        arg_parser.add_argument('-O',
                                '--organization',
                                action='store',
                                # required=True,
                                choices=["comsoc", "cs", "ias", "sb", "wie"],
                                help='Specify the name of the organization issuing the certificate.')
        arg_parser.add_argument('-N',
                                '--no-mail',
                                action='store_true',
                                help='Use this flag if generated certificates need not be mailed to the recipients.')
        arg_parser.add_argument('-T',
                                '--type',
                                action='store',
                                choices=["p", "participants", "w", "winners"],
                                # required=True,
                                help='Specify the type of the certificate being issued.')
        return arg_parser

    def get_args(self):
        args = self.__init_arg_parser().parse_args()
        return {
            "org_name": args.organization,
            "cert_type": args.type,
            "event_name": args.event_name,
            "csv_path": args.file,
            "event_date": args.date
        }