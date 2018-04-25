<template>
    <div class="network-legend">
        <div class="network-legend-content">
            <h6>Legend</h6>
            <ul>
                <li>
                    <span>
                        <i class="fas fa-star star-icon" :style="starColor"></i>
                        Query List & Pathway
                    </span>
                </li>
                <li v-for="(pathway, index) in selectedPathways" :key="index">
                        <span>
                            <div v-if="pathway==='query_list'" class="color-box" v-bind:style="{ background: pathwayColors[pathway] }">
                            </div>
                            <div v-else class="color-box circle" v-bind:style="{ background: pathwayColors[pathway] }">
                            </div>
                        </span>
                    {{ pathwayDisplayNames[pathway] }} <i v-if="pathway !== 'query_list'">: {{pathwaysPValsScientificNotation[pathway]}}</i>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: "network-legend",
        computed: {
            pathwayColors() {
                return this.$store.state.pathwayColors;
            },
            pathwayDisplayNames() {
                return this.$store.state.pathwayDisplayNames;
            },
            selectedPathways() {
                return this.$store.state.selectedPathways;
            },
            starColor() {
                const queryListColor = this.$store.state.pathwayColors['query_list']
                return { color: queryListColor}
            },
            pathwaysPValsScientificNotation() {
                let pathwaysPValsScientificNotation = {};
                const pVals = this.$store.state.pathwaysPVals;
                for (let pathway in pVals) {
                        let pVal = pVals[pathway];
                        if (pVal === 1 || pVal === 0) {
                            pathwaysPValsScientificNotation[pathway] = pVal
                        } else {
                            pathwaysPValsScientificNotation[pathway] = pVal.toExponential(2)
                        }

                }
                return pathwaysPValsScientificNotation;
            },
        }
    }
</script>

<style>

    .network-legend {
        width: 18%;
        height: auto;
        position:absolute;
        top:0;
        right:0;
        margin-top: 50px;
        margin-right: 50px;
        border: solid 1px black;
        padding-left: 2px;
    }

    .color-box {
      float: left;
      width: 20px;
      height: 20px;
      margin-right: 5px;
      border: 1px solid rgba(0, 0, 0, .2);
    }

    .circle {
        border-radius: 50%;
    }

    .star-icon {
        font-size: 20px;
    }

    .network-legend-content ul {
        width: auto;
        height: 90%;
        margin: auto;
        font-size: small;
        /*transform: translate(-50%, -50%);*/
    }


</style>