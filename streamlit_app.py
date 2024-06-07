import streamlit as st
import requests
from PIL import Image

st.set_page_config(
            page_title="Poker Assistant", # => Poker Assistant - Streamlit
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed



cards_list=[ 'ace of clubs',  'ace of diamonds',  'ace of hearts',  'ace of spades',
                    'eight of clubs',  'eight of diamonds',  'eight of hearts',  'eight of spades',
                    'five of clubs',  'five of diamonds',  'five of hearts',  'five of spades',
                    'four of clubs',  'four of diamonds',  'four of hearts',  'four of spades',
                    'jack of clubs',  'jack of diamonds',  'jack of hearts',  'jack of spades',
                     'king of clubs',  'king of diamonds',  'king of hearts',  'king of spades',
                     'nine of clubs',  'nine of diamonds',  'nine of hearts',  'nine of spades',
                     'queen of clubs',  'queen of diamonds',  'queen of hearts',  'queen of spades',
                     'seven of clubs',  'seven of diamonds',  'seven of hearts',  'seven of spades',
                     'six of clubs',  'six of diamonds',  'six of hearts',  'six of spades',
                    'ten of clubs',  'ten of diamonds',  'ten of hearts',  'ten of spades',
                     'three of clubs',  'three of diamonds',  'three of hearts', 'three of spades',
                    'two of clubs', 'two of diamonds',  'two of hearts', 'two of spades']

# Function to get suggestions based on user input
def print_list(list):
    for i in list:
        print(f'\n{i}')

def get_suggestions(input_text, suggestions_list):
    if input_text.lower() in suggestions_list and len(input_text)>1:
        return st.success('Thank you!')
    if input_text.lower() not in suggestions_list and len(input_text)>1:
        if len([s for s in suggestions_list if s.lower().startswith(input_text[:2].lower())]) ==0:
            st.error("Please follow this for format e.g 'nine of diamonds'")
        if len(input_text) >=2:
            return st.markdown(f"<span style='color:red;'>Did you mean:<br>- {'<br>- '.join([s for s in suggestions_list if s.lower().startswith(input_text[:-1].lower())])}</span>",unsafe_allow_html=True)
        if len(input_text) >=1:
            return st.markdown(f"<span style='color:red;'>Did you mean:<br>- {'<br>- '.join([s for s in suggestions_list if s.lower().startswith(input_text[:-1].lower())])}</span>",unsafe_allow_html=True)




st.title(
    'Poker Assistant'
    )


# Initialize session state variables for form inputs if they don't exist
if 'nbofplayer' not in st.session_state:
    st.session_state.nbofplayer = 0
if 'postion' not in st.session_state:
    st.session_state.position =0
if 'prefloppredictions' not in st.session_state:
    st.session_state.prefloppredictions = {}
if 'floppredictions' not in st.session_state:
    st.session_state.floppredictions = {}
if 'riverpredictions' not in st.session_state:
    st.session_state.riverpredictions = {}
if 'turnpredictions' not in st.session_state:
    st.session_state.turnpredictions = {}
if 'preflopdecision' not in st.session_state:
    st.session_state.preflopdecision = ''
if 'flopdecision' not in st.session_state:
    st.session_state.flopdecision = ''
if 'riverdecision' not in st.session_state:
    st.session_state.riverdecision = ''
if 'turndecision' not in st.session_state:
    st.session_state.turndecision = ''
if 'preflop1' not in st.session_state:
    st.session_state.preflop1 = ''
if 'preflop2' not in st.session_state:
    st.session_state.preflop2 = ''
if 'flop1' not in st.session_state:
    st.session_state.flop1 = ''
if 'flop2' not in st.session_state:
    st.session_state.flop2 = ''
if 'flop3' not in st.session_state:
    st.session_state.flop3 = ''
if 'turn' not in st.session_state:
    st.session_state.turn = ''
if 'river' not in st.session_state:
    st.session_state.river = ''
#
if 'preflop1_cor_inc' not in st.session_state:
    st.session_state.preflop1_cor_inc = ''
if 'preflop2_cor_inc' not in st.session_state:
    st.session_state.preflop2_cor_inc = ''
if 'flop1_cor_inc' not in st.session_state:
    st.session_state.flop1_cor_inc = ''
if 'flop2_cor_inc' not in st.session_state:
    st.session_state.flop2_cor_inc = ''
if 'flop3_cor_inc' not in st.session_state:
    st.session_state.flop3_cor_inc = ''
if 'turn_cor_inc' not in st.session_state:
    st.session_state.turn_cor_inc = ''
if 'river_cor_inc' not in st.session_state:
    st.session_state.river_cor_inc = ''
#
if 'preflop_recom' not in st.session_state:
    st.session_state.preflop_recom = ''
if 'flop_recom' not in st.session_state:
    st.session_state.flop_recom = ''
if 'turn_recom' not in st.session_state:
    st.session_state.turn_recom = ''
if 'river_recom' not in st.session_state:
    st.session_state.river_recom = ''



st.markdown('### Before we start I need some information')
st.session_state.nbofplayer = st.text_input("How many players are there?")
st.session_state.position = st.text_input("What is your position?")

# PREFLOP
st.markdown(
    '## Preflop'
    )

# Define the FastAPI endpoint

def get_prediction(files):
    API_URL = "https://final-docker-image-qscwgte56a-ew.a.run.app/predict"
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


def get_preflop(num_players, position_int, first_card, second_card, raised=False ):
    API_URL = "https://final-docker-image-qscwgte56a-ew.a.run.app/preflop"
    params = {
        'num_players' : num_players,
        'position_int': position_int,
        'raised': raised,
        'first_card': first_card,
        'second_card': second_card
    }

    try:
        response = requests.get(API_URL, params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        st.error("Failed to decode JSON response.")
        return None

def get_flop(num_players, position_int, first_card, second_card, first_board_card, second_board_card, third_board_card, raised=False ):
    #API_URL = "https://final-docker-image-qscwgte56a-ew.a.run.app/flop"
    '''params = {
        'num_players' : num_players,
        'position_int': position_int,
        'first_card': first_card,
        'second_card': second_card,
        'first_board_card' : first_board_card,
        'second_board_card': second_board_card,
        'third_board_card': third_board_card,
        'raised': raised
    }'''

    API_URL = f'https://final-docker-image-qscwgte56a-ew.a.run.app/flop?first_card={first_card}&second_card={second_card}&num_players={num_players}&position_int={position_int}&first_board_card={first_board_card}&second_board_card={second_board_card}&third_board_card={third_board_card}&raised={raised}'
    response = requests.post(API_URL)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle the error response
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return None


def get_turn(num_players, position_int, first_card, second_card, first_board_card, second_board_card, third_board_card, fourth_board_card, raised=False ):
    #API_URL = "https://final-docker-image-qscwgte56a-ew.a.run.app/turn"
    '''params = {
        'num_players' : num_players,
        'position_int': position_int,
        'first_card': first_card,
        'second_card': second_card,
        'first_board_card' : first_board_card,
        'second_board_card': second_board_card,
        'third_board_card': third_board_card,
        'fourth_board_card': fourth_board_card,
        'raised': raised
    }'''

    API_URL = f'https://final-docker-image-qscwgte56a-ew.a.run.app/turn?first_card={first_card}&second_card={second_card}&num_players={num_players}&position_int={position_int}&first_board_card={first_board_card}&second_board_card={second_board_card}&third_board_card={third_board_card}&fourth_board_card={fourth_board_card}&raised={raised}'
    response = requests.post(API_URL)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle the error response
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

def get_river(num_players, position_int, first_card, second_card, first_board_card, second_board_card, third_board_card, fourth_board_card, fifth_board_card, raised=False):
    #API_URL = "https://final-docker-image-qscwgte56a-ew.a.run.app/river"
    '''params = {
        'num_players': num_players,
        'position_int': position_int,
        'raised': raised,
        'first_card': first_card,
        'second_card': second_card,
        'first_board_card': first_board_card,
        'second_board_card': second_board_card,
        'third_board_card': third_board_card,
        'fourth_board_card': fourth_board_card,
        'fifth_board_card': fifth_board_card
    }'''
    API_URL = f'https://final-docker-image-qscwgte56a-ew.a.run.app/river?first_card={first_card}&second_card={second_card}&num_players={num_players}&position_int={position_int}&first_board_card={first_board_card}&second_board_card={second_board_card}&third_board_card={third_board_card}&fourth_board_card={fourth_board_card}&fifth_board_card={fifth_board_card}&raised={raised}'
    response = requests.post(API_URL)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle the error response
        print(f"Error: {response.status_code}")
        print(f"Response content: {response.text}")
        return None

# File uploader
uploaded_files_1 = st.file_uploader("Upload your two cards", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="upload1")
if uploaded_files_1:
    # Display uploaded images
    #st.image([Image.open(file) for file in uploaded_files], width=200)

    # Predict button
    if st.button("Get Preflop Predictions"):
        with st.spinner("Sending images to the model..."):
            predictions = get_prediction(uploaded_files_1)
            st.session_state.prefloppredictions = predictions

if len(st.session_state.prefloppredictions)>0 :
    predictions = st.session_state.prefloppredictions
    st.success("Predictions received!")
    results = predictions.get("results", [])
    feedback = {}

    col1, col2 = st.columns(2)
    with col1:
            st.image(Image.open(uploaded_files_1[0]), width=200)
            st.markdown(f"**Prediction:** {results[0][0]}")

            # Add buttons for feedback
            cor1, incor1 = st.columns(2)

            with cor1:
                button_cor1 = st.button("👍", key='pred1_correct')
                if button_cor1:
                    st.session_state.preflop1_cor_inc = 'correct'
                    st.session_state.preflop1 = results[0][0]

            with incor1:
                button_incor1 = st.button('👎', key='pred1_incorrect' )
                if button_incor1:
                    st.session_state.preflop1_cor_inc = 'incorrect'
            if st.session_state.preflop1_cor_inc == 'incorrect':
                preflop1_user_input = st.text_input('Enter the correct card',key='preflop1_inc_text')
                if len(preflop1_user_input)>1:
                    get_suggestions(preflop1_user_input,cards_list)
                if preflop1_user_input.lower() in cards_list:
                    st.session_state.preflop1 = preflop1_user_input.lower()
    with col2:
            st.image(Image.open(uploaded_files_1[1]), width=200)
            st.markdown(f"**Prediction:** {results[1][0]}")

            # Add buttons for feedback
            cor2, incor2 = st.columns(2)

            with cor2:
                button_cor2 = st.button("👍", key='pred2_correct')
                if button_cor2:
                    st.session_state.preflop2_cor_inc = 'correct'
                if st.session_state.preflop2_cor_inc == 'correct':
                    st.session_state.preflop2 = results[1][0]

            with incor2:
                button_incor2 = st.button('👎', key='pred2_incorrect')
                if button_incor2:
                    st.session_state.preflop2_cor_inc = 'incorrect'
            if st.session_state.preflop2_cor_inc == 'incorrect':
                preflop2_user_input = st.text_input('Enter the correct card',key='preflop2_inc_text')
                if len(preflop2_user_input)>1:
                    get_suggestions(preflop2_user_input,cards_list)
                if preflop2_user_input.lower() in cards_list:
                    st.session_state.preflop2 = preflop2_user_input.lower()

if st.session_state.preflop1 !='' and st.session_state.preflop2 != '':
    st.markdown(f'#### Your preflop hand is *{st.session_state.preflop1}* and *{st.session_state.preflop2}*')

    if st.button('🧞 Get Recommendation', key='preflop_reco'):
        with st.spinner("Calculating..."):
                preflop_reco = get_preflop(st.session_state.nbofplayer, st.session_state.position, st.session_state.preflop1, st.session_state.preflop2, raised=False )['message']
        st.session_state.preflop_recom = preflop_reco
    if st.session_state.preflop_recom:
        st.write(st.session_state.preflop_recom)


    #Continue or Follow
    # Create buttons with custom styles
    cont1, fold1 = st.columns(2)
    with cont1:
        preflop_continue_button = st.button('✅ Continue', key='prefol_continue_button')
        if preflop_continue_button:
            st.session_state.preflopdecision = 'Continue'
    with fold1:
        preflop_fold_button = st.button('❌ Fold', key='prefold_fold_button')
        if preflop_fold_button:
            st.session_state.preflopdecision = 'Fold'



# Flop
if st.session_state.preflopdecision == 'Continue':
    st.markdown(
        '## Flop'
        )

    # File uploader
    uploaded_files_2 = st.file_uploader("Upload 3 images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="upload2")
    if uploaded_files_2:
        # Display uploaded images
        #st.image([Image.open(file) for file in uploaded_files], width=200)

        # Predict button
        if st.button("Get Flop Predictions"):
            with st.spinner("Sending images to the model..."):
                predictions = get_prediction(uploaded_files_2)
                st.session_state.floppredictions = predictions

    if len(st.session_state.floppredictions)>0 :
        predictions = st.session_state.floppredictions
        st.success("Predictions received!")
        results = predictions.get("results", [])

        cola, colb, colc = st.columns(3)

        with cola:
                st.image(Image.open(uploaded_files_2[0]), width=200)
                st.markdown(f"**Prediction:** {results[0][0]}")

                # Add buttons for feedback
                cor3, incor3 = st.columns(2)
                with cor3:
                    button_cor3 = st.button("👍", key='pred3_correct')
                    if button_cor3:
                        st.session_state.flop1 = results[0][0]
                        st.session_state.flop1_cor_inc = 'correct'

                with incor3:
                    button_incor3 = st.button('👎', key='pred3_incorrect' )
                    if button_incor3:
                        st.session_state.flop1_cor_inc = 'incorrect'
                if st.session_state.flop1_cor_inc == 'incorrect':
                    flop1_user_input = st.text_input('Enter the correct card',key='flop1_inc_text')
                    if len(flop1_user_input)>1:
                        get_suggestions(flop1_user_input,cards_list)
                    if flop1_user_input.lower() in cards_list:
                        st.session_state.flop1 = flop1_user_input.lower()
        with colb:
                st.image(Image.open(uploaded_files_2[1]), width=200)
                st.markdown(f"**Prediction:** {results[1][0]}")

                # Add buttons for feedback
                cor4, incor4 = st.columns(2)

                with cor4:
                    button_cor4 = st.button("👍", key='pred4_correct')
                    if button_cor4:
                        st.session_state.flop2 = results[1][0]
                        st.session_state.flop2_cor_inc = 'correct'
                with incor4:
                    button_incor4 = st.button('👎', key='pred4_incorrect')
                    if button_incor4:
                        st.session_state.flop2_cor_inc = 'incorrect'
                if st.session_state.flop2_cor_inc == 'incorrect':
                    flop2_user_input = st.text_input('Enter the correct card',key='flop2_inc_text')
                    if len(flop2_user_input)>1:
                        get_suggestions(flop2_user_input,cards_list)
                    if flop2_user_input.lower() in cards_list:
                        st.session_state.flop2 = flop2_user_input.lower()
        with colc:
                st.image(Image.open(uploaded_files_2[2]), width=200)
                st.markdown(f"**Prediction:** {results[2][0]}")

                # Add buttons for feedback
                cor5, incor5 = st.columns(2)

                with cor5:
                    button_cor5 = st.button("👍", key='pred5_correct')
                    if button_cor5:
                        st.session_state.flop3 = results[2][0]
                        st.session_state.flop3_cor_inc = 'correct'
                with incor5:
                    button_incor5 = st.button('👎', key='pred5_incorrect')
                    if button_incor5:
                        st.session_state.flop3_cor_inc = 'incorrect'
                if st.session_state.flop3_cor_inc == 'incorrect':
                    flop3_user_input = st.text_input('Enter the correct card',key='flop3_inc_text')
                    if len(flop3_user_input)>1:
                        get_suggestions(flop3_user_input,cards_list)
                    if flop3_user_input.lower() in cards_list:
                        st.session_state.flop3 = flop3_user_input.lower()

if st.session_state.flop1 !='' and st.session_state.flop2 != '' and st.session_state.flop3 != '' :
    st.markdown(f'#### Your preflop hand is *{st.session_state.preflop1}* and *{st.session_state.preflop2}*')
    st.markdown(f'#### The flop is *{st.session_state.flop1}*, *{st.session_state.flop2}* and *{st.session_state.flop3}*')
    if st.button('🧞 Get Recommendation', key='flop_reco'):
        with st.spinner("Calculating..."):
                flop_reco = get_flop(st.session_state.nbofplayer, st.session_state.position, st.session_state.preflop1, st.session_state.preflop2,st.session_state.flop1,st.session_state.flop2,st.session_state.flop3, raised=False )['message']
        st.session_state.flop_recom = flop_reco
    if st.session_state.flop_recom:
        if len(st.session_state.flop_recom)>60:
            st.write(st.session_state.flop_recom[:-15])
        else:
            st.write(st.session_state.flop_recom)

    #Continue or Fold Flop
    # Create buttons with custom styles
    cont2, fold2 = st.columns(2)
    with cont2:
        fold_continue_button = st.button('✅ Continue', key='fold_continue_button')
    if fold_continue_button:
        st.session_state.flopdecision = 'Continue'
    with fold2:
        fold_fold_button = st.button('❌ Fold', key='fold_fold_button')
    if fold_fold_button:
        st.session_state.flopdecision = 'Fold'

# Turn
if st.session_state.flopdecision == 'Continue':
    st.markdown(
        '## Turn'
        )

    # File uploader
    uploaded_files_3 = st.file_uploader("Upload one image", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="upload3")
    if uploaded_files_3:
        # Display uploaded images
        #st.image([Image.open(file) for file in uploaded_files], width=200)

        # Predict button
        if st.button("Get Turn Prediction"):
            with st.spinner("Sending images to the model..."):
                predictions = get_prediction(uploaded_files_3)
                st.session_state.turnpredictions = predictions

    if len(st.session_state.turnpredictions)>0 :
        predictions = st.session_state.turnpredictions
        st.success("Predictions received!")
        results = predictions.get("results", [])

        turncol1, turncol2 = st.columns(2)
        with turncol1:
            st.image(Image.open(uploaded_files_3[0]), width=200)
            st.markdown(f"**Prediction:** {results[0][0]}")

            # Add buttons for feedback
            cor6, incor6 = st.columns(2)
            with cor6:
                button_cor6 = st.button("👍", key='turn_correct')
                if button_cor6:
                    st.session_state.turn_cor_inc = 'correct'
                if st.session_state.turn_cor_inc == 'correct':
                    st.session_state.turn = results[0][0]

            with incor6:
                button_incor6 = st.button('👎', key='turn_incorrect' )
                if button_incor6:
                    st.session_state.turn_cor_inc = 'incorrect'
            if st.session_state.turn_cor_inc == 'incorrect':
                turn_user_input = st.text_input('Enter the correct card',key='turn_inc_text')
                if len(turn_user_input)>1:
                    get_suggestions(turn_user_input,cards_list)
                if turn_user_input.lower() in cards_list:
                    st.session_state.turn = turn_user_input.lower()

if st.session_state.turn !='':
    st.markdown(f'#### Your preflop hand is *{st.session_state.preflop1}* and *{st.session_state.preflop2}*')
    st.markdown(f'#### The flop is *{st.session_state.flop1}*, *{st.session_state.flop2}* and *{st.session_state.flop3}*')
    st.markdown(f'#### The turn is *{st.session_state.turn}*')
    if st.button('🧞 Get Recommendation', key='turn_reco'):
        with st.spinner("Calculating..."):
                turn_reco = get_turn(st.session_state.nbofplayer, st.session_state.position, st.session_state.preflop1, st.session_state.preflop2,st.session_state.flop1,st.session_state.flop2,st.session_state.flop3,st.session_state.turn, raised=False )['message']
        st.session_state.turn_recom = turn_reco
    if st.session_state.turn_recom:
        if len(st.session_state.turn_recom)>60:
            st.write(st.session_state.turn_recom[:-15])
        else:
            st.write(st.session_state.turn_recom)

    #Continue or Follow
    # Create buttons with custom styles
    cont3, fold3 = st.columns(2)
    with cont3:
        turn_continue_button = st.button('✅ Continue', key='turn_continue_button')
    if turn_continue_button:
        st.session_state.turndecision = 'Continue'
    with fold3:
        turn_fold_button = st.button('❌ Fold', key='turn_fold_button')
    if turn_fold_button:
        st.session_state.turndecision = 'Fold'




# River
if st.session_state.turndecision == 'Continue':
    st.markdown(
        '## River'
        )

    # File uploader
    uploaded_files_4 = st.file_uploader("Upload one image", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="upload4")
    if uploaded_files_4:
        # Display uploaded images
        #st.image([Image.open(file) for file in uploaded_files], width=200)

        # Predict button
        if st.button("Get River Prediction"):
            with st.spinner("Sending images to the model..."):
                predictions = get_prediction(uploaded_files_4)
                st.session_state.riverpredictions = predictions

    if len(st.session_state.riverpredictions)>0 :
        predictions = st.session_state.riverpredictions
        st.success("Predictions received!")
        results = predictions.get("results", [])

        rivercol1, rivercol2 = st.columns(2)
        with rivercol1:
            st.image(Image.open(uploaded_files_4[0]), width=200)
            st.markdown(f"**Prediction:** {results[0][0]}")

            # Add buttons for feedback
            cor7, incor7 = st.columns(2)
            with cor7:
                button_cor7 = st.button("👍", key='river_correct')
                if button_cor7:
                    st.session_state.river_cor_inc = 'correct'
                if st.session_state.river_cor_inc == 'correct':
                    st.session_state.river = results[0][0]

            with incor7:
                button_incor7 = st.button('👎', key='river_incorrect' )
                if button_incor7:
                    st.session_state.river_cor_inc = 'incorrect'
            if st.session_state.river_cor_inc == 'incorrect':
                river_user_input = st.text_input('Enter the correct card',key='river_inc_text')
                if len(river_user_input)>1:
                    get_suggestions(river_user_input,cards_list)
                if river_user_input.lower() in cards_list:
                    st.session_state.river = river_user_input.lower()

    if st.session_state.river !='':
        st.markdown(f'#### Your preflop hand is *{st.session_state.preflop1}* and *{st.session_state.preflop2}*')
        st.markdown(f'#### The flop is *{st.session_state.flop1}*, *{st.session_state.flop2}* and *{st.session_state.flop3}*')
        st.markdown(f'#### The turn is *{st.session_state.turn}*')
        st.markdown(f'#### The river is *{st.session_state.river}*')
        if st.button('🧞 Get Recommendation', key='river_reco'):
            with st.spinner("Calculating..."):
                    river_reco = get_river(st.session_state.nbofplayer, st.session_state.position, st.session_state.preflop1, st.session_state.preflop2,st.session_state.flop1,st.session_state.flop2,st.session_state.flop3,st.session_state.turn,st.session_state.river, raised=False )['message']
            st.session_state.river_recom = river_reco
    if st.session_state.river_recom:
        st.write(st.session_state.river_recom)

    #Continue or Follow
    # Create buttons with custom styles
    contend, foldend = st.columns(2)
    with contend:
        won_button = st.button('🎉 I won', key='won_button')
    if won_button:
        st.balloons()
    with foldend:
        lost_button = st.button('😭 I lost', key='lost_button')
    if lost_button:
        st.snow()
