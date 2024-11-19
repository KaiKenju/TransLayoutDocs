# TransLayoutDocs
Phá triển  TableEngine của PaddleOCR để khôi phục bố cục và hỗ trợ dịch thuật tài liệu

<div align="center">
<!-- width=120 height=120 -->
<img alt="ocr_vietnamese" src="assets/logo_doc.png" > 
<h1>TransLayoutDocs</h1>

 🌎 English / [Vietnamese](README_vn.md) 

<img src="assets/vietnamese_ocr.png" width=700>

</div>
<br>

> **Related Projects**：
>
> - [Recognition-table-with-table-transformer](https://github.com/KaiKenju/Recognition-Table-with-Table_Transformer-and-vietOCR): The combination of Table Transformer and vietOCR creates a powerful table recognition system that extracts table structure from images and simultaneously recognizes Vietnamese characters. Table Transformer handles table layout and structure, while vietOCR focuses on accurate character recognition, providing high accuracy in extracting table data from Vietnamese documents.
>
> - [Vietnamese_OCR_documents](https://github.com/KaiKenju/Vietnamese_OCR_documents): is used to convert text from images or scanned documents into digital format, allowing automatic processing and analysis of text data. This technology is very useful in extracting information from Vietnamese documents, making information searching and management easier and more efficient.
<br>

<br>

# Table of Contents

# Introduction
<div align="center">
    <img src="assets\compare_result.png" width="800">
</div>

# Installization 
- Clone  this project:

```[bash]
git clone https://github.com/KaiKenju/TransLayoutDocs.git
```

- Initial enviromment with Miniconda (Default: python=3.10):

```[bash]
conda create -n <env_name> python=3.10
```
- Activate conda
```[bash]
conda activate <env_name> 
cd TransLayoutDocs
```
- Run the commands:
```[bash]
pip install -r requirements.txt
```

# Quick Start
```[bash]
python main.py
```