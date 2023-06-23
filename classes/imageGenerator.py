from diffusers import DiffusionPipeline
from PIL.Image import Image


def generate(prompt):
    # Load the HF pipeline
    model = DiffusionPipeline.from_pretrained("prompthero/openjourney")

    # Generate an image from the prompt
    output_image: Image = model(prompt).images[0]

    # Save the image to a local file
    with open(r"C:\Users\t4iga\OneDrive\Documentos\GitHub\PROMET.EU\files\images\image.jpeg", "w") as f:
        output_image.save(f, format="JPEG")


generate("a hacker sitting in a chair in front of a monitor coding with shades of green in the background, in a darkened room, with some code jumping off the screen, mdjrny-v4 style")