<template>
    <div class="multiple-pathway-selector">
            <div class="label-and-swatch">
                <input type="checkbox" id="pw-checkbox" v-model="checked" />
                Select All With Edges
            </div>
    </div>
</template>

<script>
    export default {
        name: "multiple-pathway-selector",
        computed: {
            checked: {
                get() {
                    const pathwaysEdgeCounts = Object.assign({}, this.$store.state.pathwaysEdgeCounts);
                    const predefinedPathways = this.$store.state.predefinedPathways.slice();
                    const selectedPathways = this.$store.state.selectedPathways.slice();

                    // return false if a pathway has edges and is not selected
                    const notAllPathwaysSelected = predefinedPathways.some((pathway) => {
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
                        if (selectedPathways.indexOf(pathway) !== -1) {
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
                }
            }
        }
    }
</script>

<style>
.multiple-pathway-selector {
    border: solid 1px yellow;
}
</style>