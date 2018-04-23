<template>
    <div class="network-controls">
        <database-selector />
        <!--<degree-selector />-->
    </div>
</template>

<script>
    import DatabaseSelector from './NetworkSelectorDatabase.vue'
    import DegreeSelector from './NetworkSelectorDegree.vue'

    export default {
        name: "network-controls",
        data() {
            return {
            }
        },
        components: {
            DegreeSelector,
            DatabaseSelector
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