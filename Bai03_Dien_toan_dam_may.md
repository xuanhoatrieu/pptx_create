**Bài 03: Điện toán đám mây và công tác trực tuyến**

**1.4.1. Khái niệm Điện toán đám mây (Cloud Computing)** 

Điện toán đám mây là một mô hình công nghệ nổi bật trên thế giới trong những năm gần đây. Khái niệm này đã thay đổi đáng kể cách thức các doanh nghiệp và người dùng cuối tiếp cận công nghệ thông tin. Về bản chất, **Điện toán đám mây đề cập đến việc thao tác, cấu hình và truy cập các tài nguyên phần cứng và phần mềm từ xa** qua mạng Internet. Thay vì phải sở hữu và tự quản lý hạ tầng công nghệ thông tin tại chỗ, người dùng có thể "thuê" các tài nguyên tính toán (như máy chủ, lưu trữ, cơ sở dữ liệu, mạng, phần mềm, phân tích, và trí tuệ) từ một nhà cung cấp dịch vụ đám mây. 

Viện Tiêu chuẩn và Công nghệ Quốc gia Hoa Kỳ (NIST) định nghĩa: "Điện toán đám mây là một mô hình cho phép truy cập mạng theo yêu cầu, ở mọi nơi, một cách thuận tiện, tới một bể tài nguyên tính toán có thể cấu hình được (ví dụ: mạng, máy chủ, lưu trữ, ứng dụng, và dịch vụ) mà có thể được cung cấp và giải phóng nhanh chóng với nỗ lực quản lý hoặc tương tác với nhà cung cấp dịch vụ ở mức tối thiểu".

**1.4.2. Lợi ích của điện toán đám mây**

* **Tối ưu chi phí:** Giảm thiểu chi phí đầu tư ban đầu (CAPEX) vào phần cứng và hạ tầng, chuyển sang chi phí vận hành (OPEX) theo mô hình trả tiền theo mức độ sử dụng (pay-as-you-go).   
* **Sự linh hoạt và khả năng mở rộng (Agility and Elasticity):** Nhanh chóng tăng hoặc giảm quy mô tài nguyên để đáp ứng với nhu cầu thay đổi của doanh nghiệp, đảm bảo hiệu suất và tối ưu hóa chi phí.   
* **Độc lập về nền tảng:** Người dùng có thể truy cập các ứng dụng và dữ liệu từ bất kỳ đâu, trên mọi thiết bị có kết nối Internet như máy tính, điện thoại di động, hoặc máy tính bảng, thông qua một trình duyệt web.  
* **Hỗ trợ làm việc nhóm:** Dễ dàng chia sẻ dữ liệu, đồng bộ tài liệu và cộng tác thời gian thực.  
* **Tính an toàn và khôi phục dữ liệu:** Dữ liệu được sao lưu trên nhiều máy chủ, giảm rủi ro mất mát do hỏng thiết bị hoặc sự cố.

**1.4.3. Hệ sinh thái Điện toán đám mây**

![Cloud Computing là gì? Điện toán đám mây công nghiệp- Myrobot][image1]

*Hình 37 Cloud Computing*

**\* Các mô hình dịch vụ (Service Models)** 

Điện toán đám mây thường được cung cấp qua ba mô hình dịch vụ cơ bản là IaaS, PaaS, và SaaS. Các mô hình này được phân tầng, kế thừa các cơ chế quản lý và bảo mật từ tầng dưới nó. Gần đây, các mô hình mới như FaaS và CaaS đã trở nên phổ biến, cung cấp mức độ trừu tượng hóa cao hơn. 

**Hạ tầng như một Dịch vụ (Infrastructure-as-a-Service \- IaaS):** Cung cấp các tài nguyên tính toán cơ bản nhất như máy chủ ảo (virtual machines), lưu trữ và mạng. Khách hàng thuê hạ tầng này và tự chịu trách nhiệm cài đặt, quản lý hệ điều hành, và các ứng dụng. 

Ví dụ: Amazon Web Services (AWS) EC2, Microsoft Azure Virtual Machines, Google Compute Engine. 

**Nền tảng như một Dịch vụ (Platform-as-a-Service \- PaaS):** Cung cấp một môi trường (platform) cho phép các nhà phát triển xây dựng, thử nghiệm, triển khai và quản lý ứng dụng mà không cần quan tâm đến hạ tầng bên dưới. 

