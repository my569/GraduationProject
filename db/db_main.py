from acm import acm_db
from ccf import ccf_db

import os

if __name__ == '__main__':
    acm_db = acm_db.ACM_DB()
    acm_db.run()
    ccf_db = ccf_db.CCF_DB()
    ccf_db.run()