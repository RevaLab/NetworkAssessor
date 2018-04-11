<template>
    <div class="pathway-statistics">
        <modal name="pathway-members" class="pathway-members-modal">OKAY
        </modal>
        <div class="tooltip">
            <a v-on:click="showPathwayMembers">{{ pathwayMemberCount }}</a>
            <span class="tooltiptext">Pathway Members</span>
        </div>
        <div class="tooltip">
            <p v-if="pathwayEdgesReady">{{ pathwayEdgeCount }}</p>
            <span class="tooltiptext">Additional edges if you add this pw</span>
        </div>
    </div>
</template>

<script>
    export default {
        name: "pathway-statistics",
        data() {
            return {}
        },
        props: ['pathway'],
        computed: {
            pathwayEdgesReady() {
              return this.$store.state.pathwaysEdgeCounts[this.pathway]
            },
            pathwayEdgeCount() {
                const subnetwork = this.$store.state.subnetwork;
                const networkDegree = this.$store.state.networkDegree;

                const currentSub = subnetwork[networkDegree];

                const edgesLength = currentSub["links"].length;

                return this.$store.state.pathwaysEdgeCounts[this.pathway][networkDegree] - edgesLength;
            },
            pathwayMemberCount() {
                return this.$store.state.pathwayMemberCounts[this.pathway]
            },
        },
        methods: {
            showPathwayMembers() {
                this.$modal.show('pathway-members')
            }
        }
    }
</script>

<style>
    .tooltip {
    /*position: relative;*/
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