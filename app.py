import gradio as gr
import easyocr
from gtts import gTTS
import tempfile
from PIL import Image

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# OCR Function using EasyOCR
def extract_text(image):
    results = reader.readtext(image)
    if results:
        text = " ".join([res[1] for res in results])
        return text
    else:
        return "No text detected."

# Convert text to speech
def text_to_speech(text):
    if text and text.strip() != "No text detected.":
        tts = gTTS(text)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        return temp_audio.name
    return None

# Main function for Gradio
def process_image(image):
    text = extract_text(image)
    audio_file = text_to_speech(text)
    return text, audio_file

# Gradio Interface
iface = gr.Interface(
    fn=process_image,
    inputs=gr.Image(type="filepath", label="Upload Image"),
    outputs=[gr.Textbox(label="Extracted Text"), gr.Audio(label="Audio Output")],
    title="Low-Vision Audio Reader",
    description="Upload an image with text (like a book page or menu). The app extracts the text and reads it aloud."
)

iface.launch()
