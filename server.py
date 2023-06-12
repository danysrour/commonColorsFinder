import os
from flask import Flask, render_template, redirect, request, url_for, flash,abort
from flask_bootstrap import Bootstrap
from forms import UploadForm
from werkzeug.utils import secure_filename
import requests
from io import BytesIO
from PIL import Image
from collections import Counter
import imghdr

PORT = 5000

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


def get_common_colors(image_url, num_colors):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()

        # Check if the response contains valid image data
        image_format = imghdr.what(None, h=response.content)
        if image_format not in ['jpeg', 'png']:
            raise ValueError("Unsupported image format")

        # Open the image using Pillow
        image = Image.open(BytesIO(response.content))

        # Resize the image for faster processing
        image.thumbnail((200, 200))

        # Convert the image to RGB mode if it's not already
        image = image.convert('RGB')

        # Get the pixel data from the image
        pixels = list(image.getdata())

        # Count the occurrences of each color
        color_counts = Counter(pixels)

        # Get the most common colors
        most_common_colors = color_counts.most_common(num_colors)

        return most_common_colors
    except (requests.exceptions.RequestException, ValueError) as e:
        print("An error occurred:", str(e))
        return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png']


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadForm()

    if request.method == "POST":

        image_url = form.image_url.data
        image = form.image.data

        if image == "" and image_url == "":
            flash(message="Please provide either an image url or upload an image.")

        else:
            if image_url != "":

                num_colors = 5
                common_colors = get_common_colors(image_url, num_colors)
                if common_colors is not None:
                    flash(message="Most common colors from the image URL:")
                    for color, count in common_colors:
                        flash(f"Color: {color}, Count: {count}")


            if image != "":
                # Check if the 'image' field exists in the form

                file = request.files['image']

                # Check if the file has an allowed extension
                if file and allowed_file(file.filename):
                    # Secure the filename to prevent any path traversal
                    filename = secure_filename(file.filename)

                    # Save the file to the upload folder
                    file_path = os.path.join("static/UPLOAD_FOLDER/", filename)
                    file.save(file_path)

                    full_url = f"http://127.0.0.1:{PORT}/{file_path}"

                    num_colors = 5
                    common_colors = get_common_colors(full_url, num_colors)
                    if common_colors is not None:
                        flash(message="Most common colors in the uploaded image:")
                        for color, count in common_colors:
                            flash(f"Color: {color}, Count: {count}")


    return render_template("home.html", form=form)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, port=PORT)
