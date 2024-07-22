import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import time

# Function to load images from a local directory
def load_image(image_path):
    return Image.open(image_path)

# Predefined meme templates in the img folder
img_folder = "img"
trending_templates = [os.path.join(img_folder, img) for img in ["bernie.jpg", "grumpy cat.jpg", "awkward penguin.jpg"]]
favorites_templates = [os.path.join(img_folder, img) for img in ["philosoraptor.jpg", "success kid.jpg"]]

ai_magic = {
    'img\\bernie.jpg': ['I am once again asking','for you to vote'],
    'img\\grumpy cat.jpg': ['There are two political parties','and they are both bad'],
    'img\\awkward penguin.jpg': ['Mailed in my ballot','On November 6th'],
    'img\\philosoraptor.jpg': ['If voting is right','Why does it feel so wrong this year'],
    'img\\success kid.jpg': ['First time voting','Picked the winner'],
}

# Main function
def main():
    st.title("Meme Maker")

    # initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'template' not in st.session_state:
        st.session_state.template = ""
    if 'mode' not in st.session_state:
        st.session_state.template = "trending"
    if 'top_text' not in st.session_state:
        st.session_state.top_text = ""
    if 'bottom_text' not in st.session_state:
        st.session_state.bottom_text = ""


    col1, col2 = st.columns([.6,.4])

    with col1:
        st.image('img/slide.png', use_column_width='auto')

    with col2:
        meme_maker(st.session_state.step)

# meme maker
def meme_maker(step):
    if step == 1:
        meme_tempaltes()
    if step == 2:
        meme_editing()
    if step == 3:
        generate_meme_view()

def meme_tempaltes():
    st.header("Select Template")

    # Display Trending Templates
    st.subheader("Trending Templates")
        
    for template in trending_templates:
        st.image(template, use_column_width=True)
        if st.button(os.path.basename(template), key=template):
            st.session_state.template = template
            st.session_state.step = 2
            st.session_state.mode = "trending"
            st.rerun()
        st.write('')
            
    # Display Favorites Templates
    st.subheader("AI suggested")
    for template in favorites_templates:
        st.image(template, use_column_width=True)
        if st.button(os.path.basename(template), key=template):
            st.session_state.template = template
            st.session_state.step = 2
            st.session_state.mode = "context"
            st.rerun()

def meme_editing():
    st.header("Edit Your Meme Text")
    st.image(st.session_state.template, use_column_width=True)

    # placeholder
    if st.session_state.mode == "context":
        top_text, bottom_text = get_ai_magic()
    else:
        top_text = st.session_state.top_text
        bottom_text = st.session_state.bottom_text
    set_text(top_text, bottom_text)
    
    if st.button('AI help', type='primary'):
        with st.spinner():
            top_text, bottom_text = get_ai_magic()
            set_text(top_text, bottom_text)
            time.sleep(1)
    
    with st.form(key='form'):
        form_top_text = st.text_input("Top Text", value=st.session_state.top_text, )
        form_bottom_text = st.text_input("Bottom Text", value=st.session_state.bottom_text)

        col10, col11 = st.columns(2)

        with col11:
            submit_button = st.form_submit_button("Generate", type='primary')
                
        if submit_button:
                if len(form_top_text) < 1 or len(form_bottom_text) < 1:
                    st.toast('Please input text')
                else:
                    set_text(form_top_text, form_bottom_text)
                    st.session_state.step = 3
                    st.rerun()

    if st.button("Back"):
        st.session_state.step = 1
        st.experimental_rerun()


def set_text(top_text, bottom_text):
    st.session_state.top_text = top_text
    st.session_state.bottom_text = bottom_text

def get_ai_magic():
    top_text = ai_magic[st.session_state.template][0]
    bottom_text = ai_magic[st.session_state.template][1]
    return top_text, bottom_text

def generate_meme_view():
    st.header("Your Meme")

    meme_image = generate_meme(st.session_state.template, st.session_state.top_text, st.session_state.bottom_text)
    st.image(meme_image)

    col10, col11 = st.columns(2)
    with col10:
        if st.button("Edit Text"):
            st.session_state.step = 2
            st.experimental_rerun()

    with col11:
        if st.button("Publish", type='primary'):
            st.success("Meme Published!")

# Function to generate meme with text
from PIL import Image, ImageDraw, ImageFont

def load_image(template_path):
    return Image.open(template_path)

def generate_meme(template_path, top_text, bottom_text):
    image = load_image(template_path)
    draw = ImageDraw.Draw(image)
    font_path = "arial.ttf"  # Update this path to your font file if necessary

    # Convert text to all caps
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # Function to dynamically scale and center text with outline
    def draw_text_centered(draw, text, position, image_width, font, max_width, outline_color="black", fill_color="white"):
        # Calculate the text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # If the text is too wide, scale it down
        while text_width > max_width:
            font_size = font.size - 1
            if font_size <= 0:
                break  # Prevent infinite loop if the text is too long
            font = ImageFont.truetype(font_path, font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Calculate the centered position
        x = (image_width - text_width) / 2
        y = position

        # Draw outline by drawing text multiple times in offset positions
        offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]
        for offset in offsets:
            draw.text((x + offset[0], y + offset[1]), text, font=font, fill=outline_color)
        
        # Draw the main text
        draw.text((x, y), text, font=font, fill=fill_color)

    # Add top text
    image_width, image_height = image.size
    max_width = image_width - 20  # Padding from the image edges
    initial_font_size = 40  # Initial font size for scaling
    font = ImageFont.truetype(font_path, initial_font_size)
    draw_text_centered(draw, top_text, 10, image_width, font, max_width)

    # Add bottom text
    draw_text_centered(draw, bottom_text, image_height - 60, image_width, font, max_width)

    return image

#def generate_meme(template_path, top_text, bottom_text):
#    image = load_image(template_path)
#    draw = ImageDraw.Draw(image)
#    font = ImageFont.truetype("arial.ttf", 40)

#    # Add top text
#    draw.text((10, 10), top_text, font=font, fill="white")

    # Add bottom text
#    width, height = image.size
#    draw.text((10, height - 50), bottom_text, font=font, fill="white")

#    return image

if __name__ == "__main__":
    main()