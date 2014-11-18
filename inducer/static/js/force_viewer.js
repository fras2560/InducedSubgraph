var width = 400,
    height = 400,
    fill = d3.scale.category20();


var g_outer = d3.select("#g_graph")
  .append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .attr("pointer-events", 'all')

// init svg
var h_outer = d3.select("#h_graph")
  .append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .attr("pointer-events", "all");

var g_vis = g_outer
  .append('svg:g')
    .call(d3.behavior.zoom().on("zoom", grescale))
    .on("dblclick.zoom", null)
  .append("svg:g")
    .on("mousemove", gmousemove)
    .on("mousedown", gmousedown)
    .on("mouseup", gmouseup);

g_vis.append('svg:rect')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'white')

var h_vis = h_outer
  .append('svg:g')
    .call(d3.behavior.zoom().on("zoom", hrescale))
    .on("dblclick.zoom", null)
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
    .nodes([{name:0}]) // initialize with a single node
    .linkDistance(50)
    .charge(-200)
    .on("tick", h_tick);

var g_force = d3.layout.force()
  .size([width, height])
  .nodes([{name:0}])
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
    coloring: null,
    vis: h_vis,
    force: h_force,
    type:"H",
    scale:hrescale,
    text:h_vis.selectAll('.text')
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
    force: g_force,
    type:"G",
    induced_nodes:null,
    induced_edges:null,
    coloring:null,
    scale:grescale,
    text:g_vis.selectAll(".text")
};
// keeps track of which grpah is selected
var last_clicked = null;

// add keyboard callback
d3.select(window)
    .on("keydown", keydown);

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
  last_clicked = g_graph;
  updateClickLabel("G");
  mousedown(g_graph);
}

function hmousedown(){
  last_clicked = h_graph;
  updateClickLabel("H")
  mousedown(h_graph);
}

function gmousemove(){
  var point = d3.svg.mouse(this);
  mousemove(g_graph, point[0], point[1]);
}

function hmousemove(){
  var point = d3.svg.mouse(this)
  mousemove(h_graph, point[0], point[1]);
}

function mouseup(graph, xpoint, ypoint) {
  if (graph.mousedown_node) {
    // hide drag line
    graph.drag_line
      .attr("class", "drag_line_hidden")

    if (!graph.mouseup_node) {
      // induced subgraph no longer valid
      clearSubgraph();
      clearColoring();

      // add node
      var node = {x: xpoint, y: ypoint, name:graph.nodes.length},
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
  mouseup(g_graph, point[0], point[1]);
}

function hmouseup(){
  var point = d3.svg.mouse(this)
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

  h_graph.text.attr("x", function(d) { return d.x-4;})
    .attr("y", function(d) { return d.y+4;})

}

function g_tick(){
  g_graph.link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  g_graph.node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });

  g_graph.text.attr("x", function(d) { return d.x-4;})
    .attr("y", function(d) { return d.y+5;})
}

function grescale(){
  rescale(g_graph);
}

function hrescale(){
  rescale(h_graph);
}

