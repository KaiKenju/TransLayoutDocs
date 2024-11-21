# TransLayoutDocs
Phá triển  TableEngine của PaddleOCR để khôi phục bố cục và hỗ trợ dịch thuật tài liệu

<div align="center">
<!-- width=120 height=120 -->
<img alt="ocr_vietnamese" src="assets/logo_doc.png" > 
<h1>TransLayoutDocs</h1>

 🌎 English / [Vietnamese](README_vn.md) 

</div>
<br>

> **Related Projects**：
>
> - [Recognition-table-with-table-transformer](https://github.com/KaiKenju/Recognition-Table-with-Table_Transformer-and-vietOCR): A system combining Table Transformer and vietOCR for accurate table structure and Vietnamese character recognition from images.
>
> - [Vietnamese_OCR_documents](https://github.com/KaiKenju/Vietnamese_OCR_documents): Converts text from images or scans into digital format, streamlining Vietnamese text processing and information management.
<br>

<br>

# Table of Contents

# Dependencies
- Python > 3.6

# Introduction
<div align="center">
    <img src="assets\compare_result.png" width="800">
</div>
- Image: RecoveryLayout + Translate
<div align="center">
    <img src="assets/layout_trans.png" width="800">
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

Still update