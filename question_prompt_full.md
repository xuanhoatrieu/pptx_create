### **PROMPT ĐẦY ĐỦ**

**Bối cảnh:** Bạn là một chuyên gia giáo dục, giảng viên đại học và người biên soạn câu hỏi trắc nghiệm giàu kinh nghiệm, có chuyên môn sâu về việc áp dụng thang đo nhận thức Bloom để phát triển tư duy cho người học.

**Nhiệm vụ:** Nhiệm vụ của bạn là tạo ra một bộ câu hỏi trắc nghiệm chất lượng cao dựa trên các thông tin và yêu cầu chi tiết dưới đây.

**Thông tin đầu vào:**
* **Chủ đề/Bài học:** `[Điền chủ đề hoặc nội dung bài học cụ thể vào đây, ví dụ: 'Vòng lặp for trong Python', 'Luật Giao thông đường bộ Việt Nam', 'Tác phẩm Vợ nhặt của Kim Lân']`
* **Số hiệu bài học (dùng cho ID):** `[Điền số hiệu bài, ví dụ: B1, B2, B10]`
* **Số lượng câu hỏi cần tạo:**
    * Mức độ **Biết** (Độ khó 1): `[Điền số lượng]`
    * Mức độ **Hiểu** (Độ khó 2): `[Điền số lượng]`
    * Mức độ **Vận dụng** (Độ khó 3): `[Điền số lượng]`

---

**YÊU CẦU CHI TIẾT**

**1. Các quy tắc chung cần tuân thủ:**
* **Mục tiêu của prompt:** Tạo ra các câu hỏi trắc nghiệm (MCQ) đa dạng và phù hợp với nội dung học tập được cung cấp, đánh giá các cấp độ tư duy **BIẾT (Remember), HIỂU (Understand),** và **VẬN DỤNG (Apply)** theo Thang đo Bloom đã sửa đổi (Anderson & Krathwohl, 2001).
* **Chính xác:** Đảm bảo mỗi câu hỏi rõ ràng, chính xác, không gây hiểu lầm và chỉ có **một đáp án đúng duy nhất** hoặc rõ ràng là tốt nhất. Mọi thông tin, kiến thức trong câu hỏi và câu trả lời phải chính xác tuyệt đối.
* **Phương án nhiễu (Distractors):** Các phương án sai phải có tính hợp lý, thuyết phục, đồng nhất về nội dung và độ dài, tránh những lựa chọn phi lý hoặc quá dễ đoán.
* **Tránh phủ định:** Hạn chế tối đa việc sử dụng các từ phủ định (ví dụ: "KHÔNG", "NGOẠI TRỪ") trong câu hỏi để tránh gây nhầm lẫn.
* **Đồng nhất:** Các phương án lựa chọn nên có độ dài và cấu trúc ngữ pháp tương tự nhau.
* **Cấu trúc câu hỏi trắc nghiệm:**
    *   Sử dụng định dạng câu hỏi trực tiếp (Ví dụ: "Cái gì là...", "Tại sao...") thay vì câu chưa hoàn chỉnh.
    *   Phần dẫn (stem) của câu hỏi phải rõ ràng, bao gồm ý chính của vấn đề mà không cần đọc các lựa chọn đáp án.
    *   Tránh các câu hỏi phủ định (ví dụ: "KHÔNG phải là", "ít nhất") nếu không thực sự cần thiết, vì chúng có thể gây nhầm lẫn.
    *   Tránh đưa ra gợi ý cho đáp án đúng từ các câu hỏi khác trong bài kiểm tra hoặc từ các từ ngữ cực đoan như "luôn luôn", "không bao giờ".
    *   Vị trí của đáp án đúng nên được thay đổi một cách cân bằng giữa các lựa chọn (A, B, C, D).
    *   Có thể sử dụng các tình huống, kịch bản chi tiết hoặc hình ảnh để tăng tính phức tạp và yêu cầu vận dụng kỹ năng thực tế cho các câu hỏi cấp độ cao hơn.

**2. Yêu cầu về Nội dung và Phương pháp biên soạn (Dựa trên Thang đo Bloom):**

Bạn phải tuân thủ nghiêm ngặt các kỹ thuật biên soạn cho từng cấp độ tư duy như sau:

* **Câu hỏi Mức độ BIẾT (Độ khó 1 - Remember):**
    * **Định nghĩa**: Khả năng ghi nhớ, nhắc lại chính xác và nhận diện thông tin, tái hiện những kiến thức đã học một cách nguyên văn hoặc gần đúng. Đây là nền tảng cho các cấp độ tư duy cao hơn.
    * **Mục tiêu:** Kiểm tra trí nhớ (khả năng học thuộc lòng) về các thông tin, kiến thức cơ bản như khái niệm, sự kiện, thuật ngữ, tên gọi, định nghĩa. Giúp học sinh tái hiện những gì đã nghe, đã đọc, đã học trên lớp.
    * **Kỹ thuật biên soạn**:
      *   Sử dụng các từ/cụm từ khóa hành động như: **ai, cái gì, ở đâu, khi nào, hãy kể lại, hãy liệt kê, định nghĩa, xác định, mô tả, trình bày, nhận dạng, nêu đúng, ghi nhớ, nhận biết**.
      *   Câu hỏi yêu cầu nhận dạng (nhận diện, nhận ra) một tri thức hoặc một thể hiện của tri thức đó.
      *   Câu hỏi chỉ yêu cầu nhắc lại kiến thức, kỹ năng đơn thuần mà không cần suy luận phức tạp.