// rescale g
function rescale(graph) {
  trans=d3.event.translate;
  scale=d3.event.scale;

  graph.vis.attr("transform",
      "translate(" + trans + ")"
      + " scale(" + scale + ")");
}

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
  graph.node.enter()
      .insert("circle")
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
            if (graph.mouseup_node == graph.mousedown_node) { resetMouseVars(graph); return; }

            // add link
            var link = {source: graph.mousedown_node, target: graph.mouseup_node};
            graph.links.push(link);

            // select new link
            graph.selected_link = link;
            graph.selected_node = null;

            // enable zoom
            graph.vis.call(d3.behavior.zoom().on("zoom"), graph.scale);
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
  // draw induced subgraph
  if (graph.type == "G"){
      graph.node
        .classed("induced_node", function(d){
            if (!g_graph.induced_nodes){return false}
            arrayLength = g_graph.induced_nodes.length;
            for (var i = 0; i < arrayLength; i++) {
              if (d.index === g_graph.induced_nodes[i]){
                return true;
              }else{
              }
            }
          }
        );
      graph.link
        .classed("induced_edge", function(d) { 
          if (!g_graph.induced_edges){return false}
          arrayLength = g_graph.induced_edges.length;
          for (var i = 0; i < arrayLength; i++) {
            if ((d.target.index === g_graph.induced_edges[i][0] && d.source.index === g_graph.induced_edges[i][1]) 
                || (d.target.index === g_graph.induced_edges[i][1] && d.source.index === g_graph.induced_edges[i][0])
              ){
              return true;
            }else{
            }
          }
        }
      );
    }
  if (graph.coloring != null){
    var colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    for(var i = 0; i < graph.coloring.length; i++){
      graph.node
        .classed("color_" + colors[i], function(d){
          if($.inArray(d.index, graph.coloring[i]) != -1){
            return true;
          }else{
            return false;
          }
        });
    }
  }else{
    var colors = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    for(var i = 0; i < colors.length; i++){
      graph.node
        .classed("color_" + colors[i], function(d){
          return false;
        });
    }
  }
  graph.text = graph.text.data(graph.nodes);
  graph.text.enter()
    .insert("text")
    .attr("x", 1)
    .attr("y", ".1em")
    .attr("class", "text")
    .text(function(d) { 
      return d.name; })
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
        if (graph.mouseup_node == graph.mousedown_node) { resetMouseVars(graph); return; }

        // add link
        var link = {source: graph.mousedown_node, target: graph.mouseup_node};
        graph.links.push(link);

        // select new link
        graph.selected_link = link;
        graph.selected_node = null;

        // enable zoom
        graph.vis.call(d3.behavior.zoom().on("zoom"), graph.scale);
        redraw(graph);
      } 
    })
    .transition()
      .duration(750)
      .ease('elastic');

  graph.text.exit().transition()
    .remove();

  if (d3.event) {
    // prevent browser's default behavior
    d3.event.preventDefault();
  }

  graph.force.start();
}

function spliceLinksForNode(graph, node) {
  toSplice = graph.links.filter(
    function(l) { 
      return (l.source === node) || (l.target === node); });
  toSplice.map(
    function(l) {
      graph.links.splice(graph.links.indexOf(l), 1); });
}

function keydown() {
  /*
    the function that handles any keydown events
    Parameters:
      none
  */
  if (!last_clicked) return;
  if (!last_clicked.selected_node && !last_clicked.selected_link) return;
  switch (d3.event.keyCode) {
    case 8: // backspace
    case 46: { // delete
      clearSubgraph();
      clearColoring();
      if (last_clicked.selected_node) {
        last_clicked.nodes.splice(last_clicked.nodes.indexOf(last_clicked.selected_node), 1);
        spliceLinksForNode(last_clicked, last_clicked.selected_node);
      }
      else if (last_clicked.selected_link) {
        last_clicked.links.splice(last_clicked.links.indexOf(last_clicked.selected_link), 1);
      }
      last_clicked.selected_link = null;
      last_clicked.selected_node = null;
      redraw(last_clicked);
      break;
    }
    case 32:{ // space
      check4VertexGraphs();
      break;
    }
    case 67:{ // C
      checkContains();
      break;
    }
  }
}

function clearGraph(graph){
  /* clearGraph 
      a function that takes a graph and clears it nodes
      Paramaters:
        graph: the graph to clear
   */
  var node;
  while (graph.nodes.length > 0){
    node = graph.nodes[graph.nodes.length - 1];
    graph.nodes.splice(graph.nodes.indexOf(node) , 1);
    spliceLinksForNode(graph, node);
    redraw(graph);
  }
}

function updateClickLabel(graph){
  $('#selected').text("Selected Graph: "+graph);
}

