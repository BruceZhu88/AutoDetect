
from common.Config import Config

main_cfg_path = '../config/main.ini'
config = Config(main_cfg_path)
config.cfg_load()
log_path = config.cfg.get('Log', 'path')
cfg_path = config.cfg.get('Config', 'path')
