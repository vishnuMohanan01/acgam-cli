import argparse
import os


class ArgParser:
    def __init__(self):
        self.program_name = os.environ["PROGRAM_NAME"]

    def __init_arg_parser(self):
        from .. import constants

        arg_parser = argparse.ArgumentParser(prog=self.program_name,
                                             usage='python3 main.py [options] [value]',
                                             description='Generates and mails certificates for given recipients.')
        arg_parser.add_argument('-d',
                                '--date',
                                action='store',
                                # required=True,
                                help='To specify the event date.')
        arg_parser.add_argument('-f',
                                '--csv-file',
                                action='store',
                                # required=True,
                                help='To specify the CSV file path.')
        arg_parser.add_argument('-e',
                                '--event-name',
                                action='store',
                                # required=True,
                                help='Specify the event id.')
        arg_parser.add_argument('-O',
                                '--organization',
                                action='store',
                                # required=True,
                                help='Specify the name of the organization issuing the certificate.')
        arg_parser.add_argument('-N',
                                '--no-mail',
                                action='store_true',
                                default=True,
                                help='Use this flag if generated certificates need not be mailed to the recipients. [Default]')
        arg_parser.add_argument('-r',
                                '--recipient-type',
                                action='store',
                                choices=constants.RECIPIENT_TYPES,
                                # required=True,
                                help='Specify the type of the certificate being issued.')
        arg_parser.add_argument('-t',
                                '--test',
                                action='store_true',
                                # required=True,
                                help='Use this flag for test runs. Generates certs, no mail, no logging to DB.')
        # Unimplemented
        # TODO: add these features
        arg_parser.add_argument('-a',
                                '--add-event',
                                action='store',
                                # required=True,
                                help='To add an event  to DB. Specify the event name as value. Returns event ID.')
        arg_parser.add_argument('-E',
                                '--event-id',
                                action='store',
                                # required=True,
                                help='Specify the event id.')
        arg_parser.add_argument('-g',
                                '--get-event-id',
                                action='store',
                                # required=True,
                                help='Specify the event name.')
        return arg_parser

    def get_args(self):
        args = self.__init_arg_parser().parse_args()
        return {
            "org_name": args.organization,
            "recipient_type": args.recipient_type,
            "event_name": args.event_name,
            "csv_path": args.file,
            "event_date": args.date
        }
