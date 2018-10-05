<template>
    <div class="network">
        <div id="cy"></div>
        <!--<div class="statistics">-->
            <!--<div class="statistics-content">-->
                <!--<p><b>Nodes:</b> {{ networkStatistics.nodeLength }}</p>-->
                <!--<p><b>Edges:</b> {{ networkStatistics.edgesLength }}</p>-->
            <!--</div>-->
        <!--</div>-->
        <div v-if="loading" class="loading">Loading&#8230;</div>
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
                loading: true,
            }
        },
        components: {
        },
        computed: {
            queryGenes() {
              return this.$store.state.userPathways['query_list']['genes']
            },
            networkDatabase() {
              return this.$store.state.networkDatabase;
            },
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
                        nodeLength: this.subnetwork['elements']['nodes'].length - this.isolateCount,
                        edgesLength: this.subnetwork['elements']['edges'].length
                    };
                }

                return statistics;
            },
        },
        watch: {
            userPathways() {
                this.updateNetwork();
            },
            selectedPathways() {
                this.updateNetwork();
            },
            networkDatabase() {
                this.updateNetwork();
            },
            pathwayColors() {
                cytoscapeOptions.colorPathwaysAndCheckForQLAndPWHits(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
                cytoscapeOptions.colorQueryGeneEdges(cy, this.queryGenes, this.pathwayColors['query_list']);
                cytoscapeOptions.applyMouseEvents(cy, this.queryGenes, this.pathwayColors['query_list']);
            },
            subnetwork() {
                // let
                if (!this.pathwayColors) {
                    return;
                }
                this.runCytoscape(this.subnetwork, this.pathwayColors);
                const { queryListAndPWHit, queryListGenesInNetwork } = cytoscapeOptions.colorPathwaysAndCheckForQLAndPWHits(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
                cytoscapeOptions.applyMouseEvents(cy, this.queryGenes, this.pathwayColors['query_list']);
                cytoscapeOptions.colorQueryGeneEdges(cy, this.queryGenes, this.pathwayColors['query_list']);
                this.$store.dispatch('updateQueryListAndPathwayHit', queryListAndPWHit);
                this.$store.dispatch('updateQueryListGenesInNetwork', queryListGenesInNetwork);
                cytoscapeOptions.addRelationsToEdges(cy);
            }
        },
        methods: {
            updateNetwork() {
                this.loading = true;
                const queryGenesPathwayData = {
                    pathways: this.$store.state.selectedPathways,
                    networkDatabase: this.$store.state.networkDatabase,
                    userPathways: this.$store.state.userPathways,
                };

                this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
            },
            runCytoscape(subnetwork) {
                // console.log('running cytoscape')
                let cytoscape_options = {
                    ...subnetwork,
                    container: document.getElementById('cy'),
                    layout: {
                        name: 'cose-bilkent',
                        ...cytoscapeOptions.coseOptions,
                        spacingFactor: 0,
                        // padding: 0,
                        condense: true
                    },
                    style: [
                        {
                            selector: 'node',
                            style: {
                                'label': 'data(id)',
                                // 'lineColor': '#b7b7b7',
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                // 'color': '#b7b7b7',
                                'width': '0.08em',
                            }
                        }
                    ]
                };
                cy = cytoscape(cytoscape_options);

                let count = 0;
                // REMOVES ISOLATES
                cy.nodes().forEach(node => {
                    if (node.neighborhood().length === 0) {
                        cy.remove(node);
                        count += 1;
                    }
                });
                this.isolateCount = count;
                cy.fit();
                // cy.center(cy.nodes());
                this.loading = false;
            }
        }
    }

</script>

<style>
    #cy {
        width: 100%;
        height: 90%;
        border: solid 1px black;
    }

    .network {
      width: 100%;
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

    /*LOADING CSS*/

    /* Absolute Center Spinner */
    .loading {
      position: fixed;
      z-index: 999;
      height: 2em;
      width: 2em;
      overflow: show;
      margin: auto;
      top: 0;
      left: 0;
      bottom: 0;
      right: 0;
    }

    /* Transparent Overlay */
    .loading:before {
      content: '';
      display: block;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0,0,0,0.3);
    }

    /* :not(:required) hides these rules from IE9 and below */
    .loading:not(:required) {
      /* hide "loading..." text */
      font: 0/0 a;
      color: transparent;
      text-shadow: none;
      background-color: transparent;
      border: 0;
    }

    .loading:not(:required):after {
      content: '';
      display: block;
      font-size: 10px;
      width: 1em;
      height: 1em;
      margin-top: -0.5em;
      -webkit-animation: spinner 1500ms infinite linear;
      -moz-animation: spinner 1500ms infinite linear;
      -ms-animation: spinner 1500ms infinite linear;
      -o-animation: spinner 1500ms infinite linear;
      animation: spinner 1500ms infinite linear;
      border-radius: 0.5em;
      -webkit-box-shadow: rgba(0, 0, 0, 0.75) 1.5em 0 0 0, rgba(0, 0, 0, 0.75) 1.1em 1.1em 0 0, rgba(0, 0, 0, 0.75) 0 1.5em 0 0, rgba(0, 0, 0, 0.75) -1.1em 1.1em 0 0, rgba(0, 0, 0, 0.5) -1.5em 0 0 0, rgba(0, 0, 0, 0.5) -1.1em -1.1em 0 0, rgba(0, 0, 0, 0.75) 0 -1.5em 0 0, rgba(0, 0, 0, 0.75) 1.1em -1.1em 0 0;
      box-shadow: rgba(0, 0, 0, 0.75) 1.5em 0 0 0, rgba(0, 0, 0, 0.75) 1.1em 1.1em 0 0, rgba(0, 0, 0, 0.75) 0 1.5em 0 0, rgba(0, 0, 0, 0.75) -1.1em 1.1em 0 0, rgba(0, 0, 0, 0.75) -1.5em 0 0 0, rgba(0, 0, 0, 0.75) -1.1em -1.1em 0 0, rgba(0, 0, 0, 0.75) 0 -1.5em 0 0, rgba(0, 0, 0, 0.75) 1.1em -1.1em 0 0;
    }

    /* Animation */

    @-webkit-keyframes spinner {
      0% {
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
      }
      100% {
        -webkit-transform: rotate(360deg);
        -moz-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        -o-transform: rotate(360deg);
        transform: rotate(360deg);
      }
    }
    @-moz-keyframes spinner {
      0% {
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
      }
      100% {
        -webkit-transform: rotate(360deg);
        -moz-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        -o-transform: rotate(360deg);
        transform: rotate(360deg);
      }
    }
    @-o-keyframes spinner {
      0% {
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
      }
      100% {
        -webkit-transform: rotate(360deg);
        -moz-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        -o-transform: rotate(360deg);
        transform: rotate(360deg);
      }
    }
    @keyframes spinner {
      0% {
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -ms-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
      }
      100% {
        -webkit-transform: rotate(360deg);
        -moz-transform: rotate(360deg);
        -ms-transform: rotate(360deg);
        -o-transform: rotate(360deg);
        transform: rotate(360deg);
      }
    }
</style>
