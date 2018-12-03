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
        <div id="filtering-card-loader-container" v-if="!goTermsLoaded">
            <spinner></spinner>
        </div>
        <div v-if="goTermsLoaded">
            <div class="go-terms-selector" v-for="goTerm in goTerms">
                <go-term-selector
                        v-bind:goTerm="goTerm.goId"
                        v-bind:goTermData="goTerm"
                        v-bind:ontology="ontology"
                ></go-term-selector>
            </div>
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
                // loadingTerms: true,
                // anotherTest: true
            };
        },
        props: ['ontology'],
        components: {
            GoTermSelector,
        },
        computed: {
            goTerms() {
                const goData = this.$store.state.GO[this.ontology];
                const unsortedTerms = Object.keys(goData).reduce(
                    (acc, goTerm) => {
                        return goData[goTerm].name.toLowerCase()
                            .indexOf(this.searchTerm.toLowerCase()) > -1 ?
                            acc.concat({ ...goData[goTerm], goId: goTerm }) : acc;
                    },
                    []
                );

                function compare(a,b) {
                      if (a.genes.length < b.genes.length)
                          return 1;
                      if (a.genes.length > b.genes.length)
                          return -1;
                      return 0;
                }

                return unsortedTerms.sort(compare);
            },
            goTermsLoaded() {
                return this.$store.state.goTermsLoaded;
            }
        },
        methods: {
            selectAll(event) {
                this.goTerms.forEach((goTerm) => {
                    this.$store.dispatch(
                        'updateGOTermSelection',
                        {
                            ontology: this.ontology,
                            goTerm: goTerm.goId,
                            selected: event.target.checked
                        }
                    );
                });
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
        width: 33%;
        overflow-y: scroll;
    }

    .search-bar {
        width: 80%;
        padding-left: 10px;
    }

    .go-terms-selector {
        display: block;
    }

    .filtering-card-header h5 {
        text-align: center;
        padding-top: 5px;
    }

    .go-terms-selector {
        padding-left: 5px;
    }

    .select-all {
        padding-left: 2px;
    }

    #filtering-card-loader-container {
        /*height: 30%;*/
        width: 100%;
        margin-top: -20%;
        /*background-color: pink;*/
        display: flex;
        flex-direction: column;
    }


</style>