import sys
import logging
from configparser import ConfigParser
from pathlib import Path
 
# set sensible defaults for the configurable fields
DATA_PATH = 'Data'
DATABASE_NAME = 'CVEfixes_sample.db'
USER = 'wangyue6761'
TOKEN = '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'
SAMPLE_LIMIT = 25
NUM_WORKERS = 4
LOGGING_LEVEL = logging.WARNING  # 表示INFO的会输出

# full path to the .db file
DATABASE = Path(DATA_PATH) / DATABASE_NAME
config_read = False

log_level_map = {'DEBUG': logging.DEBUG,
                 'INFO': logging.INFO,
                 'WARNING': logging.WARNING,
                 'ERROR': logging.ERROR,
                 'CRITICAL': logging.CRITICAL
                 }

logging.basicConfig(level=LOGGING_LEVEL,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger('CVEfixes')
logger.removeHandler(sys.stderr)

 
def read_config() -> None:
    """
    Read CVEfixes configuration from .CVEfixies.ini, $HOME/.config/CVEfixes.ini or $HOME/.CVEfixes.ini

    Sets global constants with values found in the ini file.
    """
    global DATA_PATH, DATABASE_NAME, DATABASE, USER, TOKEN, SAMPLE_LIMIT, NUM_WORKERS, LOGGING_LEVEL, config_read

    config = ConfigParser()
    if config.read(['.CVEfixes.ini',
                    Path.home() / '.config' / 'CVEfixes.ini',
                    Path.home() / '.CVEfixes.ini']):
        # try and update settings for each of the values, use
        DATA_PATH = config.get('CVEfixes', 'database_path', fallback=DATA_PATH)
        DATABASE_NAME = config.get('CVEfixes', 'database_name', fallback=DATABASE_NAME)
        USER = config.get('GitHub', 'user', fallback=USER)
        TOKEN = config.get('GitHub', 'token', fallback=TOKEN)
        SAMPLE_LIMIT = config.getint('CVEfixes', 'sample_limit', fallback=SAMPLE_LIMIT)
        NUM_WORKERS = config.getint('CVEfixes', 'num_workers', fallback=NUM_WORKERS)
        Path(DATA_PATH).mkdir(parents=True, exist_ok=True)  # create the directory if not exists.
        DATABASE = Path(DATA_PATH) / DATABASE_NAME
        LOGGING_LEVEL = log_level_map.get(config.get('CVEfixes', 'logging_level', fallback='WARNING'), logging.WARNING)
        # map.get,map中该key不存在值时，返回默认值
        config_read = True
    else:
        logger.warning('Cannot find CVEfixes config file in the working or $HOME directory, see INSTALL.md')
        sys.exit()


if not config_read:
    read_config()
    logger.setLevel(LOGGING_LEVEL)
    # 下面get这么多logger干啥
    logging.getLogger("requests").setLevel(LOGGING_LEVEL)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connection").setLevel(logging.WARNING)
    logging.getLogger("pathlib").setLevel(LOGGING_LEVEL)
    logging.getLogger("subprocess").setLevel(LOGGING_LEVEL)
    logging.getLogger("h5py._conv").setLevel(logging.WARNING)
    logging.getLogger("git.cmd").setLevel(LOGGING_LEVEL)
    logging.getLogger("github.Requester").setLevel(LOGGING_LEVEL)
