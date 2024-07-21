import streamlit as st

# Create two columns
col1, col2 = st.columns(2)

# Add headers and place the buttons in the first column and the checkboxes in the second
col1.header("MESSAGE")
if col1.button('Germany'):
    st.session_state.country_clicked = 'Germany'
if col1.button('France'):
    st.session_state.country_clicked = 'France'
if col1.button('Italy'):
    st.session_state.country_clicked = 'Italy'
if col1.button('Spain'):
    st.session_state.country_clicked = 'Spain'
if col1.button('Portugal'):
    st.session_state.country_clicked = 'Portugal'
if col1.button('Netherlands'):
    st.session_state.country_clicked = 'Netherlands'
if col1.button('Belgium'):
    st.session_state.country_clicked = 'Belgium'
if col1.button('Switzerland'):
    st.session_state.country_clicked = 'Switzerland'
if col1.button('Brazil'):
    st.session_state.country_clicked = 'Brazil'
if col1.button('Argentina'):
    st.session_state.country_clicked = 'Argentina'
if col1.button('Colombia'):
    st.session_state.country_clicked = 'Colombia'
if col1.button('Chile'):
    st.session_state.country_clicked = 'Chile'
if col1.button('Peru'):
    st.session_state.country_clicked = 'Peru'

col2.header("CHECKBOX")
if col2.checkbox('Check me out'):
    st.write('Look, a checkbox!')

# Add a new section for the description
st.header("DESCRIPTION")

if st.button('Germany Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Germany'):
    st.info('Berlin is the capital of Germany.')
if st.button('France Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'France'):
    st.info('Paris is the capital of France.')
if st.button('Italy Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Italy'):
    st.info('Rome is the capital of Italy.')
if st.button('Spain Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Spain'):
    st.info('Madrid is the capital of Spain.')
if st.button('Portugal Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Portugal'):
    st.info('Lisbon is the capital of Portugal.')
if st.button('Netherlands Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Netherlands'):
    st.info('Amsterdam is the capital of Netherlands.')
if st.button('Belgium Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Belgium'):
    st.info('Brussels is the capital of Belgium.')
if st.button('Switzerland Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Switzerland'):
    st.info('Bern is the capital of Switzerland.')
if st.button('Brazil Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Brazil'):
    st.info('Brasília is the capital of Brazil.')
if st.button('Argentina Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Argentina'):
    st.info('Buenos Aires is the capital of Argentina.')
if st.button('Colombia Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Colombia'):
    st.info('Bogotá is the capital of Colombia.')
if st.button('Chile Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Chile'):
    st.info('Santiago is the capital of Chile.')
if st.button('Peru Description') or ('country_clicked' in st.session_state and st.session_state.country_clicked == 'Peru'):
    st.info('Lima is the capital of Peru.')

st.session_state.country_clicked = ''  # Reset the state after displaying the description