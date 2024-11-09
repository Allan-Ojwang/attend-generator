import streamlit as st
from PIL import Image, ImageDraw
import base64
from io import BytesIO

# Set page title and layout
st.set_page_config(
    page_title="PW Poster Generator",
    layout="wide",
    page_icon="pw.jpg"  # Option 3: Local file path to an icon image
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
            height: 300px; /* Set a specific height for the image */
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
poster_template_path = "poster_template.jpg"  # Update this with the path to your poster template
poster_template = Image.open(poster_template_path)

# Section: Event Poster and Details (Side-by-Side Layout)
col1, col2 = st.columns([1, 1.5])  # Set width ratios

with col1:
    st.markdown("### The Great Commission Gathering")
    st.subheader("Personalize your Poster")
    st.write("Make this poster your own by adding an image.")
    st.write("Nov 23, 10:00 AM")

# Placeholder for the final poster preview in col2
poster_placeholder = col2.empty()

# Section: Upload Image
uploaded_file = st.file_uploader("Add a photo that represents you or your brand. Images should be high resolution for best results.", type=["jpg", "jpeg", "png"])

# Helper function to crop an image to a circle
def crop_to_circle(image):
    # Resize the image to 450x450
    image = image.resize((445, 445))
    # Create a mask for the circular crop
    mask = Image.new("L", (445, 445), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 445, 445), fill=255)
    # Apply the mask to make the image circular
    result = Image.new("RGBA", (445, 445))
    result.paste(image, (0, 0), mask)
    return result

# Check if an image has been uploaded
if uploaded_file:
    # Open and process the uploaded image
    user_photo = Image.open(uploaded_file)

    # Crop the uploaded image to a circle with 450x450 dimensions
    circular_photo = crop_to_circle(user_photo)

    # Combine user image with the poster template
    final_poster = poster_template.copy()
    position = (329, 121)  # Adjust position as needed
    final_poster.paste(circular_photo, position, circular_photo)

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
