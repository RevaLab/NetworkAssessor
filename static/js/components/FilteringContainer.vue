<template>
    <div class="filtering-container">
        <filtering-card v-bind:ontology="'cellularLocation'"/>
        <filtering-card v-bind:ontology="'molecularFunction'"/>
        <filtering-card v-bind:ontology="'biologicalProcess'"/>
    </div>
</template>

<script>
    import FilteringCard from './FilteringCard.vue';

    export default {
        name: "filtering-container",
        components: {
            FilteringCard
        },
    }
</script>

<style scoped>
    .filtering-container {
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
        height: 30vh;
    }
</style>