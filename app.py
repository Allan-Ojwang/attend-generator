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
        /* Main app background color */
        .stApp {
            background-color: #1c1e21; /* Dark background */
            padding-top: 20px;
            font-family: 'Poppins', sans-serif;
            color: white;
        }
        
        /* Event poster container */
        .event-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #2b2d31;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        /* Text color */
        .stMarkdown, .stButton > button {
            color: white;
            font-family: 'Poppins', sans-serif;
        }

        /* Upload image section */
        .upload-section {
            background-color: #2b2d31;
            border: 2px dashed #4a4a4a;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
        }

        /* Upload button styling */
        .stFileUploader label {
            background-color: #3a3b3d;
            padding: 10px 20px;
            border-radius: 5px;
            border: 1px solid #4a4a4a;
            font-size: 16px;
            cursor: pointer;
        }

        /* Save poster button */
        .save-button button {
            background-color: #007bff !important;
            color: white !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            width: 100%;
            padding: 10px;
        }

        /* Custom height for the poster template image in col2 */
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
cloud_image_path = "cloud.png"
cloud_image = Image.open(cloud_image_path)

# Section: Event Poster and Details (Side-by-Side Layout)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### The Great Commission Gathering!!!")
    st.subheader("Personalize your Poster")
    st.write("Make this poster your own by adding an image.")
    st.write("Nov 23, 10:00 AM")

# Placeholder for the final poster preview in col2
poster_placeholder = col2.empty()

# Function to resize the uploaded image without cropping and to center it
def resize_image(image, target_width, target_height):
    # Ensure the image fits within the target dimensions without cropping
    image.thumbnail((target_width, target_height), Image.LANCZOS)

    # Create a new blank image with the target dimensions and transparent background
    new_image = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 0))

    # Calculate position to center the image
    offset_x = (target_width - image.width) // 2
    offset_y = (target_height - image.height) // 2

    # Paste the resized image onto the blank image, centered
    new_image.paste(image, (offset_x, offset_y), image.convert('RGBA'))

    return new_image

# Section: Upload Image
uploaded_file = st.file_uploader("Add a photo that represents you or your brand. Images should be high resolution for best results.", type=["jpg", "jpeg", "png"])

# Check if an image has been uploaded
if uploaded_file:
    # Open and process the uploaded image
    user_photo = Image.open(uploaded_file)

    # Resize user image to fit within a defined target area on the poster
    target_width, target_height = 450, 350  # Adjust based on the template's space for the image
    resized_photo = resize_image(user_photo, target_width, target_height)

    # Resize the cloud image
    cloud_width, cloud_height = 650, 320
    resized_cloud = cloud_image.resize((cloud_width, cloud_height))

    # Combine user image with the poster template
    final_poster = poster_template.copy()

    # Shift user image 10px to the left and place it
    position = (140 - 10, 140)  # Adjust the position to shift 10 pixels left
    final_poster.paste(resized_photo, position, resized_photo.convert('RGBA'))

    # Position the cloud image below the user image
    cloud_position = (position[0], position[1] + target_height)  # Place cloud below the uploaded image
    final_poster.paste(resized_cloud, cloud_position, resized_cloud.convert('RGBA'))

    # Save final poster to BytesIO for previewing and downloading
    buffered = BytesIO()
    final_poster.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Update the placeholder with the final preview image
    poster_placeholder.markdown(
        f'<img class="poster-image" src="data:image/png;base64,{img_str}" alt="Customized Poster">',
        unsafe_allow_html=True,
    )

    # Display the "Save Poster" download button below the poster
    st.markdown('<div class="save-button">', unsafe_allow_html=True)
    st.download_button(
        label="Save Poster",
        data=buffered,
        file_name="final_poster.png",
        mime="image/png",
    )
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Display the initial template if no image has been uploaded
    poster_placeholder.markdown(
        f'<img class="poster-image" src="data:image/jpg;base64,{base64.b64encode(open(poster_template_path, "rb").read()).decode()}" alt="Event Poster">',
        unsafe_allow_html=True,
    )