<template>
    <div class="gene-input">
        <button id="try-example"
                class="button is-info"
                v-on:click="addExampleList"
        >
            Try Example
        </button>
        <textarea
            v-model="geneList"
            placeholder="Enter Query Gene List"
        >
        </textarea>
        <!--<input-->
            <!--type="text"-->
            <!--v-model="title"-->
            <!--placeholder="Optional List Title"-->
        <!--/>-->
       <button class="button is-primary"
           v-on:click="submitGeneList"
       >
            Analyze
       </button>
    </div>
</template>

<script>
    export default {
        name: "gene-input",
        data () {
            return {
                geneList: ''
            }
        },
        computed: {
        },
        methods: {
            addExampleList() {
                this.geneList = ['OLFML3', 'LOC441208 ', 'ZNRF2P1', 'PEMT', 'KIAA1609 ', 'TLDC1', 'MMP2', 'FOXA2', 'XBP1'].join("\n")
                // this.geneList =['FLT3', 'SMO', 'GLA', 'SGCB', 'OAT', 'CAPN3', 'ASS1', 'AGXT', 'AKT1', 'PTPN1',
                //     'PIAS1', 'CDKN1B', 'THEM4', 'CCNE1', 'MAP2K4'].join("\n")
            },
            submitGeneList() {
                let userPathways = JSON.parse(this.$ls.get('userPathways', '{}'));

                delete userPathways['query_list'];
                this.$ls.set('userPathways', JSON.stringify(userPathways));
                // update gene input as a user pathway
                let queryListAsUserPathway = {
                    query_list: {
                        color: '#00ffff',
                        genes: this.geneList.split("\n"),
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
.gene-input {
    display: flex;
    flex-direction: column;
    margin: auto;
    max-width: 45%;
    min-width: 450px;
}

.gene-input textarea {
    width: 100%;
    margin: 20px auto;
    border: 1px solid;
    height: 400px;
}

.gene-input .button {
    width: 100%;
    margin: auto;
}

.gene-input #try-example {
    margin-left:auto;
    margin-right:0;
    margin-bottom: -10px;
    max-width: 20%;
    min-width: 150px;
}
</style>