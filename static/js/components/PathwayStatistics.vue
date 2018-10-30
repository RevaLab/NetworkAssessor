<template>
    <div class="pathway-statistics">
        <div class=""></div>
        <modal v-bind:name="modalName">
            <pathway-members v-bind:pathway="pathway"/>
        </modal>
        <modal v-bind:name="overlapMembersModal">
            <h3 class="modal-header">{{ pathwayName }} &cap; Query List</h3>
            <div class="overlap-members">{{ overlap.join("\n") }}</div>
        </modal>
        <modal v-bind:name="queryListNetworkNodesModal">
            <h3 class="modal-header">Query List Genes with Interactions</h3>
            <div class="overlap-members">{{ queryListNetworkNodes.join("\n") }}</div>
        </modal>
        <modal v-bind:name="queryListNotInPPIModal">
            <h3 class="modal-header">Query List Genes not found in PPI db</h3>
            <div class="overlap-members">{{ queryGenesNotInPPI.join("\n") }}</div>
        </modal>
        <div class="tooltip">
            <a v-on:click="showPathwayMembers"
               v-on:mouseover="labelHover('Pathway Members: click for genes')"
               v-on:mouseleave="labelDoneHovering">
                {{ pathwayMemberCount }}
            </a>
            <span class="tooltiptext">Pathway Members</span>
        </div>

        <div class="tooltip" v-if="!notQueryList">
            <a v-on:click="showQueryListNotInPPI"
               v-on:mouseover="labelHover('Query list genes not found in PPI')"
               v-on:mouseleave="labelDoneHovering">
                {{ queryGenesNotInPPI.length }}
            </a>
            <span class="tooltiptext">Genes not in the PPI db</span>
        </div>

        <div class="tooltip" v-if="!notQueryList">
            <a v-on:click="showQueryListNetworkNodes"
               v-on:mouseover="labelHover('Query list genes with interactions')"
               v-on:mouseleave="labelDoneHovering">
                {{ queryListNetworkNodes.length }}
            </a>
            <span class="tooltiptext">Query list genes with interactions</span>
        </div>

        <div class="tooltip" v-if="notQueryList">
            <p
                v-on:mouseover="labelHover('Edges between pathway and query list')"
                v-on:mouseleave="labelDoneHovering"
            >
                {{ pathwayEdgeCount }}
            </p>
            <span class="tooltiptext">Edges between pathway and query list</span>
        </div>
        <div class="tooltip" v-if="notQueryList">
            <a v-on:click="showOverlap"
               v-on:mouseover="labelHover('Pathway \u2229 Query List: click for genes')"
               v-on:mouseleave="labelDoneHovering">
                {{ overlap.length }}
            </a>
            <span class="tooltiptext">Overlap between pathway and query list</span>
        </div>
        <div class="tooltip" v-if="pathwayPVal">
            <p
                v-on:mouseover="labelHover('Significance')"
                v-on:mouseleave="labelDoneHovering">
            {{ isMinPVal }}{{ pathwayPVal }}
            </p>
            <span class="tooltiptext">Significance</span>
        </div>
    </div>
</template>

<script>
    import pathwayMembers from './PathwayMembers.vue'
    import intersection from 'lodash/intersection.js'

    export default {
        name: "pathway-statistics",
        data() {
            return {
                isMinPVal: '',
                // overlap: 'overlap',
            }
        },
        props: ['pathway'],
        components: {
            pathwayMembers
        },
        computed: {
            pathwayName() {
                return this.$store.state.pathwayDisplayNames[this.pathway]
            },
            overlap() {
                let pathwayMembers = this.$store.state.pathwayMembers[this.pathway];
                if (this.pathway.indexOf('Chromatin_Remodeling') > -1) {
                    console.log(pathwayMembers)
                }
                let queryList = this.$store.state.userPathways['query_list']['genes'];
                return intersection(queryList, pathwayMembers)
            },
            queryListNetworkNodes() {
                return this.$store.state.queryListGenesInNetwork;
            },
            notQueryList() {
                return this.pathway !== 'query_list';
            },
            modalName() {
              return this.pathway + "_members"
            },
            overlapMembersModal() {
                return this.pathway + "_overlapMembers"
            },
            queryListNetworkNodesModal() {
                return this.pathway + "_query_list_members_modal"
            },
            queryListNotInPPIModal() {
                return this.pathway + "_query_list_not_in_ppi_modal"
            },
            queryGenesNotInPPI() {
                return this.$store.state.queryGenesNotInPPI;
            },
            pathwayEdgeCount() {
                return this.$store.state.pathwaysEdgeCounts[this.pathway];
            },
            pathwayPVal() {
                const pVal = this.$store.state.pathwaysPVals[this.pathway];
                if (pVal) {
                    if (pVal === .00001) {
                        this.isMinPVal = '< '
                    }
                    if (pVal >= .05) {
                        return pVal
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
            },
            showOverlap() {
                this.$modal.show(this.overlapMembersModal)
            },
            showQueryListNetworkNodes() {
                // if (!this.notQueryList) {
                    this.$modal.show(this.queryListNetworkNodesModal)
                // }
            },
            showQueryListNotInPPI() {
                    this.$modal.show(this.queryListNotInPPIModal)
            },
            labelHover(label) {
                this.$store.dispatch('updateLabelHover', label)
            },
            labelDoneHovering() {
                this.$store.dispatch('updateLabelHover', 'Hover over number for details')
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
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}

.pathway-statistics {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 50%;
  margin-left: 10px;
}

.pathway-statistics a {
  color: purple;
}

.pathway-statistics a:hover {
  text-decoration: underline;
}

.overlap-members {
    margin: 10px;
    padding: 10px;
    white-space: pre;
}

.modal-header {
    /*margin: 0 auto;*/
    text-align: center;
    padding-top: 5px;
}

    .tooltip p {
        cursor: default;
    }
</style>
