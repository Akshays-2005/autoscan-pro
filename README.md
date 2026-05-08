# 📄 AutoScan Pro

AutoScan Pro is a full-stack AI-assisted document scanner application built using **React, Flask, and OpenCV**.  
It automatically detects documents from uploaded images, corrects perspective distortion, and generates clean scanned outputs similar to apps like **CamScanner**, **Adobe Scan**, and **Microsoft Lens**.

---

# 🚀 Features

✅ Automatic document detection  
✅ Perspective correction / document alignment  
✅ OpenCV-based image enhancement  
✅ Clean scanned output generation  
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
Detect Document Edges
      ↓
Find Contours
      ↓
Perspective Transform
      ↓
Enhance Scan Quality
      ↓
Download Final Scanned Image
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
| CLAHE Enhancement | Improves contrast |
| Gaussian Blur | Noise reduction |
| Canny Edge Detection | Detects document boundaries |
| Morphological Operations | Improves edge connectivity |
| Contour Detection | Finds document shape |
| Polygon Approximation | Detects document corners |
| Perspective Transform | Flattens document |
| Image Enhancement | Improves readability |

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
clahe = cv2.createCLAHE()
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

## 5️⃣ Contour Detection

Contours are extracted and sorted by area to find the document.

```python
contours, _ = cv2.findContours(...)
```

---

## 6️⃣ Perspective Transformation

The document is aligned using OpenCV perspective warp.

```python
cv2.getPerspectiveTransform()
cv2.warpPerspective()
```

---

## 7️⃣ Final Enhancement

The scanned image is sharpened and enhanced for readability.

---

# 📸 Screenshots

## Original Image

- Perspective distorted document image

## Processed Output

- Flat aligned scanned document

---

# 🔌 API Endpoint

## Process Document

```http
POST /process-document
```

### Request

Multipart form-data containing image file.

### Response

Processed scanned image.

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

## Run Frontend

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:8080
```

---

# ⚙️ Backend Setup

## Navigate to Backend

```bash
cd backend
```

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
opencv-python
numpy
```

---

# 🌟 Key Highlights

- Real-world Computer Vision application
- Full-stack implementation
- Robust contour detection pipeline
- Perspective correction algorithm
- Practical OpenCV usage
- Clean UI/UX design

---

# 🚧 Future Improvements

- 📄 PDF export
- 🧾 OCR text extraction
- 📱 Mobile camera support
- 🌗 Automatic threshold/B&W scan mode
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
