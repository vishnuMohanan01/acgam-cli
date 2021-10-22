import os

import pandas as pd

from utils.cert.cert import Cert
from utils.checks.cert_template_check import CertTemplateChecks
from utils.checks.df_checks import DFChecks
from utils.checks.other_checks import OtherChecks
from utils.error_lib import *
from utils.make_dirs_and_files import make_gen_certs_dir
from utils.parse_args import ArgParser


if __name__ == '__main__':
    # importing constants
    import constants

    # env vars
    EXECUTION_MODE = os.environ["EXECUTION_MODE"]

    # parsing args
    args = ArgParser().get_args()

    # derived vars
    is_winners = args["cert_type"] in ["winners", "w"]

    recipients_df = None
    if os.path.isfile(os.path.join(args["csv_path"])):
        recipients_df = pd.read_csv(args["csv_path"])
    else:
        raise GeneralError(f"Given CSV File {args['csv_path']} doesn't exist.")

    # dataframe file checks
    DFChecks(df=recipients_df, is_winners=is_winners).begin()

    # cert template checks
    CertTemplateChecks(template_dir=constants.TEMPLATE_DIR).begin()

    # creating useful dirs and files
    certs_store_dir = make_gen_certs_dir(gen_certs_dir=constants.GENERATED_CERTS_DIR, event_name=args["event_name"])

    # other checks
    OtherChecks(certs_store_dir=certs_store_dir).begin()

    # creating and sending certificates
    cert = Cert(cert_template_name,
                recipient_type,
                event_name,
                event_start_date,
                is_winner,
                template_path)
    purpose = "{} - {}".format(cert.event_name, cert.certificate_title)
    email_error_list = []
    #
    # try:
    #     index = 0
    #     for recipient_name, recipient_email, college_name in zip(recipient_names, recipient_emails, college_names):
    #         cert_path = cert.create(recipient_name, college_name, None if not is_winner else winner_positions[index], dir_name, event_id, recipient_email)
    #         error_email = mail(cert, recipient_email)
    #         if error_email is not None:
    #             email_error_list.append(error_email)
    #         index += 1
    # except Exception as e:
    #     sys.stderr.write(str(e))
    #     sys.stdout.flush()
    #     if os.path.exists(cert_gen_dir_path):
    #         if len(os.listdir(cert_gen_dir_path)) != 0:
    #             try:
    #                 notify(cert_gen_dir_path, auth_user_email, auth_user_name, purpose, False, action_time, email_error_list, csv_file_path)
    #             except Exception as e:
    #                 shutil.rmtree(cert_gen_dir_path)
    #                 os.remove(csv_file_path)
    #                 sys.stdout.write("There was an issue.")
    #                 sys.stdout.flush()
    #                 sys.stdout.write("exit")
    #                 sys.stdout.flush()
    #                 exit()
    #             shutil.rmtree(cert_gen_dir_path)
    #             os.remove(csv_file_path)
    #             sys.stdout.flush()
    #         else:
    #             os.rmdir(cert_gen_dir_path)
    #     os.remove(csv_file_path)
    #     sys.stdout.write("There was an issue.")
    #     sys.stdout.flush()
    #     sys.stdout.write("exit")
    #     sys.stdout.flush()
    #     exit()
    #
    # try:
    #     notify(cert_gen_dir_path, auth_user_email, auth_user_name, purpose, True, action_time, email_error_list, csv_file_path)
    # except Exception as e:
    #     shutil.rmtree(cert_gen_dir_path)
    #     os.remove(csv_file_path)
    #     sys.stdout.flush()
    #     sys.stdout.write("exit")
    #     sys.stdout.flush()
    #     exit()
    # shutil.rmtree(os.path.join(cert_gen_dir_path, "..", "zipped"))
    # os.remove(csv_file_path)
    # shutil.rmtree(cert_gen_dir_path)
    # sys.stdout.flush()
    # sys.stdout.write("exit")
    # sys.stdout.flush()
    # exit()
