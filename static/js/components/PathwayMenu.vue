<template>
    <div class="pathway-menu">
        <ul id="pathways-ul">
            <li v-for="(pathway, index) in pathways">
                <pathway-color-selector v-bind:pathwayName="pathway"/>
            </li>
        </ul>
    </div>
</template>

<script>
    import PathwayColorSelector from './PathwayColorSelector.vue'

    export default {
        name: "pathway-menu",
        data() {
            return {
                pathways: ['AKT_ext_path', 'Apoptosis_path', 'Apoptosis_ext_path', 'CALC_PKC_ext_path',
                    'Cellular_Architecture_and_Microenvironment_path', 'Cell_Cycle_Control_path',
                    'Cell_Cycle_ext_path', 'Chromatin_Remodeling-DNA_Methylation_path',
                    'DNA_Damage_path', 'ERK_ext_path', 'G-Protein_Signaling_path',
                    'Hedgehog_Signaling_path', 'HIPPO_ext_path', 'Hormone_Signaling_path',
                    'Immune_Checkpoints_path', 'B-Catenin-WNT_Signaling_path', 'Jack_Stat_ext_path',
                    'Janus_Kinase_JAK-or-Signal_Transducers_and_Activators_of_Transcription_STAT_path',
                    'Kinase_Fusions_path', 'Metabolic_Signaling_path', 'NFKB_ext_path', 'Notch_ext_path',
                    'PI3K-AKT1-MTOR_Signaling_path', 'Protein_Degradation_Ubiquitination_path',
                    'Receptor_Tyrosine_KinaseORGrowth_Factor_Signaling_path', 'RNA_Splicing_path',
                    'TGF-B_Signaling_path', 'TGFB_ext_path', 'WNT_ext_path',
                    'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path']

            }
        },
        components: {
            PathwayColorSelector
        }
    }
</script>

<style scoped>

</style>