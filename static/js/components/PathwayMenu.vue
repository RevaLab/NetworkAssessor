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
          pathways() {
              const pathways =
                  this.predefinedPathways ?
                    this.$store.state.predefinedPathways :
                    Object.keys(this.$store.state.userPathways);
              const pathwaysEdgeCounts = this.$store.state.pathwaysEdgeCounts;
              const networkDegree = this.$store.state.networkDegree;

              let sortable = [];
              let ordered_pathways = [];

              pathways.forEach(pathway => {
                    if (pathway === 'query_list') {
                        ordered_pathways.push('query_list');
                        return;
                    }
                    sortable.push(
                        [
                            pathway,
                            pathwaysEdgeCounts[pathway][networkDegree]
                        ]
                    );
              });

              sortable.sort(function(a, b) {
                    return b[1] - a[1];
              });

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
            PathwayColorSelector
        }
    }
</script>

<style>
    .pathway-menu {
        /*border: solid red 1px;*/
        display: flex;
        flex-direction: column;
        padding: 0;
    }

    ul {
        overflow: auto;
        margin-left: 0;
        padding: 0;
        /*border: solid 1px purple;*/
    }

    #pathways-ul {
        padding: 0;
        margin: auto 5px;
    }

    li {
        list-style-type: none;
        width: 100%;
        /*border: solid 1px green;*/
        padding: 0;
    }

</style>