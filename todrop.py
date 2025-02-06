import streamlit as st
import streamlit.components.v1 as components
import json

def load_graph_data():
    # Load your JSON files
    try:
        with open('nodes.json', 'r') as f:
            nodes = json.load(f)
        with open('links.json', 'r') as f:
            links = json.load(f)
    except FileNotFoundError:
        # Default data if files not found
        nodes = [
            {"id": "Person1", "type": "person"},
            {"id": "Person2", "type": "person"},
            {"id": "Person3", "type": "person"},
            {"id": "CompanyA", "type": "company"},
            {"id": "CompanyB", "type": "company"}
        ]
        links = [
            {"source": "Person1", "target": "CompanyA"},
            {"source": "Person2", "target": "CompanyA"},
            {"source": "Person2", "target": "CompanyB"},
            {"source": "Person3", "target": "CompanyB"}
        ]
    return {"nodes": nodes, "links": links}

def force_graph(graph_data):
    # Convert the Python dict to a JavaScript-friendly string
    graph_data_js = json.dumps(graph_data)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
        <style>
            .node-person {{ fill: #69b3a2; }}
            .node-company {{ fill: #404080; }}
            .link {{ stroke: #999; stroke-opacity: 0.6; }}
            .node-label {{ font-size: 12px; }}
        </style>
    </head>
    <body>
        <div id="graph"></div>
        <script>
            // Load data from Python
            const data = {graph_data_js};

            const width = 1500;
            const height = 800;
            
            const svg = d3.select("#graph")
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            const simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id))
                .force("charge", d3.forceManyBody().strength(-400))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("y", d3.forceY(d => d.type === "company" ? height * 0.7 : height * 0.3).strength(1));

            const link = svg.append("g")
                .selectAll("line")
                .data(data.links)
                .join("line")
                .attr("class", "link");

            const node = svg.append("g")
                .selectAll("circle")
                .data(data.nodes)
                .join("circle")
                .attr("class", d => `node-${d.type}`)
                .attr("r", d => d.type === "company" ? 25 : 20)
                .call(drag(simulation));

            const labels = svg.append("g")
                .selectAll("text")
                .data(data.nodes)
                .join("text")
                .attr("class", "node-label")
                .text(d => d.id)
                .attr("dx", 0)
                .attr("dy", 25)
                .attr("text-anchor", "middle");

            simulation.on("tick", () => {{
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);

                labels
                    .attr("x", d => d.x)
                    .attr("y", d => d.y);
            }});

            function drag(simulation) {{
                function dragstarted(event) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    event.subject.fx = event.subject.x;
                    event.subject.fy = event.subject.y;
                }}
                
                function dragged(event) {{
                    event.subject.fx = event.x;
                    event.subject.fy = event.y;
                }}
                
                function dragended(event) {{
                    if (!event.active) simulation.alphaTarget(0);
                    // Nodes will stay where they are dragged
                }}
                
                return d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended);
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(html, height=850)

def main():
    st.title("People-Company Network Graph")
    graph_data = load_graph_data()
    force_graph(graph_data)

if __name__ == "__main__":
    main()
