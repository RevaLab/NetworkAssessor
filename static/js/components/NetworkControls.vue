<template>
    <div class="network-controls">
        <database-selector />
        <degree-selector />
        <pathway-color-selector-query-list />
        <multiple-pathway-selector />
    </div>
</template>

<script>
    import DatabaseSelector from './NetworkSelectorDatabase.vue'
    import DegreeSelector from './NetworkSelectorDegree.vue'
    import MultiplePathwaySelector from './MultiplePathwaySelector.vue'
    import PathwayColorSelectorQueryList from './PathwayColorSelector_QueryList.vue'


    export default {
        name: "network-controls",
        data() {
            return {
            }
        },
        components: {
            DegreeSelector,
            DatabaseSelector,
            PathwayColorSelectorQueryList,
            MultiplePathwaySelector
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