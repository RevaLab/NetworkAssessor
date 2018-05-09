<template>
  <div class="pathway-color-selector">
    <div class="pathway">
      <div class="pathway-label">
        <input type="checkbox" id="pw-checkbox" v-model="checked" />
        <label for="pw-checkbox">{{ pathwayName }}</label>
      </div>
      <swatches
      class="pathway-swatch"
      v-model="color"
      colors="text-advanced"
      popover-to="right"
      shapes="circles"
      row-length="5"
      :trigger-style="triggerStyle"
      />
      <pathway-statistics v-bind:pathway="pathway"/>
      <a class="delete" v-on:click="removeUserPathway" v-if="userPathway"></a>
    </div>
  </div>
</template>

<script>
import Swatches from 'vue-swatches'
import "vue-swatches/dist/vue-swatches.min.css"
import pathwayStatistics from './PathwayStatistics.vue'

export default {
  name: "network-controls",
  data() {
    return {
      triggerStyle: {
        width: '20px',
        height: '20px',
        margin: '5px',
      }
    }
  },
  props: ['pathway'],
  computed: {
    pathwayName() {
      const displayNames = this.$store.state.pathwayDisplayNames;
      return displayNames[this.pathway]
    },
    userPathway() {
      return this.$store.state.userPathways[this.pathway]
    },
    checked: {
      get() {
        let selectedPathways = this.$store.state.selectedPathways;
        return selectedPathways.includes(this.pathway)
      },
      set() {
        let selectedPathways = this.$store.state.selectedPathways;
        let previousSelectedPathways = selectedPathways.slice(1);
        this.$store.dispatch('holdPreviousSelectedPathways', previousSelectedPathways)

        const isNotSelected = !selectedPathways.includes(this.pathway);

        if (isNotSelected) {
          selectedPathways = selectedPathways.concat([this.pathway]);
        } else {
          let pw_index = selectedPathways.indexOf(this.pathway);
          selectedPathways.splice(pw_index, 1);
        }

        this.$store.dispatch('updateSelectedPathways', selectedPathways);
      }
    },
    color: {
      get() {
        return this.$store.state.pathwayColors[this.pathway]
      },
      set(hexValue) {
        let pathwayColorData = {};
        pathwayColorData[this.pathway] = hexValue;

        this.$store.dispatch('updatePathwayColors', pathwayColorData)
      }
    },
    // triggerStyle() {
    //     let styleOptions = {
    //         width: '20px',
    //         height: '20px',
    //         margin: '5px',
    //     };
    //
    //     if (this.queryList) {
    //         // renders query list selector as a square
    //       styleOptions['border-radius'] = '0px'
    //     }
    //
    //     return styleOptions;
    // },
    // queryList () {
    //     return this.pathway === 'query_list';
    // }
  },
  components: {
    Swatches,
    pathwayStatistics
  },
  methods: {
    removeUserPathway() {
      const pathway = this.pathway;
      let userPathways = Object.assign({}, this.$store.state.userPathways);

      // remove user pathway from list in store
      delete userPathways[pathway];
      this.$store.dispatch('updateUserPathways', userPathways);

      // remove user pathway display data
      const displayData = {
        pathways: {},
        add: false
      };
      displayData['pathways'][pathway] = pathway;

      this.$store.dispatch(
        'updateUserPathwayDisplay',
        displayData
      );

      // remove user pathway from selected pathways
      let selectedPathways = this.$store.state.selectedPathways.slice();
      let pw_index = selectedPathways.indexOf(pathway);
      if (pw_index !== -1) {
        selectedPathways.splice(pw_index, 1);
        this.$store.dispatch('updateSelectedPathways', selectedPathways)
      }

      // update pathways in local storage
      this.$ls.set('userPathways', JSON.stringify(userPathways));
    }
  }
}
</script>

<style>

.vue-swatches {
  position: inherit;
  height: 25px;
}

.vue-swatches__container {
  margin-left: 200px;
}

.pathway {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  align-items: center;
  padding: 7px 0;
}

.pathway-color-selector {
  display: flex;
  flex-direction: row;
}

.pathway-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: left;
  width: 65%;
}

.pathway-label:hover {
  cursor: pointer;
}

.pathway-label input {
  cursor: inherit;
}

.pathway-label label {
  cursor: inherit;
}

#pw-checkbox {
  margin-right: 10px;
}
</style>
