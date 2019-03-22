from os.path import dirname, abspath

PREFIX = dirname(dirname(abspath(__file__))) + '/HUJI-CAPTCHA/'

NUM_DUMP_PATH = PREFIX + 'data_dump/digits_dump/'
CAPTCHAS_DUMP_PATH = PREFIX + 'data_dump/captchas_dump/'
MODEL_DUMP = PREFIX + 'model_dump/'
CLASSIFIED_IM_PATH = PREFIX + 'classified_digits/'
