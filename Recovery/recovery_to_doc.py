# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from copy import deepcopy
import cv2
from docx import Document
from docx import shared
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches

from Recovery.table_process import HtmlToDocx

from utils.logging import get_logger

logger = get_logger()


def convert_info_docx(img, res, save_folder, img_name):
    doc = Document()
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"]._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    doc.styles["Normal"].font.size = shared.Pt(12)

    flag = 1
    for i, region in enumerate(res):
        # if len(region["res"]) == 0:
        #     continue
        img_idx = region["img_idx"]
        if flag == 2 and region["layout"] == "single":
            section = doc.add_section(WD_SECTION.CONTINUOUS)
            section._sectPr.xpath("./w:cols")[0].set(qn("w:num"), "1")
            flag = 1
        elif flag == 1 and region["layout"] == "double":
            section = doc.add_section(WD_SECTION.CONTINUOUS)
            section._sectPr.xpath("./w:cols")[0].set(qn("w:num"), "2")
            flag = 2

        # if region["type"].lower() == "figure":
        #     excel_save_folder = os.path.join(save_folder, img_name)
        #     img_path = os.path.join(
        #         excel_save_folder, "{}_{}.jpg".format(region["bbox"], img_idx)
        #     )
        #     paragraph_pic = doc.add_paragraph()
        #     paragraph_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #     run = paragraph_pic.add_run("")
        #     if flag == 1:
        #         run.add_picture(img_path, width=shared.Inches(5))
        #     elif flag == 2:
        #         run.add_picture(img_path, width=shared.Inches(2))
        if str(region.get("type", "")).lower() == "figure":
            excel_save_folder = os.path.join(save_folder, img_name)
            if not os.path.exists(excel_save_folder):
                os.makedirs(excel_save_folder)

            # Tạo đường dẫn ảnh
            bbox = region.get("bbox", "default_bbox")
            img_idx = region.get("img_idx", "default_idx")
            img_path = os.path.join(
                excel_save_folder, "{}_{}.jpg".format(bbox, img_idx)
            )

            # Kiểm tra file ảnh
            if not os.path.exists(img_path):
                print("\n")
                print(f"Ảnh không tồn tại: {img_path}")
                continue

            # Kiểm tra kích thước ảnh
            img = cv2.imread(img_path)
            if img is None or img.shape[0] < 10 or img.shape[1] < 10:
                print("\n")
                print(f"Ảnh quá nhỏ hoặc không tồn tại: {img_path}")
                continue

            # Thêm ảnh vào Word
            if os.path.exists(img_path):
                paragraph_pic = doc.add_paragraph()
                paragraph_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = paragraph_pic.add_run("")
                if flag == 1:
                    run.add_picture(img_path, width=Inches(5))
                elif flag == 2:
                    run.add_picture(img_path, width=Inches(2.6))
            else:
                print(f"Ảnh không tồn tại tại đường dẫn: {img_path}")

        
        elif region["type"].lower() == "title":
            doc.add_heading(region["res"][0]["text"])
        elif region["type"].lower() == "table":
            parser = HtmlToDocx()
            parser.table_style = "TableGrid"
            parser.handle_table(region["res"]["html"], doc)
        elif region["type"] == "equation" and "latex" in region["res"]: # fix nốt với các công thức
            pass
        else:
            paragraph = doc.add_paragraph()
            paragraph_format = paragraph.paragraph_format
            for i, line in enumerate(region["res"]):
                if i == 0:
                    paragraph_format.first_line_indent = shared.Inches(0.25)
                text_run = paragraph.add_run(line["text"] + " ")
                text_run.font.size = shared.Pt(12)

    # save to docx
    docx_path = os.path.join(save_folder, "{}_ocr.docx".format(img_name))
    doc.save(docx_path)
    logger.info("docx save to {}".format(docx_path))


def sorted_layout_boxes(res, w):
    """
    Sort text boxes in order from top to bottom, left to right
    args:
        res(list):ppstructure results
    return:
        sorted results(list)
    """
    num_boxes = len(res)
    if num_boxes == 1:
        res[0]["layout"] = "single"
        return res

    sorted_boxes = sorted(res, key=lambda x: (x["bbox"][1], x["bbox"][0]))
    _boxes = list(sorted_boxes)

    new_res = []
    res_left = []
    res_right = []
    i = 0

    while True:
        if i >= num_boxes:
            break
        if i == num_boxes - 1:
            if (
                _boxes[i]["bbox"][1] > _boxes[i - 1]["bbox"][3]
                and _boxes[i]["bbox"][0] < w / 2
                and _boxes[i]["bbox"][2] > w / 2
            ):
                new_res += res_left
                new_res += res_right
                _boxes[i]["layout"] = "single"
                new_res.append(_boxes[i])
            else:
                if _boxes[i]["bbox"][2] > w / 2:
                    _boxes[i]["layout"] = "double"
                    res_right.append(_boxes[i])
                    new_res += res_left
                    new_res += res_right
                elif _boxes[i]["bbox"][0] < w / 2:
                    _boxes[i]["layout"] = "double"
                    res_left.append(_boxes[i])
                    new_res += res_left
                    new_res += res_right
            res_left = []
            res_right = []
            break
        elif _boxes[i]["bbox"][0] < w / 4 and _boxes[i]["bbox"][2] < 3 * w / 4:
            _boxes[i]["layout"] = "double"
            res_left.append(_boxes[i])
            i += 1
        elif _boxes[i]["bbox"][0] > w / 4 and _boxes[i]["bbox"][2] > w / 2:
            _boxes[i]["layout"] = "double"
            res_right.append(_boxes[i])
            i += 1
        else:
            new_res += res_left
            new_res += res_right
            _boxes[i]["layout"] = "single"
            new_res.append(_boxes[i])
            res_left = []
            res_right = []
            i += 1
    if res_left:
        new_res += res_left
    if res_right:
        new_res += res_right
    return new_res
