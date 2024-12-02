import os
import tempfile
import streamlit as st
import ffmpeg

# Streamlit Web App
st.title("Video Metadata Removal Tool")

# File Upload
uploaded_file = st.file_uploader("Upload a Video File", type=["mp4", "mkv", "avi", "mov"])

if uploaded_file:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name

    # Output file path
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    # Process the video to remove metadata
    try:
        st.write("Processing video to remove metadata...")
        ffmpeg.input(input_path).output(output_path, map_metadata="-1").run()
        st.success("Metadata removed successfully!")

        # Allow user to download the new video
        with open(output_path, "rb") as file:
            st.download_button(
                label="Download Video",
                data=file,
                file_name="video_no_metadata.mp4",
                mime="video/mp4"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Clean up temporary files
    finally:
        os.remove(input_path)
        os.remove(output_path)
