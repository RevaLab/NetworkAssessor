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

            <div class="network-legend">
                <div class="network-legend-content">
                    <h6>Legend</h6>
                    <ul>
                        <li>
                            <span>
                                <i class="fas fa-star star-icon" :style="starColor"></i>
                                Query List & Pathway
                            </span>
                        </li>
                        <li v-for="(pathway, index) in selectedPathways" :key="index">
                                <span>
                                    <div v-if="pathway==='query_list'" class="color-box" v-bind:style="{ background: pathwayColors[pathway] }"></div>
                                    <div v-else class="color-box circle" v-bind:style="{ background: pathwayColors[pathway] }"></div>
                                    {{ pathwayDisplayNames[pathway] }}
                                </span>
                        </li>
                    </ul>
                </div>
            </div>

        </div>
        <div v-else>Loading...</div>
    </div>
</template>

<script>
    import cytoscape from 'cytoscape';
    import coseBilkent from 'cytoscape-cose-bilkent';
    import cytoscapeOptions from '../src/cytoscapeOptions.js'

    cytoscape.use( coseBilkent );
    let cy;

    export default {
        name: "network",
        data() {
            return {
                isolateCount: 0,
            }
        },
        computed: {
            starColor() {
                const queryListColor = this.$store.state.pathwayColors['query_list']
                return { color: queryListColor}
            },
            networkDatabase() {
              return this.$store.state.networkDatabase;
            },
            pathwayDisplayNames() {
                return this.$store.state.pathwayDisplayNames;
            },
            userPathways() {
                return this.$store.state.userPathways;
            },
            selectedPathways() {
                return this.$store.state.selectedPathways;
            },
            subnetwork() {
                let networkDegree = this.$store.state.networkDegree;
                // let networkDegree = 'first_degree';
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
                        nodeLength: this.subnetwork['elements']['nodes'].length - this.isolateCount,
                        edgesLength: this.subnetwork['elements']['edges'].length
                    };
                }

                return statistics;
            },
        },
        watch: {
            userPathways() {
                // must hit this to calculate the pathway edge counts for this user pw
                this.updateNetwork()
            },
            selectedPathways() {
                this.updateNetwork()
            },
            networkDatabase() {
                this.updateNetwork()
            },
            pathwayColors() {
                cytoscapeOptions.colorPathways(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
            },
            subnetwork() {
                this.runCytoscape(this.subnetwork, this.pathwayColors);
                cytoscapeOptions.colorPathways(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
                cytoscapeOptions.applyMouseEvents(cy);
                this.isolateCount = cytoscapeOptions.hideIsolateNodes(cy);
            }
        },
        mounted() {
            this.updateNetwork()
        },
        methods: {
            updateNetwork() {
                const queryGenesPathwayData = {
                    pathways: this.$store.state.selectedPathways,
                    networkDatabase: this.$store.state.networkDatabase,
                    userPathways: this.$store.state.userPathways,
                };

                this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
            },
            runCytoscape(subnetwork) {
                let cytoscape_options = {
                    ...subnetwork,
                    container: document.getElementById('cy'),
                    layout: {
                        name: 'cose-bilkent',
                        ...cytoscapeOptions.coseOptions
                    },
                    style: [
                        {
                            selector: 'node',
                            style: {
                                'label': 'data(id)',
                                'lineColor': '#b7b7b7',
                                // 'width': '1px',
                                // "text-valign" : "center",
                                // "text-halign" : "center",
                                // 'color': 'white',
                                // 'text-outline-width': '2px',
                                // 'text-outline-opacity': '1',
                                // 'text-outline-color': 'black'
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                'color': '#b7b7b7',
                                'width': '0.08em',
                                'stroke-opacity': '0.9'
                            }
                        }
                    ]
                };
                cy = cytoscape(cytoscape_options);
                cy.nodes().forEach(node => {
                    if (node.neighborhood().length === 0) {
                        cy.remove(node);
                    }
                });
                cy.fit()
            }
        }
    }

</script>

<style>
    #cy {
        width: 100%;
        height: 95vh;
    }

    .network {
        width: 78%;
        height: 100%;
    }

    .statistics {
        width: 10%;
        height: 10%;
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

    .network-legend {
        width: 10%;
        height: auto;
        position:absolute;
        top:0;
        right:0;
        margin-top: 50px;
        margin-right: 50px;
        border: solid 1px black;
        padding-left: 2px;
        /*background-color: #6DDCBD;*/
    }

    .network-legend-content ul {
        width: auto;
        height: 90%;
        margin: auto;
        font-size: small;
        /*transform: translate(-50%, -50%);*/
    }

    /*.network-legend-content li {*/
        /*display: inline-block;*/
        /*!*transform: translate(-50%, -50%);*!*/
    /*}*/
    .color-box {
      float: left;
      width: 20px;
      height: 20px;
      margin-right: 5px;
      border: 1px solid rgba(0, 0, 0, .2);
        /*border-radius: 50%;*/
    }

    .circle {
        border-radius: 50%;
    }

    .star-icon {
        /*color: #00ff00;*/
        font-size: 20px;
    }

</style>