Ví dụ: Google App Engine, Microsoft Azure App Service, Heroku. 

**Phần mềm như một Dịch vụ (Software-as-a-Service \- SaaS):** Cung cấp các ứng dụng phần mềm hoàn chỉnh, sẵn sàng để sử dụng qua Internet, thường theo mô hình thuê bao. Người dùng cuối truy cập và sử dụng phần mềm qua trình duyệt web hoặc ứng dụng di động mà không cần lo lắng về việc cài đặt hay bảo trì. 

Ví dụ: Microsoft 365, Google Workspace, Salesforce, Canva. 

**Chức năng như một Dịch vụ (Function-as-a-Service \- FaaS) hay Điện toán phi máy chủ (Serverless Computing):** Đây là một mô hình nâng cao của PaaS, nơi các nhà phát triển chỉ cần viết và tải lên các đoạn mã (functions) để thực thi các tác vụ cụ thể. Nhà cung cấp đám mây sẽ tự động quản lý việc cấp phát tài nguyên và thực thi mã khi có sự kiện kích hoạt. Người dùng chỉ trả tiền cho thời gian mã được thực thi, tính bằng mili giây. 

Ví dụ: AWS Lambda, Google Cloud Functions, Microsoft Azure Functions. 

![7 Different Types of Cloud Computing Structures | UniPrint.net][image2]

*Hình 38 Mô hình dịch vụ Cloud computing*

**\* Phân loại các mô hình điện toán đám mây** 

**Đám mây công cộng (Public Cloud):** Hạ tầng đám mây thuộc sở hữu và được vận hành bởi một nhà cung cấp bên thứ ba (ví dụ: AWS, Google Cloud, Microsoft Azure). Họ cung cấp tài nguyên tính toán của mình như máy chủ và lưu trữ qua Internet. Đây là mô hình phổ biến nhất, mang lại lợi ích về quy mô và chi phí.

**Đám mây riêng (Private Cloud):** Hạ tầng đám mây được xây dựng và sử dụng độc quyền bởi một tổ chức duy nhất. Đám mây riêng có thể được đặt tại trung tâm dữ liệu của chính tổ chức hoặc do một bên thứ ba vận hành. Mô hình này cung cấp mức độ kiểm soát và bảo mật cao nhất, thường được các cơ quan chính phủ hoặc các tổ chức tài chính lựa chọn. 

**Đám mây lai (Hybrid Cloud):** Là sự kết hợp giữa đám mây công cộng và đám mây riêng, được liên kết với nhau bằng công nghệ cho phép chia sẻ dữ liệu và ứng dụng giữa chúng. Đám mây lai mang lại cho doanh nghiệp sự linh hoạt cao hơn, nhiều tùy chọn triển khai hơn và giúp tối ưu hóa hạ tầng, bảo mật và tuân thủ hiện có. 

**Đa đám mây (Multi-cloud):** Là chiến lược sử dụng dịch vụ từ nhiều hơn một nhà cung cấp đám mây công cộng. Ví dụ, một công ty có thể sử dụng AWS cho IaaS, đồng thời sử dụng Google Workspace cho SaaS. Chiến lược này giúp doanh nghiệp tránh phụ thuộc vào một nhà cung cấp duy nhất (vendor lock-in) và tận dụng được thế mạnh riêng của từng nền tảng.

![7 Different Types of Cloud Computing Structures | UniPrint.net][image3]

*Hình 39 Coud Deployment Models*

**1.4.4. Một số công cụ điện toán đám mây phổ biến**

**Google Drive:** Tích hợp sâu trong hệ sinh thái Google Workspace, nổi bật với khả năng cộng tác và đồng bộ hóa thời gian thực trên Docs, Sheets, và Slides. Về bảo mật, Google Drive sử dụng mã hóa AES 256-bit và TLS/SSL. Tuy nhiên, Google giữ 

khóa mã hóa, gây ra một số lo ngại về quyền riêng tư. Người dùng được khuyến nghị bật xác thực hai yếu tố (2FA) để tăng cường bảo mật. 

