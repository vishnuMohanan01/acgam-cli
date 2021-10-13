import os


def make_gen_certs_dir(gen_certs_dir, event_name):
    if not os.path.isfile(os.path.join(gen_certs_dir)):
        os.mkdir(os.path.join(gen_certs_dir))

    from datetime import datetime
    curr_time_stamp = datetime.now().strftime("%d-%b-%Y_(%H:%M:%S)")
    certs_store_dir = f"{event_name}_{curr_time_stamp}"
    os.mkdir(os.path.join(gen_certs_dir, certs_store_dir))

    return certs_store_dir
