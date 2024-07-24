import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import time

# Function to load images from a local directory
def load_image(image_path):
    return Image.open(image_path)

# Predefined meme templates in the img folder
img_folder = "img"
trending_templates = [os.path.join(img_folder, img) for img in ["grumpy cat.jpg", "awkward penguin.jpg", "philosoraptor.jpg",]]
favorites_templates = [os.path.join(img_folder, img) for img in ["bernie.jpg", "success kid.jpg"]]
search_templates = [os.path.join(img_folder, img) for img in ["search/Advice-Dog.jpg", "search/bad-advice-cat.jpg"]]

ai_magic = {
    'img\\bernie.jpg': ['I am once again asking','for you to vote'],
    'img\\grumpy cat.jpg': ['There are two political parties','and they are both bad'],
    'img\\awkward penguin.jpg': ['Mailed in my ballot','On November 6th'],
    'img\\philosoraptor.jpg': ['If voting is right','Why does it feel so wrong this year'],
    'img\\success kid.jpg': ['First time voting','Picked the winner'],
    'img\\search/Advice-Dog.jpg': ['Don\'t forget your','mail in ballot!'],
    'img\\search/bad-advice-cat.jpg': ['Wait till the last minute','Before reading about the candidates'],
}

# Main function
def main():
    st.title("Meme Maker")

    # initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'template' not in st.session_state:
        st.session_state.template = ""
    if 'mode' not in st.session_state:
        st.session_state.mode = "trending"
    if 'top_text' not in st.session_state:
        st.session_state.top_text = ""
    if 'bottom_text' not in st.session_state:
        st.session_state.bottom_text = ""
    if 'vibe' not in st.session_state:
        st.session_state.vibe = ""
    if 'searched' not in st.session_state:
        st.session_state.searched = 0


    col1, col2 = st.columns([.6,.4])

    if st.session_state.step == 5:
        exploded_view()
    elif st.session_state.step == 6:
        collab_base()
    else:
        with col1:
            st.image('img/slide.png', use_column_width='auto')

        with col2:
            meme_maker(st.session_state.step)

# meme maker
def meme_maker(step):
    if step == 0:
        view_select()
    if step == 1:
        meme_tempaltes()
    if step == 2:
        meme_editing()
    if step == 3:
        generate_meme_view()
    if step == 4:
        vibe_search()

def view_select():
    option = st.selectbox(label='Select Mode',
        options=['Template Search','Vibe', 'Collaboration'])
    if st.button('Go', type='primary'):
        if option == 'Template Search':
            st.session_state.step = 1
        elif option == 'Vibe':
            st.session_state.step = 4
        else:
            st.session_state.step = 6
        st.rerun()

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
    
    # Search your own
    results = search_templates
    st.subheader("Search")
    col60, col61 = st.columns([.7,.3])
    with col60:
        search_query = st.text_input(label='Template search', value='advice')

    with col61:
        st.write(' ')
        if st.button('Go', type='primary'):
            if search_query == 'advice':
                st.session_state.searched = 1
        
    if st.session_state.searched == 1:
        for result in results:
            st.image(result, use_column_width=True)
            if st.button(os.path.basename(result), key=result):
                st.session_state.template = result
                st.session_state.step = 2
                st.session_state.mode = "search"
                st.write(st.session_state.template )
                st.session_state.searched = 0
                st.rerun()
        else:
            st.write('No results')

    if st.button('Back'):
        st.session_state.step = 0
        st.session_state.searched = 0
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
        st.session_state.top_text = ''
        st.session_state.bottom_text = ''
        st.rerun()


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
            st.toast("Meme published!")
            st.balloons()
            st.session_state.tempalte = ''
            st.session_state.step = 0
            time.sleep(1.5)
            st.rerun()
            
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

