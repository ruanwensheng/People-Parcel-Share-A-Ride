# People and Parcel Share A Ride (PPSAR)

## Introduction
People and Parcel Share A Ride (PPSAR) là một bài toán tối ưu hóa định tuyến phương tiện, trong đó K taxi phục vụ N hành khách và M kiện hàng. Mục tiêu là tối ưu chiều dài tuyến đường dài nhất trong số các tuyến nhằm giảm tổng quãng đường di chuyển, tiết kiệm chi phí vận hành và nâng cao hiệu suất vận tải.

Bài toán này có ứng dụng trong các dịch vụ vận tải công cộng, giao nhận hàng hóa và tối ưu hóa logistics trong đô thị.

## Constraints
- **Điểm xuất phát và kết thúc:** Tất cả các taxi xuất phát từ điểm 0 và kết thúc tại điểm 2*N+2*M+1.
- **Giới hạn tải trọng:** Khối lượng hàng hóa trên mỗi taxi không vượt quá sức chứa của nó.
- **Ràng buộc hành khách:** Mỗi hành khách phải được vận chuyển trực tiếp từ điểm \( i \) đến \( i + N + M \) mà không có trung chuyển.
- **Ràng buộc hàng hóa:** Mỗi kiện hàng phải được vận chuyển từ điểm \( j + N \) đến điểm \( j + 2N + M \), đảm bảo kiện hàng được giao đến đúng địa điểm.

## Test Cases
Tổng cộng có 15 test case với các giá trị tăng dần của N, M, K nhằm kiểm tra độ hiệu quả của thuật toán. Dưới đây là một số test case tiêu biểu:
- **test01:** N = 3, M = 3, K = 2
- **test04:** N = 5, M = 5, K = 2
- **test10:** N = 7, M = 7, K = 4
- **test11:** N = 30, M = 30, K = 3
- **test15:** N = 50, M = 50, K = 4

## Solutions
### Exact Solutions
Các phương pháp chính xác đảm bảo tìm ra lời giải tối ưu nhưng yêu cầu thời gian tính toán cao:
- **Constraint Programming (CP):**
  - Sử dụng OR-Tools để xác định biến, ràng buộc và mục tiêu tối ưu hóa.
  - Xây dựng danh sách mở rộng cho khối lượng hàng hóa và ma trận khoảng cách.
  - Áp dụng quy hoạch ràng buộc để đảm bảo các tuyến đường hợp lệ.

- **Integer Programming (IP):**
  - Sử dụng lập trình tuyến tính nguyên để tìm lời giải tối ưu.
  - Áp dụng các biến quyết định để mô hình hóa bài toán.
  - Định nghĩa các hàm mục tiêu để tối ưu hóa tuyến đường.

- **Backtracking:**
  - Duyệt toàn bộ các cấu hình tuyến đường khả thi.
  - Loại bỏ các cấu hình vi phạm ràng buộc sớm nhằm giảm không gian tìm kiếm.
  - Tìm kiếm sâu hơn nếu cấu hình hiện tại có khả năng cải thiện lời giải.

### Heuristic Solutions
Các phương pháp xấp xỉ cho lời giải nhanh hơn nhưng có thể không tối ưu:
- **Greedy Algorithm:**
  - Chọn taxi có quãng đường ngắn nhất để phục vụ điểm tiếp theo.
  - Giúp tìm lời giải nhanh nhưng có thể bị mắc kẹt tại cực tiểu cục bộ.

- **Local Search (2-Opt):**
  - Cải thiện tuyến đường bằng cách đảo ngược đoạn đường nhằm giảm tổng khoảng cách.
  - Lặp lại quy trình tối ưu hóa đến khi không còn cải thiện.

- **Genetic Algorithm:**
  - Áp dụng thuật toán di truyền để tối ưu hóa tuyến đường bằng cách chọn lọc, lai ghép và đột biến.
  - Hoạt động song song với nhiều lời giải, giúp tránh rơi vào cực tiểu cục bộ.

## Comparison & Conclusion
### Thời gian thực thi
- **Exact Methods** (Constraint Programming, Integer Programming) đảm bảo kết quả tối ưu nhưng tốn nhiều thời gian tính toán.
- **Heuristic Methods** (Greedy, Local Search, Genetic Algorithm) nhanh hơn nhưng có thể không tìm được kết quả tối ưu.
- **Genetic Algorithm** có sự cân bằng tốt giữa độ chính xác và thời gian chạy.

### Độ chính xác của lời giải
- **Integer Programming và Constraint Programming** luôn tìm ra kết quả tối ưu nhưng có thể mất nhiều thời gian khi kích thước bài toán tăng.
- **Greedy Algorithm** nhanh nhưng dễ bị kẹt ở kết quả không tối ưu.
- **Genetic Algorithm** đưa ra kết quả tốt nhất trong nhóm heuristic nhưng cần thêm tối ưu để cải thiện hiệu suất.

### Tổng kết
- Nếu ưu tiên kết quả tối ưu tuyệt đối, sử dụng **Constraint Programming hoặc Integer Programming**.
- Nếu cần kết quả nhanh và có thể chấp nhận sai số, **Greedy và Local Search** là lựa chọn tốt.
- **Genetic Algorithm** có tiềm năng tốt nếu được cải tiến thêm để đạt hiệu suất cao hơn.

## Authors
Nhóm 17:
- **Nguyen Van Thang** - 20235559
- **Pham Ngoc Trinh** - 20230092
- **Nguyen Vu Thuy** - 20235562
- **Tran Hoang Thai** - 20235621

## Acknowledgments
Cảm ơn các thầy cô đã hướng dẫn và hỗ trợ trong quá trình thực hiện dự án. Chúng tôi cũng cảm ơn các thành viên trong nhóm đã làm việc chăm chỉ để hoàn thành bài toán này.

