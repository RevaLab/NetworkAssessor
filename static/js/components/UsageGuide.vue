<template>
    <!--<div class="usage-guide">-->

    <!--</div>-->
    <div class="usage-guide-steps">
        <div class="usage-guide-step">
                    <button
                class="button is-warning"
                v-on:click="navigateHome"
        >
            Return to Input Page
        </button>
        </div>
        <div class="usage-guide-step">
            <h4>Enter a query gene list</h4>
            Enter a gene list of consideration. Genes may be separated by line breaks, spaces, or tabs.
            <img src="static/walkthrough/step1-gene-input.png">
        </div>
        <div class="usage-guide-step">
            <h4>Press analyze</h4>
            A network of interactions in your query list will be calculated,
                and the following significance will be determined:
                <br>- edges among genes of your query set
                <br>- edges between query set genes and 30 major cancer pathways
            <img src="static/walkthrough/step2-press-analyze.png">
        </div>
        <div class="usage-guide-step">
            <h4>View the Query Network</h4>
            After the user inputs a gene set, the application renders
            interaction networks using established protein-protein
            interaction databases, HPRD or BioGrid.
            <img src="static/walkthrough/step3-query-network.png">
        </div>
       <div class="usage-guide-step">
            <h4>Select Pathways of Interest</h4>
            Major cancer pathways are ranked based on the assessed significance
            of their interactions to the network formed by a given gene set.
            To this end, we developed statistics based on the number of
            interactions between genes of a biologically meaningful pathway and
            multiple random gene sets (~1,000,000) of sizes ranging from 1 to ~1000.
            The significance of a given gene set's relationship to a pathway is
            assessed by comparing the number of interactions between the gene set
            interaction network and the pathway genes against the pathway-specific
            random distribution.
            <img src="static/walkthrough/step4-add-pathway.png">
       </div>
       <div class="usage-guide-step">
           <h4>Customize Network Visualization</h4>
           Pathways of interest can be styled according to what the user finds meaningful or intuitive.
           In the course of this assessment, users can also assess the roles of individual
           genes in a given biological pathway. For example, given a set of upregulated genes
           in a particular cancer, a user can immediately generate hypotheses of
           activation roles of the genes which interact with driver genes of major cancer pathways.
           <img src="static/walkthrough/step5-customize-pathway.png">
       </div>
       <div class="usage-guide-step">
           <h4>View More Information</h4>
           Users can see more information, including:
           - Pathways genes with multiple degrees of separation from the query list
           - Members of the pathways of consideration
           - Edges connecting query genes to pathway genes versus edges exclusively connecting pathway genes
           <img src="static/walkthrough/step6-degrees.png">
           <img src="static/walkthrough/step6-pathway-members.png">
           <img src="static/walkthrough/step6-view-edges.png">
       </div>
    </div>
</template>

<script>
    export default {
        name: "usage-guide",
        methods: {
            navigateHome() {
                this.$router.push('/')
            }
        }
    }
</script>

<style>

    .usage-guide-step img {
        border: solid 1px black;
        margin-top: 5px;
        width: 100%;
    }

    .usage-guide-step h4 {
        font-weight: bold;
        text-align: center;
        vertical-align: middle;
    }

    .usage-guide-step {
        margin-top: 10px;
        background-color: lightgray;
        padding: 5px;
    }

    .usage-guide-steps {
          display: flex;
          flex-direction: column;
        width: 60%;
          min-width: 300px;
          height: 90%;
          margin: 5px;
          /*border-bottom: none;*/
          /*font-size: small;*/
          background-color: grey;
          padding: 10px;
          box-sizing: border-box;
          overflow: auto;
        margin: 0 auto;
    }
</style>