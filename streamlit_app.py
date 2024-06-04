import streamlit as st
import requests
from PIL import Image
import cv2
import io


st.markdown(
    '# Poker Assistant'
    )

balloons_button= st.button('Balloons')
if balloons_button:
    st.balloons()


# Define the FastAPI endpoint
API_URL = "http://127.0.0.1:8000/predict"

def get_prediction(files):
    files_to_upload = [("files", (file.name, file.getvalue(), file.type)) for file in files]
    try:
        response = requests.post(API_URL, files=files_to_upload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        st.error("Failed to decode JSON response.")
        return None

st.title("Image Prediction App")

# File uploader
uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    # Display uploaded images
    st.image([Image.open(file) for file in uploaded_files], width=200)

    # Predict button
    if st.button("Get Predictions"):
        with st.spinner("Sending images to the model..."):
            predictions = get_prediction(uploaded_files)
            if predictions:
                st.success("Predictions received!")

                # Display the results and confirmation buttons
                results = predictions.get("results", [])
                feedback = {}
                for i, (file, result) in enumerate(zip(uploaded_files, results)):
                    st.image(Image.open(file), width=200)
                    st.markdown(f"**Prediction:** {result}")

                    # Add buttons for feedback
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Correct {i+1}"):
                            feedback[file.name] = "Correct"
                    with col2:
                        if st.button(f"Incorrect {i+1}"):
                            feedback[file.name] = "Incorrect"

                # Display feedback results
                st.write("Feedback results:")
                for image_name, feedback_result in feedback.items():
                    st.write(f"{image_name}: {feedback_result}")


if st.checkbox('Show content'):
    # Display a camera input widget
    image = st.camera_input("Take a picture")
    # If the user takes a picture, display the image
    if image:
        # Convert the image to OpenCV format
        image_cv = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the image using OpenCV
        cv2.imshow("Image", image_cv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
