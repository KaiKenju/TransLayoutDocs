import argparse
import os
import cv2
import torch
from paddleocr import PPStructure, save_structure_res
from Recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

def process_image(input_path, output_path, lang, device):
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)  
        print(f"Output folder created: {output_path}")
    else:
        print(f"Output folder already exists: {output_path}")
    table_engine = PPStructure(recovery=True, drop_score=0.3, return_ocr_result_in_table=True)
    
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
    convert_info_docx(img, res, output_path, os.path.basename(input_path).split('.')[0], lang, device)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an image for table detection and OCR.")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input image file.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output folder.")
    parser.add_argument("--lang", type=str, default="vi", help="Language for Translate  ('vi', 'jp', default is 'vi').")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cpu", help="Device to use: 'cpu' or 'cuda' (default: 'cpu').")
    
    args = parser.parse_args()

    device = "cuda" if args.device == "cuda" and torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    process_image(args.input_path, args.output_path, args.lang, device)

#python img2docx.py --input=./inputs/imgs/chap4.png --output=./detail_img --lang=vi --device=cpu