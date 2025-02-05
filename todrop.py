import streamlit as st
import streamlit.components.v1 as components

def force_graph():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
        <style>
            .node { fill: #69b3a2; }
            .link { stroke: #999; stroke-opacity: 0.6; }
        </style>
    </head>
    <body>
        <div id="graph"></div>
        <script>
            // Sample data
            const data = {
                nodes: [
                    {id: 1}, {id: 2}, {id: 3}, {id: 4}, {id: 5}
                ],
                links: [
                    {source: 1, target: 2},
                    {source: 2, target: 3},
                    {source: 3, target: 4},
                    {source: 4, target: 5},
                    {source: 5, target: 1}
                ]
            };

            // Set up SVG
            const width = 600;
            const height = 400;
            
            const svg = d3.select("#graph")
                .append("svg")
                .attr("width", width)
                .attr("height", height);

            // Create force simulation
            const simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id))
                .force("charge", d3.forceManyBody().strength(-100))
                .force("center", d3.forceCenter(width / 2, height / 2));

            // Draw links
            const link = svg.append("g")
                .selectAll("line")
                .data(data.links)
                .join("line")
                .attr("class", "link");

            // Draw nodes
            const node = svg.append("g")
                .selectAll("circle")
                .data(data.nodes)
                .join("circle")
                .attr("class", "node")
                .attr("r", 10)
                .call(drag(simulation));

            // Update positions
            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
            });

            // Drag functionality
            function drag(simulation) {
                function dragstarted(event) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    event.subject.fx = event.subject.x;
                    event.subject.fy = event.subject.y;
                }
                
                function dragged(event) {
                    event.subject.fx = event.x;
                    event.subject.fy = event.y;
                }
                
                function dragended(event) {
                    if (!event.active) simulation.alphaTarget(0);
                    event.subject.fx = null;
                    event.subject.fy = null;
                }
                
                return d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended);
            }
        </script>
    </body>
    </html>
    """
    
    components.html(html, height=450)

def main():
    st.title("Force-Directed Graph Example")
    force_graph()

if __name__ == "__main__":
    main()
