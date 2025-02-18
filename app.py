
api_key = 'AIzaSyBz8LdpmIqHNIwRNC4gBxEZ0OOglJR6oB4'                                          
import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

# Initialize session state
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "api_key_configured" not in st.session_state:
    st.session_state.api_key_configured = False

# Function to configure API
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)  # Correct API key setup
        st.session_state.api_key = api_key
        st.session_state.api_key_configured = True
        st.success("API key configured successfully!")
    except Exception as e:
        st.error(f"Error configuring API key: {str(e)}")

# Main app layout
st.title("Image Description with Google Gemini")

# Sidebar API key input
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API key:", type="password")
    if st.button("Configure API"):
        if api_key:
            initialize_gemini(api_key)
        else:
            st.error("Please enter an API key")

# Main content
if not st.session_state.api_key_configured:
    st.info("Please configure your API key in the sidebar to continue.")
else:
    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Open and display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Convert image to bytes
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format="PNG")  
            img_bytes = img_byte_array.getvalue()

            # Generate description button
            if st.button("Generate Description"):
                try:
                    with st.spinner("Analyzing image..."):  
                        model = genai.GenerativeModel("gemini-1.5-flash")

                        # Generate response with image bytes
                        response = model.generate_content(
                            [
                                "Describe this picture in detail, including:\n"
                                "- Landscape and setting\n"
                                "- Buildings and architecture\n"
                                "- Art style or aesthetic elements\n"
                                "- Any visible text or signs and their significance\n"
                                "- Overall mood or atmosphere",
                                {"mime_type": "image/png", "data": img_bytes}  # Correct way to pass image
                            ]
                        )
                        
                        # Display response
                        st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred while generating the description: {e}")

        except Exception as e:
            st.error(f"An error occurred while processing the uploaded image: {e}")

