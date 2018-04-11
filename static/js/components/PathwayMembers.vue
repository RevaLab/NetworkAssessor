<template>
    <div class="pathway-members">
        <h3 v-bind:style="styleObject">{{ pathway }}</h3>
        <div class="gene-list-pathway-members">{{ pathwayMembers }}</div>
    </div>
</template>

<script>
    export default {
        name: "pathway-members",
        data() {
            return {}
        },
        props: ['pathway'],
        computed: {
            pathwayMembers() {
                return this.$store.state.pathwayMembers[this.pathway].join("\n")
            },
            styleObject() {
                let pathwayColor = this.$store.state.pathwayColors[this.pathway]
                return {backgroundColor: pathwayColor}
            }
        }
    }
</script>

<style>
    .pathway-members {
        height: 100%;
        overflow-y: scroll;
    }

    .gene-list-pathway-members {
        white-space: pre;
    }

</style>