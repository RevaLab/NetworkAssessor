<template>
    <div class="pathway-members">
        <h3 v-bind:style="styleObject">{{ pathwayName }}</h3>
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
            pathwayName() {
                return this.$store.state.pathwayDisplayNames[this.pathway]
            },
            pathwayMembers() {
                return this.$store.state.pathwayMembers[this.pathway].join("\n")
            },
            styleObject() {
                let pathwayColor = this.$store.state.pathwayColors[this.pathway];
                return {
                    margin: "10px",
                    padding: "10px",
                    backgroundColor: pathwayColor
                }
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
        margin: 10px;
        padding: 10px;
        white-space: pre;
    }

</style>