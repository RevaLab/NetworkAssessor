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
            }
        },
        computed: {
            geneList: {
              get() {
                return this.$store.state.geneInput.join('\n');
              },
              set(geneInput) {
                this.$store.dispatch(
                    'addGeneInput',
                    geneInput.split('\n')
                );
                return geneInput
              }
            }
        },
        methods: {
            addExampleList() {
              this.geneList = ["FLT3", "SMO", "GLA",
                  "SGCB", "OAT", "CAPN3", "ASS1", "AGXT",
                  "AKT1", "PTPN1", "PIAS1", "CDKN1B", "THEM4", "CCNE1", "MAP2K4"].join('\n');
            },
            submitGeneList() {
                let geneInput = this.$store.state.geneInput;
                let userPathwaysObj = JSON.stringify({
                    'original_pathway_1': {
                        color: '#000000',
                        genes: ['AKT1', 'AKT2', 'AKT3', 'GSK3B', 'MTOR', 'PDPK1', 'PIK3CA', 'PIK3CB', 'PIK3CD', 'PIK3CG', 'PIK3R1', 'PIK3R2', 'PIK3R3', 'PIK3R4', 'PIK3R5', 'PIK3R6', 'PRAS40', 'PTEN', 'TSC1', 'TSC2']
                    },
                    'original_pathway_2': {
                        color: '#cc66cc',
                        genes: ['AKT1', 'AKT2', 'AKT3', 'GSK3B', 'MTOR', 'PDPK1', 'PIK3CA', 'PIK3CB', 'PIK3CD', 'PIK3CG', 'PIK3R1', 'PIK3R2', 'PIK3R3', 'PIK3R4', 'PIK3R5', 'PIK3R6', 'PRAS40', 'PTEN', 'TSC1', 'TSC2']
                    }
                });
                // this.$ls.set('userPathways')
                this.$ls.set('userPathways', userPathwaysObj)
                let userPathways = JSON.parse(this.$ls.get('userPathways', 'boop fallback'));

                // this.$ls.set('userPathways', userPathways);
                console.log(userPathways);
                this.$store.dispatch('updateUserPathways', userPathways);
                this.$store.dispatch(
                    'getPathwaySubnetwork',
                    {
                        queryGenes: geneInput,
                        pathways: ['query-list'],
                        networkDatabase: 'hprd',
                        userPathways
                    }
                );
                this.$router.push('/network');
            }
        },
    }
</script>

<style scoped>
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