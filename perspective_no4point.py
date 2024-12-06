# import cv2
# import numpy as np

# def order_points(pts):
#     """
#     Sắp xếp lại 4 điểm theo thứ tự: trên trái, trên phải, dưới phải, dưới trái.
#     """
#     rect = np.zeros((4, 2), dtype="float32")
#     s = pts.sum(axis=1)
#     rect[0] = pts[np.argmin(s)]  # trên trái
#     rect[2] = pts[np.argmax(s)]  # dưới phải

#     diff = np.diff(pts, axis=1)
#     rect[1] = pts[np.argmin(diff)]  # trên phải
#     rect[3] = pts[np.argmax(diff)]  # dưới trái

#     return rect

# def detect_and_transform_quadrilaterals(image_path, expansion=10):
#     """
#     Phát hiện các vùng văn bản và áp dụng biến đổi phối cảnh lên tứ giác bao quanh chúng,
#     không thêm các bộ lọc cải thiện văn bản.
#     """
#     # Đọc ảnh đầu vào
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Dùng GaussianBlur để giảm nhiễu
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#     # Dùng Canny để phát hiện cạnh
#     edges = cv2.Canny(blurred, 50, 150)

#     # Dùng Morphology để kết nối các cạnh (dilate -> close)
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
#     closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

#     # Tìm các contour
#     contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     all_points = []  # Mảng để lưu tất cả các điểm trong các tứ giác

#     for contour in contours:
#         # Bỏ qua các contour quá nhỏ
#         if cv2.contourArea(contour) < 1000:
#             continue

#         # Tìm hình chữ nhật xoay nhỏ nhất bao quanh contour
#         rect = cv2.minAreaRect(contour)
#         box = cv2.boxPoints(rect)  # Lấy 4 đỉnh của tứ giác
#         box = np.intp(box)         # Chuyển tọa độ sang số nguyên

#         # Tính tâm của tứ giác
#         center_x = np.mean(box[:, 0])
#         center_y = np.mean(box[:, 1])

#         # Mở rộng các đỉnh ra xa tâm
#         expanded_box = []
#         for point in box:
#             x_new = int(point[0] + (point[0] - center_x) * (expansion / 100))
#             y_new = int(point[1] + (point[1] - center_y) * (expansion / 100))
#             expanded_box.append([x_new, y_new])

#         expanded_box = np.array(expanded_box, dtype=np.float32)

#         # Sắp xếp lại các điểm theo thứ tự chuẩn
#         ordered_box = order_points(expanded_box)

#         # Thêm các điểm vào mảng tổng hợp
#         all_points.extend(ordered_box)

#     # Chuyển mảng các điểm thành một numpy array và sắp xếp lại
#     all_points = np.array(all_points, dtype=np.float32)

#     # Tính toán tứ giác bao quanh tất cả các điểm
#     hull = cv2.convexHull(all_points)

#     # Tính kích thước mới cho hình ảnh (sau khi biến đổi phối cảnh)
#     rect = cv2.minAreaRect(hull)
#     box = cv2.boxPoints(rect)  # Lấy 4 đỉnh của tứ giác bao quanh
#     box = np.intp(box)

#     # Sắp xếp lại các điểm của tứ giác bao quanh
#     ordered_box = order_points(box)

#     # Tính toán kích thước của hình ảnh biến đổi
#     width = max(np.linalg.norm(ordered_box[0] - ordered_box[1]),
#                 np.linalg.norm(ordered_box[2] - ordered_box[3]))
#     height = max(np.linalg.norm(ordered_box[0] - ordered_box[3]),
#                  np.linalg.norm(ordered_box[1] - ordered_box[2]))

#     # Tạo danh sách 4 điểm đích (hình chữ nhật)
#     dst_points = np.array([
#         [0, 0],
#         [width - 1, 0],
#         [width - 1, height - 1],
#         [0, height - 1]
#     ], dtype=np.float32)

#     # Tính ma trận biến đổi phối cảnh
#     M = cv2.getPerspectiveTransform(ordered_box, dst_points)

#     # Áp dụng biến đổi phối cảnh
#     transformed = cv2.warpPerspective(image, M, (int(width), int(height)), flags=cv2.INTER_CUBIC)

#     # Hiển thị ảnh gốc và ảnh sau khi biến đổi phối cảnh
#     cv2.imshow("Transformed Quadrilateral", transformed)
    
#     # Vẽ tứ giác bao quanh lên ảnh gốc để tham khảo
#     cv2.drawContours(image, [np.intp(ordered_box)], 0, (0, 255, 0), 2)

#     cv2.imshow("Original Image with Quadrilaterals", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# # Gọi hàm với đường dẫn ảnh
# detect_and_transform_quadrilaterals('inputs\imgs\perspective_img.png', expansion=8)


import cv2
import numpy as np

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
        return

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

    # Vẽ tứ giác hợp nhất lên ảnh gốc
    cv2.drawContours(image, [np.intp(expanded_box)], 0, (0, 255, 0), 2)

    # Hiển thị và lưu kết quả
    cv2.imshow("Original Image with Merged Quadrilateral", image)
    cv2.imshow("Transformed Image", transformed)
    cv2.imwrite("merged_quadrilateral.png", image)
    cv2.imwrite("transformed_image.png", transformed)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Gọi hàm
detect_and_transform_largest_quadrilateral('inputs/imgs/chap4.png', expansion=12)

