from flask import Flask, request, send_file
from html2image import Html2Image
from io import BytesIO
import os

app = Flask(__name__)


def calculate_percentage(x, y):
    """
    Calculate the percentage based on the given x and y values.

    :param x: Numerator (completed progress)
    :param y: Denominator (total progress)
    :return: Percentage of progress as a float
    """
    if y > 0:
        return (x / y) * 100
    return 0


def create_html_content(label, x, y, percentage, color, width, height, fontsize, font_name):
    """
    Generate the HTML content for the progress bar image.

    :param label: The label text above the progress bar
    :param x: Completed progress
    :param y: Total progress
    :param percentage: Percentage of progress
    :param color: Progress bar color
    :param width: Width of the progress bar
    :param height: Height of the progress bar
    :param fontsize: Font size for the text
    :param font_name: Font name to be used in the HTML
    :return: HTML string for the progress bar
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family={font_name.replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: '{font_name}', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: transparent;
            }}
            .progress-container {{
                width: {width}px;
                position: relative;
            }}
            .progress-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
                font-size: {fontsize}px;
                color: #A9A9A9;
            }}
            .progress-bar {{
                position: relative;
                background-color: #3e3e3e;
                border-radius: 5px;
                overflow: hidden;
                height: {height}px;
            }}
            .progress-bar-inner {{
                background: linear-gradient(to right, {color}, #66bb6a);
                height: 100%;
                width: {percentage}%;
            }}
            .percentage-text {{
                position: absolute;
                right: 0;
                top: 50%;
                transform: translateY(-50%);
                font-size: {fontsize}px;
                font-weight: bold;
                color: white;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
                padding-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="progress-container">
            <div class="progress-header">
                <span style="font-weight: bold;">{label}</span>
                <span style="font-weight: bold;">{x}/{y}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-bar-inner"></div>
                <div class="percentage-text">{percentage:.1f}%</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def generate_image_from_html(html_content, width, height):
    """
    Convert the provided HTML string into a PNG image using Html2Image.

    :param html_content: The HTML content to be rendered as an image
    :param width: Width of the final image (including padding)
    :param height: Height of the final image
    :return: The path to the generated image file
    """
    hti = Html2Image(temp_path='./output', keep_temp_files=False)
    path = hti.screenshot(html_str=html_content, size=(
        width + 10, height + 50), save_as="progress.png")
    return path[0]


@app.route('/progress-bar', methods=['GET'])
def progress_bar():
    """
    Handle the /progress-bar endpoint, generate a progress bar image, and return it as a PNG file.

    The function extracts query parameters, calculates the percentage, generates HTML content,
    converts the HTML to an image, and sends the image as a response.
    """
    # Extract query parameters with defaults
    x = int(request.args.get('x', 0))
    y = int(request.args.get('y', 1))
    color = f"#{request.args.get('color', '4caf50')}"  # Default green color
    label = request.args.get('label', 'Progress')
    width = int(request.args.get('width', 400))
    height = int(request.args.get('height', 50))
    fontsize = int(request.args.get('fontsize', 16))
    font_name = request.args.get('font', 'Roboto')  # Default to Roboto font

    # Calculate percentage
    percentage = calculate_percentage(x, y)

    # Generate the HTML content
    html_content = create_html_content(
        label, x, y, percentage, color, width, height, fontsize, font_name)

    # Generate image from HTML content
    image_path = generate_image_from_html(html_content, width, height)

    # Open the image file and prepare it for sending
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()

    # Send the image as response
    response = send_file(BytesIO(img_data), mimetype='image/png')

    # Delete the generated image file after sending the response
    os.remove(image_path)

    return response


if __name__ == '__main__':
    # Use PORT environment variable or default to 8001 if not set
    port = int(os.environ.get("PORT", 8001))
    app.run(host="0.0.0.0", port=port)
