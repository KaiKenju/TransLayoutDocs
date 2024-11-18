# # import os
# # import cv2
# # from paddleocr import PPStructure,save_structure_res
# # from ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx

# # # Chinese image
# # # table_engine = PPStructure(recovery=True)
# # # English image
# # table_engine = PPStructure(recovery=True, lang='en')

# # save_folder = './doc'
# # img_path = 'test.png'
# # img = cv2.imread(img_path)
# # result = table_engine(img)
# # save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

# # for line in result:
# #     line.pop('img')
# #     print(line)

# # h, w, _ = img.shape
# # res = sorted_layout_boxes(result, w)
# # convert_info_docx(img, res, save_folder, os.path.basename(img_path).split('.')[0])


import os
import shutil
from pdf2image import convert_from_path
from paddleocr import PPStructure, save_structure_res
from ppstructure.recovery.recovery_to_doc import sorted_layout_boxes, convert_info_docx
from docxcompose.composer import Composer
from docx import Document
import cv2
import numpy as np
from tqdm import tqdm

# Khởi tạo PaddleOCR với ngôn ngữ tiếng Anh
table_engine = PPStructure(recovery=True, lang='en')

# Đường dẫn thư mục lưu trữ
save_folder = './doc_en1'
os.makedirs(save_folder, exist_ok=True)

# Hàm xử lý từng trang PDF
def process_image_to_word(img, page_number):
    result = table_engine(img)
    save_structure_res(result, save_folder, f'page_{page_number}')
    
    for line in result:
        line.pop('img')
        print(line)
    
    h, w, _ = img.shape
    res = sorted_layout_boxes(result, w)
    convert_info_docx(img, res, save_folder, f'page_{page_number}')
    print(f"Trang {page_number} đã xử lý xong.")

# Hàm gộp các file Word và đảm bảo ảnh hiển thị đúng
def merge_word_documents_with_images(doc_folder, output_file):
    # Lấy danh sách file .docx và sắp xếp theo thứ tự
    doc_files = sorted(
        [f for f in os.listdir(doc_folder) if f.endswith('.docx')],
        key=lambda x: int(x.split('_')[1].split('.')[0]) if x.startswith('page_') else float('inf')
    )
    
    if not doc_files:
        raise ValueError(f"Thư mục '{doc_folder}' không chứa file .docx hợp lệ.")
    
    # Tạo file Word hợp nhất
    master_doc = Document(os.path.join(doc_folder, doc_files[0]))
    composer = Composer(master_doc)
    
    # Hợp nhất các file còn lại
    for filename in doc_files[1:]:
        sub_doc_path = os.path.join(doc_folder, filename)
        sub_doc = Document(sub_doc_path)
        composer.append(sub_doc)
    
    # Di chuyển tất cả thư mục "media" từ các file con vào gốc
    for folder in os.listdir(doc_folder):
        folder_path = os.path.join(doc_folder, folder)
        if os.path.isdir(folder_path) and folder.startswith('page_'):
            media_folder = os.path.join(folder_path, 'media')
            if os.path.exists(media_folder):
                for media_file in os.listdir(media_folder):
                    shutil.move(os.path.join(media_folder, media_file), os.path.join(doc_folder, media_file))
                shutil.rmtree(media_folder)
    
    # Lưu file hợp nhất
    composer.save(output_file)
    print(f"Hợp nhất hoàn tất: {output_file}")

# Xử lý PDF thành file Word
def process_pdf_to_word(pdf_path):
    # Chuyển đổi từng trang PDF thành hình ảnh
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(tqdm(images, desc="Đang xử lý các trang")):
        # Chuyển đổi từ PIL Image sang OpenCV Image
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        process_image_to_word(img, i + 1)
    
    # Gộp các file Word
    merge_word_documents_with_images(save_folder, 'final_output.docx')
    print("Hoàn thành! File Word hợp nhất lưu tại: final_output.docx")

# Đường dẫn file PDF đầu vào
pdf_path = '2009.09941v3.pdf'
process_pdf_to_word(pdf_path)

