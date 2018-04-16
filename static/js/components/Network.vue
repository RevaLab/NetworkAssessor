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
    import cytoscapeOptions from '../src/cytoscapeOptions.js'

    cytoscape.use( coseBilkent );
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
                cytoscapeOptions.colorPathways(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
            },
            subnetwork() {
                this.runCytoscape(this.subnetwork, this.pathwayColors);
                cytoscapeOptions.colorPathways(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
                cytoscapeOptions.applyMouseEvents(cy);
            }
        },
        methods: {
            updateNetwork() {
                const queryGenesPathwayData = {
                    pathways: this.selectedPathways,
                    networkDatabase: this.$store.state.networkDatabase,
                    userPathways: this.$store.state.userPathways
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
                                'lineColor': 'gray'
                            }
                        }
                    ]
                };
                cy = cytoscape(cytoscape_options);
            }
        }
    }

</script>

<style>
    #cy {
        width: 100%;
        height: 95vh;
        display: block;
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