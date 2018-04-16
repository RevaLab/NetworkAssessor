<template>
    <div class="network">
        <div v-if="subnetwork">
            <div id="cy"></div>
            <div class="statistics">
                <div class="statistics-content">
                    <p><b>Nodes:</b> {{ networkStatistics.nodeLength }}</p>
                    <p><b>Edges:</b> {{ networkStatistics.edgesLength }}</p>
                </div>
            </div>
        </div>
        <div v-else>Loading...</div>
    </div>
</template>

<script>
    import cytoscape from 'cytoscape';
    import coseBilkent from 'cytoscape-cose-bilkent';

    cytoscape.use( coseBilkent );
    // const cytoscape = require('cytoscape');
    let cy;

    export default {
        name: "network",
        data() {
            return {
            }
        },
        computed: {
            userPathways() {
                return this.$store.state.userPathways;
            },
            selectedPathways() {
                return this.$store.state.selectedPathways;
            },
            subnetwork() {
                let networkDegree = this.$store.state.networkDegree;
                return this.$store.state.subnetwork[networkDegree];
            },
            pathwayColors() {
                return this.$store.state.pathwayColors;
            },
            networkStatistics() {
                let statistics = {
                    nodeLength: 'calculating...',
                    edgesLength: 'calculating...'
                };

                if (this.subnetwork['elements']['nodes'].length) {
                    statistics = {
                        nodeLength: this.subnetwork['elements']['nodes'].length,
                        edgesLength: this.subnetwork['elements']['edges'].length
                    };
                }

                return statistics;
            },
        },
        watch: {
            userPathways() {
                this.updateNetwork()
            },
            selectedPathways() {
                this.updateNetwork()
            },
            pathwayColors() {
              colorPathways(this.subnetwork, this.pathwayColors, this.selectedPathways);
            },
            subnetwork() {
                runCytoscape(this.subnetwork, this.pathwayColors);
                colorPathways(this.subnetwork, this.pathwayColors, this.selectedPathways);
            }
        },
        mounted() {
            runCytoscape(this.$store.state.subnetwork)
        },
        methods: {
            updateNetwork() {
                const queryGenesPathwayData = {
                    pathways: this.selectedPathways,
                    networkDatabase: this.$store.state.networkDatabase,
                    userPathways: this.$store.state.userPathways
                };
                this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
            }
        }
    }

    function runCytoscape(subnetwork) {
        let cytoscape_options = {
            ...subnetwork,
            container: document.getElementById('cy'),
            layout: {
                name: 'cose-bilkent',
                ...defaultOptions
            },
            style: [
                {
                    selector: 'node',
                    style: {
                        'label': 'data(id)',
                    }
                }
            ]
        };
        cy = cytoscape(cytoscape_options);
    }

    function colorPathways(subnetwork, pathwayColors, selectedPathways) {
        cy.nodes().forEach(node => {
            node.data('pathways').forEach( pathway => {
                if (selectedPathways.includes(pathway)) {
                    if ( pathway === 'query_list' ) {
                        node.style('shape', 'rectangle')
                    } else {
                        node.style('shape', 'ellipse')
                    }
                    node.style('background-color', pathwayColors[pathway]);
                }
            })
        });
    }

    const defaultOptions = {
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
      nodeRepulsion: 4500,
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
    };

</script>

<style>
    #cy {
        width: 100%;
        height: 95vh;
      /*width: 1000px;*/
      /*height: 1000px;*/
      display: block;
        /*background-color: pink;*/
    }
    .network {
        width: 78%;
    }

    .statistics {
        width: 10%;
        height: 10%;
        /*border: solid 1px black;*/
        position:absolute;
        bottom:0;
        right:0;
        margin-bottom: 10px;
        margin-right: 10px;
    }

    .statistics-content {
        position: relative;
        float: left;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .statistics-content p {
        margin-bottom: 0 !important;
    }
</style>