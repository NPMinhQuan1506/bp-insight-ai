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
│   ├── binarizer.py                  # Step 2: Convert grayscale → binary (0/1)
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
- **Formula**
# RGB to Grayscale Conversion Example

## 1. Original Image
Suppose you have a 3×3 pixel image with original RGB colors as follows:

| Pixel | R   | G   | B   |
|-------|-----|-----|-----|
| P1    | 255 | 0   | 0   |
| P2    | 0   | 255 | 0   |
| P3    | 0   | 0   | 255 |
| P4    | 255 | 255 | 255 |
| P5    | 0   | 0   | 0   |
| P6    | 128 | 128 | 128 |
| P7    | 200 | 100 | 50  |
| P8    | 50  | 50  | 200 |
| P9    | 100 | 200 | 100 |

---

## 2. Convert RGB → Grayscale
**Formula**
```
Gray = 0.299*R + 0.587*G + 0.114*B   (luminance formula)
```

**Examples:**
- **P1** (Red) → Gray = `0.299×255 + 0.587×0 + 0.114×0` ≈ **76**
- **P4** (White) → Gray ≈ **255**
- **P5** (Black) → Gray = **0**
- **P6** (Gray 128,128,128) → Gray ≈ **128**

---

## 3. Result Matrix – `list[list[int]]`
After converting all pixels to grayscale values (0–255), the 3×3 image becomes:

```python
[
  [ 76, 150,  29 ],  # Row 1
  [255,   0, 128 ],  # Row 2
  [144,  71, 170 ]   # Row 3
]
```
- Each **row** in the list = one row of pixels in the image.
- Each **integer** = pixel brightness (**0 = black** → **255 = white**). 

- **Process:**
  - Use `PIL.Image` or manually read pixels.
  - Convert to `'L'` mode (grayscale).
- **Output:** `list[list[int]]` (pixel matrix).
- **Testing:** Check if the file exists and pixel values are within [0, 255].

---

### **Step 2 – Binarization**
- **Goal:** Convert the grayscale image into a binary image (0 or 1).
    After the image has been converted to **grayscale** (0–255), the **binarization** step aims to transform it into a **binary image** with only **two values**:
    - **0** → black (pixel removed, not part of the text)
    - **1** → white (pixel kept, part of the background)
    *(Or reversed depending on the system: 0 for background, 1 for text)*

    This makes it easier for OCR algorithms to detect the shape of characters because they only have to work with two states: "present" or "absent" pixel.

---
- **Method:**
  - **Fixed threshold** (default 128).
    - Choose a fixed threshold, e.g., **128**.
    - Formula:
      ```
      pixel_bin = 1 if pixel_gray ≥ 128
                  0 if pixel_gray < 128
      ```
    - **Pros:** fast, easy to implement.
    - **Cons:** if the image has uneven lighting, a fixed threshold can cause detail loss or background merging.  
  - **Otsu's threshold** (automatically determine optimal threshold).
    - An algorithm that automatically finds the **best threshold** to separate background and text based on the **histogram distribution** of the image.
    - Principle: find the threshold value where **the variance between two pixel groups (black and white)** is maximized → best separation of text/background.
    - **Pros:** automatically adapts to various lighting conditions.
    - **Cons:** slightly more computationally complex than fixed threshold.
- **Output:** `list[list[int]]` containing only `{0, 1}`.
    The result is a **binary matrix** `list[list[int]]` containing only **0 and 1**.

    Example – from a 3×3 grayscale image:
    ```python
    [
    [ 76, 150,  29 ],
    [255,   0, 128 ],
    [144,  71, 170 ]
    ]
    ```
    If threshold = 128, the binary image will be:
    ```python
    [
    [ 0, 1, 0 ],  # Row 1
    [ 1, 0, 1 ],  # Row 2
    [ 1, 0, 1 ]   # Row 3
    ]
    ```
    - **0**: pixel less than threshold (black)
    - **1**: pixel greater than or equal to threshold (white)

    ---

- **Testing:** Ensure image dimensions are preserved and all values belong to `{0, 1}`.
  - Ensure the **binary image size** matches the grayscale image size.
  - All pixel values ∈ {0, 1}.
  - Visual check to confirm text is preserved clearly.
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
3. **Step 2:** Binarize → preview binary.
4. **Step 3:** Region detection → draw bounding boxes (ASCII or preview).
5. **Step 4:** Recognize digits → print results.
6. **Step 5:** Blood pressure evaluation → print alert.

