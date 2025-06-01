
# 🔐 Multi-Media Steganography Web Application

A user-friendly Streamlit-based web application to perform steganography on different types of media—images, audio, and email attachments. It allows users to hide and reveal text or images, send and receive stego files securely with verification codes.

## 💡 Features

### 1. Text in Image
- Hide a secret text message in an image (PNG, JPG, JPEG).
- Reveal hidden messages from images.
- Download the stego image.

### 2. Image in Image
- Embed one image inside another.
- Extract hidden image from the stego image.
- Download both stego and revealed images.

### 3. Email Steganography with Verification
- Send a PNG image with hidden message and verification code via Gmail.
- Verify the message using the verification code.
- Receive and reveal hidden message using code verification.

### 4. Audio Steganography
- Hide a text message inside a WAV audio file.
- Reveal a hidden message from a stego audio file.
- Download the stego audio file.

## 🔧 Technologies Used
- Python
- Streamlit
- PIL (Pillow)
- Wave
- Base64
- Email / smtplib

## 📦 Installation

```bash
pip install streamlit pillow
```

> Note: To use email functionality, enable 2-step verification and use an App Password for Gmail.

## 🚀 Running the App

```bash
streamlit run app.py
```

## 🔐 Security
- App password is required for Gmail integration.
- Verification code is generated and sent with the hidden message to verify message authenticity.

## 📁 Folder Structure

```
.
├── app.py
├── stegno.png
└── README.md
```

## 📸 Screenshots
(Add your screenshots here if required)

## 📬 Contact

**Developer:** Harish H Kulkarni  
**Email:** kulkarniharish4102000@gmail.com

---

© 2025 Multi-Media Steganography. All rights reserved.
