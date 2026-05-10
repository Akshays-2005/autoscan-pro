# 📄 AutoScan Pro

## 🔗 Live Demo

Frontend:  
https://autoalign-doc.netlify.app/

GitHub Repository:  
https://github.com/Akshays-2005/autoscan-pro

---

AutoScan Pro is a full-stack computer vision–based document alignment and scanning application built using **React, Flask, and OpenCV**.

It automatically detects document boundaries, corrects perspective distortion, aligns skewed documents, and preserves the original document appearance similar to applications like **Adobe Scan**, **CamScanner**, and **Microsoft Lens**.

---

# 🚀 Features

✅ Automatic document detection  
✅ Perspective correction / document alignment  
✅ Color-preserving document alignment  
✅ Dynamic perspective correction  
✅ Automatic contour validation  
✅ OpenCV-based image enhancement  
✅ Before vs After preview  
✅ Download processed image  
✅ Responsive modern UI  
✅ Flask REST API backend  
✅ Drag & drop image upload  

---

# 🖼️ Demo Workflow

```text
Upload Image
      ↓
Convert to Grayscale
      ↓
Contrast Enhancement
      ↓
Edge Detection
      ↓
Find Document Contours
      ↓
Perspective Transform
      ↓
Aligned Output Image
```

---

# 🛠️ Tech Stack

## Frontend

- React 18
- TypeScript
- Vite
- TailwindCSS
- React Query
- Radix UI
- Lucide Icons

## Backend

- Flask
- Flask-CORS
- OpenCV
- NumPy

---

# 🧠 Computer Vision Concepts Used

This project implements several important image processing techniques:

| Concept | Purpose |
|---|---|
| Grayscale Conversion | Simplifies processing |
| CLAHE Enhancement | Improves low-light visibility |
| Gaussian Blur | Noise reduction |
| Canny Edge Detection | Detects document boundaries |
| Morphological Operations | Improves edge connectivity |
| Contour Detection | Finds document shape |
| Polygon Approximation | Detects document corners |
| Rotated Rectangle Recovery | Handles imperfect contours |
| Perspective Geometry | Corrects skewed documents |
| Perspective Transform | Flattens document |
| Image Enhancement | Improves clarity |

---

# 📂 Project Structure

```bash
autoscan-pro/
│
├── backend/
│   ├── app.py
│   ├── utils.py
│   └── requirements.txt
│
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── App.tsx
│
├── public/
├── package.json
├── vite.config.ts
└── README.md
```

---

# ⚙️ How It Works

## 1️⃣ Upload Document Image

The user uploads an image containing a document.

---

## 2️⃣ Preprocessing

The backend converts the image into grayscale and enhances contrast using CLAHE.

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(
    clipLimit=3.5,
    tileGridSize=(8,8)
)

gray = clahe.apply(gray)
```

---

## 3️⃣ Noise Reduction

Gaussian Blur is applied to smooth the image.

```python
blur = cv2.GaussianBlur(gray, (5, 5), 0)
```

---

## 4️⃣ Edge Detection

Canny Edge Detection identifies document boundaries.

```python
edges = cv2.Canny(blur, 20, 100)
```

---

## 5️⃣ Morphological Operations

Morphological operations improve contour connectivity.

```python
edges = cv2.dilate(edges, kernel, iterations=2)

edges = cv2.erode(edges, kernel, iterations=1)

edges = cv2.morphologyEx(
    edges,
    cv2.MORPH_CLOSE,
    kernel,
    iterations=2
)
```

---

## 6️⃣ Contour Detection

Contours are extracted and sorted by area to find the document.

```python
contours, _ = cv2.findContours(
    edges,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
```

---

## 7️⃣ Perspective Transformation

The document is aligned using OpenCV perspective warp.

```python
matrix = cv2.getPerspectiveTransform(
    ordered,
    dst
)

warped = cv2.warpPerspective(
    img,
    matrix,
    (width, height)
)
```

---

## 8️⃣ Final Enhancement

The aligned document is enhanced while preserving original colors and contents.

```python
warped = cv2.detailEnhance(
    warped,
    sigma_s=10,
    sigma_r=0.15
)
```

---

# 📸 Screenshots

## Original Image

- Perspective distorted document image

## Processed Output

- Perspective-corrected aligned document with preserved colors and content

---

# 🔌 API Endpoint

## Process Document

```http
POST /process-document
```

### Request

Multipart form-data containing image file.

### Response

Processed aligned image.

---

# 🧪 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Akshays-2005/autoscan-pro.git

cd autoscan-pro
```

---

# 🖥️ Frontend Setup

## Install Dependencies

```bash
npm install
```

---

## Run Frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

# ⚙️ Backend Setup

## Navigate to Backend

```bash
cd backend
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Flask Server

```bash
python app.py
```

Backend runs at:

```text
http://localhost:5000
```

---

# 📦 Backend Dependencies

```txt
Flask
Flask-CORS
opencv-python-headless
numpy
gunicorn
```

---

# 🌐 Deployment

## Frontend Deployment

- Netlify

## Backend Deployment

- Render

The frontend communicates with the Flask-OpenCV backend using REST API calls.

---

# 🌟 Key Highlights

- Real-world Computer Vision application
- Full-stack implementation
- Robust contour detection pipeline
- Perspective correction algorithm
- Practical OpenCV usage
- Responsive UI/UX design
- Color-preserving alignment system
- Production-style deployment

---

# 🚧 Future Improvements

- 📄 PDF export
- 🧾 OCR text extraction
- 📱 Mobile camera support
- 🌗 Optional black & white scan mode
- ☁️ Cloud storage integration
- 📚 Multi-page document scanning
- 🎥 Real-time webcam document scanning

---

# 📚 Learning Outcomes

This project demonstrates practical understanding of:

- Image Processing
- OpenCV
- Perspective Geometry
- REST APIs
- Full Stack Development
- Frontend + Backend Integration
- Computer Vision Pipelines
- Contour-Based Object Detection

---

# 🤝 Contributing

Contributions are welcome!

Feel free to:
- Fork the repository
- Create a feature branch
- Submit pull requests

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Akshay S

GitHub:  
https://github.com/Akshays-2005

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub!