**Microsoft OneDrive:** Là một phần không thể thiếu của Microsoft 365, tích hợp chặt chẽ với các ứng dụng Office (Word, Excel, PowerPoint) và các công cụ cộng tác như SharePoint và Teams. 

**Dropbox:** Một trong những dịch vụ tiên phong và vẫn rất phổ biến, được biết đến với sự đơn giản và hiệu quả trong việc đồng bộ hóa tệp tin.

**iCloud:** Là dịch vụ lưu trữ đám mây của Apple, cho phép người dùng đồng bộ và sao lưu dữ liệu như ảnh, video, danh bạ, ghi chú và tài liệu giữa các thiết bị Apple như iPhone, iPad, Mac. iCloud giúp truy cập dữ liệu mọi lúc, mọi nơi và hỗ trợ khôi phục dữ liệu khi cần thiết, đồng thời tăng cường bảo mật thông qua mã hóa và xác thực hai yếu tố.

| Tiêu chí | Google Drive | OneDrive | Dropbox | iCloud |
| ----- | ----- | ----- | ----- | ----- |
| **Nhà phát triển** | Google | Microsoft | Dropbox Inc. | Apple |
| **Tích hợp hệ điều hành** | Android, ChromeOS, Windows, iOS, macOS | Windows, iOS, macOS, Android | Đa nền tảng (Windows, macOS, Linux, iOS...) | iOS, macOS (tốt nhất), Windows, web |
| **Dung lượng miễn phí** | 15 GB | 5 GB | 2 GB | 5 GB |
| **Gói nâng cấp phổ biến** | 100 GB (1.99 USD/tháng) | 100 GB (1.99 USD/tháng), Microsoft 365 kèm | 2 TB (9.99 USD/tháng) | 50 GB (0.99 USD/tháng), 200 GB, 2 TB |
| **Tính năng nổi bật** | Hợp tác trực tuyến, Google Docs/Sheets | Tích hợp Office 365, sao lưu máy tính | Chia sẻ file linh hoạt, lịch sử phiên bản | Đồng bộ ảnh, danh bạ, thiết bị Apple |
| **Tốc độ đồng bộ** | Nhanh, ổn định | Rất nhanh trên Windows | Nhanh, hiệu quả | Nhanh với thiết bị Apple, giới hạn ngoài hệ |
| **Bảo mật** | Mã hóa TLS và AES 128-bit | Mã hóa AES 256-bit, xác thực 2 bước | Mã hóa AES 256-bit, xác thực 2 bước | Mã hóa đầu-cuối với ảnh, 2FA, Apple ID |
| **Hạn chế** | Phụ thuộc tài khoản Google | Tối ưu cho Windows, ít hỗ trợ Linux | Dung lượng miễn phí ít, gói cao cấp đắt | Ít linh hoạt với thiết bị không phải của Apple |

![Đã tạo hình ảnh][image4]

*Hình 41 So sánh các dịch vụ lưu trữ*

![Real-World Applications of Cloud Computing][image5]

*Hình 40 Application of Cloud Computing* 

**1.4.5. Cộng tác và quản lý công việc trực tuyến** 

Trong môi trường làm việc số, kỹ năng cộng tác và quản lý công việc trực tuyến là yếu tố then chốt để nâng cao năng suất. Các bộ công cụ đám mây như Google Workspace và Microsoft 365 cung cấp một hệ sinh thái toàn diện cho mục đích này. 

**Hệ sinh thái Google Workspace** 

Google Workspace là bộ công cụ làm việc và cộng tác trực tuyến của Google, giúp người dùng học tập và làm việc hiệu quả mọi lúc, mọi nơi. Hệ sinh thái này bao gồm nhiều ứng dụng tích hợp chặt chẽ, nổi bật như:

* **Gmail** – Email chuyên nghiệp, bảo mật cao.

* **Google Drive** – Lưu trữ, chia sẻ và đồng bộ dữ liệu trên nền tảng đám mây.

* **Google Docs, Sheets, Slides** – Soạn thảo văn bản, bảng tính, thuyết trình trực tuyến, hỗ trợ cộng tác thời gian thực.

* **Google Meet** – Họp, học trực tuyến với video và chat tích hợp.

* **Google Calendar** – Lên lịch, quản lý công việc và sự kiện.

* **Google Forms** – Tạo biểu mẫu, khảo sát, thu thập dữ liệu nhanh chóng.

