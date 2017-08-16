
# ROW_TYPE_VERT = 1
# ROW_TYPE_HOR = 2

# ROW_DIR_DOWN = 1
# ROW_DIR_RIGHT = 2

# def get_row_idx(row_type, row_dir, idx_from, idx_to):

def get_row_idx(col_inc, line_inc, idx_from, idx_to):
    idxs_ret = []
    idxs_ret.append(idx_from)

    l = idx_from // 15
    c = idx_from % 15
    
    while idx_from != idx_to:
            l = l + col_inc
            c = c + line_inc
            idx_from = l * 15 + c
            idxs_ret.append(idx_from)
    return idxs_ret
