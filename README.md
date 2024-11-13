# Bluesky Terminal Poster

A simple terminal-based Python application that allows users to post text, images, @mentions, and alt text directly to Bluesky. If you want to read more about is, [this blog post](https://www.m365princess.com/blogs/bluesky-terminal-poster/) is for you.

## Requirements

- **Python** 3.7 or later
- A **Bluesky account**
- **Bluesky API** access, including:
  - A handle (e.g., `your_handle.bsky.social`)
  - An app-specific password

### Python Libraries

This application requires the following Python library, which can be installed using `pip`:

- `requests` (for handling HTTP requests)

## Features

- Post messages directly from the terminal to your Bluesky feed
@Mentions: Tag other Bluesky users directly in your posts by typing @username
- Image Attachments: Optionally attach images to your posts in formats such as JPEG or PNG (maximum 1 MB)
- Alt Text for Images: Provide alt text descriptions for images to improve accessibility

## Setup

1. Fork and clone the Repository
2. Install Dependencies

```bash
pip install requests
```

3. Set Up Your Bluesky API Access

Ensure you have the following information:

* Bluesky Handle: Your Bluesky username (e.g., your_handle.bsky.social).
* App-Specific Password: Generate this from your Bluesky account settings.

4. Run the Application

```
python bluesky_post_image.py
```

* When prompted, enter the content you wish to post
* @Mentions: You can mention other users by typing @username in your post content. The application will automatically resolve the @mention to the appropriate Bluesky identifier
* Image Attachments: If you wish to include an image, provide the path to the image file when prompted. The image must:
  * Be in a supported format (.jpeg, .png, etc.)
  * Be less than 1 MB in size
* Alt Text: If an image is attached, you’ll be prompted to enter an alt text description for accessibility
* Upon successful posting, a confirmation message will be displayed, including the response from the Bluesky API

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to Bluesky for their great API documentation.
