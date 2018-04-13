<template>
    <div class="network" id="network-test">
        <div v-if="subnetwork">
            <button v-on:click="getPathwaySubnetwork">SUBNETWORK</button>
            <div id="cy"></div>
            <div class="statistics">
                <div class="statistics-content">
                    <p>Nodes: {{ networkStatistics.nodeLength }}</p>
                    <p>Edges: {{ networkStatistics.edgesLength }}</p>
                </div>
            </div>
            <div id="loader-bg">
                <div id="loader"></div>
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
            subnetwork() {
                return this.$store.state.subnetwork;
            },
            pathwayColors() {
                return this.$store.state.pathwayColors;
            },
            networkDegree() {
                return this.$store.state.networkDegree;
            },
            networkStatistics() {
                const subnetwork = this.$store.state.subnetwork;
                const networkDegree = this.$store.state.networkDegree;
                let statistics = {
                    nodeLength: 0,
                    edgesLength: 0
                };

                const currentSub = subnetwork[networkDegree];

                if (currentSub) {
                    statistics.nodeLength = currentSub["nodes"].length;
                    statistics.edgesLength = currentSub["links"].length;
                }

                return statistics;
            },

        },
        watch: {
            pathwayColors() {
              colorPathways(this.$store.state.subnetwork, this.$store.state.pathwayColors)
            },
            subnetwork() {
                runCytoscape(this.$store.state.subnetwork, this.$store.state.pathwayColors)
                colorPathways(this.$store.state.subnetwork, this.$store.state.pathwayColors)
            }
        },
        methods: {
          getPathwaySubnetwork() {
              this.$store.dispatch('getPathwaySubnetwork')
          }
        },
        updated() {
            let loader = document.getElementById('loader-bg');
            loader.style.visibility = 'hidden';
        },
        mounted() {
            runCytoscape(this.$store.state.subnetwork)
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

    function colorPathways(subnetwork, pathwayColors) {
        cy.nodes().forEach(node => {
            if (node.data('pathways')) {
                let firstPathway = node.data('pathways')[0];
                node.style('background-color', pathwayColors[firstPathway]);
            }
        });
    }

</script>

<style>
    #cy {
      width: 1000px;
      height: 1000px;
      display: block;
        background-color: pink;
    }
    .network {
        width: 78%;
    }

    .loader {
        position: absolute;
        left: 0;
        top: 0;
        right: 0;
        bottom: 0;
        margin: auto;
        width: 8em;
        height: 8em;
    }

    #loader-bg {
        visibility: none;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0);
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