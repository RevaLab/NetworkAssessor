<template>
    <div class="user-pathways">
        <h2>User Pathways</h2>
        <ul id="pathways-ul">
            <li v-for="(pathwayData, pathway) in userPathways">
                <pathway-color-selector v-bind:pathwayName=pathway />
            </li>
        </ul>
    </div>
</template>

<script>
    import Swatches from 'vue-swatches'
    import PathwayColorSelector from './PathwayColorSelector.vue'

    export default {
        name: "user-pathways",
        computed: {
            userPathways() {
                return this.$store.state.userPathways;
            },
        },
        components: {
            PathwayColorSelector,
            Swatches
        },
        mounted() {
            let userPathways = this.$ls.get('userPathways', {
                'original_pathway': {
                    color: '#000000',
                    genes: ['PIAS1', 'CAPN3', 'FLT3', 'AKT1', 'PTPN1', 'OAT', 'GLA', 'AGXT', 'CDKN1B', 'SMO', 'ASS1', 'CCNE1', 'MAP2K4', 'THEM4', 'SGCB']
                }
            });
            this.$store.dispatch('updateUserPathways', userPathways)
        }
    }
</script>

<style>
    .user-pathways {
        height: 35%;
    }

</style>