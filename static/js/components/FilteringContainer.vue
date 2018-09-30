<template>
    <div class="filtering-container">
        <div class="search-bar">
            <div class="field">
              <div class="control">
                <input class="input is-small" type="text" placeholder="Search" v-model="searchTerm">
              </div>
            </div>
        </div>
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
                ontology: 'cellularLocation', // Should be prop,
                searchTerm: ''
            };
        },
        components: {
            GoTermSelector,
        },
        computed: {
            goTerms() {
                const goData = this.$store.state.GO[this.ontology];
                return Object.keys(goData).reduce(
                    (acc, goTerm) => {
                        return goData[goTerm].name.toLowerCase()
                            .indexOf(this.searchTerm.toLowerCase()) > -1 ?
                            {...acc, [goTerm]: goData[goTerm]} : acc
                    },
                    {}
                )
            }
        },
        methods: {
        }
    }
</script>

<style scoped>
    .go-terms-selector {
        display: block;
    }
</style>