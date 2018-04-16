// import tippy from 'tippy.js'


export default {
    colorPathways(subnetwork, pathwayColors, selectedPathways, cy) {
        cy.nodes().forEach(node => {
            // pull out only the selected pathways this node's a part of
            let pathwaySelectedNodes = node.data('pathways').filter(function(n) {
                return selectedPathways.indexOf(n) !== -1;
            });
            pathwaySelectedNodes.forEach(pathway => {
                if ( pathwaySelectedNodes.includes('query_list') &&
                    pathwaySelectedNodes.length === 1) {
                        node.style('shape', 'rectangle')
                } else if (
                    pathwaySelectedNodes.includes('query_list') &&
                    pathwaySelectedNodes.length > 1 ) {
                    node.style('shape', 'star')
                } else {
                    node.style('shape', 'ellipse');
                }
                    node.style('background-color', pathwayColors[pathway]);
            })
        })
    },
    applyMouseEvents(cy) {
        cy.on('mousedown', function(event){
            let evtTarget = event.target;
            if (evtTarget !== cy) {
                evtTarget.connectedEdges().animate({
                    style: {lineColor: 'blue'}
                });
            }
        });

        cy.on('mouseup', function(event){
            let evtTarget = event.target;

            if (evtTarget !== cy) {
                evtTarget.connectedEdges().animate({
                    style: { lineColor: 'gray' }
                });
            }
        });

        // cy.on('mouseover', function(event) {
        //     let evtTarget = event.target;
        //     if (evtTarget !== cy && evtTarget.data('pathways')) {
        //         const virtualReference = {
        //             attributes: {
        //                 title: evtTarget.data('pathways').join("\n")
        //             },
        //             getBoundingClientRect() {
        //                 return {
        //                     width: 1000,
        //                     height: 1000,
        //                     top: '100px',
        //                     left: '100px',
        //                     right: '200px',
        //                     bottom: '200px'
        //                 }
        //             },
        //             clientHeight: 100,
        //             clientWidth: 100
        //         };
        //         tippy(virtualReference)
        //         // console.log(evtTarget)
        //     }
        // })
    },
    coseOptions: {
      // Called on `layoutready`
      ready() {

      },
      // Called on `layoutstop`
      stop() {
      },
      // Whether to include labels in node dimensions. Useful for avoiding label overlap
      nodeDimensionsIncludeLabels: true,
      // number of ticks per frame; higher is faster but more jerky
      refresh: 30,
      // Whether to fit the network view after when done
      fit: true,
      // Padding on fit
      padding: 10,
      // Whether to enable incremental mode
      randomize: true,
      // Node repulsion (non overlapping) multiplier
      nodeRepulsion: 3000,
      // Ideal (intra-graph) edge length
      idealEdgeLength: 50,
      // Divisor to compute edge forces
      edgeElasticity: 0.45,
      // Nesting factor (multiplier) to compute ideal edge length for inter-graph edges
      nestingFactor: 0.1,
      // Gravity force (constant)
      gravity: 0.25,
      // Maximum number of iterations to perform
      numIter: 2500,
      // Whether to tile disconnected nodes
      tile: true,
      // Type of layout animation. The option set is {'during', 'end', false}
      animate: false,
      // Amount of vertical space to put between degree zero nodes during tiling (can also be a function)
      tilingPaddingVertical: 10,
      // Amount of horizontal space to put between degree zero nodes during tiling (can also be a function)
      tilingPaddingHorizontal: 10,
      // Gravity range (constant) for compounds
      gravityRangeCompound: 1.5,
      // Gravity force (constant) for compounds
      gravityCompound: 1.0,
      // Gravity range (constant)
      gravityRange: 3.8,
      // Initial cooling factor for incremental layout
      initialEnergyOnIncremental: 0.5
    }
}