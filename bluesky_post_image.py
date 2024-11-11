import requests
import json
from datetime import datetime, timezone
import os
import mimetypes  

# Replace with your Bluesky handle and app password
handle = 'your_name.bsky.social'
app_password = 'your app password'

# Bluesky API endpoints
pds_url = 'https://bsky.social'
session_endpoint = f'{pds_url}/xrpc/com.atproto.server.createSession'
post_endpoint = f'{pds_url}/xrpc/com.atproto.repo.createRecord'
upload_image_endpoint = f'{pds_url}/xrpc/com.atproto.repo.uploadBlob'


session = {}

# Function to create a session
def create_session():
    session_data = {
        'identifier': handle,
        'password': app_password
    }
    session_response = requests.post(session_endpoint, json=session_data)
    session_response.raise_for_status()
    global session
    session = session_response.json()
    print("Session created:", session)  

# Function to upload an image
def upload_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at path: {image_path}")
        return None

    # Determine the correct MIME type based on the file extension
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        print("Error: Could not determine the MIME type for the image.")
        return None

    with open(image_path, 'rb') as image_file:
        img_bytes = image_file.read()

    # Enforce the file size limit (1 MB)
    if len(img_bytes) > 1000000:
        print(f"Error: Image file size too large. 1000000 bytes maximum, got: {len(img_bytes)}")
        return None

    headers = {
        'Content-Type': mime_type,
        'Authorization': f"Bearer {session['accessJwt']}"
    }
    image_response = requests.post(upload_image_endpoint, headers=headers, data=img_bytes)
    print(f"Image upload response status code: {image_response.status_code}")  
    print(f"Image upload response content: {image_response.content}")  
    image_response.raise_for_status()
    
    return image_response.json()

# Function to create a post with optional image attachment
def create_post(content, image_path=None):
    post_data = {
        '$type': 'app.bsky.feed.post',
        'text': content,
        'createdAt': datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    # If an image path is provided, upload the image and add it to the post data
    if image_path:
        image_response = upload_image(image_path)
        if not image_response or 'blob' not in image_response:
            print("Error: Failed to retrieve blob from image upload response")
            return

        # Add image reference to the post data, as per documentation format
        post_data['embed'] = {
            '$type': 'app.bsky.embed.images',
            'images': [
                {
                    'image': image_response['blob'],  # Use the blob metadata as-is
                    'alt': 'An image attached to the post'
                }
            ]
        }

    record_data = {
        'repo': session['did'],
        'collection': 'app.bsky.feed.post',
        'record': post_data
    }
    headers = {
        'Authorization': f"Bearer {session['accessJwt']}"
    }

    post_response = requests.post(post_endpoint, headers=headers, json=record_data)
    print("Post request data:", record_data) 
    print("Post request response:", post_response.text) 
    post_response.raise_for_status()
    return post_response.json()

if __name__ == '__main__':
    try:
        
        create_session()
        post_content = input("Enter your post content: ")
        image_path = input("Enter the path to your image file (or leave blank to skip): ").strip()
        image_path = image_path if image_path else None 

        response = create_post(post_content, image_path)
        if response:
            print("Post successful!")
            print(json.dumps(response, indent=2))

    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", err)
    except Exception as e:
        print("An unexpected error occurred:", e)
