<template>
    <div class="network">
        <div v-if="subnetwork">
            <div id="cy"></div>
            <div class="statistics">
                <div class="statistics-content">
                    <p>Nodes: {{ networkStatistics.nodeLength }}</p>
                    <p>Edges: {{ networkStatistics.edgesLength }}</p>
                </div>
            </div>
        </div>
        <div v-else>Loading...</div>
    </div>
</template>

<script>
    const cytoscape = require('cytoscape');
    let cy;

    export default {
        name: "network",
        data() {
            return {
                // loading: true
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

                // if (currentSub) {
                //     statistics.nodeLength = 'CALCULATE ME';
                //     statistics.edgesLength = 'CALCULATE ME';
                // }

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
                name: 'cose'
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

    // function changeQueryGenes

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
        border: solid 1px black;
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