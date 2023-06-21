from diffusers import DiffusionPipeline
from PIL.Image import Image


def generate(prompt):
    # Load the HF pipeline
    model = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

    # Generate an image from the prompt
    output_image: Image = model(prompt).images[0]

    # Save the image to a local file
    with open(r"C:\Users\t4iga\OneDrive\Documentos\GitHub\PROMET.EU\files\images\image.jpeg", "w") as f:
        output_image.save(f, format="JPEG")