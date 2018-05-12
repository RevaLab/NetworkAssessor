<template>
  <div class="network">
    <div id="cy"></div>
    <!--<div class="statistics">-->
    <!--<div class="statistics-content">-->
    <!--<p><b>Nodes:</b> {{ networkStatistics.nodeLength }}</p>-->
    <!--<p><b>Edges:</b> {{ networkStatistics.edgesLength }}</p>-->
    <!--</div>-->
    <!--</div>-->
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
      cytoscapeOptions.colorPathwaysAndCheckForQLAndPWHits(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
      cytoscapeOptions.colorQueryGeneEdges(cy, this.queryGenes, this.pathwayColors['query_list']);
    },
    subnetwork() {
      // let
      if (!this.pathwayColors) {
        return;
      }
      this.runCytoscape(this.subnetwork, this.pathwayColors);
      const queryListAndPWHit = cytoscapeOptions.colorPathwaysAndCheckForQLAndPWHits(this.subnetwork, this.pathwayColors, this.selectedPathways, cy);
      cytoscapeOptions.applyMouseEvents(cy, this.queryGenes, this.pathwayColors['query_list']);
      cytoscapeOptions.colorQueryGeneEdges(cy, this.queryGenes, this.pathwayColors['query_list']);
      this.$store.dispatch('updateQueryListAndPathwayHit', queryListAndPWHit)
    }
  },
  mounted() {
    // this.updateNetwork();
  },
  beforeUpdate(){
  },
  updated() {
    // this.loading = false;
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
      cy.nodes().forEach(node => {
        if (node.neighborhood().length === 0) {
          cy.remove(node);
          count += 1;
        }
      });
      this.isolateCount = count;
      cy.fit();
      // cy.center(cy.nodes());
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
  width: 100%;
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

</style>
