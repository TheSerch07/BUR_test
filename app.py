import os
import certifi

from datetime import datetime
from flask import Flask, request
# from flask_cors import CORS

# packages for logging module
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s')

from utils_backend import ENVIRONMENT

app = Flask(__name__)
# CORS(app)

# app.register_blueprint(IPR_blueprint)
# app.register_blueprint(PVT_blueprint)
# app.register_blueprint(VLP_blueprint)
# app.register_blueprint(OutflowInflow_blueprint)

############################################################################
##################### requests logger modules ##############################
@app.before_request
def before_request_func():
    ## set up log folder
    if ENVIRONMENT == 'development':
        logpath = '/home/ubuntu/log/drillbi_bur/requests'
    else:
        logpath = '/mnt/log/drillbi_bur/requests'

    ## get the api_name, and construct the save_path
    urlstring = request.url
    try:
        api_name = urlstring.split("enovate.app/")[1].split("/")[0]
    except:
        api_name = "URL_ERROR"
    save_path = f'{logpath}/{api_name}/'

    ## create log folder in case it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        # os.chown(save_path, 1000, 1000)
    ## get current log date
    log_date = datetime.now().strftime("%Y"+"%m"+"%d")
    ## get source ip addr
    source_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ## set the log file to store the log info
    log = open(f'{save_path}{api_name}_{log_date}.log', 'a', encoding="utf-8")
    log.write('%s %s REQUEST %s %s \n' % (source_ip, datetime.now(),
                                    request.method, request.url))
    log.close()
    # os.chown(f'{save_path}{api_name}_{log_date}.log', 1000, 1000)

@app.after_request
def after_request_func(response):
    ## set up log folder
    if ENVIRONMENT == 'development':
        logpath = '/home/ubuntu/log/drillbi_bur/requests'
    else:
        logpath = '/mnt/log/drillbi_bur/requests'
    
    ## get the api_name, and construct the save_path
    urlstring = request.url
    try:
        api_name = urlstring.split("enovate.app/")[1].split("/")[0]
    except:
        api_name = "URL_ERROR"
    save_path = f'{logpath}/{api_name}/'

    ## create log folder in case it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        # os.chown(save_path, 1000, 1000)
    ## get current log date
    log_date = datetime.now().strftime("%Y"+"%m"+"%d")
    ## get source ip addr
    source_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ## set the log file to store the log info
    log = open(f'{save_path}{api_name}_{log_date}.log', 'a', encoding="utf-8")
    log.write('%s %s RESPONSE %s %s %s \n' % (source_ip, datetime.now(),
                                    request.method, request.url, response.status))
    log.close()
    # os.chown(f'{save_path}{api_name}_{log_date}.log', 1000, 1000)
    return response
################### end of requests logger modules #########################

if __name__ == '__main__':
    app.run()