* **Google Keep** – Ghi chú, lưu ý và quản lý ý tưởng cá nhân.

Nhờ khả năng đồng bộ và chia sẻ tức thì, Google Workspace hỗ trợ mạnh mẽ cho học tập, nghiên cứu và làm việc nhóm trong môi trường số.

![Google Workspace Administration][image6]

*Hình 42 Google Workspace*

**Hệ sinh thái Microsoft 365** 

Microsoft 365 là bộ công cụ làm việc và cộng tác trực tuyến của Microsoft, kết hợp các ứng dụng văn phòng quen thuộc với dịch vụ đám mây, giúp người dùng học tập, làm việc mọi lúc, mọi nơi và trên mọi thiết bị. Với khả năng đồng bộ, bảo mật cao và tích hợp sâu giữa các ứng dụng, Microsoft 365 hỗ trợ hiệu quả cho học tập, nghiên cứu và làm việc nhóm trong môi trường số hiện đại.

Các ứng dụng tiêu biểu gồm:

* **Outlook** – Email và lịch làm việc chuyên nghiệp.

* **Word** – Soạn thảo văn bản mạnh mẽ, nhiều tính năng định dạng.

* **Excel** – Xử lý bảng tính, phân tích dữ liệu.

* **PowerPoint** – Tạo bài thuyết trình trực quan, sinh động.

* **OneNote** – Ghi chú, quản lý ý tưởng, tài liệu học tập.

* **OneDrive** – Lưu trữ, chia sẻ dữ liệu trên đám mây.

* **Teams** – Họp, chat, cộng tác nhóm thời gian thực.

* **SharePoint** – Xây dựng và quản lý trang thông tin, tài nguyên nội bộ.

* **Copilot:** Copilot là AI tạo sinh (Generative AI) được tích hợp vào hệ sinh thái 365\. Copilot có thể tự động tóm tắt cuộc họp, đề xuất các hành động cần làm, soạn thảo email, tạo bản nháp văn bản trong Word, và phân tích dữ liệu trong Excel, giúp tự động hóa các tác vụ và nâng cao đáng kể năng suất. 

![Microsoft 365 và những lợi ích tuyệt với doanh nghiệp][image7]

*Hình 43 Microsoft 365*

**1.4.6. An toàn và bảo mật trên đám mây** 

Sự tiện lợi của điện toán đám mây đi kèm với trách nhiệm bảo vệ dữ liệu của chính người dùng. Việc dữ liệu được lưu trữ trên các máy chủ từ xa đặt ra những yêu cầu nghiêm ngặt về bảo mật để chống lại các nguy cơ truy cập trái phép, tấn công mạng và rò rỉ thông tin. Do đó, việc trang bị kiến thức và kỹ năng bảo mật cơ bản là điều kiện tiên quyết để làm việc an toàn trong môi trường số.

**\- Các rủ ro khi sử dụng điện toán đám mây**

**\- Biện pháp**

**Các biện pháp bảo mật thiết yếu cho người dùng** 

Bên cạnh việc tuân thủ pháp luật của các nhà cung cấp dịch vụ, ý thức và hành động của mỗi người dùng đóng vai trò quyết định trong việc bảo vệ tài khoản và dữ liệu của chính mình. 

**Quản lý mật khẩu (Password Management):** Mật khẩu là lớp phòng thủ đầu tiên. Một mật khẩu mạnh cần tuân thủ các nguyên tắc: có độ dài tối thiểu 12-14 ký tự, kết hợp chữ hoa, chữ thường, số và ký tự đặc biệt. Quan trọng hơn, **không bao giờ được sử dụng lại cùng một mật khẩu cho nhiều dịch vụ khác nhau**. Để quản lý hiệu quả, người dùng nên sử dụng các **trình quản lý mật khẩu (password managers)** như Bitwarden, 1Password, hoặc tính năng tích hợp sẵn trong trình duyệt để tạo và lưu trữ các mật khẩu mạnh, ngẫu nhiên cho mỗi trang web. 

