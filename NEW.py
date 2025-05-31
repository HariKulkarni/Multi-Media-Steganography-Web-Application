import os
import random
import streamlit as st
from PIL import Image
import smtplib
from email.message import EmailMessage
from io import BytesIO
import string
import wave
import base64

st.set_page_config(page_title="Multi Media Steganography", layout="centered", page_icon="🔐")

import base64
import streamlit as st

def set_background_for_class(image_path, target_class):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    css = f'''
    <style>
    .{target_class.replace(' ', '.')} {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        /* Optional: adjust other styles */
        background-position: center center;
        min-height: 100vh;
    }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# Usage
set_background_for_class("stegno.png", "main st-emotion-cache-bm2z3a ea3mdgi8")
hide_header_css = """
<style>
.st-emotion-cache-12fmjuu.ezrtsby2 {
    display: none !important;
}
</style>
"""

st.markdown(hide_header_css, unsafe_allow_html=True)

st.markdown("""
<style>
.stFileUploaderFileData,.st-emotion-cache-1aehpvj.e1bju1570 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Style element with specific class */
.st-emotion-cache-1aehpvj.e1bju1570 {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)


# CSS FOR BUTTONS
st.markdown("""
<style>
.st-emotion-cache-7ym5gk.ef3psqc12 {
    background-color: #FFD700 !important;  /* Bootstrap Blue */
    color: white !important;
    border: none !important;
    padding: 0.4em 1em !important;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}
.st-emotion-cache-7ym5gk.ef3psqc12:hover {
    background-color: #0056b3 !important;  /* Darker blue on hover */
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
# CSS for Header and Paragraphs

st.markdown("""
<style>
h1, h2  {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# CSS for Paragraphs
st.markdown("""
<style>
p {
    color: white !important;
    transition: color 0.3s ease;
}
p:hover {
    color: red !important;
}
</style>
""", unsafe_allow_html=True)
# CSS for Buttons and File Uploader
st.markdown("""
<style>
/* Style normal buttons */
div.stButton > button {
    color: black !important;
    background-color: #FFD700 !important;  /* button bg */
    border: none !important;
    padding: 0.4em 1em !important;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #FFA500 !important;  /* hover bg */
    color: white !important;                /* hover text */
}

/* Style file uploader browse button */
div.stFileUploader button {
    color: black !important;
    background-color: #FFD700 !important;
    border: none !important;
    padding: 0.4em 1em !important;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}
div.stFileUploader button:hover {
    background-color: #FFA500 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# --- Your Email Credentials ---
SENDER_EMAIL = "iamsameer826@gmail.com"
SENDER_PASSWORD = "ibbq tejc zkyt uxok"  # Use your app password here

# --- Utility Functions ---
def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# --- Steganography Image Functions ---
def hide_text_in_image(uploaded_img, secret_text):
    img = Image.open(uploaded_img).convert("RGB")
    encoded = img.copy()
    binary = ''.join([format(ord(i), '08b') for i in secret_text]) + '1111111111111110'
    data = iter(encoded.getdata())
    new_pixels = []
    for i in range(0, len(binary), 3):
        pixels = list(next(data))
        for j in range(3):
            if i + j < len(binary):
                pixels[j] = pixels[j] & ~1 | int(binary[i + j])
        new_pixels.append(tuple(pixels))
    new_pixels += list(data)
    encoded.putdata(new_pixels)
    output_buffer = BytesIO()
    encoded.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer

def reveal_text_from_image(uploaded_img):
    img = Image.open(uploaded_img).convert("RGB")
    buffer = ''
    stop_seq = '1111111111111110'
    found_terminator = False
    for pixel in img.getdata():
        for color in pixel[:3]:
            bit = str(color & 1)
            buffer += bit
            if len(buffer) >= 16 and buffer[-16:] == stop_seq:
                found_terminator = True
                break
        if found_terminator:
            break
    if not found_terminator:
        return False, "No terminator found in image data."
    chars = [buffer[i:i+8] for i in range(0, len(buffer) - 16, 8)]
    raw_message = ''.join([chr(int(c, 2)) for c in chars])
    return True, raw_message

# --- Audio Steganography ---
def hide_text_in_audio(audio_file, secret_message):
    audio = wave.open(audio_file, mode='rb')
    params = audio.getparams()
    frames = bytearray(audio.readframes(audio.getnframes()))
    audio.close()
    message = secret_message + '###END###'
    bits = ''.join([format(ord(c), '08b') for c in message])
    if len(bits) > len(frames):
        return None, "Message too long to hide in this audio."
    for i in range(len(bits)):
        frames[i] = (frames[i] & 254) | int(bits[i])
    buffer = BytesIO()
    stego_audio = wave.open(buffer, 'wb')
    stego_audio.setparams(params)
    stego_audio.writeframes(frames)
    stego_audio.close()
    buffer.seek(0)
    return buffer, "✅ Text successfully hidden in audio."

def reveal_text_from_audio(audio_file):
    audio = wave.open(audio_file, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    extracted_bits = [str(byte & 1) for byte in frame_bytes]
    extracted_bytes = [extracted_bits[i:i+8] for i in range(0, len(extracted_bits), 8)]
    decoded_text = ''.join([chr(int(''.join(byte), 2)) for byte in extracted_bytes])
    audio.close()
    hidden_message = decoded_text.split("###END###")[0]
    if hidden_message:
        return True, hidden_message
    else:
        return False, "No hidden message found or incorrect format."

# --- Image in Image Steganography ---
def hide_image_in_image(cover_img_file, secret_img_file):
    cover = Image.open(cover_img_file).convert("RGB")
    secret = Image.open(secret_img_file).resize(cover.size).convert("RGB")
    encoded = Image.new("RGB", cover.size)
    for x in range(cover.size[0]):
        for y in range(cover.size[1]):
            c_pixel = cover.getpixel((x, y))
            s_pixel = secret.getpixel((x, y))
            new_pixel = tuple((c & 0xF0) | (s >> 4) for c, s in zip(c_pixel, s_pixel))
            encoded.putpixel((x, y), new_pixel)
    output_buffer = BytesIO()
    encoded.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer

def reveal_image_from_image(stego_img_file):
    stego = Image.open(stego_img_file).convert("RGB")
    revealed = Image.new("RGB", stego.size)
    for x in range(stego.size[0]):
        for y in range(stego.size[1]):
            pixel = stego.getpixel((x, y))
            hidden_pixel = tuple((val & 0x0F) << 4 for val in pixel)
            revealed.putpixel((x, y), hidden_pixel)
    output_buffer = BytesIO()
    revealed.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer

# --- Streamlit UI ---
st.title("🎵 Multi-Media Steganography")
tabs = st.tabs(["Text in Image", "Image in Image", "Email Steganography", "Audio Steganography"])

# --- Text in Image ---
with tabs[0]:
    st.header("🔐 Hide Text in Image")
    uploaded_img = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], key="hide_text_img")
    secret_text = st.text_area("Secret Message")
    if st.button("Hide Text"):
        if uploaded_img and secret_text:
            result_img = hide_text_in_image(uploaded_img, secret_text)
            st.success("✅ Text hidden successfully.")
            st.download_button("📥 Download Image", result_img, file_name="hidden_text_image.png")
        else:
            st.error("Please upload an image and enter a secret message.")

    st.markdown("---")
    st.header("🔍 Reveal Text from Image")
    img_to_reveal = st.file_uploader("Upload Image with Hidden Text", type=['png', 'jpg'], key="reveal_text_img")
    if st.button("Reveal Text"):
        if img_to_reveal:
            with st.spinner("🔄 Extracting hidden message..."):
                success, message = reveal_text_from_image(img_to_reveal)
            if success:
                st.success("✅ Message revealed:")
                st.code(message)
            else:
                st.error(message)
        else:
            st.error("Please upload an image.")

# --- Image in Image ---
with tabs[1]:
    st.header("🖼 Hide Image in Image")
    cover_image = st.file_uploader("Upload Cover Image", type=['png', 'jpg'], key="cover_img")
    secret_image = st.file_uploader("Upload Secret Image", type=['png', 'jpg'], key="secret_img")
    if st.button("Hide Image"):
        if cover_image and secret_image:
            result_img = hide_image_in_image(cover_image, secret_image)
            st.success("✅ Image hidden successfully.")
            st.download_button("📥 Download Image", result_img, file_name="hidden_image.png")
        else:
            st.error("Please upload both cover and secret images.")

    st.markdown("---")
    st.header("🕵 Reveal Image from Image")
    stego_image = st.file_uploader("Upload Image with Hidden Image", type=['png', 'jpg'], key="reveal_img")
    if st.button("Reveal Image"):
        if stego_image:
            with st.spinner("🔄 Extracting hidden image..."):
                result_img = reveal_image_from_image(stego_image)
            st.success("✅ Hidden image revealed.")
            st.image(result_img)
            st.download_button("📥 Download Image", result_img, file_name="revealed_image.png")
        else:
            st.error("Please upload a stego image.")

# --- Email Steganography ---
# --- Email Steganography ---
with tabs[2]:
    st.header("📧 Send Image via Email with Verification Code")
    recipient = st.text_input("Recipient Email")
    # Removed subject and body inputs
    
    attach_file = st.file_uploader("Attach PNG Image", type=['png'], key="attach_img")
    secret_message = st.text_area("Secret Message to Hide")
    if st.button("Send Email"):
        if recipient and attach_file and secret_message:
            try:
                verification_code = generate_verification_code()
                hidden_message = f"{secret_message}\n\nVERIFICATION CODE: {verification_code}"
                stego_img_buffer = hide_text_in_image(attach_file, hidden_message)
                msg = EmailMessage()
                msg['Subject'] = "No Subject"
                msg['From'] = SENDER_EMAIL
                msg['To'] = recipient
                msg.set_content(f"Verification Code: {verification_code}")
                stego_img_buffer.seek(0)
                msg.add_attachment(
                    stego_img_buffer.read(),
                    maintype='image',
                    subtype='png',
                    filename=attach_file.name
                )
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                    smtp.send_message(msg)
                st.success(f"✅ Email sent with verification code: {verification_code}")
                stego_img_buffer.seek(0)
                st.download_button("📥 Download Stego Image", stego_img_buffer, file_name="stego_image.png", mime="image/png")
            except Exception as e:
                st.error(f"Failed to send email: {e}")
        else:
            st.error("Fill all fields and upload an image.")


    st.markdown("---")
    st.header("📥 Receive and Extract Verification Code and Message")
    received_img = st.file_uploader("Upload Stego Image", type=['png'], key="received_img")
    entered_code = st.text_input("Enter Verification Code", key="entered_code")
    if st.button("Extract Message"):
        if received_img and entered_code:
            success, hidden_message = reveal_text_from_image(received_img)
            if success:
                if entered_code in hidden_message:
                    st.success("✅ Code matched!")
                    message = hidden_message.rsplit('\nVERIFICATION CODE:', 1)[0].strip()
                    st.subheader("🔓 Secret Message:")
                    st.code(message)
                else:
                    st.error("❌ Code mismatch!")
                    st.code(hidden_message)
            else:
                st.error(hidden_message)
        else:
            st.error("Please upload image and enter code.")

# --- Audio Steganography ---
with tabs[3]:
    st.header("🔊 Hide Text in Audio")
    audio_file = st.file_uploader("Upload WAV Audio File", type=['wav'], key="audio_hide")
    secret_text_audio = st.text_area("Enter Secret Message to Hide")
    if st.button("Hide Text in Audio"):
        if audio_file and secret_text_audio:
            stego_audio_buffer, message = hide_text_in_audio(audio_file, secret_text_audio)
            if stego_audio_buffer:
                st.success(message)
                st.download_button("📥 Download Audio", stego_audio_buffer, file_name="hidden_audio.wav", mime="audio/wav")
            else:
                st.error(message)
        else:
            st.error("Upload WAV file and enter message.")

    st.markdown("---")
    st.header("🔎 Reveal Text from Audio")
    stego_audio = st.file_uploader("Upload Stego Audio", type=['wav'], key="audio_reveal")
    if st.button("Reveal Text from Audio"):
        if stego_audio:
            success, result = reveal_text_from_audio(stego_audio)
            if success:
                st.success("✅ Message Revealed:")
                st.code(result)
            else:
                st.error(result)
        else:
            st.error("Upload WAV audio file.")
