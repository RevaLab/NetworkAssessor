<template>
  <div class="pathway-menu">
    <ul id="pathways-ul">
      <li v-for="pathway in pathways">
        <pathway-color-selector v-bind:pathway="pathway"/>
      </li>
    </ul>
  </div>
</template>

<script>
import PathwayColorSelector from './PathwayColorSelector.vue'

export default {
  name: "pathway-menu",
  props: ['predefinedPathways'],
  computed: {
    // userPathways() {
    //     return this.$store.state.userPathways;
    // }
    pathways() {
      const userPathways = this.$store.state.userPathways;
      const pathways =
      this.predefinedPathways ?
      this.$store.state.predefinedPathways :
      Object.keys(userPathways);

      const pathwaysEdgeCounts = this.$store.state.pathwaysEdgeCounts;
      const pathwaysPVals = this.$store.state.pathwaysPVals;

      let sortable = [];
      let ordered_pathways = [];

      // if (this.predefinedPathways) {
      //     ordered_pathways.push('query_list')
      // }

      pathways.forEach(pathway => {
        if (pathway === 'query_list') {
          // ordered_pathways.push('query_list');
          return;
        }
        if (this.predefinedPathways) {
          sortable.push(
            [
              pathway,
              pathwaysPVals[pathway]
            ]
          );
        } else {
          sortable.push(
            [
              pathway,
              pathwaysEdgeCounts[pathway]
            ]
          );
        }
      });

      if (this.predefinedPathways) {
        sortable.sort(function(a, b) {
          return a[1] - b[1];
        });
      } else {
        sortable.sort(function(a, b) {
          return b[1] - a[1];
        });
      }

      sortable.forEach(pathway => {
        ordered_pathways.push(pathway[0])
      });
      return ordered_pathways;
    }
  },
  data() {
    return {
    }
  },
  components: {
    PathwayColorSelector,
  }
}
</script>

<style>
.pathway-menu {
  display: flex;
  flex-direction: column;
  padding: 0;
  background-color: lightgrey;
}

ul {
  margin-left: 0;
  padding: 0;
}

#pathways-ul {
  padding: 0;
  margin: auto 5px;
}

li {
  list-style-type: none;
  width: 100%;
  padding: 0;
}

</style>
