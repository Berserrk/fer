import streamlit as st
from streamlit_cytoscapejs import cytoscape

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        .block-container { padding: 1rem; }
        .stCytoscape { height: 800px !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# Sample elements
elements = [
    {'data': {'id': 'a', 'label': 'Node A'}},
    {'data': {'id': 'b', 'label': 'Node B'}},
    {'data': {'source': 'a', 'target': 'b'}}
]

# Available layouts
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

selected_layout = st.selectbox('Select Layout', list(layouts.keys()))

stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#666',
            'label': 'data(label)',
            'width': 50,
            'height': 50,
            'font-size': '12px',
            'text-valign': 'center',
            'text-halign': 'center'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'width': 2,
            'curve-style': 'bezier',
            'line-color': '#999'
        }
    }
]

cytoscape(
    elements=elements,
    stylesheet=stylesheet,
    layout=layouts[selected_layout],
    key='graph'
)