function clearColoring(){
  /* clearColoring
     a function that clears the colored nodes
     Parameters
        none 
  */
  $('GColoring').text("G Coloring:");
  $('HColoring').text("H Coloring:");
  g_graph.coloring = null;
  h_graph.coloring = null;
  redraw(g_graph);
  redraw(h_graph); 
}

function clearSubgraph(){
  /* clearSubgraph
      a function that clear the induced subgraph of H
   */
  $('#contains').text("G contains H:");
  g_graph.induced_nodes = null;
  g_graph.induced_edges = null;
  redraw(g_graph); 
}

function checkContains(){
  clearColoring();
  var G = {
      nodes: [],
      edges: []
  };
  var H = {
      nodes: [],
      edges: []
  };
  var arrayLength = g_graph.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    G.nodes.push(g_graph.nodes[i].index);
  }
  arrayLength = g_graph.links.length;
  for (var i = 0; i < arrayLength; i++) {
    G.edges.push([g_graph.links[i].source.index, g_graph.links[i].target.index]);
  }

  arrayLength = h_graph.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    H.nodes.push(h_graph.nodes[i].index);
  }
  arrayLength = h_graph.links.length;
  for (var i = 0; i < arrayLength; i++) {
    H.edges.push([h_graph.links[i].source.index, h_graph.links[i].target.index]);
  }
  checkContains_aux(G, H, false);
}

function check4VertexGraphs(){
  clearSubgraph();
  clearColoring();
  var G = {
      nodes: [],
      edges: []
  };
  var arrayLength = g_graph.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    G.nodes.push(g_graph.nodes[i].index);
  }
  arrayLength = g_graph.links.length;
  for (var i = 0; i < arrayLength; i++) {
    G.edges.push([g_graph.links[i].source.index, g_graph.links[i].target.index]);
  }
  var n = [0,1,2,3];
  var FourGraphs = {
                  claw:{nodes:n, edges:[[0, 1], [0, 2], [0, 3]]},
                  co_claw:{nodes:n, edges:[[1, 2], [2, 3], [1, 3]]},
                  K4:{nodes:n, edges:[[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]},
                  co_K4:{nodes:n, edges:[]},
                  diamond:{nodes:n, edges:[[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]},
                  co_diamond:{nodes:n, edges:[[2, 3]]},
                  C4:{nodes:n, edges:[[0, 1], [0, 3], [1, 2], [2, 3]]},
                  co_C4:{nodes:n, edges:[[0, 2], [1, 3]]},
                  paw:{nodes:n, edges:[[0, 1], [1, 2], [2, 3], [1, 3]]},
                  co_paw:{nodes:n, edges:[[0, 2], [0, 3]]},
                  C5:{nodes:[0, 1, 2, 3, 4], edges:[[0, 1], [0, 4], [1, 2], [2, 3], [3, 4]]}
                };
  var Hgraphs = [];
  var names = [];
  $(':checkbox').each(function() {
    if (this.checked == true){
       Hgraphs.push(FourGraphs[this.value]);
       names.push(this.value);
    }
  });
  // hide all indicators
  $('.containsPictures').hide();
  var end = Hgraphs.length;
  for(var graph = 0; graph < end;graph++){
    checkContains_aux(G, Hgraphs[graph], names[graph]);
  }
}

function checkContains_aux(G, H, multi){
  var contains = false;
  $.ajax(
    {
       type: "POST",
       contentType: "application/json",
       url: "/contains",
       data: JSON.stringify({"G":G, "H":H}),
               dataType: "json",
               success: function(results)
               {
                if (results.success == true){
                  $('#contains').text("G contains H: Yes");
                  g_graph.induced_nodes = results.nodes;
                  g_graph.induced_edges = results.edges;
                  redraw(g_graph);
                }
                if (multi == false && results.success == false){
                  $('#contains').text("G contains H: No");
                  g_graph.induced_nodes = null;
                  g_graph.induced_edges = null;
                }else{
                  if (results.success == true){
                    $('#'+multi+'Yes').show();
                  }else{
                    $('#'+multi+'No').show();
                  }
                  
                }
               }, error: function(request, error){ 
                 alert("Error: Check console");
                 console.log(request);
                 console.log(error)
               }          
      }
    );
}

function complementGraph(A){
  /*
    complementGraph
      a function that take the complement of a graph
    Parameters:
      A: the graph to take the complement of
  */
  clearColoring();
  clearSubgraph();
  var G = {
      nodes: [],
      edges: []
  };
  var arrayLength = A.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    G.nodes.push(A.nodes[i].index);
  }
  arrayLength = A.links.length;
  for (var i = 0; i < arrayLength; i++) {
    G.edges.push([A.links[i].source.index, A.links[i].target.index]);
  }
  $.ajax({
    type: "POST",
    contentType: "application/json",
    url: "\complement",
    data: JSON.stringify(G),
      dataType: "json",
      success: function(results){
        end = results.nodes.length;
        var node;
        var xpoint = width / 2;
        var ypoint = height / 2;
        var nodes = [];
        clearGraph(A);
        for(var i = 0; i < end; i++){
          node = {x: xpoint, y: ypoint, name:i};
          A.nodes.push(node);
          ypoint = ypoint + 50
          if (ypoint > height){
            ypoint = ypoint - height
            xpoint = (xpoint + 50) % width
          }
          nodes.push(node)
        }
        end = results.edges.length;
        for (var i = 0; i < end; i++){
          A.links.push({source: nodes[results.edges[i][0]], target: nodes[results.edges[i][1]]});
        }
        redraw(A);
      }, error: function(request, error){
        alert("Error");
        console.log(request);
        console.log(error)
      }
  })
}

