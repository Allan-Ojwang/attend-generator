import streamlit as st
from PIL import Image
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

# Function to set background and styles
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
        .save-button button {
            background-color: #007bff !important;
            color: white !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            width: 100%;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Call function to set styles
set_background_style()

# Load assets
poster_template_path = "template.jpg"
cloud_image_path = "cloud2.png"
overlay_image_path = "overlay.png"

poster_template = Image.open(poster_template_path).convert("RGBA")
cloud_image = Image.open(cloud_image_path).convert("RGBA")
overlay_image = Image.open(overlay_image_path).convert("RGBA")

# Section: Event Poster Details
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### The Great Commission Gathering")
    st.subheader("Personalize your Poster")
    st.write("Make this poster your own by adding an image.")
    st.write("Nov 23, 10:00 AM")

# Placeholder for poster preview
poster_placeholder = col2.empty()

# Function to resize image to fit within a target area
def resize_image(image, target_width, target_height):
    """
    Resize the uploaded image to fit within the target dimensions while maximizing size.
    """
    width_ratio = target_width / image.width
    height_ratio = target_height / image.height
    scale_factor = min(width_ratio, height_ratio)
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Center the resized image on a blank canvas
    canvas = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2
    canvas.paste(resized_image, (offset_x, offset_y), resized_image)
    return canvas

# Section: Upload Image
uploaded_file = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

# Check if an image has been uploaded
if uploaded_file:
    user_photo = Image.open(uploaded_file).convert("RGBA")

    # Resize the uploaded image
    target_width, target_height = poster_template.width, poster_template.height
    resized_photo = resize_image(user_photo, target_width, target_height)

    # Resize cloud and overlay images to match the template
    resized_cloud = cloud_image.resize(poster_template.size, Image.LANCZOS)
    resized_overlay = overlay_image.resize(poster_template.size, Image.LANCZOS)

    # Combine layers
    final_poster = poster_template.copy()
    final_poster.paste(resized_photo, (0, 0), resized_photo)
    final_poster.paste(resized_cloud, (0, 0), resized_cloud)
    final_poster.paste(resized_overlay, (0, 0), resized_overlay)

    # Save the final image to a buffer
    buffered = BytesIO()
    final_poster.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Display the poster preview
    poster_placeholder.markdown(
        f'<img src="data:image/png;base64,{img_str}" alt="Customized Poster" style="width:100%;border-radius:8px;">',
        unsafe_allow_html=True,
    )

    # Save poster button
    st.markdown('<div class="save-button">', unsafe_allow_html=True)
    st.download_button(
        label="Save Poster",
        data=buffered,
        file_name="final_poster.png",
        mime="image/png",
    )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Display the template if no image has been uploaded
    poster_placeholder.markdown(
        f'<img src="data:image/png;base64,{base64.b64encode(open(poster_template_path, "rb").read()).decode()}" alt="Poster Template" style="width:100%;border-radius:8px;">',
        unsafe_allow_html=True,
    )