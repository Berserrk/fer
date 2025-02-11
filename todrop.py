import streamlit as st
from streamlit_cytoscapejs import cytoscape

# Example showing different layouts
layouts = {
    'random': {'name': 'random'},
    'grid': {'name': 'grid'},
    'circle': {'name': 'circle'},
    'concentric': {'name': 'concentric'},
    'breadthfirst': {'name': 'breadthfirst'},
    'cose': {'name': 'cose'},
    'cola': {'name': 'cola'},
    'euler': {'name': 'euler'},
    'spread': {'name': 'spread'},
    'dagre': {'name': 'dagre'},
    'klay': {'name': 'klay'}
}

# Layout selector
selected_layout = st.selectbox('Select Layout', list(layouts.keys()))

cytoscape(
    elements=elements,
    layout=layouts[selected_layout],
    key='graph'
)