$(function() {
    $('#upload-file-btn-g').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        loadGraph(g_graph, form_data);
    });
});

$(function() {
    $('#upload-file-btn-h').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        loadGraph(h_graph, form_data);
    });
});

function loadGraph(A, form_data){
  /* loadGraph
      a function that loads a graph
      Parameters:
        A: the graph A to be loaded to
   */
      clearSubgraph();
      clearColoring();
     $('.loadClose').hide();
     $.ajax({
      type: 'POST',
      url: '/loadGraph',
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: false,
      success: function(data) {
          data = $.parseJSON(data);
          if (data.success == true){
            end = data.graph.nodes.length;
            var node;
            var xpoint = width / 2;
            var ypoint = height / 2;
            var nodes = [];
            clearGraph(A);
            for(var i = 0; i < end; i++){
              node = {x: xpoint, y: ypoint, name:i}
              A.nodes.push(node);
              ypoint = ypoint + 50
              if (ypoint > height){
                ypoint = ypoint - height
                xpoint = (xpoint + 50) % width
              }
              nodes.push(node)
            }
            end = data.graph.edges.length;
            for (var i = 0; i < end; i++){
              A.links.push({source: nodes[data.graph.edges[i][0]], target: nodes[data.graph.edges[i][1]]});
            }
            redraw(A);
            $('.loadClose').show()
          }else{
            alert("Failed to load graph");
          }
      }, error: function(request, error){
          alert("Error: check console");
          console.log(request);
          console.log(error) ;
      }
  });
}

function resetGraph(A){
  /*
    resetGraph
    a function that resets the graph to one vertex
    Parameters
      A: the graph A to be reset
  */
  clearGraph(A);
  clearColoring();
  var node = {x: width/2, y: height / 2, name:0};
  A.nodes.push(node);
  redraw(A);
}

