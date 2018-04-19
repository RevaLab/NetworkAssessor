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
                this.geneList = ['CD4', 'DARS2', 'NDUFA10', 'NDUFC2', 'ALDH6A1', 'NDUFB10', 'NDUFB3', 'SORD',
                    'NDUFA9', 'NDUFS1', 'NDUFA3', 'NDUFA12', 'PIK3CD', 'CA1', 'HBA1', 'FGB', 'FGG', 'SLC22A6',
                    'HBB', 'FAH', 'WAS', 'CSK', 'TST', 'OAS1', 'SLC22A2', 'INPP5D', 'ADD2', 'ANK1', 'ARHGAP25',
                    'ARHGAP30', 'ARHGAP31', 'ARHGEF6', 'BIN2', 'CCT2', 'CCT5', 'COPA', 'DEF6', 'DOCK2', 'EPB41',
                    'EPB42', 'EVI2B', 'EVL', 'FMNL1', 'FNBP1', 'FYB1', 'GIPC2', 'GMIP', 'HCLS1', 'LCP1', 'LCP2',
                    'LPGAT1', 'MCM3', 'NUMA1', 'SPTA1', 'SPTB', 'TAP1', 'TAP2', 'WDR81', 'USP15', 'YOD1',
                    'PTPN6', 'SAMHD1', 'SKAP2', 'CDK17', 'RCSD1', 'CCT8', 'FERMT3', 'COPB2', 'LRPPRC', 'GPSM3',
                    'MYO1F', 'SH3BP1', 'SLC4A1', 'IL16', 'LSP1', 'PLEKHF2', 'RMND1', 'HBD', 'PTPRC', 'MCM4',
                    'SMC3', 'STK4', 'TAPBP', 'WDR91'].join("\n")
            },
            submitGeneList() {
                let userPathways = JSON.parse(this.$ls.get('userPathways', '{}'));
                delete userPathways['query_list'];
                // update gene input as a user pathway
                let queryListAsUserPathway = {
                    query_list: {
                        color: '#dd7e6b',
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

                // make API call to retrieve graph
                // this.$store.dispatch(
                //     'getPathwaySubnetwork',
                //     {
                //         pathways: [],
                //         networkDatabase: 'hprd',
                //         userPathways,
                //         previousSelectedPathways: [],
                //         pathwaysEdgeCounts: {}
                //     }
                // );

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