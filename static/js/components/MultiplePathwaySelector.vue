<template>
  <div class="multiple-pathway-selector">
    <div class="label-and-swatch multi-selector">
      <a class="button is-small" v-on:click="clearSelection">Clear</a>
    </div>
  </div>
</template>

<script>
    export default {
        name: "multiple-pathway-selector",
        methods: {
          clearSelection() {
            const userPathways = this.$store.state.userPathways;
            const selectedPathways = this.$store.state.selectedPathways.slice();
            let selectedUserPathways = [];

            Object.keys(userPathways).forEach((pathway) => {
                if (selectedPathways.includes(pathway)) {
                    selectedUserPathways.push(pathway)
                }
            });

            this.$store.dispatch('updateSelectedPathways', selectedUserPathways);
          }
        },
        computed: {
            allChecked: {
                get() {

                    const pathwaysEdgeCounts = Object.assign({}, this.$store.state.pathwaysEdgeCounts);
                    const predefinedPathways = this.$store.state.predefinedPathways.slice();
                    const selectedPathways = this.$store.state.selectedPathways.slice();

                    // this means
                    if (selectedPathways.length === 1) {
                        return false;
                    }

                    let notAllPathwaysSelected = true;
                    // return false if a pathway has edges and is not selected
                    notAllPathwaysSelected = predefinedPathways.some((pathway) => {
                        return (
                            pathwaysEdgeCounts[pathway]
                            && (!selectedPathways.includes(pathway))
                        )
                    });
                    return !notAllPathwaysSelected;
                },
                set(checkedVal) {
                    let pathwaysWithEdgesAndSelectedUserPathways = [];
                    const selectedPathways = this.$store.state.selectedPathways.slice();
                    const userPathways = this.$store.state.userPathways;

                    Object.keys(userPathways).forEach((pathway) => {
                        if (selectedPathways.includes(pathway)) {
                            pathwaysWithEdgesAndSelectedUserPathways.push(pathway)
                        }
                    });

                    if (checkedVal) {
                        const pathwaysEdgeCounts = Object.assign({}, this.$store.state.pathwaysEdgeCounts);
                        const predefinedPathways = this.$store.state.predefinedPathways.slice();

                        predefinedPathways.forEach((pathway) => {
                            if (pathwaysEdgeCounts[pathway]) {
                                pathwaysWithEdgesAndSelectedUserPathways.push(pathway)
                            }
                        });
                    }

                    this.$store.dispatch('updateSelectedPathways', pathwaysWithEdgesAndSelectedUserPathways);
                    // return checkedVal;

                }
            }
        },
        mounted() {
            this.allChecked = false;
        }
    }
</script>

<style>
.multiple-pathway-selector {
    display: flex;
    flex-direction: row;
}

    .multi-selector {
        margin: auto;
    }
</style>
