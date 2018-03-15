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
                geneList: '',
                // title: '',
            }
        },
        methods: {
            addExampleList() {
              this.geneList = "FLT3\n" +
                  "SMO\n" +
                  "GLA\n" +
                  "SGCB\n" +
                  "OAT\n" +
                  "CAPN3\n" +
                  "ASS1\n" +
                  "AGXT\n" +
                  "AKT1\n" +
                  "PTPN1\n" +
                  "PIAS1\n" +
                  "CDKN1B\n" +
                  "THEM4\n" +
                  "CCNE1\n" +
                  "MAP2K4"
            },
            submitGeneList() {
                let geneInput = this.geneList.split('\n');
                this.$store.dispatch(
                    'getPathwaySubnetwork',
                    {
                        queryGenes: geneInput,
                        pathways: ['query-list']
                    }
                );
                this.$store.dispatch(
                    'addGeneInput',
                    geneInput
                );
                this.$router.push('/network');
            }
        }
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