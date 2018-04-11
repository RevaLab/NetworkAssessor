<template>
    <div class="user-pathway-add-form">
        <input
            type="text"
            v-model="title"
            placeholder="Enter Pathway Name"
        />
        <textarea
            v-model="geneList"
            v-bind:placeholder="placeholder"
        >
        </textarea>
        <button class="button is-primary"
           v-on:click="addPathway"
        >
            Add Pathway
        </button>
    </div>
</template>

<script>
export default {
    name: 'user-pathway-add-form',
    data() {
        return {
            placeholder: 'Enter Pathway Genes Separated by New Lines\nGene1\nGene2',
            title: 'Original Pathway Name',
            geneList: ''
        }
    },
    methods: {
        addPathway() {
            let userPathways = JSON.parse(this.$ls.get('userPathways', '{}'))
            console.log("BEFORE ADDING");
            console.log(this.$ls.get('userPathways'));
            console.log(this.title);
            console.log(this.geneList);
            userPathways[this.title] = {
                color: "#000000",
                genes: this.geneList.split("\n")
            };
            this.$ls.set('userPathways', JSON.stringify(userPathways));
            console.log("AFTER ADDING");
            console.log(this.$ls.get('userPathways'));

            this.$store.dispatch('updateUserPathways', userPathways);

            this.$modal.hide('add-user-pathway')
        }
    }
}
</script>

<style>
    .user-pathway-add-form {
        display: flex;
        flex-direction: column;
        /*height: 100%;*/
    }

    .user-pathway-add-form textarea {
        background-color: pink;
        height: 150px;
        width: 85%;
        margin: 8px auto;
    }

</style>