**Xác thực hai yếu tố (Two-Factor Authentication \- 2FA):** Đây là một lớp bảo mật cực kỳ quan trọng, bổ sung thêm một bước xác minh sau khi nhập mật khẩu. Ngay cả khi kẻ xấu có được mật khẩu của bạn, chúng cũng không thể đăng nhập nếu không có yếu tố thứ hai này. Các hình thức 2FA phổ biến bao gồm: mã số gửi qua tin nhắn SMS, mã số sinh ra từ ứng dụng xác thực (Google Authenticator, Microsoft Authenticator), hoặc khóa bảo mật vật lý (YubiKey). Người dùng **bắt buộc** phải kích hoạt 2FA trên tất cả các tài khoản quan trọng như email, mạng xã hội và ngân hàng. 

**Phân quyền chia sẻ (Sharing Permissions):** Khi chia sẻ tệp hoặc thư mục trên các dịch vụ như Google Drive hay OneDrive, người dùng cần hiểu rõ và áp dụng đúng các quyền truy cập. Nguyên tắc "đặc quyền tối thiểu" (principle of least privilege) nên được tuân thủ: chỉ cấp quyền hạn thấp nhất đủ để người khác hoàn thành công việc. 

**Người xem (Viewer):** Chỉ có thể xem nội dung, không thể bình luận hay chỉnh sửa. 

**Người nhận xét (Commenter):** Có thể xem và để lại bình luận, nhưng không thể thay đổi nội dung gốc. 

**Người chỉnh sửa (Editor):** Có toàn quyền xem, bình luận, chỉnh sửa và chia sẻ tiếp tài liệu. Cần hết sức cẩn trọng khi cấp quyền này. 

**Nhận diện lừa đảo (Phishing):** Phishing là hình thức tấn công giả mạo các email, tin nhắn hoặc trang web uy tín để lừa người dùng tiết lộ thông tin nhạy cảm như mật khẩu, thông tin thẻ tín dụng. Các dấu hiệu nhận biết một cuộc tấn công phishing bao gồm: các yêu cầu khẩn cấp, lời đe dọa khóa tài khoản, các lỗi chính tả hoặc ngữ pháp, địa chỉ email người gửi đáng ngờ, và các đường link dẫn đến những trang web không quen thuộc. Nguyên tắc vàng là: **luôn kiểm tra kỹ người gửi và không bao giờ nhấp vào các liên kết đáng ngờ**. Thay vào đó, hãy tự truy cập trang web chính thức của dịch vụ bằng cách gõ địa chỉ trực tiếp vào trình duyệt.

**\- Khung pháp lý tại Việt Nam** 

Tại Việt Nam, nhận thức về tầm quan trọng của an toàn dữ liệu được thể hiện qua một hệ thống các văn bản quy phạm pháp luật ngày càng hoàn thiện. Các quy định này tạo ra một hành lang pháp lý để bảo vệ quyền và lợi ích hợp pháp của cá nhân và tổ chức trên không gian mạng. Một số văn bản tiêu biểu bao gồm: 

**Luật An ninh mạng (2018):** Là văn bản pháp lý cốt lõi, quy định các hoạt động bảo vệ an ninh quốc gia và đảm bảo trật tự, an toàn xã hội trên không gian mạng; trách nhiệm của các cơ quan, tổ chức, cá nhân có liên quan. 

**Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân:** Đây là một nghị định quan trọng, quy định chi tiết về quyền của chủ thể dữ liệu, trách nhiệm của bên kiểm soát và xử lý dữ liệu, cũng như các biện pháp bảo vệ dữ liệu cá nhân, có ảnh hưởng trực tiếp đến cách các dịch vụ đám mây xử lý thông tin người dùng tại Việt Nam. 

**Nghị định số 147/2024/NĐ-CP của Chính phủ:** Quy định về quản lý, cung cấp, sử dụng dịch vụ Internet và thông tin trên mạng. 

**Luật Công nghiệp công nghệ số (2025):** Được Quốc hội thông qua ngày 14/6/2025, luật này được kỳ vọng sẽ tạo ra một khuôn khổ toàn diện để thúc đẩy và quản lý ngành công nghiệp công nghệ số, trong đó có các vấn đề liên quan đến an toàn và chủ quyền dữ liệu. 

 **Thảo luận và bài tập thực hành** 

Bài tập nhóm sử dụng chức năng share drive để cùng nhau làm báo cáo thiết lập bảo mật cơ bản trên các nền tảng phổ biến như Facebook, Google, email trường.