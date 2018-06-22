from bisect import bisect_left


def calculate_network_pathway_pval(inter_pw_subgraph_edges, query_genes, pathway, all_pw_distribution):
    normalized_inter_pw_subgraph_edges = inter_pw_subgraph_edges / len(query_genes)
    pw_distribution = all_pw_distribution[pathway]

    rank = 100000 - bisect_left(pw_distribution, normalized_inter_pw_subgraph_edges)
    p_val = rank / float(len(pw_distribution))
    return p_val


def calculate_all_pathways_p_vals(pathways_edge_counts, len_query_gene_set, all_gene_set_pathway_p_vals):

    pathways_p_vals = {}

    major_cancer_pathways = ['AKT_ext_path', 'Apoptosis_path', 'Apoptosis_ext_path', 'CALC_PKC_ext_path',
                     'Cellular_Architecture_and_Microenvironment_path', 'Cell_Cycle_Control_path',
                     'Cell_Cycle_ext_path', 'Chromatin_Remodeling-DNA_Methylation_path', 'DNA_Damage_path',
                     'ERK_ext_path', 'G-Protein_Signaling_path', 'Hedgehog_Signaling_path', 'HIPPO_ext_path',
                     'Hormone_Signaling_path', 'Immune_Checkpoints_path', 'B-Catenin-WNT_Signaling_path',
                     'Jack_Stat_ext_path',
                     'Janus_Kinase_JAK-or-Signal_Transducers_and_Activators_of_Transcription_STAT_path',
                     'Kinase_Fusions_path', 'Metabolic_Signaling_path', 'NFKB_ext_path', 'Notch_ext_path',
                     'PI3K-AKT1-MTOR_Signaling_path', 'Protein_Degradation_Ubiquitination_path',
                     'Receptor_Tyrosine_KinaseORGrowth_Factor_Signaling_path', 'RNA_Splicing_path',
                     'TGF-B_Signaling_path', 'TGFB_ext_path', 'WNT_ext_path',
                     'Mitogen_Activated_Protein-MAP_Kinase_Signaling_path']

    pathway_p_vals_for_gene_set_of_current_count = all_gene_set_pathway_p_vals[len_query_gene_set]

    for pathway in pathways_edge_counts:
        if pathway not in major_cancer_pathways:
            continue

        inter_pw_subgraph_edges = pathways_edge_counts[pathway]
        p_val = pathway_p_vals_for_gene_set_of_current_count[pathway][inter_pw_subgraph_edges]
        pathways_p_vals[pathway] = p_val

    return pathways_p_vals
