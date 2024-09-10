import psutil
import time
import requests
import os 
import sys
from yaml import load, Loader
import logging
from math import floor

##### Setup  ##### 

DEFAULT_LOG_PATH="/usr/local/custom-exporter/logs"
LOG_PATH_ENV="CUSTOM_EXPORTER_LOG"

if LOG_PATH_ENV in os.environ :
    log_path = os.environ[LOG_PATH_ENV]
else:
    log_path = DEFAULT_LOG_PATH

logging.basicConfig(filename=log_path,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('customExporter')

logger.info("Logging file used:"+log_path)

#### 'Functions' ####

def get_config_path()->str:
    """ Get config path """
    DEFAULT_CONFIG_PATH="/etc/custom-exporter/config.yml"
    CONFIG_FILE_PATH_ENV="CUSTOM_EXPORTER_CONFIG"

    if CONFIG_FILE_PATH_ENV in os.environ :
        return  os.environ[CONFIG_FILE_PATH_ENV]
    else:
        return DEFAULT_CONFIG_PATH

def parse_yml(path:str)->dict:
    """Load YAML file into a dict object"""
    try : 
        file = open(path,"r")
        yaml = file.read()
        dict_object = load(yaml,Loader)
        return dict_object
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)
     
def get_proc_infos(fields:list)->dict:
    """ Fetch processus informations """
    try : 
        procs_info = []
        for proc_info in psutil.process_iter(fields):
            procs_info.append(proc_info.as_dict(fields))
            
    except Exception as e:
        logger.error(f"Failed to gather processus information : {str(e)}")
        sys.exit(1)
    info = {
        "info": procs_info,
        "time": floor(time.time())
    }
    return info

def post_request(url:str, json:dict )->None:
    """
    Send a POST request ,expecting status code 200 
    """
    try: 
        response = requests.post(url,json=json)
        if response.status_code != 200 : 
            raise Exception(f"Invalid status code received. Expecting 200 , got {str(response.status_code)}")
    except Exception as e : 
        logger.error(f"Failed to send processus information:{str(e)}")

def main(configuration:dict)->None:
    """
    Gather processus information and send a post request 
    """
    procs_info = get_proc_infos(configuration['fields'])
    post_request(configuration["target"]["url"],procs_info)


if __name__=="__main__":
    config_path = get_config_path()
    logger.info("Configuration path used:"+config_path)
    configuration = parse_yml(config_path)
    logger.info("Configuration used : "+configuration.__str__())
    while True :
        try : 
            main(configuration)
        except Exception as e:
            logger.error(f"Unexpected bug occured : {str(e)}")
            sys.exit(1)
        time.sleep(60)
