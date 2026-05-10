# 📄 AutoScan Pro

## 🔗 Live Demo

Frontend: https://autoalign-doc.netlify.app/

GitHub Repository:  
https://github.com/Akshays-2005/autoscan-pro

---

# 🚀 About The Project

AutoScan Pro is a full-stack computer vision–based document alignment and scanning application built using **React, Flask, and OpenCV**.

The system automatically detects document boundaries, corrects perspective distortion, aligns skewed documents, and preserves the original document appearance using advanced image processing techniques.

The application is inspired by real-world document scanner applications such as **Adobe Scan**, **CamScanner**, and **Microsoft Lens**.

---

# ✨ Features

✅ Automatic document detection  
✅ Perspective correction / document alignment  
✅ Color-preserving document alignment  
✅ Dynamic perspective transformation  
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
CLAHE Contrast Enhancement
      ↓
Gaussian Blur
      ↓
Canny Edge Detection
      ↓
Morphological Operations
      ↓
Contour Detection
      ↓
Perspective Transformation
      ↓
Aligned Final Output