function k_vertex(){
  /* k_vertex
      a function that checks if graph G has a k-vertex for k=0 to v
      Parameters:
        none
  */
  var G = {
      nodes: [],
      edges: []
  };
  var arrayLength = g_graph.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    G.nodes.push(g_graph.nodes[i].index);
  }
  arrayLength = g_graph.links.length;
  for (var i = 0; i < arrayLength; i++) {
    G.edges.push([g_graph.links[i].source.index, g_graph.links[i].target.index]);
  }
  var n = [0,1,2,3];
  var FourGraphs = {
                  claw:{nodes:n, edges:[[0, 1], [0, 2], [0, 3]]},
                  co_claw:{nodes:n, edges:[[1, 2], [2, 3], [1, 3]]},
                  K4:{nodes:n, edges:[[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]},
                  co_K4:{nodes:n, edges:[]},
                  diamond:{nodes:n, edges:[[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]},
                  co_diamond:{nodes:n, edges:[[2, 3]]},
                  C4:{nodes:n, edges:[[0, 1], [0, 3], [1, 2], [2, 3]]},
                  co_C4:{nodes:n, edges:[[0, 2], [1, 3]]},
                  paw:{nodes:n, edges:[[0, 1], [1, 2], [2, 3], [1, 3]]},
                  co_paw:{nodes:n, edges:[[0, 2], [0, 3]]},
                  C5:{nodes:[0, 1, 2, 3, 4], edges:[[0, 1], [0, 4], [1, 2], [2, 3], [3, 4]]}
                };
  var Hgraphs = [];
  var names = [];
  $(':checkbox').each(function() {
    if (this.checked == true){
       Hgraphs.push(FourGraphs[this.value]);
       names.push(this.value);
    }
  });
  $.ajax({
    type: 'POST',
    url: '/k_vertex',
    contentType: "application/json",
    data: JSON.stringify({'G':G, 'subgraphs':Hgraphs}),
      dataType: "json",
    success: function(data) {
      var end = data.length;
      var entry;
      var subsets;
      var subsetsLength;
      $('#k_modalList').empty();
      for (var k = 0; k < end; k++){
        if(data[k].has_k_vertex == true && data[k].combinations.length > 0){
          subset = " (" + data[k].combinations[0] + ")";
          subsetsLength = data[k].combinations.length;
          for (var set = 1; set < subsetsLength; set++){
            subset += " , (" + data[k].combinations[set] + ")";
          }
          entry = "<li>" + k + ": Yes " + subset + "</li>";
        }else if(data[k].has_k_vertex == true){
          entry = "<li>" + k + ": Yes </li>";
        }else{
          entry = "<li>" + k + ": No </li>";
        }
        $('#k_modalList').append(entry);
      }
      $('#k_modal').modal("show");

    }, error: function(request, error){
      alert("Error: check console");
      console.log(request);
      console.log(error);
    }
  });
}

function colorGraph(A, graph_name){
  /* colorGraph
    a function which colors one graph with lowest chromatic number
    Parameters:
      A: the graph to color
      graph_name: the name of the graph labels to update
  */
  $('#' + graph_name + 'ColorLoader').show();
  var G = {
      nodes: [],
      edges: []
  }
  var arrayLength = A.nodes.length;
  for (var i = 0; i < arrayLength; i++){
    G.nodes.push(A.nodes[i].index);
  }
  arrayLength = A.links.length;
  for (var i = 0; i < arrayLength; i++){
    G.edges.push([A.links[i].source.index, A.links[i].target.index]);
  }
  console.log(G);
  $.ajax({
    type: 'POST',
    url: '/coloring',
    contentType: "application/json",
    data: JSON.stringify(G),
      dataType: "json",
    success: function(graph){
      console.log(graph);
      if (graph != null){
        clearSubgraph();
        A.coloring = graph;
        $("#" + graph_name +"Coloring").text(graph_name + " Coloring: " + graph.length);
        redraw(A);
        $('#' + graph_name + 'ColorLoader').hide();
      }else{
        alert("No coloring could be found (>10)");
      }
    }, error: function(request, error){
        alert("Error-> check console");
        console.log(request);
        console.log(error);
    }
  });  
}

function joinGraphs(A, B){
  /* joinGraphs
      a function which joins one graph with another
      Parameters:
        A: the graph to join to
        B: the graph that being join on another
   */
  var G = {
      nodes: [],
      edges: []
  };
  var H = {
      nodes: [],
      edges: []
  };
  var arrayLength = A.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    G.nodes.push(A.nodes[i].index);
  }
  arrayLength = A.links.length;
  for (var i = 0; i < arrayLength; i++) {
    G.edges.push([A.links[i].source.index, A.links[i].target.index]);
  }

  arrayLength = B.nodes.length;
  for (var i = 0; i < arrayLength; i++) {
    H.nodes.push(B.nodes[i].index);
  }
  arrayLength = B.links.length;
  for (var i = 0; i < arrayLength; i++) {
    H.edges.push([B.links[i].source.index, B.links[i].target.index]);
  }
  $.ajax({
    type: 'POST',
    url: '/join',
    contentType: "application/json",
    data: JSON.stringify({'G':G, 'H':H}),
      dataType: "json",
    success: function(graph) {
      end = graph.nodes.length;
      var node;
      var xpoint = width / 2;
      var ypoint = height / 2;
      var nodes = [];
      clearGraph(A);
      for(var i = 0; i < end; i++){
        node = {x: xpoint, y: ypoint, name:i}
        A.nodes.push(node);
        ypoint = ypoint + 50
        if (ypoint > height){
          ypoint = ypoint - height
          xpoint = (xpoint + 50) % width
        }
        nodes.push(node)
      }
      end = graph.edges.length;
      for (var i = 0; i < end; i++){
        A.links.push({source: nodes[graph.edges[i][0]], target: nodes[graph.edges[i][1]]});
      }
      redraw(A);
    }, error: function(request, error){
      alert("Error: check console");
      console.log(request);
      console.log(error);
    }
  });
}

