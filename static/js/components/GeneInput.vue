<template>
    <div class="gene-input">
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
       <button
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
            submitGeneList() {
                this.$store.dispatch(
                    'getSubnetwork',
                    this.geneList
                )
            }
        }
    }
</script>

<style scoped>
.gene-input {
    display: flex;
    flex-direction: column;
}
.gene-input textarea {
    max-width: 40%;
    min-width: 300px;
    margin: 30px auto;
    border: 1px solid green;
}
.gene-input input {
    max-width: 40%;
    min-width: 300px;
    margin: 30px auto;
    border: 1px solid green;
}
</style>