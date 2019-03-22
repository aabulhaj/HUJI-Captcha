import io
import os
from urllib.request import Request, urlopen, urlcleanup

from PIL import Image

import paths

CAPTCHAS_TO_DOWNLOAD = 1500


def download_captchas(n_captchas, file_base_name):
    for i in range(n_captchas):
        req = Request('https://www.huji.ac.il/dataj/resources/captcha/stu/')
        req.add_header('Referer', 'https://www.huji.ac.il/dataj/controller/stu/?')
        req.add_header('Connection', 'keep-alive')
        resp = urlopen(req)

        picture_stream = io.BytesIO(resp.read())

        picture = Image.open(picture_stream)

        picture.save('{dir}{name}.png'.format(dir=paths.CAPTCHAS_DUMP_PATH, name=file_base_name + i))

    urlcleanup()


if __name__ == '__main__':
    captcha_files = [-1]
    for captcha_file in os.listdir(paths.CAPTCHAS_DUMP_PATH):
        captcha_files.append(int(captcha_file.split('.')[0]))

    # Prevents name conflicts.
    captcha_files.sort()
    base_name = captcha_files[-1] + 1

    download_captchas(CAPTCHAS_TO_DOWNLOAD, base_name)
