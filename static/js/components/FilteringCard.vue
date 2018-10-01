<template>
    <div class="filtering-card">
        <div class="filtering-card-header">
            <h5>{{ displayNames[ontology] }}</h5>
        </div>
        <div class="search-bar">
            <div class="field">
              <div class="control">
                <input class="input is-small" type="text" placeholder="Search" v-model="searchTerm">
              </div>
            </div>
        </div>
        <div class="select-all">
            <label class="checkbox">
            <input type="checkbox" v-model="selectAllChecked" v-on:click="selectAll">
                Select All
        </label>
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
        name: "filtering-card",
        data() {
            return {
                // ontology: 'cellularLocation', // Should be prop,
                searchTerm: '',
                selectAllChecked: false,
                goTermsLength: 0,
                displayNames: {
                    'cellularLocation': 'Cellular Location',
                    'molecularFunction': 'Molecular Function',
                    'biologicalProcess': 'Biological Process'
                },
            };
        },
        props: ['ontology'],
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
            selectAll(event) {
                for (let goTerm in this.goTerms) {
                    if (this.goTerms.hasOwnProperty(goTerm)) {
                        this.$store.dispatch(
                            'updateGOTermSelection',
                            {
                                ontology: this.ontology,
                                goTerm,
                                selected: event.target.checked
                            }
                        );
                    }
                }
            },
        },
        watch: {
            goTerms() {
                // if new length is greater than this.listLength, then selectAll = false
                if (Object.keys(this.goTerms).length > this.goTermsLength) {
                    this.selectAllChecked = false;
                }

                this.goTermsLength = Object.keys(this.goTerms).length;
            }
        }
    }
</script>

<style scoped>
    .filtering-card {
        border: 1px solid black;
    }

    .go-terms-selector {
        display: block;
    }
</style>