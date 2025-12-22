from PIL import Image
import traceback

def process_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        img_greyscale = img.convert("L")
        img_greyscale.save(output_path)
        return True
    except Exception as e:
        traceback.print_exc()
        return False
