<template>
    <div class="filtering-container">
        <div class="go-terms-selector" v-for="(goTermData, goTerm) in goTerms">
            <go-term-selector
                    v-bind:goTerm="goTerm"
                    v-bind:goTermData="goTermData"
                    v-bind:ontology="ontology"
            ></go-term-selector>
        </div>
    </div>
</template>

<script>
    import GoTermSelector from './GoTermSelector.vue';

    export default {
        name: "filtering-container",
        data() {
            return {
                ontology: 'cellularLocation',
            };
        },
        components: {
            GoTermSelector,
        },
        computed: {
            goTerms() {
                return this.$store.state.GO.cellularLocation;
            },
        },
    }
</script>

<style scoped>
    .go-terms-selector {
        display: block;
    }
</style>