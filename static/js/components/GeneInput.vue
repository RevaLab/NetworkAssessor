<template>
    <div class="gene-input">
        <div class="navigation-from-input">
                    <button id="usage-guide"
                        class="button is-warning"
                        v-on:click="viewUsageGuide"
                >
                    Usage Guide
                </button>
                <button id="try-example"
                        class="button is-info"
                        v-on:click="addExampleList"
                >
                    Try Example
                </button>
        </div>
        <div id="gene-input-texts">
            <div v-bind:class="{ 'half-area': filtering, 'full-area': !filtering }">
                <textarea
                    id="unfiltered-gene-list"
                    v-model="geneList"
                    placeholder="Enter Query Gene List, Up to 200 genes"
                >
                </textarea>
                <label class="gene-input-filter" v-if="filtering" for="unfiltered-gene-list">Unfiltered: {{ geneListArr.length }} genes</label>
            </div>
            <div v-if="filtering" v-bind:class="{ 'half-area': filtering }">
                <textarea
                    id="filtered-gene-list"
                    v-model="filteredGeneListStr"
                ></textarea>
                <label class="gene-input-filter"  for="filtered-gene-list">Filtered</label>
            </div>
        </div>
        <!--<input-->
            <!--type="text"-->
            <!--v-model="title"-->
            <!--placeholder="Optional List Title"-->
        <!--/>-->
        <div v-if="filtering">
            <filtering-container />
        </div>
       <button class="button is-primary"
           v-on:click="submitGeneList"
       >
            {{ analyzeButtonText[filtering] }}
       </button>
        <button class="button is-warning"
           v-on:click="filterGenes"
        >
            {{ geneFiltering[filtering] }}
        </button>
        <div class="lab-info">
            <div>Under development at: <strong>Reva Lab</strong> by Anna Calinawan
                <br></div>
            <div>
            Contact: anna.calinawan@mssm.edu, boris.reva@mssm.edu
            </div>
        </div>
    </div>
</template>

<script>
    import UsageGuide from "./UsageGuide.vue";
    import FilteringContainer from "./FilteringContainer.vue"

    export default {
        components: {
            UsageGuide,
            FilteringContainer
        },
        name: "gene-input",
        data () {
            return {
                analyzeButtonText: {
                    true: 'Analyze Unfiltered Genes',
                    false: 'Analyze'
                },
                geneList: '',
                filtering: false,
                geneFiltering: {
                    true: 'Analyze Filtered Genes',
                    false: 'Filter Genes'
                },
            }
        },
        computed: {
            geneListArr() {
                let geneListArr = [];
                const trimmedGeneList = this.geneList.trim();

                if (trimmedGeneList.length === 0) {
                    return []
                }
                if (trimmedGeneList.includes("\t") && trimmedGeneList.includes(" ")) {
                    alert("Enter genes separated by a newline, tab, or space. Your list seems to include multiple separators.")
                    return;
                }

                if (trimmedGeneList.includes("\t")) {
                    geneListArr = trimmedGeneList.split("\t");
                } else if (trimmedGeneList.includes(" ")) {
                    geneListArr = trimmedGeneList.split(" ");
                } else {
                    geneListArr = trimmedGeneList.split("\n")
                }

                return geneListArr;
            },
            filteredGeneList() {
                let filteredGeneList = Object.keys(this.$store.state.GO.cellularLocation).reduce(
                    (acc, goTerm) => {
                        const goData = this.$store.state.GO.cellularLocation[goTerm];
                        return goData.selected ? acc.concat(goData.genes) : acc
                    },
                    []);
                return Array.from(new Set(filteredGeneList))
            },
            filteredGeneListStr() {
                return this.filteredGeneList.join("\n")
            }
        },
        methods: {
            viewUsageGuide() {
                this.$router.push('/usage-guide');
            },
            addExampleList() {
                this.geneList =['FLT3', 'SMO', 'GLA', 'SGCB', 'OAT', 'CAPN3', 'ASS1', 'AGXT', 'AKT1', 'PTPN1',
                    'PIAS1', 'CDKN1B', 'THEM4', 'CCNE1', 'MAP2K4', 'ATG7','ATG12','BAD','BCL2L1'].join("\n")
            },
            filterGenes() {
              this.filtering = true
            },
            submitGeneList() {
                let userPathways = JSON.parse(this.$ls.get('userPathways', '{}'));

                delete userPathways['query_list'];
                this.$ls.set('userPathways', JSON.stringify(userPathways));

                if (!this.geneList.length) {
                    alert("Please enter genes.");
                    return;
                }

                if (this.geneListArr.length > 200) {
                    alert("Please limit gene set to 200 for now");
                    return;
                }

                // update gene input as a user pathway
                let queryListAsUserPathway = {
                    query_list: {
                        color: '#00ffff',
                        genes: this.geneListArr,
                        displayName: 'Query List'
                    }
                };

                // add information for user pathways to store
                userPathways = {...userPathways, ...queryListAsUserPathway};
                let displayData = {
                    pathways: {},
                    add: true
                };

                for (let pathway in userPathways) {
                    displayData['pathways'][pathway] =
                        userPathways[pathway]['displayName'];
                }

                this.$store.dispatch('updateUserPathways', userPathways);
                this.$store.dispatch('updateUserPathwayDisplay', displayData);

                this.$router.push('/network');
            }
        },
    }
</script>

<style>
    #gene-input-texts {
        display: flex;
        flex-direction: row;
        width: 100%;
    }

    .half-area {
        display: flex;
        flex-direction: column;
        width: 50%;
    }

    .full-area {
        width: 100%;
    }

    .gene-input {
        display: flex;
        flex-direction: column;
        margin: auto;
        max-width: 45%;
        min-width: 450px;
    }


    .gene-input textarea {
        margin: 20px 2px auto;
        border: 1px solid;
        height: 30vh;
        width: 100%;
    }

    .gene-input .button {
        width: 95%;
        margin: 10px auto;
    }

    .gene-input #try-example {
        margin-left:auto;
        margin-right:0;
        margin-bottom: -10px;
        max-width: 20%;
        min-width: 150px;
    }

    .gene-input #usage-guide {
        margin-left:0;
        margin-right:auto;
        margin-bottom: -10px;
        max-width: 20%;
        min-width: 150px;
    }

    .navigation-from-input {
        display: flex;
        flex-direction: row;
    }
    .lab-info {
        display: inline-block;
        font-size: small;
        background-color: lightgray;
        margin-top: 80px;
        padding: 8px;
        /*width: 100%;*/
    }

    .gene-input-filter {
        margin: 2px auto
    }

</style>
