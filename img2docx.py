import os
import cv2
from paddleocr import PPStructure,save_structure_res
from Recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

# Chinese image
# table_engine = PPStructure(recovery=True)
# English image
table_engine = PPStructure(recovery=True, lang='en')

save_folder = './detail_img'
img_path = './inputs/imgs/check2.png'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)

h, w, _ = img.shape
res = sorted_layout_boxes(result, w)
convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])