var width = 400,
    height = 200,
    fill = d3.scale.category20();


var g_outer = d3.select("#g_graph")
  .append("svg:svg")
    .attr("width", width)
    .attr("height". height)
    .attr("potiner-events", 'all')

// init svg
var h_outer = d3.select("#h_graph")
  .append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .attr("pointer-events", "all");

var g_vis = g_outer
  .append("svg:svg")
    .on("mousemove", gmousemove)
    .on("mousedown", gmousedown)
    .on("mouseup", gmouseup);

g_vis.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'white');  

var h_vis = h_outer
  .append('svg:g')
    .on("mousemove", hmousemove)
    .on("mousedown", hmousedown)
    .on("mouseup", hmouseup);

h_vis.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'white');

// init h_force layout
var h_force = d3.layout.force()
    .size([width, height])
    .nodes([{}]) // initialize with a single node
    .linkDistance(50)
    .charge(-200)
    .on("tick", h_tick);

var g_force = d3.layout.force()
  .size([width, height])
  .nodes([{}])
  .linkDistance(50)
  .charge(-200)
  .on("tick", g_tick)

// line displayed when dragging new nodes
var h_drag_line = h_vis.append("line")
    .attr("class", "drag_line")
    .attr("x1", 0)
    .attr("y1", 0)
    .attr("x2", 0)
    .attr("y2", 0);

var g_drag_line = g_vis.append("line")
     .attr("class", "draw_line")
     .attr("x1", 0)
     .attr("y1", 0)
     .attr("x2", 0)
     .attr("y2", 0)

// get layout properties
var h_graph = {
    nodes: h_force.nodes(),
    links: h_force.links(),
    node: h_vis.selectAll(".node"),
    link: h_vis.selectAll(".link"),
    drag_line: h_drag_line,
    selected_node: null,
    selected_link: null,
    mousedown_link: null,
    mousedown_node: null,
    mouseup_node: null,
    vis: h_vis,
    force: h_force
};

var g_graph = {
    nodes: g_force.nodes(),
    links: g_force.links(),
    node: g_vis.selectAll(".node"),
    link: g_vis.selectAll(".link"),
    drag_line: g_drag_line,
    selected_node: null,
    selected_link: null,
    mousedown_link: null,
    mousedown_node: null,
    mouseup_node: null,
    vis: g_vis,
    force: g_force
}

redraw(g_graph);
redraw(h_graph);
function mousedown(graph) {
  if (!graph.mousedown_node && !graph.mousedown_link) {
    // allow panning if nothing is selected
    graph.vis.call(d3.behavior.zoom().on("zoom"), rescale);
    return;
  }
}

function mousemove(graph, xpoint, ypoint) {
  if (!graph.mousedown_node) return;
  // update drag line
  graph.drag_line
      .attr("x1", graph.mousedown_node.x)
      .attr("y1", graph.mousedown_node.y)
      .attr("x2", xpoint)
      .attr("y2", ypoint);

}
function gmousedown(){
  mousedown(g_graph);
}
function hmousedown(){
  mousedown(h_graph);
}
function gmousemove(){
  var point = d3.svg.mouse(this);
  console.log("Mousemove:", point);
  mousemove(g_graph, point[0], point[1]);
}
function hmousemove(){
  var point = d3.svg.mouse(this)
  console.log("Mousemove:", point)
  mousemove(h_graph, point[0], point[1]);
}
function mouseup(graph, xpoint, ypoint) {
  if (graph.mousedown_node) {
    // hide drag line
    graph.drag_line
      .attr("class", "drag_line_hidden")

    if (!graph.mouseup_node) {
      // add node
      var node = {x: xpoint, y: ypoint},
        n = graph.nodes.push(node);

      // select new node
      graph.selected_node = node;
      graph.selected_link = null;
      
      // add link to mousedown node
      graph.links.push({source: graph.mousedown_node, target: node});
    }

    redraw(graph);
  }
  // clear mouse event vars
  resetMouseVars(graph);
}
function gmouseup(){
  var point = d3.svg.mouse(this);
  console.log("Mouseup:", point);
  mouseup(g_graph, point[0], point[1]);
}
function hmouseup(){
  var point = d3.svg.mouse(this)
  console.log("Mouseup:", point)
  mouseup(h_graph, point[0], point[1]);
}
function resetMouseVars(graph) {
  graph.mousedown_node = null;
  graph.mouseup_node = null;
  graph.mousedown_link = null;
}

function h_tick() {
  h_graph.link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  h_graph.node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
}

function g_tick(){
  g_graph.link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  g_graph.node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
}

// rescale g
function rescale(graph) {
  trans=d3.event.translate;
  scale=d3.event.scale;

  graph.vis.attr("transform",
      "translate(" + trans + ")"
      + " scale(" + scale + ")");
}

// redraw h_force layout
function redraw(graph) {

  graph.link = graph.link.data(graph.links);

  graph.link.enter().insert("line", ".node")
      .attr("class", "link")
      .on("mousedown", 
        function(d) { 
          graph.mousedown_link = d; 
          if (graph.mousedown_link == graph.selected_link) graph.selected_link = null;
          else graph.selected_link = graph.mousedown_link; 
          graph.selected_node = null; 
          redraw(graph); 
        })

  graph.link.exit().remove();

  graph.link
    .classed("link_selected", function(d) { return d === graph.selected_link; });

  graph.node = graph.node.data(graph.nodes);

  graph.node.enter().insert("circle")
      .attr("class", "node")
      .attr("r", 5)
      .on("mousedown", 
        function(d) { 
          // disable zoom
          graph.vis.call(d3.behavior.zoom().on("zoom"), null);

          graph.mousedown_node = d;
          if (graph.mousedown_node == graph.selected_node) graph.selected_node = null;
          else graph.selected_node = graph.mousedown_node; 
          graph.selected_link = null; 

          // reposition drag line
          graph.drag_line
              .attr("class", "link")
              .attr("x1", graph.mousedown_node.x)
              .attr("y1", graph.mousedown_node.y)
              .attr("x2", graph.mousedown_node.x)
              .attr("y2", graph.mousedown_node.y);

          redraw(graph); 
        })
      .on("mousedrag",
        function(d) {
          // redraw();
        })
      .on("mouseup", 
        function(d) { 
          if (graph.mousedown_node) {
            graph.mouseup_node = d; 
            if (graph.mouseup_node == graph.mousedown_node) { resetMouseVars(); return; }

            // add link
            var link = {source: graph.mousedown_node, target: graph.mouseup_node};
            graph.links.push(link);

            // select new link
            graph.selected_link = link;
            graph.selected_node = null;

            // enable zoom
            graph.vis.call(d3.behavior.zoom().on("zoom"), rescale);
            redraw(graph);
          } 
        })
    .transition()
      .duration(750)
      .ease("elastic")
      .attr("r", 6.5);

  graph.node.exit().transition()
      .attr("r", 0)
    .remove();

  graph.node
    .classed("node_selected", function(d) { return d === graph.selected_node; });

  

  if (d3.event) {
    // prevent browser's default behavior
    d3.event.preventDefault();
  }

  graph.force.start();

}

function spliceLinksForNode(graph) {
  toSplice = graph.links.filter(
    function(l) { 
      return (l.source === graph.node) || (l.target === graph.node); });
  toSplice.map(
    function(l) {
      graph.links.splice(graph.links.indexOf(l), 1); });
}