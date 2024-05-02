from PIL import Image
from flask import Flask, render_template, request
import numpy as np
from sklearn.cluster import KMeans

# Extract dominant colors from image and convert them into hex-codes
def extract_dominant_colors(array, num_colors):
    # Reshape the 3D image array into a 2D array
    pixels = array.reshape(-1, 3)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the centroids of the clusters (representative colors)
    dominant_colors = kmeans.cluster_centers_

    # Convert centroids to hexadecimal format
    hex_colors = []
    for color in dominant_colors:
        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)
        hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
        hex_colors.append(hex_code)

    return hex_colors


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Ge image chosen by user and save it to static folder
        if "image_file" in request.files:
            image_file = request.files["image_file"]
            file_name = "static/uploaded_image.jpg"
            image_file.save(file_name)

            # Create nd-array from the image
            my_image = Image.open(file_name)
            image_array = np.array(my_image)

            # Extract 10 dominant colors from image array
            pixels = extract_dominant_colors(array=image_array, num_colors=10)
            return render_template("index.html", pixels=pixels, file_name=file_name)

    return render_template("index.html", pixels=None, file_name=None)


if __name__ == "__main__":
    app.run(debug=True)