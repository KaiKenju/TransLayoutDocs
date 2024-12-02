import cv2
import matplotlib.pyplot as plt

def resize_image(img, max_dim=800):
    """
    Giảm kích thước ảnh sao cho chiều dài lớn nhất của ảnh nằm trong khoảng max_dim,
    giữ nguyên tỷ lệ khung hình. Nếu ảnh nhỏ hơn hoặc bằng max_dim, giữ nguyên.
    
    :param img: Ảnh đầu vào (numpy array).
    :param max_dim: Kích thước tối đa cho chiều dài lớn nhất của ảnh.
    :return: Ảnh sau khi resize (hoặc giữ nguyên nếu không cần resize).
    """
    h, w = img.shape[:2]
    
    # Nếu cả hai chiều của ảnh nhỏ hơn hoặc bằng max_dim, giữ nguyên
    if max(h, w) <= max_dim:
        return img

    # Tính tỷ lệ scale để chiều dài lớn nhất bằng max_dim
    scale = max_dim / max(h, w)
    new_width = int(w * scale)
    new_height = int(h * scale)

    # Resize ảnh
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized_img

def show_comparison(original_img, processed_img):
    """
    Hiển thị so sánh giữa ảnh gốc và ảnh đã xử lý, kèm theo kích thước.
    :param original_img: Ảnh gốc.
    :param processed_img: Ảnh đã xử lý.
    """
    # Chuyển ảnh từ BGR sang RGB để hiển thị với matplotlib
    original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    processed_img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(12, 6))

    # Hiển thị ảnh gốc
    plt.subplot(1, 2, 1)
    plt.title("Ảnh Gốc")
    plt.imshow(original_img_rgb)
    plt.axis('off')
    plt.text(
        10, 50, f"Kích thước: {original_img.shape[1]} x {original_img.shape[0]}",
        color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.7)
    )

    # Hiển thị ảnh đã xử lý
    plt.subplot(1, 2, 2)
    plt.title("Ảnh Đã Xử Lý")
    plt.imshow(processed_img_rgb)
    plt.axis('off')
    plt.text(
        10, 50, f"Kích thước: {processed_img.shape[1]} x {processed_img.shape[0]}",
        color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.7)
    )

    plt.tight_layout()
    plt.show()


# Đọc ảnh gốc
input_path = 'inputs/imgs/develop.png'
original_img = cv2.imread(input_path)

if original_img is None:
    raise FileNotFoundError(f"Ảnh không tồn tại tại đường dẫn {input_path}")

# Resize ảnh (nếu cần)
processed_img = resize_image(original_img, max_dim=900)

# Hiển thị sự so sánh
show_comparison(original_img, processed_img)
