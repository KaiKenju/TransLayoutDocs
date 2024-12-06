import cv2
import numpy as np

import cv2
import matplotlib.pyplot as plt

def resize_image(img, max_dim=900):
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

def order_points(pts):
    """
    Sắp xếp lại 4 điểm theo thứ tự: trên trái, trên phải, dưới phải, dưới trái.
    """
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # trên trái
    rect[2] = pts[np.argmax(s)]  # dưới phải

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # trên phải
    rect[3] = pts[np.argmax(diff)]  # dưới trái

    return rect


def detect_and_transform_largest_quadrilateral(image_path, expansion=10):
    """
    Phát hiện vùng văn bản lớn nhất (hợp nhất từ các contour nhỏ hơn),
    và áp dụng biến đổi phối cảnh.
    """
    # Đọc ảnh đầu vào
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Làm mờ và phát hiện cạnh
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Dùng Morphology để kết nối các cạnh
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Tìm các contour
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Hợp nhất tất cả contour thành một hình bao quanh lớn nhất
    all_points = []
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Bỏ qua contour nhỏ
            all_points.extend(contour[:, 0, :])

    if not all_points:
        print("Không tìm thấy khối văn bản đủ lớn.")
        return None

    # Tạo convex hull bao quanh tất cả các điểm
    all_points = np.array(all_points, dtype=np.float32)
    hull = cv2.convexHull(all_points)

    # Tính toán tứ giác bao quanh vùng hợp nhất
    rect = cv2.minAreaRect(hull)
    box = cv2.boxPoints(rect)  # Lấy 4 đỉnh của tứ giác
    box = np.intp(box)

    # Mở rộng các cạnh ra xa tâm
    center_x = np.mean(box[:, 0])
    center_y = np.mean(box[:, 1])
    expanded_box = []
    for point in box:
        x_new = int(point[0] + (point[0] - center_x) * (expansion / 100))
        y_new = int(point[1] + (point[1] - center_y) * (expansion / 100))
        expanded_box.append([x_new, y_new])
    expanded_box = np.array(expanded_box, dtype=np.float32)

    # Sắp xếp lại các điểm
    ordered_box = order_points(expanded_box)

    # Tính kích thước cho hình ảnh sau biến đổi
    width = max(np.linalg.norm(ordered_box[0] - ordered_box[1]),
                np.linalg.norm(ordered_box[2] - ordered_box[3]))
    height = max(np.linalg.norm(ordered_box[0] - ordered_box[3]),
                 np.linalg.norm(ordered_box[1] - ordered_box[2]))

    # Định nghĩa điểm đích (hình chữ nhật)
    dst_points = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype=np.float32)

    # Tính ma trận biến đổi phối cảnh
    M = cv2.getPerspectiveTransform(ordered_box, dst_points)

    # Áp dụng biến đổi phối cảnh
    transformed = cv2.warpPerspective(image, M, (int(width), int(height)), flags=cv2.INTER_CUBIC)

    # Trả về ảnh đã biến đổi
    print("Đã biến đổi ảnh perspective")
    return transformed
