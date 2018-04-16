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
            <p v-if="pathwayEdgesReady">{{ pathwayEdgeCount }}</p>
            <span class="tooltiptext">Total edges if this pathway is added</span>
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
            pathwayEdgesReady() {
              return this.$store.state.pathwaysEdgeCounts[this.pathway]
            },
            pathwayEdgeCount() {
                const networkDegree = this.$store.state.networkDegree;

                return this.$store.state.pathwaysEdgeCounts[this.pathway][networkDegree];
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
        border-bottom: 1px dotted black;
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
        justify-content: right;
    }

</style>