<template>
    <div class="network-controls">
        <database-selector />
        <degree-selector />
    </div>
</template>

<script>
    import DatabaseSelector from './DatabaseSelector.vue'
    import DegreeSelector from './DegreeSelector.vue'

    export default {
        name: "network-controls",
        data() {
            return {
                selectedValue: "first_degree"
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