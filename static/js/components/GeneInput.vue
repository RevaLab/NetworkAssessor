<template>
    <div class="gene-input">
        <button id="try-example"
                class="button is-info"
                v-on:click="addExampleList"
        >
            Try Example
        </button>
        <textarea
            v-model="geneListString"
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
            geneListString() {
                return this.geneList.join('\n')
            },
            geneList: {
              get() {
                return this.$store.state.geneInput;
              },
              set(geneInput) {
                this.$store.dispatch(
                    'addGeneInput',
                    geneInput
                );
              }
            }
        },
        methods: {
            addExampleList() {
              this.geneList = ["FLT3", "SMO", "GLA",
                  "SGCB", "OAT", "CAPN3", "ASS1", "AGXT",
                  "AKT1", "PTPN1", "PIAS1", "CDKN1B", "THEM4", "CCNE1", "MAP2K4"];
            },
            submitGeneList() {
                let geneInput = this.geneList;
                this.$store.dispatch(
                    'getPathwaySubnetwork',
                    {
                        queryGenes: geneInput,
                        pathways: ['query-list'],
                        networkDatabase: 'hprd'
                    }
                );
                this.$store.dispatch(
                    'addGeneInput',
                    geneInput
                );
                this.$router.push('/network');
            }
        },
        // beforeRouteLeave(to, from, next) {
        //     next()
        // }
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

/*.gene-input input {*/
    /*max-width: 40%;*/
    /*min-width: 300px;*/
    /*margin: 30px auto;*/
    /*border: 1px solid;*/
/*}*/

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