function copyGraph(A, B){
  /* copyGraph
      a function which copies one graph to another
      parameters:
        A: the graph to copy from
        B: the graph to copy to
   */
  var end = A.nodes.length;
  var node;
  var nodes = {};
  clearGraph(B);
  for(var x = 0; x < end; x++){
    node = {x:A.nodes[x].x, y:A.nodes[x].y, name:A.nodes[x].name};
    B.nodes.push(node);
    nodes[node.name] = node;
  }
  end = A.links.length;
  for(var y = 0; y < end; y++){
    B.links.push({source: nodes[A.links[y].source.name], target: nodes[A.links[y].target.name]});
  }
  redraw(B);
}

$(function(){
    $('#save-file-btn-g').click(function(){

        var G = {
          nodes: [],
          edges: []
        };
        var arrayLength = g_graph.nodes.length;
        for (var i = 0; i < arrayLength; i++) {
          G.nodes.push(g_graph.nodes[i].index);
        }
        arrayLength = g_graph.links.length;
        for (var i = 0; i < arrayLength; i++) {
          G.edges.push([g_graph.links[i].source.index, g_graph.links[i].target.index]);
        }
        saveFile_aux(G);
    });
})

$(function(){
    $('#save-file-btn-h').click(function(){

        var H = {
          nodes: [],
          edges: []
        };
        var arrayLength = h_graph.nodes.length;
        for (var i = 0; i < arrayLength; i++) {
          H.nodes.push(h_graph.nodes[i].index);
        }
        arrayLength = h_graph.links.length;
        for (var i = 0; i < arrayLength; i++) {
          H.edges.push([h_graph.links[i].source.index, h_graph.links[i].target.index]);
        }
        saveFile_aux(H);
    });
})

function saveFile_aux(G){
        $.ajax({
            type: "POST",
            url: "/save_file",
            contentType: "application/json",
            data: JSON.stringify(G),
            dataType: "json",
            success: function(result) {
                // check for a filename
                console.log(result);
                $('#downloadLink').show();
            },error: function(request, error){
                alert("Error: check console");
                console.log(request);
                console.log(error);
            }
        });
}