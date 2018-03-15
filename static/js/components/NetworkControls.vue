<template>
    <div class="network-controls">
        <degree-selector />
    </div>
</template>

<script>
    import DegreeSelector from './DegreeSelector.vue'

    export default {
        name: "network-controls",
        data() {
            return {
                selectedValue: "first_degree"
            }
        },
        components: {
          DegreeSelector
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