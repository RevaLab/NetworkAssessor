<template>
    <div class="network-controls">
        <database-selector />
        <degree-selector />
        <toggle-options />
        <pathway-color-selector-query-list />
    </div>
</template>

<script>
    import DatabaseSelector from './NetworkSelectorDatabase.vue'
    import DegreeSelector from './NetworkSelectorDegree.vue'
    import PathwayColorSelectorQueryList from './PathwayColorSelector_QueryList.vue'
    import ToggleOptions from "./ToggleOptions.vue";


    export default {
        name: "network-controls",
        data() {
            return {
            }
        },
        components: {
            ToggleOptions,
            DegreeSelector,
            DatabaseSelector,
            PathwayColorSelectorQueryList,
        },
    }
</script>

<style>

</style>