def vibe_search():
    st.header('Search by Vibe')

    with st.form(key='vibe_search'):
        vibe_input = st.text_input(label='Vibe', value='exciting', placeholder='sad')
        submit_button = st.form_submit_button(label='Search', type='primary')
    
        if submit_button:
            if len(vibe_input) < 1:
                st.toast('Please input text')
            else:
                st.session_state.vibe = vibe_input
                st.rerun()
    
    if st.session_state.vibe == 'exciting':
        memes = ['img/vibe/exciting/exciting1.jpg',
        'img/vibe/exciting/exciting2.jpg',
        'img/vibe/exciting/exciting3.jpg']
    elif st.session_state.vibe == 'sad':
        memes = ['img/vibe/sad/sad1.jpg',
        'img/vibe/sad/sad2.jpg',
        'img/vibe/sad/sad3.jpg']
    else:
        memes = []
        
    if len(memes) > 0:
        for meme in memes:
            st.image(meme, use_column_width=True)
            if st.button(os.path.basename(meme), key=meme):
                st.session_state.template = meme
                st.session_state.step = 5
                st.rerun()
            st.write('')
    else:
        if len(st.session_state.vibe)>0: 
            st.write('No results found')
    
    if st.button('Back'):
        if len(st.session_state.vibe) > 0:
            st.session_state.step = 4
            st.session_state.vibe = ''
            st.rerun()
        else:
            st.session_state.step = 0
        st.rerun()

def exploded_view():
    st.header('Preview')
    st.image(st.session_state.template, use_column_width=True)
    col20, col21 = st.columns([.1,.9])
    with col20:
        if st.button('Back'):
            st.session_state.step = 4
            st.rerun()
    with col21:
        if st.button('Publish', type='primary'):
            st.toast('Meme published!')
            st.balloons()
            st.session_state.template = ''
            st.session_state.step=0
            time.sleep(1.5)
            st.rerun()

def collab_base():
    st.header('Team Collaboration')
    col30, col31 = st.columns([.7,.3])

    with col30:
        if len(st.session_state.template) > 0:
            st.image(st.session_state.template, use_column_width=True)
        else:
            st.image('img/slide2.png', use_column_width='auto')
    
    with col31:
        votes1 = [6,0,0,2]
        votes2 = [0,3,3,1]
        votes3 = [1,1,0,0]
        if len(st.session_state.template) > 0:
            display_comments(votes1, votes2, votes3)
        else:
            display_collab_memes(votes1, votes2, votes3)

def display_collab_memes(votes1, votes2, votes3):
    memes = ['img/collab/collab1.jpg',
    'img/collab/collab2.jpg',
    'img/collab/collab3.jpg',
    ]

    for meme in memes:
        if meme == 'img/collab/collab1.jpg':
            votes(votes1[0],votes1[1],votes1[2],votes1[3])
        elif meme == 'img/collab/collab2.jpg':
            votes(votes2[0],votes2[1],votes2[2],votes2[3])
        elif meme == 'img/collab/collab3.jpg':
            votes(votes3[0],votes3[1],votes3[2],votes3[3])
        
        st.image(meme, use_column_width=True)
        if st.button(os.path.basename(meme), key=meme):
            st.session_state.template = meme
            st.rerun()
        st.write('')
    
    if st.button('Back'):
        st.session_state.step = 0
        st.rerun()

def display_comments(votes1, votes2, votes3):
    if st.session_state.template == 'img/collab/collab1.jpg':
        votes(votes1[0],votes1[1],votes1[2],votes1[3])
        comment('Jim', 'good choice!', '👍')
        comment('Dwight', 'This is exactly the kind of strategic thinking we need. Use it.', '👍')
    elif st.session_state.template == 'img/collab/collab2.jpg':
        votes(votes2[0],votes2[1],votes2[2],votes2[3])
        comment('Toby', 'While this meme is clever, it might come across as unprofessional to some.', '😩')
    else:
        votes(votes3[0],votes3[1],votes3[2],votes3[3])
        st.write('No comments')

    col40, col41 = st.columns([.4,.6])
    with col40:
        if st.button('Back'):
            st.session_state.template  = ''
            st.rerun()
    with col41:
        if st.button('Publish',type='primary'):
            st.toast('Meme published!')
            st.balloons()
            st.session_state.template  = ''
            st.session_state.step = 0
            time.sleep(1.5)
            st.rerun()

def comment(username, body, icon):
    with st.expander(label=username, expanded=True, icon=icon):
        st.write(body)

def votes(num_thumbs_up, num_thumbs_down,num_sad, num_comments):
    a, b, c, d = st.columns(4)

    with a:
        st.write(num_thumbs_up)
        st.write('👍')

    with b:
        st.write(num_thumbs_down)
        st.write('👎')

    with c:
        st.write(num_sad)
        st.write('😩')
    
    with d:
        st.write(num_comments)
        st.write('💬')

if __name__ == "__main__":
    main()