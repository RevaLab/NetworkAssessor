<template>
    <div class="network-controls">
        <database-selector />
        <degree-selector />
        <toggle-legend />
        <pathway-color-selector-query-list />
    </div>
</template>

<script>
    import DatabaseSelector from './NetworkSelectorDatabase.vue'
    import DegreeSelector from './NetworkSelectorDegree.vue'
    import PathwayColorSelectorQueryList from './PathwayColorSelector_QueryList.vue'
    import ToggleLegend from "./ToggleLegend.vue";


    export default {
        name: "network-controls",
        data() {
            return {
            }
        },
        components: {
            ToggleLegend,
            DegreeSelector,
            DatabaseSelector,
            PathwayColorSelectorQueryList,
        },
        methods: {
        }
    }
</script>

<style>

/*label.radio {*/
    /*margin-right: 20px;*/
/*}*/

</style>