import streamlit as st
from PIL import Image, ImageOps
import base64
from io import BytesIO

# Set page title and layout
st.set_page_config(
    page_title="PW Poster Generator",
    layout="wide",
    page_icon="pw.jpg"
)

# Load Poppins font from Google Fonts
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

# Function to set the background color and custom styles
def set_background_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1c1e21;
            padding-top: 20px;
            font-family: 'Poppins', sans-serif;
            color: white;
        }

        .stMarkdown, .stButton > button {
            color: white;
            font-family: 'Poppins', sans-serif;
        }

        .upload-section {
            background-color: #2b2d31;
            border: 2px dashed #4a4a4a;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
        }

        .stFileUploader label {
            background-color: #3a3b3d;
            padding: 10px 20px;
            border-radius: 5px;
            border: 1px solid #4a4a4a;
            font-size: 16px;
            cursor: pointer;
        }

        .save-button button {
            background-color: #007bff !important;
            color: white !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            width: 100%;
            padding: 10px;
        }

        .poster-image {
            height: 300px; 
            object-fit: contain;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Call the function to set styles
set_background_style()

# Load the poster template
poster_template_path = "template.jpg"
poster_template = Image.open(poster_template_path)

# Load the cloud image
cloud_image_path = "cloud2.png"
cloud_image = Image.open(cloud_image_path)

# Section: Event Poster and Details
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### The Great Commission Gathering")
    st.subheader("Personalize your Poster")
    st.write("Make this poster your own by adding an image.")
    st.write("Nov 23, 10:00 AM")

# Placeholder for the final poster preview
poster_placeholder = col2.empty()

# Function to resize image to fit within a target area
def resize_image(image, target_width, target_height):
    """
    Resize the uploaded image to fit within the target dimensions while maximizing its size.
    """
    # Determine the scale factor to fit within target dimensions
    width_ratio = target_width / image.width
    height_ratio = target_height / image.height
    scale_factor = min(width_ratio, height_ratio)

    # Calculate new dimensions
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)

    # Resize the image while maintaining aspect ratio
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Create a blank canvas with target dimensions
    new_image = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))

    # Calculate centering offsets
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2

    # Paste resized image onto the blank canvas
    new_image.paste(resized_image, (offset_x, offset_y), resized_image.convert("RGBA"))

    return new_image

# Section: Upload Image
uploaded_file = st.file_uploader("Add a photo that represents you or your brand. Images should be high resolution for best results.", type=["jpg", "jpeg", "png"])

# Check if an image has been uploaded
if uploaded_file:
    # Open and process the uploaded image
    user_photo = Image.open(uploaded_file)

    # Resize user image to fit within the space on the poster
    target_width, target_height = 550, 550  # Larger width and height
    resized_photo = resize_image(user_photo, target_width, target_height)

    # Resize the cloud image
    cloud_width, cloud_height = 950, 420
    resized_cloud = cloud_image.resize((cloud_width, cloud_height))

    # Combine user image with the poster template
    final_poster = poster_template.copy()

    # Place the user image
    position = (120, 140)  # Adjust the position as needed
    final_poster.paste(resized_photo, position, resized_photo.convert('RGBA'))

    # Place the cloud image
    cloud_position = (-100, 280)  # Position of the cloud
    final_poster.paste(resized_cloud, cloud_position, resized_cloud.convert('RGBA'))

    # Save the final poster
    buffered = BytesIO()
    final_poster.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Display the final poster preview
    poster_placeholder.markdown(
        f'<img class="poster-image" src="data:image/png;base64,{img_str}" alt="Customized Poster">',
        unsafe_allow_html=True,
    )

    # Display the "Save Poster" download button
    st.markdown('<div class="save-button">', unsafe_allow_html=True)
    st.download_button(
        label="Save Poster",
        data=buffered,
        file_name="final_poster.png",
        mime="image/png",
    )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Display the template if no image is uploaded
    poster_placeholder.markdown(
        f'<img class="poster-image" src="data:image/jpg;base64,{base64.b64encode(open(poster_template_path, "rb").read()).decode()}" alt="Event Poster">',
        unsafe_allow_html=True,
    )