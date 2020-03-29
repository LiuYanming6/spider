# https://kns.cnki.net/kns/checkcode.aspx?t=0.4529926421852408
from PIL import Image
from aip import AipOcr

# 1. gif to png
# def processImage(infile):
#     try:
#         im = Image.open(infile)
#     except IOError:
#         print("Cant load", infile)
#         sys.exit(1)
#     i = 0
#     mypalette = im.getpalette()
#
#     try:
#         while 1:
#             im.putpalette(mypalette)
#             new_im = Image.new("RGBA", im.size)
#             new_im.paste(im)
#             new_im.save('foo' + str(i) + '.png')
#
#             i += 1
#             im.seek(im.tell() + 1)
#
#     except EOFError:
#         pass  # end of sequence


# 2 gif to jpg
# Image.open('prev.gif').convert('RGB').save('prev.jpg')

# 转换
im = Image.open('E:/checkcode.gif')
transparency = im.info['transparency']
im.save('E:/checkcode.png', transparency=transparency)

""" 你的 APPID AK SK """
APP_ID = '11458429'
API_KEY = 'jaQmNx4VBbmisrhG50BxUVxL'
SECRET_KEY = 'dNa27rGzTOOw1Wrspl4VjEmblmKomXiH'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 调用通用文字识别, 图片参数为本地图片 """
# client.basicGeneral(image)

""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"
#
""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == "__main__":
    # """ 带参数调用通用文字识别, 图片参数为本地图片 """
    ret = client.basicGeneral(get_file_content('../zhiwang/checkcode.png'), options)
    print(ret)
