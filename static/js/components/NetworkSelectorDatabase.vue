<template>
  <div class="db-selector">
    <p>PPI Database:</p>
    <div class="radio-group">
      <input type="radio" id="biogrid" value="biogrid" v-model="picked">
      <label for="biogrid">BioGRID</label>
    </div>
    <div class="radio-group">
      <input type="radio" id="hprd" value="hprd" v-model="picked">
      <label for="hprd">HPRD</label>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
    }
  },
  computed: {
    picked: {
      get() {
        return this.$store.state.networkDatabase
      },
      set(database) {
        // const pathways = this.$store.state.selectedPathways;
        // const queryGenes = this.$store.state.geneInput;
        // const userPathways = this.$store.state.userPathways;
        //
        // const queryGenesPathwayData = {
        //     pathways,
        //     queryGenes,
        //     userPathways,
        //     networkDatabase: database
        // };

        this.$store.dispatch('updateDatabase', database);
        // this.$store.dispatch('getPathwaySubnetwork', queryGenesPathwayData);
      }
    }
  },
  updated() {
  }
}
</script>

<style>
.db-selector {
  padding: 10px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.radio-group-container {
  display: flex;
  flex-direction: column;
}

</style>
