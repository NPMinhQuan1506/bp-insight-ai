Chắc chắn rồi! Thêm bước khử nhiễu là một cải tiến cực kỳ quan trọng và thực tế cho quy trình xử lý ảnh. Nó sẽ giúp tăng độ chính xác của các bước sau, đặc biệt là bước nhị phân hóa Otsu.

Dưới đây là phiên bản tài liệu của bạn đã được cập nhật, bao gồm **Step 1.5 - Denoising** được tích hợp một cách liền mạch vào cấu trúc hiện có.

---

# 🩺 BP Insight AI

BP Insight AI is a lightweight, modular Python application designed to automatically extract blood pressure readings from images of digital monitors (e.g. OMRON, Microlife) using OCR, and diagnose hypertension risk based on standard WHO thresholds.

🔍 **Features:**
- OCR-based text extraction using EasyOCR
- Detection of SYS, DIA, and PUL from noisy medical images
- Rule-based diagnosis logic aligned with WHO classifications
- Gradio web UI for real-time, user-friendly testing
- Modular structure ready for integration with EHR systems or personal health apps

🧠 Designed for:
- Healthcare automation
- Remote monitoring support
- Smart health devices and applications

# Source Tree
bp-insight-ai/
├── app/
│   ├── __init__.py                  # Define APP_NAME, VERSION, FOLDER_IMAGE_NAME
│   ├── image_loader.py              # Step 1: Load image & convert to grayscale
│   ├── **denoiser.py**                  # **Step 1.5: Apply denoising filter (e.g., Gaussian Blur)**
│   ├── binarizer.py                 # Step 2: Convert grayscale → binary (0/1)
│   ├── region_detector.py           # Step 3: Detect digit regions (Connected Components)
│   ├── digit_recognizer.py          # Step 4: Recognize digits (custom template matching)
│   ├── utils.py                     # Common utilities (list images, ASCII preview, etc.)
│
├── input_images/                    # Test images from BP monitors
│   ├── example1.jpg
│   ├── example2.png
│   └── ...
│
├── tests/
│   ├── test_image_loader.py         # Unit tests for Step 1
│   ├── **test_denoiser.py**             # **Unit tests for Step 1.5**
│   ├── test_binarizer.py            # Unit tests for Step 2
│   ├── test_region_detector.py      # Unit tests for Step 3
│   ├── test_digit_recognizer.py     # Unit tests for Step 4
│
├── main.py                          # CLI menu: run steps interactively
├── README.md                        # Project description & usage
└── requirements.txt                 # (Optional) List dependencies (if any)

## Implementation Steps

### **Step 1 – Load & Grayscale**
- **Goal:** Read `.png/.jpg` files and convert them into a grayscale matrix (0–255).
- **Process:**
  - Use `PIL.Image` or manually read pixels.
  - Convert to `'L'` mode (grayscale).
- **Output:** `list[list[int]]` (pixel matrix).
- **Testing:** Check if the file exists and pixel values are within [0, 255].

---

### **Step 1.5 – Denoising (Optional but Recommended)**
- **Goal:** Reduce random pixel noise (e.g., sensor noise, compression artifacts) from the grayscale image. This crucial step "cleans" the image's histogram, allowing Otsu's algorithm to find a more accurate and stable threshold in the next step.
- **Method:**
  - **Gaussian Blur:** This is the most common and effective method.
  - **Principle:** It replaces each pixel's value with a weighted average of its surrounding pixels. Pixels closer to the center have more influence, creating a natural-looking blur that smooths out noise.
  - A small kernel size (e.g., 3x3 or 5x5) is usually sufficient to reduce noise without blurring the digit shapes too much.
- **Output:** A "smoother" grayscale matrix `list[list[int]]` with noise reduced.
- **Testing:** Verify that image dimensions are preserved. A visual check is key: the output image should appear slightly blurrier than the grayscale input, with "salt-and-pepper" noise spots blended into their surroundings.

---

### **Step 2 – Binarization**
- **Goal:** Convert the (denoised) grayscale image into a binary image (0 or 1). This simplifies the image so that algorithms only need to distinguish between "text" and "background".
- **Method:**
  - **Fixed threshold** (default 128).
  - **Otsu's threshold** (automatically determine optimal threshold). This method benefits greatly from the previous denoising step.
- **Output:** `list[list[int]]` containing only `{0, 1}`.
- **Testing:** Ensure image dimensions are preserved and all values belong to `{0, 1}`.

---

### **Step 3 – Region Detection**
- **Goal:** Identify digit blobs in the binary image.
- **Method:**
  - Traverse the image → group connected `1` pixels (**Connected Components**).
  - Filter by size/ratio (remove noise, keep digits).
  - Sort bounding boxes from left to right.
- **Output:** List of bounding boxes `(x, y, w, h)`.
- **Testing:** Ensure detected regions are reasonable and all bounding boxes are within image bounds.

---

### **Step 4 – Digit Recognition**
- **Goal:** Determine which digit each detected region represents.
- **Method:**
  - **Template matching** (compare against digit templates 0–9).
  - Implement correlation/pixel matching manually, without external AI libraries.
- **Output:** List of digits (SYS, DIA, PUL).
- **Testing:** Compare results with known labeled sample images.

---

### **Step 5 – Evaluation & Diagnosis**
- **Goal:** Provide blood pressure classification (Normal / High / Low).
- **Process:**
  - Read the three values: SYS, DIA, PUL → compare with medical standards.
  - Output classification and alerts.
- **Output:** Diagnostic text.
- **Testing:** Test multiple simulated cases.

---

## 📌 Main Flow (`main.py`)
1. Show menu to select an image from `input_images/`.
2. **Step 1:** Load image → preview grayscale.
3. **Step 1.5:** Denoise image → preview denoised image.
4. **Step 2:** Binarize → preview binary.
5. **Step 3:** Region detection → draw bounding boxes (ASCII or preview).
6. **Step 4:** Recognize digits → print results.
7. **Step 5:** Blood pressure evaluation → print alert.