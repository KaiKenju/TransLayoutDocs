import os
import cv2
import argparse
from paddleocr import PPStructure, save_structure_res
from Recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

def process_image(input_path, output_path, lang):
    
    table_engine = PPStructure(recovery=True, lang=lang, drop_score=0.3, return_ocr_result_in_table=True)
    
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {input_path}")
    
    
    result = table_engine(img)
    save_structure_res(result, output_path, os.path.basename(input_path).split('.')[0])

    for line in result:
        line.pop('img')
        print(line)

    h, w, _ = img.shape
    res = sorted_layout_boxes(result, w)
    convert_info_docx(img, res, output_path, os.path.basename(input_path).split('.')[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an image and extract tables using PaddleOCR.")
    parser.add_argument('--input', required=True, help="Path to the input image.")
    parser.add_argument('--output', required=True, help="Path to the output folder.")
    parser.add_argument('--lang', default='vi', choices=['en', 'ch', 'vi'], help="Language for translate (default: 'vi').")
    args = parser.parse_args()

    process_image(args.input, args.output, args.lang)