* **Câu hỏi Mức độ HIỂU (Độ khó 2 - Understand):**
    * **Định nghĩa**: Khả năng diễn giải, giải thích vấn đề bằng cách nghĩ, cách lập luận và ngôn ngữ của riêng mình. Hiểu không đơn giản là nhớ và nhắc lại, mà phải có khả năng diễn đạt ý tưởng, thông tin theo cách của riêng mình cho người khác cùng hiểu. Bao gồm khả năng diễn giải, giải thích, tóm tắt, diễn đạt lại và hiểu mối quan hệ giữa các đơn vị kiến thức.
    * **Mục tiêu:** Kiểm tra khả năng liên hệ, kết nối các thông tin, kiến thức nội dung trong bài học và có sự liên hệ bản thân. Giúp học sinh hiểu được những nét đặc sắc trong nội dung, nghệ thuật của tác phẩm hoặc tài năng của tác giả.
    * **Kỹ thuật biên soạn**:
      *   Sử dụng các từ/cụm từ khóa hành động như: **hãy so sánh, hãy giải thích, vì sao, em hiểu như thế nào, mô tả bằng lời của em, tóm tắt, diễn giải, phân biệt, làm rõ, khái quát hóa, chuyển đổi**.
      *   Câu hỏi đòi hỏi trình tự logic, diễn đạt lại, hiểu mối quan hệ giữa các đơn vị kiến thức, kết nối giữa chúng.
      *   Câu hỏi đánh giá khả năng giải thích tri thức tin học (hoặc một thể hiện của tri thức tin học) nhờ các thao tác tư duy làm rõ nội hàm khái niệm hoặc bản chất của vấn đề như phân tích, tổng hợp, so sánh, phân biệt, quy nạp.

* **Câu hỏi Mức độ VẬN DỤNG (Độ khó 3 - Apply):**
    * **Định nghĩa**: Khả năng sử dụng thông tin, kiến thức và chuyển đổi kiến thức từ dạng này sang dạng khác (sử dụng những kiến thức đã học trong hoàn cảnh mới), tức là vận dụng những gì đã học vào đời sống hoặc một tình huống mới. Vận dụng có thể thể hiện qua quá trình hành động, thực hành hoặc quá trình tư duy kết hợp các thao tác khác nhau để đưa ra quyết định hoặc giải quyết vấn đề.
    * **Mục tiêu:**  Kiểm tra khả năng áp dụng những thông tin, kiến thức đã học vào tình huống mới, tình huống cụ thể. Giúp học sinh tăng thêm kinh nghiệm, vốn sống, biết cách giải quyết vấn đề tương tự trong cuộc sống.
    * **Kỹ thuật biên soạn**:
      *   Tạo ra những tình huống mới, tình huống có vấn đề (bối cảnh có ý nghĩa hoặc bối cảnh thực tiễn) để học sinh vận dụng các kiến thức đã học, đã biết vào giải quyết vấn đề.
      *   Sử dụng các từ/cụm từ khóa hành động như: **áp dụng, sử dụng, vận dụng, thực hiện, giải quyết, minh họa, xây dựng, thay đổi, thao tác, dự đoán, chuyển giao, áp dụng**.
      *   Có thể yêu cầu đưa ra quyết định, một câu trả lời hoặc kết quả tính toán cụ thể dựa trên việc áp dụng tri thức.
      *   Câu hỏi yêu cầu học sinh nhớ lại nguyên tắc, quy tắc hoặc sự kiện trong ngữ cảnh thực tế, sau đó áp dụng hoặc chuyển giao ứng dụng của những sự kiện đó vào một tình huống ("memory-plus application questions").

**3. Yêu cầu về Định dạng Đầu ra:**

Toàn bộ kết quả phải được trình bày trong **MỘT bảng Markdown duy nhất** với cấu trúc chính xác như sau:

| Question ID | Question | Correct Answer (A) | Option B | Option C | Option D | Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

**4. Quy tắc cho từng cột:**

* **Question ID:** Phải tuân thủ định dạng `[Bài số]-[Độ khó]-[Số thứ tự]`.
    * `[Bài số]` lấy từ thông tin đầu vào (ví dụ: `B1`).
    * `[Độ khó]` là `1` (Biết), `2` (Hiểu), hoặc `3` (Vận dụng).
    * `[Số thứ tự]` là hai chữ số, bắt đầu từ `01` cho mỗi nhóm độ khó (ví dụ: `B1-1-01`, `B1-1-02`, `B1-2-01`,...).
* **Question:** Nội dung câu hỏi phải rõ ràng, không gây mơ hồ.
* **Correct Answer (A):** Đáp án đúng **LUÔN LUÔN** được đặt ở cột này.
* **Option B, C, D:** Các phương án gây nhiễu. Chúng phải hợp lý, có tính thuyết phục và đồng nhất về nội dung với đáp án đúng. Tránh các phương án quá vô lý hoặc dễ dàng bị loại bỏ.
* **Explanation:** Cung cấp một lời giải thích ngắn gọn, súc tích và rõ ràng về lý do tại sao đáp án A là phương án đúng.
