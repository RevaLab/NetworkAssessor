def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))


def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))


def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))


def find_tail(overlap_count, pw_count, input_count, bg_count):
    enrichment_threshold = (pw_count * input_count) / bg_count

    if overlap_count >= enrichment_threshold:
        tail = 'greater'
    else:
        tail = 'less'

    return tail


def find_enrichment_coefficient(overlap_count, pw_count, input_count, bg_count):
    enrichment_threshold = (pw_count * input_count) / bg_count

    coefficient = overlap_count/enrichment_threshold

    if coefficient < 1:
        return 1/coefficient * -1

    return coefficient


