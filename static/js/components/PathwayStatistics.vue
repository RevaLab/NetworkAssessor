<template>
    <div class="pathway-statistics">
        <modal v-bind:name="modalName">
            <pathway-members v-bind:pathway="pathway"/>
        </modal>
        <div class="tooltip">
            <a v-on:click="showPathwayMembers">{{ pathwayMemberCount }}</a>
            <span class="tooltiptext">Pathway Members</span>
        </div>
        <div class="tooltip">
            {{ pathwayEdgeCount }}
            <span class="tooltiptext">Edges between pathway and query list</span>
        </div>
        <div class="tooltip" v-if="pathwayPVal">
            {{ pathwayPVal }}
            <span class="tooltiptext">Significance</span>
        </div>
    </div>
</template>

<script>
    import pathwayMembers from './PathwayMembers.vue'

    export default {
        name: "pathway-statistics",
        data() {
            return {
            }
        },
        props: ['pathway'],
        components: {
            pathwayMembers
        },
        computed: {
            modalName() {
              return this.pathway + "_members"
            },
            pathwayEdgeCount() {
                return this.$store.state.pathwaysEdgeCounts[this.pathway];
            },
            pathwayPVal() {
                const pVal = this.$store.state.pathwaysPVals[this.pathway];
                if (pVal) {
                    if (pVal === 1) {
                        return 1
                    }
                    return pVal.toExponential(2)
                }
                return false;
            },
            pathwayMemberCount() {
                const userPathway = this.$store.state.userPathways[this.pathway];

                if (userPathway) {
                    return userPathway['genes'].length
                }

                return this.$store.state.pathwayMemberCounts[this.pathway]
            }
        },
        methods: {
            showPathwayMembers() {
                this.$modal.show(this.modalName)
            }
        }
    }
</script>

<style>
.tooltip {
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  /*z-index: 1;*/
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}

.pathway-statistics {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 50%;
  margin-left: 10px;
}

.pathway-statistics a {
  color: purple;
}

.pathway-statistics a:hover {
  text-decoration: underline;
}

</style>
