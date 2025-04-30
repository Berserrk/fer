import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import spacy
from typing import Dict, List, Tuple
from collections import Counter

# Sample documents
SAMPLE_DOCS = {
    "Tech News": """
    Apple Inc. announced its latest iPhone model today in Cupertino, California. 
    CEO Tim Cook presented the new features to an excited audience at Apple Park.
    The device will be available next month in the United States and Europe, 
    with prices starting at $999. Microsoft and Google are expected to release
    competing products later this year.
    """,
    
    "Business Report": """
    Tesla reported strong Q4 earnings, exceeding Wall Street expectations.
    The electric vehicle manufacturer, led by CEO Elon Musk, saw revenue growth
    of 25% year-over-year. The company's expansion in China and Germany has
    contributed significantly to its success. Tesla's stock price rose 5% in
    New York trading following the announcement.
    """,
    
    "Sports Update": """
    The Los Angeles Lakers defeated the Boston Celtics in a thrilling NBA match
    last night at Staples Center. LeBron James led the scoring with 32 points,
    while Jayson Tatum scored 28 points for the Celtics. The Lakers' coach
    praised the team's defensive performance in the fourth quarter. The win
    puts them at the top of the Western Conference.
    """
}

@st.cache_resource
def load_nlp_model():
    return spacy.load("en_core_web_sm")

def extract_entities(text: str, nlp) -> Dict[str, List[str]]:
    """Extract entities from text using SpaCy"""
    doc = nlp(text)
    entities = {}
    
    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        if ent.text not in entities[ent.label_]:
            entities[ent.label_].append(ent.text)
    
    return entities

def generate_summary(text: str, nlp) -> str:
    """Generate a simple summary using basic NLP techniques"""
    doc = nlp(text)
    sentences = list(doc.sents)
    
    if len(sentences) <= 3:
        return text
    
    summary = [sentences[0].text, sentences[1].text, sentences[-1].text]
    return " ".join(summary)

def create_entity_frequency_plot(entities: Dict[str, List[str]]):
    """Create a bar chart of entity frequencies by type"""
    entity_counts = {etype: len(entities[etype]) for etype in entities}
    fig = px.bar(
        x=list(entity_counts.keys()),
        y=list(entity_counts.values()),
        title="Entity Types Distribution",
        labels={'x': 'Entity Type', 'y': 'Count'}
    )
    return fig

def create_entity_network(entities: Dict[str, List[str]]):
    """Create a simple network visualization of entities"""
    nodes = []
    edges = []
    
    for i, etype in enumerate(entities.keys()):
        nodes.append(dict(name=etype, group=1))
        for entity in entities[etype]:
            nodes.append(dict(name=entity, group=2))
            edges.append(dict(source=etype, target=entity))
    
    fig = go.Figure(data=[
        go.Scatter(
            x=[1]*len(nodes),
            y=range(len(nodes)),
            mode='markers+text',
            text=[node['name'] for node in nodes],
            textposition='middle right',
            hoverinfo='text',
            marker=dict(
                size=20,
                color=[node['group'] for node in nodes],
                colorscale='Viridis'
            )
        )
    ])
    
    fig.update_layout(
        showlegend=False,
        title="Entity Network"
    )
    
    return fig

def main():
    st.set_page_config(layout="wide")
    st.title("Document Analysis Dashboard (Demo)")
    
    # Sidebar for view selection
    with st.sidebar:
        st.header("Demo Controls")
        view_mode = st.radio(
            "Select View Mode",
            ["Document-by-Document", "Comparative View"]
        )
    
    # Load NLP model
    nlp = load_nlp_model()
    
    if view_mode == "Document-by-Document":
        # Create tabs for each sample document
        tabs = st.tabs([f"📄 {name}" for name in SAMPLE_DOCS.keys()])
        
        for tab, (doc_name, text) in zip(tabs, SAMPLE_DOCS.items()):
            with tab:
                # Process document
                summary = generate_summary(text, nlp)
                entities = extract_entities(text, nlp)
                
                # Create two columns for layout
                col1, col2 = st.columns([6, 4])
                
                with col1:
                    # Summary section
                    st.subheader("Document Summary")
                    st.write(summary)
                    
                    # Entities table
                    st.subheader("Named Entities")
                    entities_data = [
                        {"Entity Type": etype, "Entity": entity}
                        for etype, elist in entities.items()
                        for entity in elist
                    ]
                    if entities_data:
                        df = pd.DataFrame(entities_data)
                        st.dataframe(
                            df,
                            column_config={
                                "Entity Type": st.column_config.Column(width="medium"),
                                "Entity": st.column_config.Column(width="large")
                            }
                        )
                
                with col2:
                    # Visualizations
                    st.subheader("Entity Distribution")
                    fig = create_entity_frequency_plot(entities)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("Entity Network")
                    network_fig = create_entity_network(entities)
                    st.plotly_chart(network_fig, use_container_width=True)
    
    else:  # Comparative View
        st.header("Comparative Analysis")
        
        # Process all documents
        all_entities = []
        for text in SAMPLE_DOCS.values():
            entities = extract_entities(text, nlp)
            all_entities.append(entities)
        
        # Create comparative visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Entity Types Across Documents")
            # Create stacked bar chart
            entity_data = []
            for i, (entities, doc_name) in enumerate(zip(all_entities, SAMPLE_DOCS.keys())):
                for etype, elist in entities.items():
                    entity_data.append({
                        "Document": doc_name,
                        "Entity Type": etype,
                        "Count": len(elist)
                    })
            
            if entity_data:
                df = pd.DataFrame(entity_data)
                fig = px.bar(
                    df,
                    x="Document",
                    y="Count",
                    color="Entity Type",
                    title="Entity Distribution Comparison"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Common Entities")
            # Find common entities across documents
            common_entities = {}
            for entities in all_entities:
                for etype, elist in entities.items():
                    if etype not in common_entities:
                        common_entities[etype] = Counter()
                    common_entities[etype].update(elist)
            
            # Display common entities as tables
            for etype, counter in common_entities.items():
                if counter:
                    st.write(f"Most common {etype}:")
                    common_df = pd.DataFrame(
                        counter.most_common(5),
                        columns=[etype, "Frequency"]
                    )
                    st.dataframe(common_df)

if __name__ == "__main__":
    main()