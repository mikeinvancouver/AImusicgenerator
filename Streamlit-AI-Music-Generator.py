import time
import requests
import streamlit as st

# Replace with your Vercel domain or localhost
base_url = 'http://localhost:3000'

# Functions for interacting with the API
def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()

def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()

def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()

def get_clip(clip_id):
    url = f"{base_url}/api/clip?id={clip_id}"
    response = requests.get(url)
    return response.json()

def generate_whole_song(clip_id):
    payload = {"clip_id": clip_id}
    url = f"{base_url}/api/concat"
    response = requests.post(url, json=payload)
    return response.json()

# Streamlit App
def main():
    st.title("AI Music Generator")
    st.write("Generate music based on your input text and style preferences.")

    # User inputs
    prompt = st.text_input("Enter the prompt for the song:", value="")
    make_instrumental = st.checkbox("Make instrumental", value=False)
    wait_audio = st.checkbox("Wait for audio completion", value=False)

    if st.button("Generate Song"):
        with st.spinner("Generating music..."):
            # Call the API to generate audio
            payload = {
                "prompt": prompt,
                "make_instrumental": make_instrumental,
                "wait_audio": wait_audio
            }
            data = generate_audio_by_prompt(payload)

            if data and "id" in data[0]:
                ids = f"{data[0]['id']},{data[1]['id']}" if len(data) > 1 else data[0]['id']
                st.success(f"Generated audio IDs: {ids}")
                st.write("Retrieving audio information...")
                
                # Wait and retrieve audio information
                for _ in range(60):
                    audio_data = get_audio_information(ids)
                    if audio_data[0]["status"] == 'streaming':
                        st.audio(audio_data[0]["audio_url"], format="audio/mp3")
                        if len(audio_data) > 1:
                            st.audio(audio_data[1]["audio_url"], format="audio/mp3")
                        break
                    time.sleep(5)
            else:
                st.error("Failed to generate music. Please try again.")

if __name__ == "__main__":
    main()
