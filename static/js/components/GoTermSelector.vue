<template>
    <div class="go-term-selector">
        <label class="checkbox">
            <input type="checkbox" v-model="checked">
            {{ goTerm }}
        </label>
        |<span>{{ goTermData.name }}</span>
        |<a v-on:click="showPathwayMembers(goTerm)">
            <span>{{ goTermData.genes.length }}</span>
         </a>
        <modal v-bind:name="goTerm">
            <div class="go-term-members">
                <h3>{{ goTerm }}: {{ goTermData.name }}</h3>
                <ul>
                    <li v-for="gene in goTermData.genes">
                        {{ gene }}
                    </li>
                </ul>
            </div>
        </modal>
    </div>
</template>

<script>
    export default {
        name: "go-term-selector",
        props: [
            'goTerm',
            'goTermData',
            'ontology',
        ],
        methods: {
            showPathwayMembers(goTerm) {
                this.$modal.show(goTerm)
            }
        },
        computed: {
            checked: {
                get() {
                    return this.$store.state.GO[this.ontology][this.goTerm].selected;
                },
                set(selected) {
                    this.$store.dispatch(
                        'updateGOTermSelection',
                        {   ontology: this.ontology,
                            goTerm: this.goTerm,
                            selected
                        }
                    );
                }
            }
        }
    }
</script>

<style scoped>
    .go-term-members {
        height: 100%;
        overflow-y: scroll;
    }

</style>