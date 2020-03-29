# import tesserocr
# import Image
#
# image = Image.open('E:/checkcode.jpg')
# image = image.convert('L')  # 将图片转为灰度图片
# threshold = 138  # 设置阈值
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
#
# image = image.point(table, '1')
# image.show()
# res = tesserocr.image_to_text(image)
# result = res.replace(' ', '')
