import tkinter as tk
from tkinter import filedialog, messagebox
import torch
from diffusers import I2VGenXLPipeline
from diffusers.utils import export_to_gif, load_image
from PIL import Image
import os

# Initialize the pipeline
pipeline = I2VGenXLPipeline.from_pretrained("ali-vilab/i2vgen-xl", torch_dtype=torch.float16, variant="fp16")
pipeline.enable_model_cpu_offload()

# Function to load image from local path
def load_local_image(image_path):
    return Image.open(image_path).convert("RGB")

# Function to create a video based on the image and prompt using the pipeline
def create_video(image_path, text, negative_text, output_folder):
    # Load the image from the local file
    image = load_local_image(image_path)

    # Set up the generator for reproducibility
    generator = torch.manual_seed(8888)

    # Generate frames using the provided pipeline
    frames = pipeline(
        prompt=text,
        image=image,
        num_inference_steps=50,
        negative_prompt=negative_text,
        guidance_scale=9.0,
        generator=generator
    ).frames[0]

    # Save the generated video as a GIF
    video_path = os.path.join(output_folder, "output_i2v.gif")
    export_to_gif(frames, video_path)
    
    return video_path

# Function to browse and select an image file
def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)

# Function to browse and select an output folder
def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)

# Function to handle the video creation
def generate_video():
    image_path = image_entry.get()
    text_prompt = text_entry.get()
    negative_prompt = negative_entry.get()
    output_folder = output_entry.get()
    
    if not image_path or not text_prompt or not output_folder:
        messagebox.showwarning("Input Error", "Please provide all inputs.")
        return

    try:
        video_path = create_video(image_path, text_prompt, negative_prompt, output_folder)
        messagebox.showinfo("Success", f"GIF created successfully at: {video_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
window = tk.Tk()
window.title("Image to Video (GIF) Generator")

# Create and place the widgets
tk.Label(window, text="Image Path:").grid(row=0, column=0, padx=5, pady=5)
image_entry = tk.Entry(window, width=50)
image_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(window, text="Browse", command=browse_image).grid(row=0, column=2, padx=5, pady=5)

tk.Label(window, text="Text Prompt:").grid(row=1, column=0, padx=5, pady=5)
text_entry = tk.Entry(window, width=50)
text_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(window, text="Negative Prompt:").grid(row=2, column=0, padx=5, pady=5)
negative_entry = tk.Entry(window, width=50)
negative_entry.grid(row=2, column=1, padx=5, pady=5)
negative_entry.insert(0, "Distorted, discontinuous, Ugly, blurry, low resolution, motionless, static, disfigured, disconnected limbs, Ugly faces, incomplete arms")

tk.Label(window, text="Output Folder:").grid(row=3, column=0, padx=5, pady=5)
output_entry = tk.Entry(window, width=50)
output_entry.grid(row=3, column=1, padx=5, pady=5)
tk.Button(window, text="Browse", command=browse_output_folder).grid(row=3, column=2, padx=5, pady=5)

tk.Button(window, text="Generate Video", command=generate_video).grid(row=4, column=1, pady=20)

# Run the main event loop
window.mainloop()
