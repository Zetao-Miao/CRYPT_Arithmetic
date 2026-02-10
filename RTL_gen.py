import os

from heuristic import *
from random import randint


def width_expr(v: int, w: int) -> str:
    if v > 0:
        return f"[{v:<{w}} : 0]"
    else:
        return " "*w


def LOOKAHEAD8_gen(num: int, suffix: str, attr: list[bool]) -> tuple[str, str]:
    left_vals = [4*num-1, num-1, 8*num-1]
    left_w = max(len(str(v)) for v in left_vals)
    width_expr_cout = width_expr(4*num-1, left_w)
    width_expr_cin = width_expr(num-1, left_w)
    width_expr_cy = width_expr(8*num-1, left_w)
    width_expr_prop = width_expr(8*num-1, left_w)
    w = max(len(width_expr_cout), len(width_expr_cin), len(width_expr_cy), len(width_expr_prop))
    signal_decl = f"""
    logic {width_expr_cout:<{w}} COUT_LA_{suffix};
    logic {width_expr_cin:<{w}} CIN_LA_{suffix};
    logic {width_expr_cy:<{w}} CY_LA_{suffix};
    logic {width_expr_prop:<{w}} PROP_LA_{suffix};
    """
    instantiation = f""""""
    for i in range(num):
        LOOKB = '"TRUE"' if attr[4*i] else '"FALSE"'
        LOOKD = '"TRUE"' if attr[4*i+1] else '"FALSE"'
        LOOKF = '"TRUE"' if attr[4*i+2] else '"FALSE"'
        LOOKH = '"TRUE"' if attr[4*i+3] else '"FALSE"'
        attr_list = [LOOKB, LOOKD, LOOKF, LOOKH]
        attr_len = max(len(s) for s in attr_list)
        COUTB = f"COUT_LA_{suffix}[{4*i}]"
        COUTD = f"COUT_LA_{suffix}[{4*i+1}]"
        COUTF = f"COUT_LA_{suffix}[{4*i+2}]"
        COUTH = f"COUT_LA_{suffix}[{4*i+3}]"
        CIN = f"CIN_LA_{suffix}[{i}]" if num > 1 else f"CIN_LA_{suffix}"
        CYA = f"CY_LA_{suffix}[{8*i}]"
        CYB = f"CY_LA_{suffix}[{8*i+1}]"
        CYC = f"CY_LA_{suffix}[{8*i+2}]"
        CYD = f"CY_LA_{suffix}[{8*i+3}]"
        CYE = f"CY_LA_{suffix}[{8*i+4}]"
        CYF = f"CY_LA_{suffix}[{8*i+5}]"
        CYG = f"CY_LA_{suffix}[{8*i+6}]"
        CYH = f"CY_LA_{suffix}[{8*i+7}]"
        PROPA = f"PROP_LA_{suffix}[{8*i}]"
        PROPB = f"PROP_LA_{suffix}[{8*i+1}]"
        PROPC = f"PROP_LA_{suffix}[{8*i+2}]"
        PROPD = f"PROP_LA_{suffix}[{8*i+3}]"
        PROPE = f"PROP_LA_{suffix}[{8*i+4}]"
        PROPF = f"PROP_LA_{suffix}[{8*i+5}]"
        PROPG = f"PROP_LA_{suffix}[{8*i+6}]"
        PROPH = f"PROP_LA_{suffix}[{8*i+7}]"
        port_list = [COUTB, COUTD, COUTF, COUTH, CIN, CYA, CYB, CYC, CYD, CYE, CYF, CYG, CYH, PROPA, PROPB, PROPC, PROPD, PROPE, PROPF, PROPG, PROPH]
        max_len = max(len(s) for s in port_list)
        instantiation += f"""
    LOOKAHEAD8 #(
        .LOOKB({LOOKB.ljust(attr_len)}),
        .LOOKD({LOOKD.ljust(attr_len)}),
        .LOOKF({LOOKF.ljust(attr_len)}),
        .LOOKH({LOOKH.ljust(attr_len)}))
    LOOKAHEAD8_{suffix}_inst{i} (
        .COUTB({COUTB.ljust(max_len)}),
        .COUTD({COUTD.ljust(max_len)}),
        .COUTF({COUTF.ljust(max_len)}),
        .COUTH({COUTH.ljust(max_len)}),
        .CIN  ({CIN.ljust(max_len)}),
        .CYA  ({CYA.ljust(max_len)}),
        .CYB  ({CYB.ljust(max_len)}),
        .CYC  ({CYC.ljust(max_len)}),
        .CYD  ({CYD.ljust(max_len)}),
        .CYE  ({CYE.ljust(max_len)}),
        .CYF  ({CYF.ljust(max_len)}),
        .CYG  ({CYG.ljust(max_len)}),
        .CYH  ({CYH.ljust(max_len)}),
        .PROPA({PROPA.ljust(max_len)}),
        .PROPB({PROPB.ljust(max_len)}),
        .PROPC({PROPC.ljust(max_len)}),
        .PROPD({PROPD.ljust(max_len)}),
        .PROPE({PROPE.ljust(max_len)}),
        .PROPF({PROPF.ljust(max_len)}),
        .PROPG({PROPG.ljust(max_len)}),
        .PROPH({PROPH.ljust(max_len)}));
"""
    return signal_decl, instantiation


def layer_admin(layer_inputs: list[int], chain_list: list[list[counter]], merge_flag: bool, merge_chain_list: list[list[counter]], reduced_inputs: list[list[list[int]]]) -> tuple[list, list, list, list]:
    """
    :param layer_inputs: the list of inputs, indicating how many bits are there in each column
    :param chain_list: the counter chains and floating counters to be applied in current layer
    :param merge_flag: whether a layer of insufficiently used GPCs should be merged with current layer
    :param merge_chain_list: the counter chains and floating counters to be merged with current layer
    :param reduced_inputs: the number input bits of the insufficiently used counters which should be set to 0
    :return: a tuple of four lists:
                first list: the layer outputs, which is the layer_inputs for the next layer
                second list: containing the inputs for counter chains and floating counters, the order corresponds to the chain_list order
                third list: containing the outputs for counter chains and floating counters, the order corresponds to the chain_list order
                fourth list: containing lists of tuples that serve for assign statement in RTL, i.e. directly moving the bits to the next layer
    """
    num_cols = len(layer_inputs)
    input_bit_pointers = [0] * num_cols
    output_bit_pointers = [0] * num_cols
    layer_outputs_list = []
    chain_inputs_list = []
    chain_outputs_list = []
    assignment_list = []
    original_num_chains = len(chain_list)
    if merge_flag:
        chain_list.extend(merge_chain_list)
    num_chains = len(chain_list)
    for k in range(num_chains):
        chain = chain_list[k]
        num_counters = len(chain)
        inputs = []
        outputs = []
        for i in range(num_counters):
            counter_inputs = chain[i].inputs
            counter_inputs[-1] -= 1 if i else 0
            num_in_cols = len(counter_inputs)
            for j in range(num_in_cols):
                inputs.append(list(range(input_bit_pointers[chain[i].applied_column+j], input_bit_pointers[chain[i].applied_column+j]+counter_inputs[num_in_cols-1-j])))
                input_bit_pointers[chain[i].applied_column+j] += counter_inputs[num_in_cols-1-j]
                if k >= original_num_chains:
                    num_reduced_inputs = reduced_inputs[k-original_num_chains][i][num_in_cols-1-j]
                    if num_reduced_inputs > 0:
                        del inputs[-1][-num_reduced_inputs:]
                    input_bit_pointers[chain[i].applied_column+j] -= num_reduced_inputs
            counter_outputs = chain[i].outputs
            counter_outputs[0] -= 1 if i != num_counters-1 else 0
            num_out_cols = len(counter_outputs)
            for j in range(num_out_cols):
                to_append = list(range(output_bit_pointers[chain[i].applied_column+j], output_bit_pointers[chain[i].applied_column+j]+counter_outputs[num_out_cols-1-j]))
                if to_append:
                    if i != 0 and j==0 and chain[i-1].name == "(3,9 : 2,3,1)":
                        outputs[-1].extend(to_append)
                    else:
                        outputs.append(to_append)
                output_bit_pointers[chain[i].applied_column+j] += counter_outputs[num_out_cols-1-j]
        chain_inputs_list.append(inputs)
        chain_outputs_list.append(outputs)
    for i in range(num_cols):
        if input_bit_pointers[i] < layer_inputs[i]:
            col_assign_list = []
            for j in range(layer_inputs[i]-input_bit_pointers[i]):
                old_idx = input_bit_pointers[i]+j
                new_idx = output_bit_pointers[i]+j
                col_assign_list.append((old_idx, new_idx))
            assignment_list.append(col_assign_list)
            output_bit_pointers[i] += (layer_inputs[i]-input_bit_pointers[i])
        else:
            assignment_list.append([])
        layer_outputs_list.append(output_bit_pointers[i])
    return layer_outputs_list, chain_inputs_list, chain_outputs_list, assignment_list


def analyze_subchain(counter_list: list[counter]) -> tuple[list, list, list]:
    subchain_list = []
    subchain_num_LOOKAHEAD8 = []
    subchain_LOOKAHEAD8_attributes = []
    subchain = []
    num_counters = len(counter_list)
    current_subchain_length = 0
    for i in range(num_counters):
        if counter_list[i].name == "(4,13 : 3,4,1)":
            current_subchain_length += 3
            subchain.append(counter_list[i])
        elif counter_list[i].name == "(3,9 : 2,3,1)":
            current_subchain_length += 2
            subchain.append(counter_list[i])
            if i != num_counters-1:
                subchain.append("SUBCHAIN_END")
                subchain_list.append(subchain)
                num_LOOKAHEAD8 = current_subchain_length // 8
                if current_subchain_length % 8:
                    num_LOOKAHEAD8 += 1
                subchain_num_LOOKAHEAD8.append(num_LOOKAHEAD8)
                num_CYMUX = current_subchain_length // 2
                attributes = []
                for j in range(4*num_LOOKAHEAD8):
                    if j == 0:
                        attributes.append(False)
                    elif j < num_CYMUX-1:
                        attributes.append(True)
                    else:
                        attributes.append(False)
                subchain_LOOKAHEAD8_attributes.append(attributes)
                current_subchain_length = 2
                subchain = []
        elif counter_list[i].name == "(9 : 4,1)":
            current_subchain_length += 2
            subchain.append(counter_list[i])
        elif counter_list[i].name == "(6 : 3]":
            current_subchain_length += 1
            subchain.append(counter_list[i])
        elif counter_list[i].name == "(2,2,3 : 4]":
            current_subchain_length += 2
            subchain.append(counter_list[i])
        elif counter_list[i].name == "(3 : 2]":
            current_subchain_length += 1
            subchain.append(counter_list[i])
        elif counter_list[i].name == "(1,5 : 3]":
            current_subchain_length += 2
            subchain.append(counter_list[i])
        else:
            current_subchain_length += 0
        if i == num_counters-1:
            subchain.append("CHAIN_END")
            subchain_list.append(subchain)
            num_LOOKAHEAD8 = current_subchain_length // 8
            if current_subchain_length % 8:
                num_LOOKAHEAD8 += 1
            subchain_num_LOOKAHEAD8.append(num_LOOKAHEAD8)
            num_CYMUX = current_subchain_length // 2
            attributes = []
            if current_subchain_length % 2 == 0:
                for j in range(4*num_LOOKAHEAD8):
                    if j == 0:
                        attributes.append(False)
                    elif j <= num_CYMUX-2:
                        attributes.append(True)
                    else:
                        attributes.append(False)
            else:
                for j in range(4*num_LOOKAHEAD8):
                    if j == 0:
                        attributes.append(False)
                    elif j < num_CYMUX-1:
                        attributes.append(True)
                    elif j == num_CYMUX-1:
                        if subchain[-2].name == "(3,9 : 2,3,1)" or subchain[-2].name == "(9 : 4,1)" or subchain[-2].name == "(2,2,3 : 4]":
                            attributes.append(False)
                        else:
                            attributes.append(True)
                    else:
                        attributes.append(False)
            subchain_LOOKAHEAD8_attributes.append(attributes)
    return subchain_list, subchain_num_LOOKAHEAD8, subchain_LOOKAHEAD8_attributes


def chain_gen(counter_list: list[counter], layer_no: int, chain_no: int, chain_inputs: list, chain_outputs: list, layer_inputs: list[int], layer_outputs: list[int], reg_flag: bool = False) -> tuple[str, str, str, str]:
    # ------ generation of comments ------
    headComment_str = f"""
    // GPC chain{chain_no} in layer{layer_no}:"""

    for counter in counter_list:
        comment_str = f"""
    // -- {counter.name} at column {counter.applied_column}"""
        headComment_str += comment_str
    headComment_str += f"""
    """

    # ------ analyze the chain into subchains ------
    subchain_list, subchain_num_LA, subchain_LA_attr = analyze_subchain(counter_list)

    # ------ generation regarding LOOKAHEAD8 blocks ------
    signal_decl = """"""
    instan = """"""
    xdc = """"""
    num_LA = len(subchain_num_LA)
    for i in range(num_LA):
        LA_signal_decl, LA_instan = LOOKAHEAD8_gen(subchain_num_LA[i], f"l{layer_no}_c{chain_no}_s{i}", subchain_LA_attr[i])
        signal_decl += LA_signal_decl
        instan += LA_instan

    # ------ generation of GPC LUTs and connection with LOOKAHEAD8------
    start_col = subchain_list[0][0].applied_column
    i_cnt = 0
    pos_cnt = 0
    num_subchain = len(subchain_list)
    for j in range(num_subchain):
        subchain = subchain_list[j]
        len_subchain = len(subchain)
        for i in range(len_subchain):
            if subchain[i] == "CHAIN_END":
                i_cnt = 0
                pos_cnt = 0
                break
            if subchain[i] == "SUBCHAIN_END":
                pos_cnt = 2
            elif subchain[i].name == "(9 : 4,1)":
                # first declare signals and instantiate LUTs
                clk_str = f"clk"
                C0_str = f"C0_c9_41_l{layer_no}_c{chain_no}_i{i_cnt}"
                CLA_str = f"CLA_c9_41_l{layer_no}_c{chain_no}_i{i_cnt}"
                O0_str = f"O0_c9_41_l{layer_no}_c{chain_no}_i{i_cnt}"
                O1_str = f"O1_c9_41_l{layer_no}_c{chain_no}_i{i_cnt}"
                CY_str = f"CY_c9_41_l{layer_no}_c{chain_no}_i{i_cnt}"
                PROP_str = f"PROP_c9_41_l{layer_no}_c{chain_no}_i{i_cnt}"
                MSB_str = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                signal_decl += f"""
    logic [8 : 0] {C0_str};
    logic         {CLA_str};
    logic         {O0_str};
    logic [3 : 0] {O1_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    logic         {MSB_str};
    """
                port_list = [clk_str, C0_str, CLA_str, O0_str, O1_str, CY_str, PROP_str, MSB_str]
                max_len = max(len(s) for s in port_list)
                instan += f"""
    c9_41 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
            .LEAVEC({'"FALSE"' if subchain[i+1] == "CHAIN_END" else '"TRUE" '}),
            .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}))
    c9_41_l{layer_no}_c{chain_no}_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O0  ({O0_str.ljust(max_len)}),
        .O1  ({O1_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
                # generate xdc lines to merge two LUT3s into one physical LUT
                xdc += f"""
### constraints for c9_41_l{layer_no}_c{chain_no}_i{i_cnt} ###
set lut_hi_l{layer_no}_c{chain_no}_i{i_cnt} [get_cells -hier -filter {{NAME =~ "*/c9_41_l{layer_no}_c{chain_no}_i{i_cnt}/LUT3_inst0"}}]
set lut_lo_l{layer_no}_c{chain_no}_i{i_cnt} [get_cells -hier -filter {{NAME =~ "*/c9_41_l{layer_no}_c{chain_no}_i{i_cnt}/LUT3_inst1"}}]
set_property LUTNM grp_l{layer_no}_c{chain_no}_i{i_cnt} $lut_hi_l{layer_no}_c{chain_no}_i{i_cnt}
set_property LUTNM grp_l{layer_no}_c{chain_no}_i{i_cnt} $lut_lo_l{layer_no}_c{chain_no}_i{i_cnt}

"""
                # connect the inputs of LUTs with layer inputs
                col = subchain[i].applied_column - start_col
                if subchain[i].in_cascade is False:
                    instan += f"""
    assign {C0_str} = layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}];
    """
                else:
                    instan += f"""
    assign {C0_str} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}]}};
    """
                # connect the outputs of LUTs with layer outputs
                if layer_outputs[subchain[i].applied_column] == 1:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}"
                else:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}[{chain_outputs[col][0]}]"
                out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}[{max(chain_outputs[col+1])}:{min(chain_outputs[col+1])}]"
                out_str_list = [out_str0, out_str1]
                max_len = max(len(s) for s in out_str_list)
                instan += f"""
    assign {out_str0.ljust(max_len)} = {O0_str};"""
                if subchain[i+1] == "CHAIN_END":
                    instan += f"""
    assign {out_str1.ljust(max_len)} = {O1_str};
    """
                else:
                    instan += f"""
    assign {out_str1.ljust(max_len)} = {O1_str}[2:0];
    """
                # connect LUTs with LOOKAHEAD8
                LUTLA_str0 = CLA_str
                LUTLA_str1 = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                LUTLA_str2 = f"CY_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str3 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2, LUTLA_str3]
                max_len = max(len(s) for s in LUTLA_str_list)
                if pos_cnt % 2:
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {O1_str}[3];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
                else:
                    instan += f"""
    assign {LUTLA_str1.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt//2}];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
                # connect carry in and out between LOOKAHEAD8 blocks is needed
                if pos_cnt % 8 == 7:
                    pos_cnt_temp = pos_cnt + 1
                else:
                    pos_cnt_temp = pos_cnt
                if pos_cnt_temp % 8 == 0:
                    if pos_cnt == 0:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}{"[0]" if subchain_num_LA[j] > 1 else "   "} = {C0_str}[8];
    """
                    else:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt_temp//8}] = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt_temp//2)-1}];
    """
                # increment GPC instance counter and position counter
                pos_cnt += 2
                i_cnt += 1
            elif subchain[i].name == "(6 : 3]":
                # this counter can only start a chain and never ends a chain
                # so it is always the first lut in a counter chain
                # first declare signals and instantiate LUTs
                clk_str = f"clk"
                C0_str = f"C0_c6_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                O_str = f"O_c6_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                MSB_str = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                signal_decl += f"""
    logic [5 : 0] {C0_str};
    logic [2 : 0] {O_str};
    logic         {MSB_str};
    """
                port_list = [clk_str, C0_str, MSB_str]
                max_len = max(len(s) for s in port_list)
                instan += f"""
    c6_3 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
           .LEAVEC('"TRUE" '))
    c6_3_l{layer_no}_c{chain_no}_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}));
    """
                # connect the inputs of LUTs with layer inputs
                col = subchain[i].applied_column - start_col
                instan += f"""
    assign {C0_str} = layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}];
    """
                # connect the outputs of LUTs with layer outputs
                if layer_outputs[subchain[i].applied_column] == 1:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}"
                else:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}[{chain_outputs[col][0]}]"
                if layer_outputs[subchain[i].applied_column+1] == 1:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}"
                else:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}[{chain_outputs[col+1][0]}]"
                out_str_list = [out_str0, out_str1]
                max_len = max(len(s) for s in out_str_list)
                instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];"""
                # connect LUTs with LOOKAHEAD8
                LUTLA_str0 = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                LUTLA_str1 = f"CY_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt}]"
                LUTLA_str2 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt}]"
                LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2]
                max_len = max(len(s) for s in LUTLA_str_list)
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = {O_str}[2];
    assign {LUTLA_str1.ljust(max_len)} = {O_str}[2];
    assign {LUTLA_str2.ljust(max_len)} = 1'b0;
    """
                # connect carry in and out between LOOKAHEAD8 blocks is needed
                instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}{"[0]" if subchain_num_LA[j] > 1 else "   "} = {C0_str}[4];
    """
                # increment GPC instance counter and position counter
                pos_cnt += 1
                i_cnt += 1
            elif subchain[i].name == "(2,2,3 : 4]":
                # first declare signals and instantiate LUTs
                clk_str = f"clk"
                C0_str = f"C0_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                C1_str = f"C1_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                C2_str = f"C2_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                CLA_str = f"CLA_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                O_str = f"O_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                CY_str = f"CY_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                PROP_str = f"PROP_c223_4_l{layer_no}_c{chain_no}_i{i_cnt}"
                MSB_str = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {C1_str};
    logic [1 : 0] {C2_str};
    logic         {CLA_str};
    logic [3 : 0] {O_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    logic         {MSB_str};
    """
                port_list = [clk_str, C0_str, C1_str, C2_str, CLA_str, O_str, CY_str, PROP_str, MSB_str]
                max_len = max(len(s) for s in port_list)
                instan += f"""
    c223_4 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
             .LEAVEC({'"FALSE"' if subchain[i+1] == "CHAIN_END" else '"TRUE" '}),
             .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}))
    c223_4_l{layer_no}_c{chain_no}_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .C1  ({C1_str.ljust(max_len)}),
        .C2  ({C2_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
                # connect the inputs of LUTS with layer inputs
                in_str_list = [C0_str, C1_str, C2_str]
                max_len = max(len(s) for s in in_str_list)
                col = subchain[i].applied_column - start_col
                if subchain[i].in_cascade is False:
                    instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}];
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1}[{chain_inputs[col+1][1]}:{chain_inputs[col+1][0]}];
    assign {C2_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+2}[{chain_inputs[col+2][1]}:{chain_inputs[col+2][0]}];
    """
                else:
                    instan += f"""
    assign {C0_str.ljust(max_len)} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}]}};
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1}[{chain_inputs[col+1][1]}:{chain_inputs[col+1][0]}];
    assign {C2_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+2}[{chain_inputs[col+2][1]}:{chain_inputs[col+2][0]}];
    """
                # connect the outputs of LUTS with layer outputs
                if layer_outputs[subchain[i].applied_column] == 1:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}"
                else:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}[{chain_outputs[col][0]}]"
                if layer_outputs[subchain[i].applied_column+1] == 1:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}"
                else:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}[{chain_outputs[col+1][0]}]"
                if layer_outputs[subchain[i].applied_column+2] == 1:
                    out_str2 = f"layer{layer_no+1}_col{subchain[i].applied_column+2}"
                else:
                    out_str2 = f"layer{layer_no+1}_col{subchain[i].applied_column+2}[{chain_outputs[col+2][0]}]"
                if layer_outputs[subchain[i].applied_column+3] == 1:
                    out_str3 = f"layer{layer_no+1}_col{subchain[i].applied_column+3}"
                else:
                    out_str3 = f"layer{layer_no+1}_col{subchain[i].applied_column+3}[{chain_outputs[col+3][0]}]"
                out_str_list = [out_str0, out_str1, out_str2, out_str3]
                max_len = max(len(s) for s in out_str_list)
                instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];
    assign {out_str2.ljust(max_len)} = {O_str}[2];"""
                if subchain[i+1] == "CHAIN_END":
                    instan += f"""
    assign {out_str3.ljust(max_len)} = {O_str}[3];
    """
                else:
                    instan += f"""
    """
                # connect LUTs with LOOKAHEAD8
                LUTLA_str0 = CLA_str
                LUTLA_str1 = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                LUTLA_str2 = f"CY_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str3 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2, LUTLA_str3]
                max_len = max(len(s) for s in LUTLA_str_list)
                if pos_cnt % 2:
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {O_str}[3];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
                else:
                    instan += f"""
    assign {LUTLA_str1.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt//2}];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
                # connect carry in and out between LOOKAHEAD8 blocks is needed
                if pos_cnt % 8 == 7:
                    pos_cnt_temp = pos_cnt + 1
                else:
                    pos_cnt_temp = pos_cnt
                if pos_cnt_temp % 8 == 0:
                    if pos_cnt == 0:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}{"[0]" if subchain_num_LA[j] > 1 else "   "} = {C0_str}[2];
    """
                    else:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt_temp//8}] = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt_temp//2)-1}];
    """
                # increment GPC instance counter and position counter
                pos_cnt += 2
                i_cnt += 1
            elif subchain[i].name == "(3 : 2]":
                # first declare signals and instantiate LUTs
                clk_str = f"clk"
                C0_str = f"C0_c3_2_l{layer_no}_c{chain_no}_i{i_cnt}"
                O_str = f"O_c3_2_l{layer_no}_c{chain_no}_i{i_cnt}"
                CY_str = f"CY_c3_2_l{layer_no}_c{chain_no}_i{i_cnt}"
                PROP_str = f"PROP_c3_2_l{layer_no}_c{chain_no}_i{i_cnt}"
                MSB_str = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {O_str};
    logic         {CY_str};
    logic         {PROP_str};
    logic         {MSB_str};
    """
                port_list = [clk_str, C0_str, O_str, CY_str, PROP_str, MSB_str]
                max_len = max(len(s) for s in port_list)
                instan += f"""
    c3_2 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
           .LEAVEC({'"FALSE"' if subchain[i+1] == "CHAIN_END" else '"TRUE" '}),
           .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
           .FIRSTS({'"TRUE" ' if pos_cnt < 2 else '"FALSE"'}),
           .LASTS ({'"TRUE" ' if i == len_subchain-2 else '"FALSE"'}))
    c3_2_l{layer_no}_c{chain_no}_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
                # connect the inputs of LUTs with layer inputs
                col = subchain[i].applied_column - start_col
                if subchain[i].in_cascade is False:
                    if len(chain_inputs[col]) == 2:
                        instan += f"""
    assign {C0_str} = {{layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}], 1'b0}};
    """
                    elif len(chain_inputs[col]) == 1:
                        instan += f"""
    assign {C0_str} = {{layer{layer_no}_col{subchain[i].applied_column}[{chain_inputs[col][0]}], 2'b0}};
    """
                    else:
                        instan += f"""
    assign {C0_str} = layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}];
    """
                else:
                    if len(chain_inputs[col]) == 1:
                        instan += f"""
    assign {C0_str} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{chain_inputs[col][0]}], 1'b0}};
    """
                    else:
                        instan += f"""
    assign {C0_str} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}]}};
    """
                # connect the outputs of LUTs with layer outputs
                if layer_outputs[subchain[i].applied_column] == 1:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}"
                else:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}[{chain_outputs[col][0]}]"
                if layer_outputs[subchain[i].applied_column+1] == 1:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}"
                else:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}[{chain_outputs[col+1][0]}]"
                out_str_list = [out_str0, out_str1]
                max_len = max(len(s) for s in out_str_list)
                instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];"""
                if subchain[i+1] == "CHAIN_END":
                    instan += f"""
    assign {out_str1.ljust(max_len)} = {O_str}[1];
    """
                else:
                    instan += f"""
    """
                # connect LUTs with LOOKAHEAD8
                LUTLA_str0 = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                LUTLA_str1 = f"CY_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt}]"
                LUTLA_str2 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt}]"
                LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2]
                max_len = max(len(s) for s in LUTLA_str_list)
                if pos_cnt % 2 == 0:
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = {O_str}[1];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
                else:
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
                # connect carry in and out between LOOKAHEAD8 blocks is needed
                if pos_cnt % 8 == 0:
                    if pos_cnt == 0:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}{"[0]" if subchain_num_LA[j] > 1 else "   "} = {C0_str}[2];
    """
                    else:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt//8}] = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt//2)-1}];
    """
                # increment GPC instance counter and position counter
                pos_cnt += 1
                i_cnt += 1
            elif subchain[i].name == "(1,5 : 3]":
                # first declare signals and instantiate LUTs
                clk_str = f"clk"
                C0_str = f"C0_c15_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                C1_str = f"C1_c15_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                CLA_str = f"CLA_c15_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                O_str = f"O_c15_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                CY_str = f"CY_c15_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                PROP_str = f"PROP_c15_3_l{layer_no}_c{chain_no}_i{i_cnt}"
                MSB_str = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                signal_decl += f"""
    logic [4 : 0] {C0_str};
    logic         {C1_str};
    logic         {CLA_str};
    logic [2 : 0] {O_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    logic         {MSB_str};
    """
                port_list = [clk_str, C0_str, C1_str, CLA_str, O_str, CY_str, PROP_str, MSB_str]
                max_len = max(len(s) for s in port_list)
                instan += f"""
    c15_3 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
            .LEAVEC({'"FALSE"' if subchain[i+1] == "CHAIN_END" else '"TRUE" '}),
            .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
            .FIRSTS({'"TRUE" ' if pos_cnt < 2 else '"FALSE"'}),
            .LASTS ({'"TRUE" ' if i == len_subchain-2 else '"FALSE"'}))
    c15_3_l{layer_no}_c{chain_no}_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .C1  ({C1_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
                # connect the inputs of LUTS with layer inputs
                in_str_list = [C0_str, C1_str]
                max_len = max(len(s) for s in in_str_list)
                col = subchain[i].applied_column - start_col
                if subchain[i].in_cascade is False:
                    if len(chain_inputs[col]) == 4:
                        instan += f"""
    assign {C0_str.ljust(max_len)} = {{layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}], 1'b0}};"""
                    else:
                        instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}];"""
                else:
                    if len(chain_inputs[col]) == 3:
                        instan += f"""
    assign {C0_str.ljust(max_len)} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}], 1'b0}};"""
                    elif len(chain_inputs[col]) == 2:
                        instan += f"""
    assign {C0_str.ljust(max_len)} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}], 2'b0}};"""
                    else:
                        instan += f"""
    assign {C0_str.ljust(max_len)} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}]}};"""
                if len(chain_inputs[col+1]) == 1:
                    if layer_inputs[subchain[i].applied_column+1] == 1:
                        instan += f"""
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1};
    """
                    else:
                        instan += f"""
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1}[{chain_inputs[col+1][0]}];
    """
                else:
                    instan += f"""
    assign {C1_str.ljust(max_len)} = 1'b0;
    """
                # connect the outputs of LUTS with layer outputs
                if layer_outputs[subchain[i].applied_column] == 1:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}"
                else:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}[{chain_outputs[col][0]}]"
                if layer_outputs[subchain[i].applied_column+1] == 1:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}"
                else:
                    out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}[{chain_outputs[col+1][0]}]"
                if layer_outputs[subchain[i].applied_column+2] == 1:
                    out_str2 = f"layer{layer_no+1}_col{subchain[i].applied_column+2}"
                else:
                    out_str2 = f"layer{layer_no+1}_col{subchain[i].applied_column+2}[{chain_outputs[col+2][0]}]"
                out_str_list = [out_str0, out_str1, out_str2]
                max_len = max(len(s) for s in out_str_list)
                instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];"""
                if subchain[i+1] == "CHAIN_END":
                    instan += f"""
    assign {out_str2.ljust(max_len)} = {O_str}[2];
    """
                else:
                        instan += f"""
    """
                # connect LUTs with LOOKAHEAD8
                LUTLA_str0 = CLA_str
                LUTLA_str1 = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                LUTLA_str2 = f"CY_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str3 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2, LUTLA_str3]
                max_len = max(len(s) for s in LUTLA_str_list)
                if pos_cnt % 2:
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {O_str}[2];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
                else:
                    instan += f"""
    assign {LUTLA_str1.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt//2}];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
                # connect carry in and out between LOOKAHEAD8 blocks is needed
                if pos_cnt % 8 == 7:
                    pos_cnt_temp = pos_cnt + 1
                else:
                    pos_cnt_temp = pos_cnt
                if pos_cnt_temp % 8 == 0:
                    if pos_cnt == 0:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}{"[0]" if subchain_num_LA[j] > 1 else "   "} = {C0_str}[4];
    """
                    else:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt_temp//8}] = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt_temp//2)-1}];
    """
                # increment GPC instance counter and position counter
                pos_cnt += 2
                i_cnt += 1
            elif subchain[i].name == "(3,9 : 2,3,1)":
                # the counter that can ends a subchain and starts a new one
                # first declare signals and instantiate LUTs
                clk_str = f"clk"
                C0_str = f"C0_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                C1_str = f"C1_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                CLA_str = f"CLA_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                O0_str = f"O0_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                O1_str = f"O1_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                O2_str = f"O2_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                CY0_str = f"CY0_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                CY1_str = f"CY1_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                PROP0_str = f"PROP0_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                PROP1_str = f"PROP1_c39_231_l{layer_no}_c{chain_no}_i{i_cnt}"
                MSB_str = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                signal_decl += f"""
    logic [8 : 0] {C0_str};
    logic [2 : 0] {C1_str};
    logic         {CLA_str};
    logic         {O0_str};
    logic [2 : 0] {O1_str};
    logic [1 : 0] {O2_str};
    logic [1 : 0] {CY0_str};
    logic [1 : 0] {CY1_str};
    logic [1 : 0] {PROP0_str};
    logic [1 : 0] {PROP1_str};
    logic         {MSB_str};
    """
                port_list = [clk_str, C0_str, C1_str, CLA_str, O0_str, O1_str, O2_str, CY0_str, CY1_str, PROP0_str, PROP1_str, MSB_str]
                max_len = max(len(s) for s in port_list)
                instan += f"""
    c39_231 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
              .LEAVEC({'"FALSE"' if subchain[i+1] == "CHAIN_END" else '"TRUE" '}),
              .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}))
    c39_231_l{layer_no}_c{chain_no}_i{i_cnt}(
        .clk  ({clk_str.ljust(max_len)}),
        .C0   ({C0_str.ljust(max_len)}),
        .C1   ({C1_str.ljust(max_len)}),
        .CLA  ({CLA_str.ljust(max_len)}),
        .O0   ({O0_str.ljust(max_len)}),
        .O1   ({O1_str.ljust(max_len)}),
        .O2   ({O2_str.ljust(max_len)}),
        .CY0  ({CY0_str.ljust(max_len)}),
        .CY1  ({CY1_str.ljust(max_len)}),
        .PROP0({PROP0_str.ljust(max_len)}),
        .PROP1({PROP1_str.ljust(max_len)}));
    """
                # connect the inputs of LUTS with layer inputs
                in_str_list = [C0_str, C1_str]
                max_len = max(len(s) for s in in_str_list)
                col = subchain[i].applied_column - start_col
                if subchain[i].in_cascade is False:
                    instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}];
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1}[{max(chain_inputs[col+1])}:{min(chain_inputs[col+1])}];
    """
                else:
                    instan += f"""
    assign {C0_str.ljust(max_len)} = {{l{layer_no}_c{chain_no}_i{i_cnt-1}, layer{layer_no}_col{subchain[i].applied_column}[{max(chain_inputs[col])}:{min(chain_inputs[col])}]}};
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1}[{max(chain_inputs[col+1])}:{min(chain_inputs[col+1])}];
    """
                # connect the outputs of LUTS with layer outputs
                if layer_outputs[subchain[i].applied_column] == 1:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}"
                else:
                    out_str0 = f"layer{layer_no+1}_col{subchain[i].applied_column}[{chain_outputs[col][0]}]"
                out_str1 = f"layer{layer_no+1}_col{subchain[i].applied_column+1}[{max(chain_outputs[col+1])}:{min(chain_outputs[col+1])}]"
                if subchain[i+1] == "CHAIN_END":
                    out_str2 = f"layer{layer_no+1}_col{subchain[i].applied_column+2}[{max(chain_outputs[col+2])}:{min(chain_outputs[col+2])}]"
                else:
                    out_str2 = f"layer{layer_no+1}_col{subchain[i].applied_column+2}[{chain_outputs[col+2][-1]}]"
                out_str_list = [out_str0, out_str1, out_str2]
                max_len = max(len(s) for s in out_str_list)
                instan += f"""
    assign {out_str0.ljust(max_len)} = {O0_str};
    assign {out_str1.ljust(max_len)} = {O1_str};"""
                if subchain[i+1] == "CHAIN_END":
                    instan += f"""
    assign {out_str2.ljust(max_len)} = {O2_str};
    """
                else:
                    instan += f"""
    assign {out_str2.ljust(max_len)} = {O2_str}[0];
    """
                # connect LUTs with LOOKAHEAD8
                LUTLA_str0 = CLA_str
                LUTLA_str1 = f"l{layer_no}_c{chain_no}_i{i_cnt}"
                LUTLA_str2 = f"CY_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str3 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt+1}:{pos_cnt}]"
                LUTLA_str4 = f"CY_LA_l{layer_no}_c{chain_no}_s{j+1}[1:0]"
                LUTLA_str5 = f"PROP_LA_l{layer_no}_c{chain_no}_s{j+1}[1:0]"
                if j == len(subchain_num_LA)-1:
                    LUTLA_str6 = f"CIN_LA_l{layer_no}_c{chain_no}_s{j+1}"
                elif subchain_num_LA[j+1] > 1:
                    LUTLA_str6 = f"CIN_LA_l{layer_no}_c{chain_no}_s{j+1}[0]"
                else:
                    LUTLA_str6 = f"CIN_LA_l{layer_no}_c{chain_no}_s{j+1}"
                LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2, LUTLA_str3, LUTLA_str4, LUTLA_str5, LUTLA_str6]
                max_len = max(len(s) for s in LUTLA_str_list)
                if subchain[i+1] != "CHAIN_END":
                    idx = pos_cnt if pos_cnt == 0 else (pos_cnt-1)//2
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{idx}];
    assign {LUTLA_str1.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j+1}[0];
    assign {LUTLA_str2.ljust(max_len)} = {CY0_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP0_str};
    assign {LUTLA_str4.ljust(max_len)} = {CY1_str};
    assign {LUTLA_str5.ljust(max_len)} = {PROP1_str};
    assign {LUTLA_str6.ljust(max_len)} = layer{layer_no}_col{subchain[i].applied_column+1}[{chain_inputs[col+1][1]}];
    """
                else:
                    idx = pos_cnt if pos_cnt == 0 else (pos_cnt-1)//2
                    instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{idx}];
    assign {LUTLA_str2.ljust(max_len)} = {CY0_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP0_str};
    """
                # connect carry in and out between LOOKAHEAD8 blocks is needed
                if pos_cnt % 8 == 7 :
                    pos_cnt_temp = pos_cnt + 1
                else:
                    pos_cnt_temp = pos_cnt
                if pos_cnt_temp % 8 == 0:
                    if pos_cnt == 0:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}{"[0]" if subchain_num_LA[j] > 1 else "   "} = {C0_str}[8];
    """
                    else:
                        instan += f"""
    assign CIN_LA_l{layer_no}_c{chain_no}_s{j}[{pos_cnt_temp//8}] = COUT_LA_l{layer_no}_c{chain_no}_s{j}[{(pos_cnt_temp//2)-1}];
    """
                # increment GPC instance counter and position counter(no need for this counter)
                i_cnt += 1

    return headComment_str, signal_decl, instan, xdc


def floatingGPC_gen(counter: counter, layer_no: int, floatingGPC_no: int, counter_inputs: list, counter_outputs: list, layer_inputs: list[int], layer_outputs: list[int], reg_flag: bool = False ) -> tuple[str, str, str, str]:
    # ------ generation of comments ------
    headComment_str = f"""
    // GPC{floatingGPC_no} in layer{layer_no}: {counter.name} at column {counter.applied_column}
    """
    # ------ generation of GPC LUTs ------
    signal_decl = f""
    instan = f""
    xdc = f""
    if counter.name == "(3 : 2]":
        clk_str = f"clk"
        C0_str = f"C0_c3_2_l{layer_no}_f{floatingGPC_no}"
        O_str = f"O_c3_2_l{layer_no}_i{floatingGPC_no}"
        CY_str = f"CY_c3_2_l{layer_no}_f{floatingGPC_no}"
        PROP_str = f"PROP_c3_2_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {O_str};
    logic         {CY_str};
    logic         {PROP_str};
    """
        port_list = [clk_str, C0_str, O_str, CY_str, PROP_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c3_2 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
           .LEAVEC({'"FALSE"'}),
           .POSODD({'"FALSE"'}),
           .FIRSTS({'"FALSE"'}),
           .LASTS ({'"FALSE"'}))
    c3_2_l{layer_no}_f{floatingGPC_no}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # connect the inputs of LUTs with layer inputs
        if len(counter_inputs[0]) == 2:
            instan += f"""
    assign {C0_str}[2:1] = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    assign {C0_str}[0]   = 1'b0;
    """
        else:
            instan += f"""
    assign {C0_str} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    """
        # connect the outputs of LUTs with layer outputs
        if layer_outputs[counter.applied_column] == 1:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}"
        else:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        if layer_outputs[counter.applied_column+1] == 1:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}"
        else:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{counter_outputs[1][0]}]"
        out_str_list = [out_str0, out_str1]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];
    """
    if counter.name == "(6 : 3]":
        clk_str = f"clk"
        C0_str = f"C0_c6_3_l{layer_no}_f{floatingGPC_no}"
        O_str = f"O_c6_3_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [5 : 0] {C0_str};
    logic [2 : 0] {O_str};
    """
        port_list = [clk_str, C0_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c6_3 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
           .LEAVEC("FALSE"))
    c6_3_l{layer_no}_f{floatingGPC_no}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}));
    """
        # connect the inputs of LUTs with layer inputs
        instan += f"""
    assign {C0_str} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    """
        # connect the outputs of LUTs with layer outputs
        if layer_outputs[counter.applied_column] == 1:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}"
        else:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        if layer_outputs[counter.applied_column+1] == 1:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}"
        else:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{counter_outputs[1][0]}]"
        if layer_outputs[counter.applied_column+2] == 1:
            out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}"
        else:
            out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}[{counter_outputs[2][0]}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];
    assign {out_str2.ljust(max_len)} = {O_str}[2];"""
    if counter.name == "(9 : 4,1)":
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c9_41_l{layer_no}_f{floatingGPC_no}"
        CLA_str = f"CLA_c9_41_l{layer_no}_f{floatingGPC_no}"
        O0_str = f"O0_c9_41_l{layer_no}_f{floatingGPC_no}"
        O1_str = f"O1_c9_41_l{layer_no}_f{floatingGPC_no}"
        CY_str = f"CY_c9_41_l{layer_no}_f{floatingGPC_no}"
        PROP_str = f"PROP_c9_41_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [8 : 0] {C0_str};
    logic         {CLA_str};
    logic         {O0_str};
    logic [3 : 0] {O1_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    """
        port_list = [clk_str, C0_str, CLA_str, O0_str, O1_str, CY_str, PROP_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c9_41 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
            .LEAVEC({'"FALSE"'}),
            .POSODD({'"FALSE"'}))
    c9_41_l{layer_no}_f{floatingGPC_no}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O0  ({O0_str.ljust(max_len)}),
        .O1  ({O1_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # generate xdc to merge two LUT3s into one physical LUT
        xdc += f"""
### constraints for c9_41_l{layer_no}_f{floatingGPC_no} ###
set lut_hi_l{layer_no}_f{floatingGPC_no} [get_cells -hier -filter {{NAME =~ "*/c9_41_l{layer_no}_f{floatingGPC_no}/LUT3_inst0"}}]
set lut_lo_l{layer_no}_f{floatingGPC_no} [get_cells -hier -filter {{NAME =~ "*/c9_41_l{layer_no}_f{floatingGPC_no}/LUT3_inst1"}}]
set_property LUTNM grp_l{layer_no}_f{floatingGPC_no} $lut_hi_l{layer_no}_f{floatingGPC_no}
set_property LUTNM grp_l{layer_no}_f{floatingGPC_no} $lut_lo_l{layer_no}_f{floatingGPC_no}


"""
        # connect the inputs of LUTs with layer inputs
        instan += f"""
    assign {C0_str} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    """
        # connect the outputs of LUTs with layer outputs
        if layer_outputs[counter.applied_column] == 1:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}"
        else:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{max(counter_outputs[1])}:{min(counter_outputs[1])}]"
        out_str_list = [out_str0, out_str1]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O0_str};
    assign {out_str1.ljust(max_len)} = {O1_str};
    """
    if counter.name == "(1,5 : 3]":
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c15_3_l{layer_no}_f{floatingGPC_no}"
        C1_str = f"C1_c15_3_l{layer_no}_f{floatingGPC_no}"
        CLA_str = f"CLA_c15_3_l{layer_no}_f{floatingGPC_no}"
        O_str = f"O_c15_3_l{layer_no}_f{floatingGPC_no}"
        CY_str = f"CY_c15_3_l{layer_no}_f{floatingGPC_no}"
        PROP_str = f"PROP_c15_3_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [4 : 0] {C0_str};
    logic         {C1_str};
    logic         {CLA_str};
    logic [2 : 0] {O_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    """
        port_list = [clk_str, C0_str, C1_str, CLA_str, O_str, CY_str, PROP_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c15_3 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
            .LEAVEC({'"FALSE"'}),
            .POSODD({'"FALSE"'}),
            .FIRSTS({'"TRUE" '}),
            .LASTS ({'"FALSE"'}))
    c15_3_l{layer_no}_f{floatingGPC_no}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .C1  ({C1_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str]
        max_len = max(len(s) for s in in_str_list)
        if len(counter_inputs[0]) == 5:
            instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];"""
        elif len(counter_inputs[0]) == 4:
            instan += f"""
    assign {C0_str.ljust(max_len)} = {{layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}], 1'b0}};"""
        else:
            instan += f"""
    assign {C0_str.ljust(max_len)} = {{layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}], 2'b0}};"""
        if len(counter_inputs[1]) == 1:
            if layer_inputs[counter.applied_column+1] == 1:
                instan += f"""
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+1};
    """
            else:
                instan += f"""
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+1}[{counter_inputs[1][0]}];
    """
        else:
            instan += f"""
    assign {C1_str.ljust(max_len)} = 1'b0;
    """
        # connect the outputs of LUTS with layer outputs
        if layer_outputs[counter.applied_column] == 1:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}"
        else:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        if layer_outputs[counter.applied_column+1] == 1:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}"
        else:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{counter_outputs[1][0]}]"
        if layer_outputs[counter.applied_column+2] == 1:
            out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}"
        else:
            out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}[{counter_outputs[2][0]}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];
    assign {out_str2.ljust(max_len)} = {O_str}[2];
    """
    if counter.name == "(3,9 : 2,3,1)":
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c39_231_l{layer_no}_f{floatingGPC_no}"
        C1_str = f"C1_c39_231_l{layer_no}_f{floatingGPC_no}"
        CLA_str = f"CLA_c39_231_l{layer_no}_f{floatingGPC_no}"
        O0_str = f"O0_c39_231_l{layer_no}_f{floatingGPC_no}"
        O1_str = f"O1_c39_231_l{layer_no}_f{floatingGPC_no}"
        O2_str = f"O2_c39_231_l{layer_no}_f{floatingGPC_no}"
        CY0_str = f"CY0_c39_231_l{layer_no}_f{floatingGPC_no}"
        CY1_str = f"CY1_c39_231_l{layer_no}_f{floatingGPC_no}"
        PROP0_str = f"PROP0_c39_231_l{layer_no}_f{floatingGPC_no}"
        PROP1_str = f"PROP1_c39_231_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [8 : 0] {C0_str};
    logic [2 : 0] {C1_str};
    logic         {CLA_str};
    logic         {O0_str};
    logic [2 : 0] {O1_str};
    logic [1 : 0] {O2_str};
    logic [1 : 0] {CY0_str};
    logic [1 : 0] {CY1_str};
    logic [1 : 0] {PROP0_str};
    logic [1 : 0] {PROP1_str};
    """
        port_list = [clk_str, C0_str, C1_str, CLA_str, O0_str, O1_str, O2_str, CY0_str, CY1_str, PROP0_str, PROP1_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c39_231 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
              .LEAVEC({'"FALSE"'}),
              .POSODD({'"FALSE"'}))
    c39_231_l{layer_no}_f{floatingGPC_no}(
        .clk  ({clk_str.ljust(max_len)}),
        .C0   ({C0_str.ljust(max_len)}),
        .C1   ({C1_str.ljust(max_len)}),
        .CLA  ({CLA_str.ljust(max_len)}),
        .O0   ({O0_str.ljust(max_len)}),
        .O1   ({O1_str.ljust(max_len)}),
        .O2   ({O2_str.ljust(max_len)}),
        .CY0  ({CY0_str.ljust(max_len)}),
        .CY1  ({CY1_str.ljust(max_len)}),
        .PROP0({PROP0_str.ljust(max_len)}),
        .PROP1({PROP1_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str]
        max_len = max(len(s) for s in in_str_list)
        instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+1}[{max(counter_inputs[1])}:{min(counter_inputs[1])}];
    """
        # connect the outputs of LUTS with layer outputs
        if layer_outputs[counter.applied_column] == 1:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}"
        else:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{max(counter_outputs[1])}:{min(counter_outputs[1])}]"
        out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}[{max(counter_outputs[2])}:{min(counter_outputs[2])}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O0_str};
    assign {out_str1.ljust(max_len)} = {O1_str};
    assign {out_str2.ljust(max_len)} = {O2_str};
    """
    if counter.name == "(2,2,3 : 4]":
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c223_4_l{layer_no}_f{floatingGPC_no}"
        C1_str = f"C1_c223_4_l{layer_no}_f{floatingGPC_no}"
        C2_str = f"C2_c223_4_l{layer_no}_f{floatingGPC_no}"
        CLA_str = f"CLA_c223_4_l{layer_no}_f{floatingGPC_no}"
        O_str = f"O_c223_4_l{layer_no}_f{floatingGPC_no}"
        CY_str = f"CY_c223_4_l{layer_no}_f{floatingGPC_no}"
        PROP_str = f"PROP_c223_4_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {C1_str};
    logic [1 : 0] {C2_str};
    logic         {CLA_str};
    logic [3 : 0] {O_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    """
        port_list = [clk_str, C0_str, C1_str, C2_str, CLA_str, O_str, CY_str, PROP_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c223_4 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
             .LEAVEC({'"FALSE"'}),
             .POSODD({'"FALSE"'}))
    c223_4_l{layer_no}_f{floatingGPC_no}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .C1  ({C1_str.ljust(max_len)}),
        .C2  ({C2_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str, C2_str]
        max_len = max(len(s) for s in in_str_list)
        instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+1}[{counter_inputs[1][1]}:{counter_inputs[1][0]}];
    assign {C2_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+2}[{counter_inputs[2][1]}:{counter_inputs[2][0]}];
    """
        # connect the outputs of LUTS with layer outputs
        if layer_outputs[counter.applied_column] == 1:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}"
        else:
            out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        if layer_outputs[counter.applied_column+1] == 1:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}"
        else:
            out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{counter_outputs[1][0]}]"
        if layer_outputs[counter.applied_column+2] == 1:
            out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}"
        else:
            out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}[{counter_outputs[2][0]}]"
        if layer_outputs[counter.applied_column+3] == 1:
            out_str3 = f"layer{layer_no+1}_col{counter.applied_column+3}"
        else:
            out_str3 = f"layer{layer_no+1}_col{counter.applied_column+3}[{counter_outputs[3][0]}]"
        out_str_list = [out_str0, out_str1, out_str2, out_str3]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];
    assign {out_str2.ljust(max_len)} = {O_str}[2];
    assign {out_str3.ljust(max_len)} = {O_str}[3];
    """
    if counter.name == "(4,13 : 3,4,1)":
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c413_341_l{layer_no}_f{floatingGPC_no}"
        C1_str = f"C1_c413_341_l{layer_no}_f{floatingGPC_no}"
        CLA_str = f"CLA_c413_341_l{layer_no}_f{floatingGPC_no}"
        O0_str = f"O0_c413_341_l{layer_no}_f{floatingGPC_no}"
        O1_str = f"O1_c413_341_l{layer_no}_f{floatingGPC_no}"
        O2_str = f"O2_c413_341_l{layer_no}_f{floatingGPC_no}"
        CY0_str = f"CY0_c413_341_l{layer_no}_f{floatingGPC_no}"
        PROP0_str = f"PROP0_c413_341_l{layer_no}_f{floatingGPC_no}"
        CY1_str = f"CY1_c413_341_l{layer_no}_f{floatingGPC_no}"
        PROP1_str = f"PROP1_c413_341_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [12 : 0] {C0_str};
    logic [3  : 0] {C1_str};
    logic [1  : 0] {CLA_str};
    logic          {O0_str};
    logic [3  : 0] {O1_str};
    logic [2  : 0] {O2_str};
    logic [2  : 0] {CY0_str};
    logic [2  : 0] {PROP0_str};
    logic [2  : 0] {CY1_str};
    logic [2  : 0] {PROP1_str};
    """
        port_list = [clk_str, C0_str, C1_str, CLA_str, O0_str, O1_str, O2_str, CY0_str, PROP0_str, CY1_str, PROP1_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c413_341 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
               .LEAVEC({'"FALSE"'}))
    c413_341_l{layer_no}_f{floatingGPC_no}(
        .clk  ({clk_str.ljust(max_len)}),
        .C0   ({C0_str.ljust(max_len)}),
        .C1   ({C1_str.ljust(max_len)}),
        .CLA  ({CLA_str.ljust(max_len)}),
        .O0   ({O0_str.ljust(max_len)}),
        .O1   ({O1_str.ljust(max_len)}),
        .O2   ({O2_str.ljust(max_len)}),
        .CY0  ({CY0_str.ljust(max_len)}),
        .PROP0({PROP0_str.ljust(max_len)}),
        .CY1  ({CY1_str.ljust(max_len)}),
        .PROP1({PROP1_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str]
        max_len = max(len(s) for s in in_str_list)
        instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+1}[{max(counter_inputs[1])}:{min(counter_inputs[1])}];
    """
        # connect the outputs of LUTS with layer outputs
        out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{max(counter_outputs[1])}:{min(counter_outputs[1])}]"
        out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}[{max(counter_outputs[2])}:{min(counter_outputs[2])}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O0_str};
    assign {out_str1.ljust(max_len)} = {O1_str};
    assign {out_str2.ljust(max_len)} = {O2_str};
    """
        # connect LUTs with LOOKAHEAD8
        LA_signal_decl, LA_instan = LOOKAHEAD8_gen(1, f"l{layer_no}_f{floatingGPC_no}", [False, False, False, False])
        signal_decl += LA_signal_decl
        instan += LA_instan
        LA_LUT_str0 = CLA_str+"[0]"
        LA_LUT_str1 = CLA_str+"[1]"
        LA_LUT_str2 = f"CIN_LA_l{layer_no}_f{floatingGPC_no}"
        LA_LUT_str3 = f"CY_LA_l{layer_no}_f{floatingGPC_no}[2:0]"
        LA_LUT_str4 = f"CY_LA_l{layer_no}_f{floatingGPC_no}[6:4]"
        LA_LUT_str5 = f"PROP_LA_l{layer_no}_f{floatingGPC_no}[2:0]"
        LA_LUT_str6 = f"PROP_LA_l{layer_no}_f{floatingGPC_no}[6:4]"
        LA_LUT_str7 = f"PROP_LA_l{layer_no}_f{floatingGPC_no}[3]"
        LA_LUT_str8 = f"CY_LA_l{layer_no}_f{floatingGPC_no}[3]"
        out_str_list = [LA_LUT_str0, LA_LUT_str1, LA_LUT_str2, LA_LUT_str3, LA_LUT_str4, LA_LUT_str5, LA_LUT_str6, LA_LUT_str7, LA_LUT_str8]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {LA_LUT_str0.ljust(max_len)} = COUT_LA_l{layer_no}_f{floatingGPC_no}[0];
    assign {LA_LUT_str1.ljust(max_len)} = COUT_LA_l{layer_no}_f{floatingGPC_no}[2];
    assign {LA_LUT_str2.ljust(max_len)} = {C0_str}[8];
    assign {LA_LUT_str3.ljust(max_len)} = {CY0_str};
    assign {LA_LUT_str4.ljust(max_len)} = {CY1_str};
    assign {LA_LUT_str5.ljust(max_len)} = {PROP0_str};
    assign {LA_LUT_str6.ljust(max_len)} = {PROP1_str};
    assign {LA_LUT_str7.ljust(max_len)} = 1'b0;
    assign {LA_LUT_str8.ljust(max_len)} = 1'b0;
    """
    if counter.name == "(5,17 : 4,5,1)":
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c517_451_l{layer_no}_f{floatingGPC_no}"
        C1_str = f"C1_c517_451_l{layer_no}_f{floatingGPC_no}"
        CLA_str = f"CLA_c517_451_l{layer_no}_f{floatingGPC_no}"
        O0_str = f"O0_c517_451_l{layer_no}_f{floatingGPC_no}"
        O1_str = f"O1_c517_451_l{layer_no}_f{floatingGPC_no}"
        O2_str = f"O2_c517_451_l{layer_no}_f{floatingGPC_no}"
        CY0_str = f"CY0_c517_451_l{layer_no}_f{floatingGPC_no}"
        PROP0_str = f"PROP0_c517_451_l{layer_no}_f{floatingGPC_no}"
        CY1_str = f"CY1_c517_451_l{layer_no}_f{floatingGPC_no}"
        PROP1_str = f"PROP1_c517_451_l{layer_no}_f{floatingGPC_no}"
        signal_decl += f"""
    logic [16 : 0] {C0_str};
    logic [4  : 0] {C1_str};
    logic [1  : 0] {CLA_str};
    logic          {O0_str};
    logic [4  : 0] {O1_str};
    logic [3  : 0] {O2_str};
    logic [3  : 0] {CY0_str};
    logic [3  : 0] {PROP0_str};
    logic [3  : 0] {CY1_str};
    logic [3  : 0] {PROP1_str};
    """
        port_list = [clk_str, C0_str, C1_str, CLA_str, O0_str, O1_str, O2_str, CY0_str, PROP0_str, CY1_str, PROP1_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c517_451 #(.OUTREG({'"TRUE" ' if reg_flag else '"FALSE"'}),
               .LEAVEC({'"FALSE"'}))
    c517_451_l{layer_no}_f{floatingGPC_no}(
        .clk  ({clk_str.ljust(max_len)}),
        .C0   ({C0_str.ljust(max_len)}),
        .C1   ({C1_str.ljust(max_len)}),
        .CLA  ({CLA_str.ljust(max_len)}),
        .O0   ({O0_str.ljust(max_len)}),
        .O1   ({O1_str.ljust(max_len)}),
        .O2   ({O2_str.ljust(max_len)}),
        .CY0  ({CY0_str.ljust(max_len)}),
        .PROP0({PROP0_str.ljust(max_len)}),
        .CY1  ({CY1_str.ljust(max_len)}),
        .PROP1({PROP1_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str]
        max_len = max(len(s) for s in in_str_list)
        instan += f"""
    assign {C0_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column}[{max(counter_inputs[0])}:{min(counter_inputs[0])}];
    assign {C1_str.ljust(max_len)} = layer{layer_no}_col{counter.applied_column+1}[{max(counter_inputs[1])}:{min(counter_inputs[1])}];
    """
        # connect the outputs of LUTS with layer outputs
        out_str0 = f"layer{layer_no+1}_col{counter.applied_column}[{counter_outputs[0][0]}]"
        out_str1 = f"layer{layer_no+1}_col{counter.applied_column+1}[{max(counter_outputs[1])}:{min(counter_outputs[1])}]"
        out_str2 = f"layer{layer_no+1}_col{counter.applied_column+2}[{max(counter_outputs[2])}:{min(counter_outputs[2])}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O0_str};
    assign {out_str1.ljust(max_len)} = {O1_str};
    assign {out_str2.ljust(max_len)} = {O2_str};
    """
        # connect LUTs with LOOKAHEAD8
        LA_signal_decl, LA_instan = LOOKAHEAD8_gen(1, f"l{layer_no}_f{floatingGPC_no}", [False, False, False, False])
        signal_decl += LA_signal_decl
        instan += LA_instan
        LA_LUT_str0 = CLA_str+"[0]"
        LA_LUT_str1 = CLA_str+"[1]"
        LA_LUT_str2 = f"CIN_LA_l{layer_no}_f{floatingGPC_no}"
        LA_LUT_str3 = f"CY_LA_l{layer_no}_f{floatingGPC_no}[3:0]"
        LA_LUT_str4 = f"CY_LA_l{layer_no}_f{floatingGPC_no}[7:4]"
        LA_LUT_str5 = f"PROP_LA_l{layer_no}_f{floatingGPC_no}[3:0]"
        LA_LUT_str6 = f"PROP_LA_l{layer_no}_f{floatingGPC_no}[7:4]"
        out_str_list = [LA_LUT_str0, LA_LUT_str1, LA_LUT_str2, LA_LUT_str3, LA_LUT_str4, LA_LUT_str5, LA_LUT_str6]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {LA_LUT_str0.ljust(max_len)} = COUT_LA_l{layer_no}_f{floatingGPC_no}[0];
    assign {LA_LUT_str1.ljust(max_len)} = COUT_LA_l{layer_no}_f{floatingGPC_no}[2];
    assign {LA_LUT_str2.ljust(max_len)} = {C0_str}[8];
    assign {LA_LUT_str3.ljust(max_len)} = {CY0_str};
    assign {LA_LUT_str4.ljust(max_len)} = {CY1_str};
    assign {LA_LUT_str5.ljust(max_len)} = {PROP0_str};
    assign {LA_LUT_str6.ljust(max_len)} = {PROP1_str};
    """
    return headComment_str, signal_decl, instan, xdc


def assignment_gen(layer_no: int, assign_list: list, reg_flag: bool) -> str:
    assign_str = f""
    num_col = len(assign_list)
    if not reg_flag:
        for col in range(num_col):
            col_assign_list = assign_list[col]
            for old_idx, new_idx in col_assign_list:
                if len(col_assign_list) == 1:
                    if old_idx == 0 and new_idx == 0:
                        assign_str += f"""
    assign layer{layer_no+1}_col{col}    = layer{layer_no}_col{col};"""
                    elif old_idx == 0:
                        assign_str += f"""
    assign layer{layer_no+1}_col{col}[{new_idx}] = layer{layer_no}_col{col};"""
                    elif new_idx == 0:
                        assign_str += f"""
    assign layer{layer_no+1}_col{col}    = layer{layer_no}_col{col}[{old_idx}];"""
                    else:
                        assign_str += f"""
    assign layer{layer_no+1}_col{col}[{new_idx}] = layer{layer_no}_col{col}[{old_idx}];"""
                else:
                    assign_str += f"""
    assign layer{layer_no+1}_col{col}[{new_idx}] = layer{layer_no}_col{col}[{old_idx}];"""
    else:
        assign_str += f"""
    always_ff @(posedge clk) begin"""
        for col in range(num_col):
            col_assign_list = assign_list[col]
            for old_idx, new_idx in col_assign_list:
                if len(col_assign_list) == 1:
                    if old_idx == 0 and new_idx == 0:
                        assign_str += f"""
        layer{layer_no+1}_col{col}    <= layer{layer_no}_col{col};"""
                    elif old_idx == 0:
                        assign_str += f"""
        layer{layer_no+1}_col{col}[{new_idx}] <= layer{layer_no}_col{col};"""
                    elif new_idx == 0:
                        assign_str += f"""
        layer{layer_no+1}_col{col}    <= layer{layer_no}_col{col}[{old_idx}];"""
                    else:
                        assign_str += f"""
        layer{layer_no+1}_col{col}[{new_idx}] <= layer{layer_no}_col{col}[{old_idx}];"""
                else:
                    assign_str += f"""
        layer{layer_no+1}_col{col}[{new_idx}] <= layer{layer_no}_col{col}[{old_idx}];"""
        assign_str += f"""
    end
    """
    return assign_str


def floatingGPC_placement(GPC_list: list[tuple[counter, int]], layer_no: int, placement_len: int) -> tuple[str, str]:
    decl = ""
    instan = ""
    num_LA = placement_len // 8
    num_LA += 1 if placement_len % 8 else 0
    attri_LA = [False, False, False, False] * num_LA
    LA_signal_decl, LA_instan = LOOKAHEAD8_gen(num_LA, f"l{layer_no}_floating_placement", attri_LA)
    decl += LA_signal_decl
    instan += LA_instan
    pos_cnt = 0

    for counter, floatingGPC_no in GPC_list:
        if counter.name == "(9 : 4,1)":
            instan += f"""
    assign CY_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}]   = CY_c9_41_l{layer_no}_f{floatingGPC_no};
    assign PROP_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}] = PROP_c9_41_l{layer_no}_f{floatingGPC_no};"""
            if pos_cnt % 8 == 0:
                instan += f"""
    assign CIN_LA_l{layer_no}_floating_placement{f"[{pos_cnt//8}]" if num_LA > 1 else "   "} = C0_c9_41_l{layer_no}_f{floatingGPC_no}[8];
    """
            else:
                instan += f"""
    """
            pos_cnt += 2

        if counter.name == "(1,5 : 3]":
            instan += f"""
    assign CY_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}]   = CY_c15_3_l{layer_no}_f{floatingGPC_no};
    assign PROP_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}] = PROP_c15_3_l{layer_no}_f{floatingGPC_no};"""
            if pos_cnt % 8 == 0:
                instan += f"""
    assign CIN_LA_l{layer_no}_floating_placement{f"[{pos_cnt//8}]" if num_LA > 1 else "   "} = C0_c15_3_l{layer_no}_f{floatingGPC_no}[4];
    """
            else:
                instan += f"""
    """
            pos_cnt += 2

        if counter.name == "(2,2,3 : 4]":
            instan += f"""
    assign CY_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}]   = CY_c223_4_l{layer_no}_f{floatingGPC_no};
    assign PROP_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}] = PROP_c223_4_l{layer_no}_f{floatingGPC_no};"""
            if pos_cnt % 8 == 0:
                instan += f"""
    assign CIN_LA_l{layer_no}_floating_placement{f"[{pos_cnt//8}]" if num_LA > 1 else "   "} = C0_c223_4_l{layer_no}_f{floatingGPC_no}[2];
    """
            else:
                instan += f"""
    """
            pos_cnt += 2

        if counter.name == "(3,9 : 2,3,1)":
            instan += f"""
    assign CY_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}]   = CY0_c39_231_l{layer_no}_f{floatingGPC_no};
    assign PROP_LA_l{layer_no}_floating_placement[{pos_cnt+1}:{pos_cnt}] = PROP0_c39_231_l{layer_no}_f{floatingGPC_no};
    assign CY_LA_l{layer_no}_floating_placement[{pos_cnt+3}:{pos_cnt+2}]   = CY1_c39_231_l{layer_no}_f{floatingGPC_no};
    assign PROP_LA_l{layer_no}_floating_placement[{pos_cnt+3}:{pos_cnt+2}] = PROP1_c39_231_l{layer_no}_f{floatingGPC_no};"""
            if pos_cnt % 8 == 0:
                instan += f"""
    assign CIN_LA_l{layer_no}_floating_placement{f"[{pos_cnt//8}]" if num_LA > 1 else "   "} = C0_c39_231_l{layer_no}_f{floatingGPC_no}[8];
    """
            elif pos_cnt % 8 == 6:
                instan += f"""
    assign CIN_LA_l{layer_no}_floating_placement[{(pos_cnt+2)//8}] = C1_c39_231_l{layer_no}_f{floatingGPC_no}[1];
    """
            else:
                instan += f"""
    """
            pos_cnt += 4

    return decl, instan


def layer_gen(layer_no: int, layer_inputs: list[int], chains_list: list[list[counter]], reg_flag: bool, merge_flag: bool, merge_counter_list: list[list[counter]], reduced_inputs: list[list[list[int]]]) -> tuple[list[int], str, str, str, str]:
    """
    :param layer_no: the index of the layer to generate RTL for
    :param layer_inputs: the list of inputs, indicating how many bits are there in each column
    :param chains_list: the counter chains and floating counters to be applied in current layer
    :param reg_flag: whether to register the outputs of this layer
    :return: a tuple of one list of integers and four strings:
                the list: the layer outputs, will be used as the layer_inputs
                first string: layer head comments
                second string: signal declaration with GPC (chain) comments
                third string: GPC instantiation and assignments
                fourth string: constraints
    """
    # analyze the layer
    next_layer_inputs, chains_inputs, chains_outputs, assignments_list = layer_admin(layer_inputs=layer_inputs,
                                                                                     chain_list=chains_list,
                                                                                     merge_flag=merge_flag,
                                                                                     merge_chain_list=merge_counter_list,
                                                                                     reduced_inputs=reduced_inputs)
    layer_head_comments = f"""
    // ------------------------------ LAYER {layer_no} ------------------------------"""
    signal_decl = f"""
    """
    instan = f""
    xdc = f""
    # declaration of the layer signal
    left_w = max(len(str(v-1)) for v in layer_inputs)
    w = max(len(width_expr(v-1, left_w)) for v in layer_inputs)
    num_col = len(layer_inputs)
    for i in range(num_col):
        if layer_inputs[i]:
            sig = width_expr(layer_inputs[i]-1, left_w)
            signal_decl += f"""logic {sig:<{w}} layer{layer_no}_col{i};
    """
    # constructing the layer with GPC (chains)
    num_chains_and_floating = len(chains_list)
    chain_cnt = 0
    floating_cnt = 0
    floating_placement_list = []
    floating_placement_len = 0
    for i in range(num_chains_and_floating):
        if len(chains_list[i]) == 1:
            f_comments, f_declaration, f_instance, f_xdc = floatingGPC_gen(chains_list[i][0], layer_no, floating_cnt, chains_inputs[i], chains_outputs[i], layer_inputs, next_layer_inputs, reg_flag)
            signal_decl += f_declaration
            instan += f_comments
            instan += f_instance
            xdc += f_xdc
            if chains_list[i][0].name == "(9 : 4,1)" or chains_list[i][0].name == "(1,5 : 3]" or chains_list[i][0].name == "(2,2,3 : 4]" or chains_list[i][0].name == "(3,9 : 2,3,1)":
                floating_placement_list.append((chains_list[i][0], floating_cnt))
                if chains_list[i][0].name == "(3,9 : 2,3,1)":
                    floating_placement_len += 4
                else:
                    floating_placement_len += 2
            floating_cnt += 1
        else:
            c_comments, c_declaration, c_instance, c_xdc = chain_gen(chains_list[i], layer_no, chain_cnt, chains_inputs[i], chains_outputs[i], layer_inputs, next_layer_inputs, reg_flag)
            signal_decl += c_declaration
            instan += c_comments
            instan += c_instance
            xdc += c_xdc
            chain_cnt += 1
    # place floating GPCs using LOOKAHEAD8
    floating_placement_decl, floating_placement_instan = floatingGPC_placement(floating_placement_list, layer_no, floating_placement_len)
    signal_decl += floating_placement_decl
    instan += floating_placement_instan
    # assign the rest of the bits in the current layer to the next layer
    instan += assignment_gen(layer_no, assignments_list, reg_flag)

    return next_layer_inputs, layer_head_comments, signal_decl, instan, xdc


def terminalAdd_gen(terminal_layer_no: int, terminal_inputs: list[int], final_output_width: int, final_output_name: str, terminal_reg_flag: bool) -> tuple[str, str]:
    # find out the tail part, the body part and the head part
    num_columns = len(terminal_inputs)
    terminalAdd_start = 0
    tail_end = 0
    head_start = num_columns-1
    terminalAdd_end = num_columns-1
    # find whether there is tail, and if so where it starts
    tail_flag = False
    for col in range(num_columns):
        if terminal_inputs[col] == 2:
            terminalAdd_start = col
            tail_flag = True
            break
        if terminal_inputs[col] == 3:
            terminalAdd_start = col
            if terminal_inputs[col+1] <= 2:
                tail_flag = True
            break
        if terminal_inputs[col] >= 4:
            terminalAdd_start = col
            break
    # if tail exits, find where it ends
    if tail_flag:
        for col in range(terminalAdd_start+1, num_columns):
            if terminal_inputs[col] >= 3:
                tail_end = col-1
                break
    # find whether there is head, and if so where it starts
    head_flag = False
    for col in range(num_columns-1, terminalAdd_start-1, -1):
        if terminal_inputs[col] == 0 and head_flag is False:
            terminalAdd_end = col-1
            head_start = col-1
        if terminal_inputs[col] == 1:
            head_flag = True
            head_start = col
        if terminal_inputs[col] >= 2:
            break
    # find where the first terminal chain ends and how many (3 : 2] counters involved
    chain1_end_col = head_start-1 if head_flag else terminalAdd_end
    two_op_start = chain1_end_col+1
    for col in range(chain1_end_col, terminalAdd_start-1, -1):
        if terminal_inputs[col] > 2:
            break
        else:
            two_op_start = col
    two_op_cols = list(range(two_op_start, chain1_end_col+1))
    ### so now we have the range for the first chain:
    ### starting from the last (1,5 : 3] counter, take two columns down and check if both columns are higher than the chain lower bound
    ### if it can be cascaded with tail part (if the tail part exits), then make the tail part into the chain
    if two_op_cols:
        end_col_15_3 = two_op_start-1
    else:
        if head_flag:
            end_col_15_3 = head_start
        else:
            end_col_15_3 = terminalAdd_end
    tail_cascade_flag = False
    if tail_flag is True and end_col_15_3 % 2 == tail_end % 2:
        tail_cascade_flag = True
    if tail_cascade_flag:
        chain_len = end_col_15_3 - terminalAdd_start + 1 + len(two_op_cols)
    else:
        if tail_flag:
            chain_len = end_col_15_3 - (tail_end + 1) + len(two_op_cols)
        else:
            chain_len = end_col_15_3 - terminalAdd_start + 1 + len(two_op_cols)
    # start to generate RTL for the first terminal chain
    if chain_len % 8 == 0:
        num_LA = chain_len // 8
    else:
        num_LA = chain_len // 8 + 1
    # declaration of the layer (terminal) signal
    signal_decl = f"""
    """
    instan = f""
    left_w = max(len(str(v-1)) for v in terminal_inputs)
    w = max(len(width_expr(v-1, left_w)) for v in terminal_inputs)
    num_col = len(terminal_inputs)
    for i in range(num_col):
        if terminal_inputs[i]:
            signal_decl += f"""logic {width_expr(terminal_inputs[i]-1, left_w):<{w}} layer{terminal_layer_no}_col{i};
    """
    signal_decl += f"""
    logic [{chain_len} : 0] terminal_chain1_out;
    """
    # generation of LOOKAHEAD8 of terminal chain 1
    attri_LA_chain1 = []
    for i in range(num_LA):
        if i == 0:
            attri_LA_chain1.extend([False, True, True, True])
        else:
            attri_LA_chain1.extend([True, True, True, True])
    decl_chain1, instan_chain1 = LOOKAHEAD8_gen(num_LA, f"terminal_chain1", attri_LA_chain1)
    signal_decl += decl_chain1
    instan += instan_chain1
    # generation of LUTs of terminal chain 1:
    ### generation of tail if tail exists
    pos_cnt = 0
    i_cnt = 0
    if tail_cascade_flag:
        for col in range(terminalAdd_start, tail_end+1):
            # first declare signals and instantiate LUTs
            clk_str = f"clk"
            C0_str = f"C0_c3_2_terminal_chain1_i{i_cnt}"
            O_str = f"O_c3_2_terminal_chain1_i{i_cnt}"
            CY_str = f"CY_c3_2_terminal_chain1_i{i_cnt}"
            PROP_str = f"PROP_c3_2_terminal_chain1_i{i_cnt}"
            MSB_str = f"terminal_chain1_i{i_cnt}"
            signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {O_str};
    logic         {CY_str};
    logic         {PROP_str};
    logic         {MSB_str};
    """
            port_list = [clk_str, C0_str, O_str, CY_str, PROP_str, MSB_str]
            max_len = max(len(s) for s in port_list)
            instan += f"""
    c3_2 #(.OUTREG({'"FALSE"'}),
           .LEAVEC({'"TRUE" '}),
           .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
           .FIRSTS({'"TRUE" ' if pos_cnt < 2 else '"FALSE"'}),
           .LASTS ({'"FALSE"'}))
    c3_2_terminal_chain1_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
            # connect the inputs of LUTs with layer inputs
            if col == terminalAdd_start:
                if terminal_inputs[col] == 0:
                    instan += f"""
    assign {C0_str}[0] = 1'b0;
    assign {C0_str}[1] = 1'b0;
    assign {C0_str}[2] = 1'b0;
    """
                if terminal_inputs[col] == 1:
                    instan += f"""
    assign {C0_str}[0] = layer{terminal_layer_no}_col{col};
    assign {C0_str}[1] = 1'b0;
    assign {C0_str}[2] = 1'b0;
    """
                if terminal_inputs[col] == 2:
                    instan += f"""
    assign {C0_str}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str}[2] = 1'b0;
    """
                elif terminal_inputs[col] == 3:
                    instan += f"""
    assign {C0_str}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str}[2] = layer{terminal_layer_no}_col{col}[2];
    """
            else:
                instan += f"""
    assign {C0_str}[2] = terminal_chain1_i{i_cnt-1};
    """
                if terminal_inputs[col] == 1:
                    instan += f"""assign {C0_str}[0] = layer{terminal_layer_no}_col{col};
    assign {C0_str}[1] = 1'b0;
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""assign {C0_str}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[1];
    """
            # connect the outputs of LUTs with layer outputs
            out_str0 = f"terminal_chain1_out[{pos_cnt}]"
            instan += f"""
    assign {out_str0} = {O_str}[0];
    """
            # connect LUTs with LOOKAHEAD8
            LUTLA_str0 = f"terminal_chain1_i{i_cnt}"
            LUTLA_str1 = f"CY_LA_terminal_chain1[{pos_cnt}]"
            LUTLA_str2 = f"PROP_LA_terminal_chain1[{pos_cnt}]"
            LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2]
            max_len = max(len(s) for s in LUTLA_str_list)
            if pos_cnt % 2 == 0:
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = {O_str}[1];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
            else:
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_terminal_chain1[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
            # connect carry in and out between LOOKAHEAD8 blocks is needed
            if pos_cnt % 8 == 0:
                if pos_cnt == 0:
                    instan += f"""
    assign CIN_LA_terminal_chain1{"[0]" if num_LA > 1 else "   "} = {C0_str}[2];
    """
                else:
                    instan += f"""
    assign CIN_LA_terminal_chain1[{pos_cnt//8}] = COUT_LA_terminal_chain1[{(pos_cnt//2)-1}];
    """
            # increment GPC instance counter and position counter
            pos_cnt += 1
            i_cnt += 1
    ### generation of body
    ### find where the boday starts and where it ends for chain1
    if tail_cascade_flag:
        body_start = tail_end + 1
    elif tail_flag is True and tail_cascade_flag is False:
        body_start = tail_end + 2
    else:
        body_start = terminalAdd_start
    if two_op_cols:
        body_end = two_op_cols[0] - 1
    else:
        if head_flag:
            body_end = head_start
        else:
            body_end = terminalAdd_end
    if body_start % 2 == body_end % 2:
        body_start += 1
    col = body_start
    while(col < body_end):
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c15_3_terminal_chain1_i{i_cnt}"
        C1_str = f"C1_c15_3_terminal_chain1_i{i_cnt}"
        CLA_str = f"CLA_c15_3_terminal_chain1_i{i_cnt}"
        O_str = f"O_c15_3_terminal_chain1_i{i_cnt}"
        CY_str = f"CY_c15_3_terminal_chain1_i{i_cnt}"
        PROP_str = f"PROP_c15_3_terminal_chain1_i{i_cnt}"
        MSB_str = f"terminal_chain1_i{i_cnt}"
        signal_decl += f"""
    logic [4 : 0] {C0_str};
    logic         {C1_str};
    logic         {CLA_str};
    logic [2 : 0] {O_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    logic         {MSB_str};
    """
        port_list = [clk_str, C0_str, C1_str, CLA_str, O_str, CY_str, PROP_str, MSB_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c15_3 #(.OUTREG({'"FALSE"'}),
            .LEAVEC({'"TRUE" '}),
            .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
            .FIRSTS({'"TRUE" ' if pos_cnt < 2 else '"FALSE"'}),
            .LASTS ({'"TRUE" ' if (col+2 >= body_end and not two_op_cols) else '"FALSE"'}))
    c15_3_terminal_chain1_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .C1  ({C1_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str]
        max_len = max(len(s) for s in in_str_list)
        if pos_cnt == 0:
            if terminal_inputs[col] == 0:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = 1'b0;
    assign {C0_str.ljust(max_len)}[4] = 1'b0;
    """
            elif terminal_inputs[col] == 1:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = 1'b0;
    assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col};
    """
            elif terminal_inputs[col] == 2:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col}[1];
    """
            elif terminal_inputs[col] == 3:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col}[2];
    """
            elif terminal_inputs[col] == 4:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col}[3];
    """
            if col == len(terminal_inputs) - 1:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
            elif terminal_inputs[col+1] == 0:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
            elif terminal_inputs[col+1] == 1:
                instan += f"""assign {C1_str.ljust(max_len)}    = layer{terminal_layer_no}_col{col+1};
    """
            else:
                instan += f"""assign {C1_str.ljust(max_len)}    = layer{terminal_layer_no}_col{col+1}[0];
    """
        else:
            instan += f"""
    assign {C0_str.ljust(max_len)}[4] = terminal_chain1_i{i_cnt-1};
    """
            if terminal_inputs[col] == 0:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = 1'b0;
    """
            elif terminal_inputs[col] == 1:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col};
    """
            elif terminal_inputs[col] == 2:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[1];
    """
            elif terminal_inputs[col] == 3:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[2];
    """
            elif terminal_inputs[col] == 4:
                instan += f"""assign {C0_str.ljust(max_len)}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[3];
    """
            if col == len(terminal_inputs) - 1:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
            elif terminal_inputs[col+1] == 0:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
            elif terminal_inputs[col+1] == 1:
                instan += f"""assign {C1_str.ljust(max_len)}    = layer{terminal_layer_no}_col{col+1};
    """
            else:
                instan += f"""assign {C1_str.ljust(max_len)}    = layer{terminal_layer_no}_col{col+1}[0];
    """
        # connect the outputs of LUTS with layer outputs
        out_str0 = f"terminal_chain1_out[{pos_cnt}]"
        out_str1 = f"terminal_chain1_out[{pos_cnt+1}]"
        out_str2 = f"terminal_chain1_out[{pos_cnt+2}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];"""
        if col == end_col_15_3-1 and not two_op_cols:
            instan += f"""
    assign {out_str2.ljust(max_len)} = {O_str}[2];
    """
        else:
            instan += f"""
    """
        # connect LUTs with LOOKAHEAD8
        LUTLA_str0 = CLA_str
        LUTLA_str1 = f"terminal_chain1_i{i_cnt}"
        LUTLA_str2 = f"CY_LA_terminal_chain1[{pos_cnt+1}:{pos_cnt}]"
        LUTLA_str3 = f"PROP_LA_terminal_chain1[{pos_cnt+1}:{pos_cnt}]"
        LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2, LUTLA_str3]
        max_len = max(len(s) for s in LUTLA_str_list)
        if pos_cnt % 2:
            instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_terminal_chain1[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {O_str}[2];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
        else:
            instan += f"""
    assign {LUTLA_str1.ljust(max_len)} = COUT_LA_terminal_chain1[{pos_cnt//2}];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
        # connect carry in and out between LOOKAHEAD8 blocks is needed
        if pos_cnt % 8 == 7:
            pos_cnt_temp = pos_cnt + 1
        else:
            pos_cnt_temp = pos_cnt
        if pos_cnt_temp % 8 == 0:
            if pos_cnt == 0:
                instan += f"""
    assign CIN_LA_terminal_chain1{"[0]" if num_LA > 1 else "   "} = {C0_str}[4];
    """
            else:
                instan += f"""
    assign CIN_LA_terminal_chain1[{pos_cnt_temp//8}] = COUT_LA_terminal_chain1[{(pos_cnt_temp//2)-1}];
    """
        # increment GPC instance counter and position counter
        pos_cnt += 2
        i_cnt += 1
        # increment column pointer
        col += 2
    ### generation of two-operand part if it exists
    if two_op_cols:
        for col in two_op_cols:
            # first declare signals and instantiate LUTs
            clk_str = f"clk"
            C0_str = f"C0_c3_2_terminal_chain1_i{i_cnt}"
            O_str = f"O_c3_2_terminal_chain1_i{i_cnt}"
            CY_str = f"CY_c3_2_terminal_chain1_i{i_cnt}"
            PROP_str = f"PROP_c3_2_terminal_chain1_i{i_cnt}"
            MSB_str = f"terminal_chain1_i{i_cnt}"
            signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {O_str};
    logic         {CY_str};
    logic         {PROP_str};
    logic         {MSB_str};
    """
            port_list = [clk_str, C0_str, O_str, CY_str, PROP_str, MSB_str]
            max_len = max(len(s) for s in port_list)
            instan += f"""
    c3_2 #(.OUTREG({'"FALSE"'}),
           .LEAVEC({'"TRUE" '}),
           .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
           .FIRSTS({'"FALSE"'}),
           .LASTS ({'"TRUE" ' if col == two_op_cols[-1] else '"FALSE"'}))
    c3_2_terminal_chain1_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
            # connect the inputs of LUTs with layer inputs
            instan += f"""
    assign {C0_str}[2] = terminal_chain1_i{i_cnt-1};
    """
            if terminal_inputs[col] == 1:
                instan += f"""assign {C0_str}[0] = layer{terminal_layer_no}_col{col};
    assign {C0_str}[1] = 1'b0;
    """
            elif terminal_inputs[col] == 2:
                instan += f"""assign {C0_str}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[1];
    """
            # connect the outputs of LUTs with layer outputs
            out_str0 = f"terminal_chain1_out[{pos_cnt}]"
            out_str1 = f"terminal_chain1_out[{pos_cnt+1}]"
            out_str_list = [out_str0, out_str1]
            max_len = max(len(s) for s in out_str_list)
            instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    """
            if col == two_op_cols[-1]:
                instan += f"""assign {out_str1.ljust(max_len)} = {O_str}[1];
    """
            # connect LUTs with LOOKAHEAD8
            LUTLA_str0 = f"terminal_chain1_i{i_cnt}"
            LUTLA_str1 = f"CY_LA_terminal_chain1[{pos_cnt}]"
            LUTLA_str2 = f"PROP_LA_terminal_chain1[{pos_cnt}]"
            LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2]
            max_len = max(len(s) for s in LUTLA_str_list)
            if pos_cnt % 2 == 0:
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = {O_str}[1];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
            else:
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_terminal_chain1[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
            # connect carry in and out between LOOKAHEAD8 blocks is needed
            if pos_cnt % 8 == 0:
                instan += f"""
    assign CIN_LA_terminal_chain1[{pos_cnt//8}] = COUT_LA_terminal_chain1[{(pos_cnt//2)-1}];
    """
            # increment GPC instance counter and position counter
            pos_cnt += 1
            i_cnt += 1
    # =================================================================================================================================
    ### so now we have the first chain, then start generation of the second chain:
    ### first, calculate the chain length and generate LOOKAHEAD8 blocks
    ##### check if there is a tail part and check further whether it has been cascaded with chain1
    ##### if there is a tail, and it hasn't been cascaded, start from the beginning of the tail to generate chain2
    ##### if there is a tail, and it has been in chain1, skip generation for tail part and start chain2 from (tail_end + 2)
    ##### if there isn't a tail, start chain2 from terminalAdd_start with (1,5 : 3] counters
    if tail_flag is True and tail_cascade_flag is False:
        chain_len = terminalAdd_end - terminalAdd_start + 1
        chain1_start = tail_end + 2
    elif tail_flag is True and tail_cascade_flag is True:
        chain_len = terminalAdd_end - (tail_end + 2) + 1
        chain1_start = terminalAdd_start
    else:
        if body_start == terminalAdd_start:
            chain_len = terminalAdd_end - (terminalAdd_start+1) + 1
            chain1_start = body_start
        else:
            chain_len = terminalAdd_end - terminalAdd_start + 1
            chain1_start = body_start
    if two_op_cols and col == terminalAdd_end:
        chain_len += 1
    if not two_op_cols and col > terminalAdd_end:
        chain_len += 1
    num_LA = chain_len // 8 if chain_len % 8 == 0 else chain_len // 8 + 1
    signal_decl += f"""
    logic [{chain_len} : 0] terminal_chain2_out;
    """
    # generation of LOOKAHEAD8 of terminal chain2
    attri_LA_chain2 = []
    for i in range(num_LA):
        if i == 0:
            attri_LA_chain2.extend([False, True, True, True])
        else:
            attri_LA_chain2.extend([True, True, True, True])
    decl_chain2, instan_chain2 = LOOKAHEAD8_gen(num_LA, f"terminal_chain2", attri_LA_chain2)
    signal_decl += decl_chain2
    instan += instan_chain2
    # generation of GPC LUTs of terminal chain2
    pos_cnt = 0
    i_cnt = 0
    if tail_flag is True and tail_cascade_flag is False:
        for col in range(terminalAdd_start, tail_end+1):
            # first declare signals and instantiate LUTs
            clk_str = f"clk"
            C0_str = f"C0_c3_2_terminal_chain2_i{i_cnt}"
            O_str = f"O_c3_2_terminal_chain2_i{i_cnt}"
            CY_str = f"CY_c3_2_terminal_chain2_i{i_cnt}"
            PROP_str = f"PROP_c3_2_terminal_chain2_i{i_cnt}"
            MSB_str = f"terminal_chain2_i{i_cnt}"
            signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {O_str};
    logic         {CY_str};
    logic         {PROP_str};
    logic         {MSB_str};
    """
            port_list = [clk_str, C0_str, O_str, CY_str, PROP_str, MSB_str]
            max_len = max(len(s) for s in port_list)
            instan += f"""
    c3_2 #(.OUTREG({'"FALSE"'}),
           .LEAVEC({'"TRUE" '}),
           .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
           .FIRSTS({'"TRUE" ' if pos_cnt < 2 else '"FALSE"'}),
           .LASTS ({'"FALSE"'}))
    c3_2_terminal_chain2_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
            # connect the inputs of LUTs with layer inputs
            if col == terminalAdd_start:
                if terminal_inputs[col] == 0:
                    instan += f"""
    assign {C0_str}[0] = 1'b0;
    assign {C0_str}[1] = 1'b0;
    assign {C0_str}[2] = 1'b0;
    """
                elif terminal_inputs[col] == 1:
                    instan += f"""
    assign {C0_str}[0] = 1'b0;
    assign {C0_str}[1] = 1'b0;
    assign {C0_str}[2] = layer{terminal_layer_no}_col{col};
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""
    assign {C0_str}[0] = 1'b0;
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[2] = layer{terminal_layer_no}_col{col}[1];
    """
                elif terminal_inputs[col] == 3:
                    instan += f"""
    assign {C0_str}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str}[2] = layer{terminal_layer_no}_col{col}[2];
    """
            else:
                instan += f"""
    assign {C0_str}[2] = terminal_chain2_i{i_cnt-1};
    """
                if terminal_inputs[col] == 1:
                    instan += f"""assign {C0_str}[0] = layer{terminal_layer_no}_col{col};
    assign {C0_str}[1] = 1'b0;
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""assign {C0_str}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str}[1] = layer{terminal_layer_no}_col{col}[1];
    """
            # connect the outputs of LUTs with layer outputs
            out_str0 = f"terminal_chain2_out[{pos_cnt}]"
            instan += f"""
    assign {out_str0} = {O_str}[0];"""
            # connect LUTs with LOOKAHEAD8
            LUTLA_str0 = f"terminal_chain2_i{i_cnt}"
            LUTLA_str1 = f"CY_LA_terminal_chain2[{pos_cnt}]"
            LUTLA_str2 = f"PROP_LA_terminal_chain2[{pos_cnt}]"
            LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2]
            max_len = max(len(s) for s in LUTLA_str_list)
            if pos_cnt % 2 == 0:
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = {O_str}[1];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
            else:
                instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_terminal_chain2[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
            # connect carry in and out between LOOKAHEAD8 blocks is needed
            if pos_cnt % 8 == 0:
                if pos_cnt == 0:
                    instan += f"""
    assign CIN_LA_terminal_chain2{"[0]" if num_LA > 1 else "   "} = {C0_str}[2];
    """
                else:
                    instan += f"""
    assign CIN_LA_terminal_chain2[{pos_cnt//8}] = COUT_LA_terminal_chain2[{(pos_cnt//2)-1}];
    """
            # increment GPC instance counter and position counter
            pos_cnt += 1
            i_cnt += 1
    ### generation of body
    ### find where the body starts and where it ends for chain2
    body_start_old = body_start
    if tail_flag is True and tail_cascade_flag is False:
        body_start = tail_end + 1
        chain1to2_start = tail_end + 2
    elif tail_flag is True and tail_cascade_flag is True:
        body_start = tail_end + 2
        chain1to2_start = body_start
    else:
        if body_start_old == terminalAdd_start:
            body_start = terminalAdd_start + 1
            chain1to2_start = body_start
        else:
            body_start = terminalAdd_start
            chain1to2_start = body_start + 1
    if two_op_cols:
        body_end = two_op_cols[0]
        chain1to2_end = two_op_cols[-1] + 1
    else:
        if head_flag:
            body_end = head_start
            chain1to2_end = head_start + 1    # changed to debug single128
        else:
            body_end = terminalAdd_end + 1
            chain1to2_end = end_col_15_3 + 1
    col = body_start
    while(col < body_end):
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c15_3_terminal_chain2_i{i_cnt}"
        C1_str = f"C1_c15_3_terminal_chain2_i{i_cnt}"
        CLA_str = f"CLA_c15_3_terminal_chain2_i{i_cnt}"
        O_str = f"O_c15_3_terminal_chain2_i{i_cnt}"
        CY_str = f"CY_c15_3_terminal_chain2_i{i_cnt}"
        PROP_str = f"PROP_c15_3_terminal_chain2_i{i_cnt}"
        MSB_str = f"terminal_chain2_i{i_cnt}"
        signal_decl += f"""
    logic [4 : 0] {C0_str};
    logic         {C1_str};
    logic         {CLA_str};
    logic [2 : 0] {O_str};
    logic [1 : 0] {CY_str};
    logic [1 : 0] {PROP_str};
    logic         {MSB_str};
    """
        port_list = [clk_str, C0_str, C1_str, CLA_str, O_str, CY_str, PROP_str, MSB_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c15_3 #(.OUTREG({'"FALSE"'}),
            .LEAVEC({'"TRUE" '}),
            .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
            .FIRSTS({'"TRUE" ' if pos_cnt < 2 else '"FALSE"'}),
            .LASTS ({'"TRUE" ' if (col+2 >= body_end and (not two_op_cols) and (not head_flag)) else '"FALSE"'}))
    c15_3_terminal_chain2_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .C1  ({C1_str.ljust(max_len)}),
        .CLA ({CLA_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # connect the inputs of LUTS with layer inputs
        in_str_list = [C0_str, C1_str]
        max_len = max(len(s) for s in in_str_list)
        if pos_cnt == 0:
            if chain1to2_start <= col <= chain1to2_end:
                instan += f"""
    assign {C0_str.ljust(max_len)}[4] = 1'b0;
    """
                instan += f"""assign {C0_str.ljust(max_len)}[3] = terminal_chain1_out[{col-chain1_start}];
    """
                if terminal_inputs[col] == 0 or terminal_inputs[col] == 1:
                    instan += f"""assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 3:
                    instan += f"""assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 4:
                    instan += f"""assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[3];
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[0] = layer{terminal_layer_no}_col{col}[1];
    """
            else:
                if terminal_inputs[col] == 0:
                    instan += f"""assign {C0_str.ljust(max_len)}[4] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 1:
                    instan += f"""assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col};
    assign {C0_str.ljust(max_len)}[3] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 3:
                    instan += f"""assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
                elif terminal_inputs[col] == 4:
                    instan += f"""assign {C0_str.ljust(max_len)}[4] = layer{terminal_layer_no}_col{col}[3];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[0] = 1'b0;
    """
            if chain1to2_start <= col+1 <= chain1to2_end:
                instan += f"""assign {C1_str.ljust(max_len)}    = terminal_chain1_out[{col+1-chain1_start}];
    """
            elif col == len(terminal_inputs) - 1:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
            elif terminal_inputs[col+1] == 0:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
            elif terminal_inputs[col+1] == 1:
                instan += f"""assign {C1_str.ljust(max_len)}    = layer{terminal_layer_no}_col{col+1};
    """
            else:
                instan += f"""assign {C1_str.ljust(max_len)}    = layer{terminal_layer_no}_col{col+1}[0];
    """
        else:
            instan += f"""
    assign {C0_str.ljust(max_len)}[4] = terminal_chain2_i{i_cnt-1};
    """
            if chain1to2_start <= col <= chain1to2_end:
                instan += f"""assign {C0_str.ljust(max_len)}[3] = terminal_chain1_out[{col-chain1_start}];
    """
                if terminal_inputs[col] == 1 or terminal_inputs[col] == 0:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[1];
    """
                elif terminal_inputs[col] == 3:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[2];
    """
                elif terminal_inputs[col] == 4:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[3];
    """
            else:
                if terminal_inputs[col] == 0:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = 1'b0;
    """
                elif terminal_inputs[col] == 1:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = 1'b0;
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[0];
    """
                elif terminal_inputs[col] == 2:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = 1'b0;
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[1];
    """
                elif terminal_inputs[col] == 3:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = 1'b0;
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[2];
    """
                elif terminal_inputs[col] == 4:
                    instan += f"""assign {C0_str.ljust(max_len)}[0] = layer{terminal_layer_no}_col{col}[0];
    assign {C0_str.ljust(max_len)}[1] = layer{terminal_layer_no}_col{col}[1];
    assign {C0_str.ljust(max_len)}[2] = layer{terminal_layer_no}_col{col}[2];
    assign {C0_str.ljust(max_len)}[3] = layer{terminal_layer_no}_col{col}[3];
    """
            if chain1to2_start <= col+1 <= chain1to2_end:
                instan += f"""assign {C1_str.ljust(max_len)}    = terminal_chain1_out[{col+1-chain1_start}];
    """
            else:
                instan += f"""assign {C1_str.ljust(max_len)}    = 1'b0;
    """
        # connect the outputs of LUTS with layer outputs
        out_str0 = f"terminal_chain2_out[{pos_cnt}]"
        out_str1 = f"terminal_chain2_out[{pos_cnt+1}]"
        out_str2 = f"terminal_chain2_out[{pos_cnt+2}]"
        out_str_list = [out_str0, out_str1, out_str2]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    assign {out_str1.ljust(max_len)} = {O_str}[1];"""
        if col+2 > chain1to2_end and col+2 >= terminalAdd_end+2:
            instan += f"""
    assign {out_str2.ljust(max_len)} = {O_str}[2];
    """
        else:
            instan += f"""
    """
        # connect LUTs with LOOKAHEAD8
        LUTLA_str0 = CLA_str
        LUTLA_str1 = f"terminal_chain2_i{i_cnt}"
        LUTLA_str2 = f"CY_LA_terminal_chain2[{pos_cnt+1}:{pos_cnt}]"
        LUTLA_str3 = f"PROP_LA_terminal_chain2[{pos_cnt+1}:{pos_cnt}]"
        LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2, LUTLA_str3]
        max_len = max(len(s) for s in LUTLA_str_list)
        if pos_cnt % 2:
            instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_terminal_chain2[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {O_str}[2];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
        else:
            instan += f"""
    assign {LUTLA_str1.ljust(max_len)} = COUT_LA_terminal_chain2[{pos_cnt//2}];
    assign {LUTLA_str2.ljust(max_len)} = {CY_str};
    assign {LUTLA_str3.ljust(max_len)} = {PROP_str};
    """
        # connect carry in and out between LOOKAHEAD8 blocks is needed
        if pos_cnt % 8 == 7:
            pos_cnt_temp = pos_cnt + 1
        else:
            pos_cnt_temp = pos_cnt
        if pos_cnt_temp % 8 == 0:
            if pos_cnt == 0:
                instan += f"""
    assign CIN_LA_terminal_chain2{"[0]" if num_LA > 1 else  "   "} = {C0_str}[4];
    """
            else:
                instan += f"""
    assign CIN_LA_terminal_chain2[{pos_cnt_temp//8}] = COUT_LA_terminal_chain2[{(pos_cnt_temp//2)-1}];
    """
        # increment GPC instance counter and position counter
        pos_cnt += 2
        i_cnt += 1
        # increment column pointer
        col += 2
    ### generation of the rest of terminal chain2
    rest_start = col
    rest_end = rest_start+chain_len-pos_cnt-1
    for col in range(rest_start, rest_end+1):
        # first declare signals and instantiate LUTs
        clk_str = f"clk"
        C0_str = f"C0_c3_2_terminal_chain2_i{i_cnt}"
        O_str = f"O_c3_2_terminal_chain2_i{i_cnt}"
        CY_str = f"CY_c3_2_terminal_chain2_i{i_cnt}"
        PROP_str = f"PROP_c3_2_terminal_chain2_i{i_cnt}"
        MSB_str = f"terminal_chain2_i{i_cnt}"
        signal_decl += f"""
    logic [2 : 0] {C0_str};
    logic [1 : 0] {O_str};
    logic         {CY_str};
    logic         {PROP_str};
    logic         {MSB_str};
    """
        port_list = [clk_str, C0_str, O_str, CY_str, PROP_str, MSB_str]
        max_len = max(len(s) for s in port_list)
        instan += f"""
    c3_2 #(.OUTREG({'"FALSE"'}),
           .LEAVEC({'"TRUE" '}),
           .POSODD({'"TRUE" ' if pos_cnt % 2 else '"FALSE"'}),
           .FIRSTS({'"FALSE"'}),
           .LASTS ({'"TRUE" ' if col == rest_end else '"FALSE"'}))
    c3_2_terminal_chain2_i{i_cnt}(
        .clk ({clk_str.ljust(max_len)}),
        .C0  ({C0_str.ljust(max_len)}),
        .O   ({O_str.ljust(max_len)}),
        .CY  ({CY_str.ljust(max_len)}),
        .PROP({PROP_str.ljust(max_len)}));
    """
        # connect the inputs of LUTs with layer inputs
        instan += f"""
    assign {C0_str}[2] = terminal_chain2_i{i_cnt-1};
    """
        if col in two_op_cols:
            instan += f"""assign {C0_str}[0] = terminal_chain1_out[{col-chain1_start}];
    assign {C0_str}[1] = 1'b0;
    """
        elif col <= chain1to2_end:
            instan += f"""assign {C0_str}[0] = terminal_chain1_out[{col-chain1_start}];
    """
            if col <= terminalAdd_end and col == chain1to2_end:
                instan += f"""assign {C0_str}[1] = layer{terminal_layer_no}_col{col};
    """
            else:
                instan += f"""assign {C0_str}[1] = 1'b0;
    """
        else:
            instan += f"""assign {C0_str}[0] = 1'b0;
    """
            if col <= terminalAdd_end:
                instan += f"""assign {C0_str}[1] = layer{terminal_layer_no}_col{col};
    """
            else:
                instan += f"""assign {C0_str}[1] = 1'b0;
    """
        # connect the outputs of LUTs with layer outputs
        out_str0 = f"terminal_chain2_out[{pos_cnt}]"
        out_str1 = f"terminal_chain2_out[{pos_cnt+1}]"
        out_str_list = [out_str0, out_str1]
        max_len = max(len(s) for s in out_str_list)
        instan += f"""
    assign {out_str0.ljust(max_len)} = {O_str}[0];
    """
        if col == rest_end:
            instan += f"""assign {out_str1.ljust(max_len)} = {O_str}[1];
    """
        # connect LUTs with LOOKAHEAD8
        LUTLA_str0 = f"terminal_chain2_i{i_cnt}"
        LUTLA_str1 = f"CY_LA_terminal_chain2[{pos_cnt}]"
        LUTLA_str2 = f"PROP_LA_terminal_chain2[{pos_cnt}]"
        LUTLA_str_list = [LUTLA_str0, LUTLA_str1, LUTLA_str2]
        max_len = max(len(s) for s in LUTLA_str_list)
        if pos_cnt % 2 == 0:
            instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = {O_str}[1];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
        else:
            instan += f"""
    assign {LUTLA_str0.ljust(max_len)} = COUT_LA_terminal_chain2[{(pos_cnt-1)//2}];
    assign {LUTLA_str1.ljust(max_len)} = {CY_str};
    assign {LUTLA_str2.ljust(max_len)} = {PROP_str};
    """
        # connect carry in and out between LOOKAHEAD8 blocks is needed
        if pos_cnt % 8 == 0:
            instan += f"""
    assign CIN_LA_terminal_chain2[{pos_cnt//8}] = COUT_LA_terminal_chain2[{(pos_cnt//2)-1}];
    """
        # increment GPC instance counter and position counter
        pos_cnt += 1
        i_cnt += 1
    ### Finally, connect the outputs of two terminal chains with the compressor tree output
    if not terminal_reg_flag:
        if terminalAdd_start != 0:
            for col in range(terminalAdd_start):
                instan += f"""
    assign {final_output_name}[{col}] = layer{terminal_layer_no}_col{col};"""
            instan += f"""
    """
        if tail_flag:
            if tail_cascade_flag:
                instan += f"""
    assign {final_output_name}[{tail_end+1}:{terminalAdd_start}] = terminal_chain1_out[{tail_end-terminalAdd_start+1}:0];
    """
                instan += f"""
    assign {final_output_name}[{final_output_width-1}:{tail_end+2}] = terminal_chain2_out[{final_output_width-tail_end-3}:0];
    """
            else:
                instan += f"""
    assign {final_output_name}[{tail_end}:{terminalAdd_start}] = terminal_chain2_out[{tail_end-terminalAdd_start}:0];
    """
                instan += f"""
    assign {final_output_name}[{final_output_width-1}:{tail_end+1}] = terminal_chain2_out[{final_output_width-terminalAdd_start-1}:{tail_end-terminalAdd_start+1}];
    """
        else:
            if chain1_start == terminalAdd_start:
                instan += f"""
    assign {final_output_name}[{terminalAdd_start}] = terminal_chain1_out[0];
    """
                instan += f"""
    assign {final_output_name}[{final_output_width-1}:{terminalAdd_start+1}] = terminal_chain2_out[{final_output_width-terminalAdd_start-2}:0];
    """
            else:
                instan += f"""
    assign {final_output_name}[{final_output_width-1}:{terminalAdd_start}] = terminal_chain2_out[{final_output_width-terminalAdd_start-1}:0];
    """
    else:
        instan += f"""
    always_ff @(posedge clk) begin"""
        if terminalAdd_start != 0:
            for col in range(terminalAdd_start):
                instan += f"""
        {final_output_name}[{col}] <= layer{terminal_layer_no}_col{col};"""
            instan += f"""
    """
        if tail_flag:
            if tail_cascade_flag:
                instan += f"""
        {final_output_name}[{tail_end+1}:{terminalAdd_start}] <= terminal_chain1_out[{tail_end-terminalAdd_start+1}:0];
    """
                instan += f"""
        {final_output_name}[{final_output_width-1}:{tail_end+2}] <= terminal_chain2_out[{final_output_width-tail_end-3}:0];
    """
            else:
                instan += f"""
        {final_output_name}[{tail_end}:{terminalAdd_start}] <= terminal_chain2_out[{tail_end-terminalAdd_start}:0];
    """
                instan += f"""
        {final_output_name}[{final_output_width-1}:{tail_end+1}] <= terminal_chain2_out[{final_output_width-terminalAdd_start-1}:{tail_end-terminalAdd_start+1}];
    """
        else:
            if chain1_start == terminalAdd_start:
                instan += f"""
        {final_output_name}[{terminalAdd_start}] <= terminal_chain1_out[0];
    """
                instan += f"""
        {final_output_name}[{final_output_width-1}:{terminalAdd_start+1}] <= terminal_chain2_out[{final_output_width-terminalAdd_start-2}:0];
    """
            else:
                instan += f"""
        {final_output_name}[{final_output_width-1}:{terminalAdd_start}] <= terminal_chain2_out[{final_output_width-terminalAdd_start-1}:0];
    """
        instan += f"""end
    """
    return signal_decl, instan


def reg_flag_list_gen(pipeline_stages: int, num_layers: int) -> list[bool]:
    reg_flag_list = [False] * num_layers
    base = num_layers // pipeline_stages
    remainder = num_layers % pipeline_stages
    idx = 0
    for stage in range(pipeline_stages):
        group_size = base + (1 if stage < remainder else 0)
        idx += group_size
        reg_flag_list[idx-1] = True
    return reg_flag_list


def compressor_gen(counter_list_rearranged: list[list], first_layer_inputs: list[int], comp_output_name: str, comp_output_width: int, last_compression_layer_bitheap: BitHeap, reg_flag_list: list[bool]) -> tuple[str, str]:
    comments = ""
    declaration = ""
    instantiation = ""
    xdc = ""
    number_of_layers = len(counter_list_rearranged)
    current_layer_inputs = first_layer_inputs
    if number_of_layers >= 2:
        merge_flag_temp, reduced_inputs = merge_last_stage(last_compression_layer_counter_list=counter_list_rearranged[-1],
                                                           last_compression_layer_bitheap=last_compression_layer_bitheap)
    else:
        merge_flag_temp = False
        reduced_inputs = [[[0]]]
    if merge_flag_temp:
        print("Last compression stage is able to be merged with its previous stage!")
        number_of_layers -= 1
    print(f"Maximum Number of Pipeline Stages of the Compressor Tree: {number_of_layers+1}")
    num_pipe = 0
    for val in reg_flag_list:
        num_pipe += 1 if val else 0
    print(f"Generated compressor tree is pipelined into {num_pipe} stages")
    for no in range(number_of_layers):
        merge_flag = True if merge_flag_temp and no == number_of_layers-1 else False
        next_layer_inputs, layer_comments, layer_declaration, layer_instantaion, layer_xdc = layer_gen(layer_no=no,
                                                                                                       layer_inputs=current_layer_inputs,
                                                                                                       chains_list=counter_list_rearranged[no],
                                                                                                       reg_flag=reg_flag_list[no],
                                                                                                       merge_flag=merge_flag,
                                                                                                       merge_counter_list=counter_list_rearranged[-1],
                                                                                                       reduced_inputs=reduced_inputs)
        declaration += layer_comments
        declaration += layer_declaration
        instantiation += layer_comments
        instantiation += layer_instantaion
        xdc += layer_xdc
        current_layer_inputs = next_layer_inputs
    terminal_declaration, terminal_instantiation = terminalAdd_gen(terminal_layer_no=number_of_layers,
                                                                   terminal_inputs=current_layer_inputs,
                                                                   final_output_name=comp_output_name,
                                                                   final_output_width=comp_output_width,
                                                                   terminal_reg_flag=reg_flag_list[-1])
    declaration += f"""
    
    
    // -------------------------------------------------- TERMINAL ADDITION ------------------------------------------------"""
    declaration += terminal_declaration
    instantiation += f"""
    
    
    // -------------------------------------------------- TERMINAL ADDITION ------------------------------------------------"""
    instantiation += terminal_instantiation
    RTL_compressor = comments + declaration + instantiation
    return RTL_compressor, xdc


def read_nonneg_int_list(filepath):
    numbers = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:      # skip the vacant line
                continue
            try:
                num = int(line)
            except ValueError:
                raise ValueError(f"line {lineno} is not an integer: {line}")
            if num < 0:
                raise ValueError(f"line {lineno} is not a non-negative integer: {line}")
            numbers.append(num)
    return numbers


def gen_bitheap_testvectors(number_list: list, test_size: int=1000) -> None:
    folder = "testvectors"
    os.makedirs(folder, exist_ok=True)
    testvectors = []
    number_of_columns = len(number_list)
    for col in range(number_of_columns):
        col_vector = []
        for i in range(test_size):
            col_vector.append(randint(0, 2**number_list[col]-1))
        testvectors.append(col_vector)
        file_path = os.path.join(folder, f"in_col{col}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            for v in col_vector:
                v_str = format(v, 'x')
                f.write(f"{v_str}\n")
    comp_out_list = []
    for i in range(test_size):
        comp_out = 0
        for col in range(number_of_columns):
            comp_out += testvectors[col][i].bit_count() * (2**col)
        comp_out_list.append(comp_out)
    file_path = os.path.join(folder, "comp_out.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        for v in comp_out_list:
            v_str = format(v, 'x')
            f.write(f"{v_str}\n")


def compressor_RTL_gen(txt_file_name: str, sv_file_name: str, compressor_module_name: str, tb_out_width: int, reg_flag_list: list[bool], visualization: bool=False, gen_testbench: bool=True, test_size: int=1000) -> None:
    # read .txt to build bit heap instances
    number_list = read_nonneg_int_list(txt_file_name)
    number_of_columns = len(number_list)
    sum_max = 0
    for col in range(number_of_columns):
        sum_max += number_list[col]*(2**col)
    width_bh = sum_max.bit_length()
    bh_inst = BitHeap(width_bh, 0)
    for col in range(number_of_columns):
        bh_inst.add_bits(col, number_list[col])

    # generation of the module head
    left_w = max(len(str(v-1)) for v in number_list)
    left_w = max([left_w, len(str(width_bh-1))])
    RTL_str = f"""`timescale 1ns / 1ps

module {compressor_module_name} (
    input  logic  {' '*left_w}      clk,
    """
    for col in range(number_of_columns):
        if number_list[col] == 0:
            continue
        elif number_list[col] == 1:
            RTL_str += f"""input  logic  {' '*left_w}      in_col{col},
    """
        else:
            RTL_str += f"""input  logic [{(number_list[col]-1):<{left_w}} : 0] in_col{col},
    """
    RTL_str += f"""output logic [{(width_bh-1):<{left_w}} : 0] comp_out
    );

    """

    # compress the bitheap and arrange layers of counters and counter chains
    if visualization:
        bh_inst.visualize(f"original_bitheap", False)
    last_compression_layer_bitheap, raw_counter_list = compressAll(bh_inst, 0, width_bh-1, visualization, True)
    counter_list = formGPCChain(raw_counter_list)

    # generate the RTL for the bit heap compressor obtained above
    first_layer_inputs = []
    for col in range(width_bh):
        if col > len(number_list)-1:
            first_layer_inputs.append(0)
        else:
            first_layer_inputs.append(number_list[col])

    compressor_RTL, compressor_xdc = compressor_gen(counter_list_rearranged=counter_list,
                                                    first_layer_inputs=first_layer_inputs,
                                                    comp_output_name="comp_out",
                                                    comp_output_width=width_bh,
                                                    last_compression_layer_bitheap=last_compression_layer_bitheap,
                                                    reg_flag_list=reg_flag_list)
    RTL_str += compressor_RTL
    # assign the module inputs with compressor inputs
    RTL_str += f"""
    // -------------------------------------- ASSIGNMENT OF MODULE INPUTS AND COMPRESSOR INPUTS --------------------------------------
    """
    for col in range(number_of_columns):
        RTL_str += f"""assign layer0_col{col:<{4}} = in_col{col};
    """

    # the tail of module
    RTL_str += f"""
endmodule"""
    # write into .sv and .xdc files
    folder = "RTL_generated"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{sv_file_name}.sv")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(RTL_str)
    folder = "xdc_generated"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{sv_file_name}.xdc")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(compressor_xdc)

    if gen_testbench:
        tb_str = f"""`timescale 1ns / 1ps
    
module {compressor_module_name}_tb ();
    // ============================== parameters ==============================
    `define CLK_P         10
    `define CLK_HP        5
    `define TS_SIZE       {test_size}
    `define INIT_RESET    200
    
    // ============================== clock ==============================
    logic clk;
    initial clk = 1'b0;
    always #`CLK_HP clk = ~clk;

    // ============================== in/out signals for DUT ==============================
    """
        for col in range(number_of_columns):
            if number_list[col] == 0:
                continue
            elif number_list[col] == 1:
                tb_str += f"""logic  {' '*left_w}      in_col{col};
    """
            else:
                tb_str += f"""logic [{(number_list[col]-1):<{left_w}} : 0] in_col{col};
    """
        tb_str += f"""logic [{(width_bh-1):<{left_w}} : 0] comp_out;
        """
        w = number_of_columns.bit_length()
        tb_str += f"""
    // ============================== DUT and its port connections ==============================
    {compressor_module_name} dut (
        .clk{' '*(w+1+3)}(clk{' '*(w+1+3)}),
        """
        for col in range(number_of_columns):
            if number_list[col] == 0:
                continue
            else:
                tb_str += f""".in_col{col:<{w+1}}(in_col{col:<{w+1}}),
        """
        tb_str += f""".comp_out(comp_out));
    """
        tb_str += f"""
    // ============================== testvectors ==============================
    """
        for col in range(number_of_columns):
            if number_list[col] == 0:
                continue
            elif number_list[col] == 1:
                tb_str += f"""logic  {' '*left_w}      in_col{col}_ts [`TS_SIZE-1 : 0];
    """
            else:
                tb_str += f"""logic [{(number_list[col]-1):<{left_w}} : 0] in_col{col}_ts [`TS_SIZE-1 : 0];
    """
        tb_str += f"""logic [{(width_bh-1):<{left_w}} : 0] comp_out_ts [`TS_SIZE-1 : 0];
    """
        tb_str += f"""
    // ============================== read testvector values ==============================
    initial begin
        """
        for col in range(number_of_columns):
            if number_list[col] == 0:
                continue
            else:
                tb_str += f"""$readmemh("../../../../../testvectors/in_col{col}.txt", in_col{col}_ts);
        """
        tb_str += f"""$readmemh("../../../../../testvectors/comp_out.txt", comp_out_ts);
    end
    """
        tb_str += f"""
    // ============================== provide test input vectors ==============================
    int i;
    initial begin
        #`INIT_RESET;
        #`CLK_HP;
        #1;
        for (i = 0; i < `TS_SIZE; i = i + 1) begin
            """
        # calculate the number of pipeline stages
        comp_pipeline_stages = 0
        for val in reg_flag_list:
            if val:
                comp_pipeline_stages += 1
        for col in range(number_of_columns):
            if number_list[col] == 0:
                continue
            else:
                tb_str += f"""in_col{col:<{w}} = in_col{col}_ts[i];
            """
        tb_str += f"""#`CLK_P;
        end
    end
    """
        tb_str += f"""
    // ============================== check the correctness of output ==============================
    int j;
    int correct_cnt;
    initial begin
        correct_cnt = 0;
        #`INIT_RESET;
        #`CLK_HP;
        #(`CLK_P*{comp_pipeline_stages});
        #1;
        for (j = 0; j < `TS_SIZE; j = j + 1) begin
            if (comp_out[{tb_out_width-1}:0] == comp_out_ts[j][{tb_out_width-1}:0]) begin
                $display("Testvector-%d CORRECT!", j);
                correct_cnt = correct_cnt + 1;
            end else begin
                $display("=================================================================================");
                $display("Testvector-%d WRONG", j);
                $display("module    output: %b", comp_out[{tb_out_width-1}:0]);
                $display("reference output: %b", comp_out_ts[j][{tb_out_width-1}:0]);
                $display("difference:       %b", comp_out_ts[j][{tb_out_width-1}:0] - comp_out[{tb_out_width-1}:0]);
                $display("=================================================================================");
            end
            #`CLK_P;
        end
        if (correct_cnt == `TS_SIZE) begin
            $display("SUCCESS!");
            $display("PASS All %d Testvectors!", `TS_SIZE);
        end else begin
            $display("TO BE DEBUGGED...");
            $display("%d out of %d testvectors failed...", (`TS_SIZE-correct_cnt), `TS_SIZE);
        end
        $finish();
    end

endmodule"""
        folder = "RTL_generated"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"{sv_file_name}_tb.sv")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(tb_str)
        gen_bitheap_testvectors(number_list=number_list, test_size=test_size)


def Bmult_bitheap_RTL_gen(width_a: int, width_b: int, bitheap_list: list[int], out_reg: bool, file_name: str) -> None:
    left_vals = [0, width_a-1, width_b-1]
    for val in bitheap_list:
        left_vals.append(val-1)
    left_w = max(len(str(v)) for v in left_vals)
    width_exprs = []
    width_expr_lens = []
    for val in left_vals:
        width_exprs.append(width_expr(val, left_w))
        width_expr_lens.append(len(width_expr(val, left_w)))
    w = max(width_expr_lens)

    RTL_str = f"""`timescale 1ns / 1ps

module {file_name} (
    input  logic {width_exprs[0]:<{w}} clk,
    input  logic {width_exprs[1]:<{w}} OPA,
    input  logic {width_exprs[2]:<{w}} OPB"""

    for i in range(3, len(width_exprs)):
        RTL_str += f""",
    output logic {width_exprs[i]:<{w}} col{i-3}"""

    RTL_str += f"""
    );
    
    """

    # declare signals for instance connection
    for i in range(3, len(width_exprs)):
        RTL_str += f"""
    logic {width_exprs[i]:<{w}} col{i-3}_wire;"""

    # generate PART1: the main part row by row
    num_of_rows = width_b // 2
    col_pointers = [0] * len(bitheap_list)
    ### generate the first row; using LUT6_2 to force LUT5 merging
    RTL_str += f"""
    
    // the main part of row 0"""
    for j in range(0, width_a, 2):
        if j == width_a - 1 :
            RTL_str += f"""
    LUT6_2 #(.INIT(64'hDD33DD33268C268C))
    LUT6_2_row0_inst{j} (
        .O6(col{j+1}_wire{f"[{col_pointers[j+1]}]" if bitheap_list[j+1] > 1 else ""}),
        .O5(col{j}_wire{f"[{col_pointers[j]}]" if bitheap_list[j] > 1 else ""}),
        .I0(OPB[0]),
        .I1(OPB[1]),
        .I2({"1'b0" if j == 0 else f"OPA[{j-1}]"}),
        .I3(OPA[{j}]),
        .I4(1'b1),
        .I5(1'b1));
    """
        else:
            RTL_str += f"""
    LUT6_2 #(.INIT(64'h226688CC268C268C))
    LUT6_2_row0_inst{j} (
        .O6(col{j+1}_wire{f"[{col_pointers[j+1]}]" if bitheap_list[j+1] > 1 else ""}),
        .O5(col{j}_wire{f"[{col_pointers[j]}]" if bitheap_list[j] > 1 else ""}),
        .I0(OPB[0]),
        .I1(OPB[1]),
        .I2({"1'b0" if j == 0 else f"OPA[{j-1}]"}),
        .I3(OPA[{j}]),
        .I4(OPA[{j+1}]),
        .I5(1'b1));
    """
        col_pointers[j] += 1
        col_pointers[j+1] += 1
    if width_a % 2 == 0:
        RTL_str += f"""
    LUT5 #(.INIT(32'h7169170F))
    LUT5_row0_inst{width_a} (
        .O (col{width_a}_wire{f"[{col_pointers[width_a]}]" if bitheap_list[width_a] > 1 else ""}),
        .I0(1'b0),
        .I1(OPB[0]),
        .I2(OPB[1]),
        .I3(OPA[{width_a-1}]),
        .I4(OPA[{width_a-1}]));
    """
        col_pointers[width_a] += 1
        RTL_str += f"""
    assign col{width_a+1}_wire{f"[{col_pointers[width_a+1]}]" if bitheap_list[width_a+1] > 1 else ""} = 1'b1;
    """
        col_pointers[width_a+1] += 1
    else:
        RTL_str += f"""
    assign col{width_a+1}_wire{f"[{col_pointers[width_a+1]}]" if bitheap_list[width_a+1] > 1 else ""} = 1'b1;
    """
        col_pointers[width_a+1] += 1
    # the rest of the rows
    for i in range(1, num_of_rows):
        RTL_str += f"""
    
    // the main part of row {i}"""
        for j in range(width_a+2):
            if j == 0:
                RTL_str += f"""
    LUT6_2 #(.INIT(64'h8E96E8F096F096F0))
    LUT6_2_row{i}_inst{j} (
        .O6(col{2*i+j+1}_wire{f"[{col_pointers[2*i+j+1]}]" if bitheap_list[2*i+j+1] > 1 else ""}),
        .O5(col{2*i+j}_wire{f"[{col_pointers[2*i+j]}]" if bitheap_list[2*i+j] > 1 else ""}),
        .I0({"1'b0" if i == 0 else f"OPB[{2*i-1}]"}),
        .I1(OPB[{2*i}]),
        .I2(OPB[{2*i+1}]),
        .I3(OPA[{j}]),
        .I4(OPA[{j+1}]),
        .I5(1'b1));
    """
                col_pointers[2*i+j] += 1
                col_pointers[2*i+j+1] += 1
            elif j == 1:
                pass
            elif j == width_a:
                RTL_str += f"""
    LUT5 #(.INIT(32'h7169170F))
    LUT5_row{i}_inst{j} (
        .O (col{2*i+j}_wire{f"[{col_pointers[2*i+j]}]" if bitheap_list[2*i+j] > 1 else ""}),
        .I0({"1'b0" if i == 0 else f"OPB[{2*i-1}]"}),
        .I1(OPB[{2*i}]),
        .I2(OPB[{2*i+1}]),
        .I3(OPA[{width_a-1}]),
        .I4(OPA[{width_a-1}]));
    """
                col_pointers[2*i+j] += 1
            elif j == width_a + 1:
                RTL_str += f"""
    assign col{2*i+j}_wire{f"[{col_pointers[2*i+j]}]" if bitheap_list[2*i+j] > 1 else ""} = 1'b1;
    """
                col_pointers[2*i+j] += 1
            else:
                if j % 2 == 0:
                    RTL_str += f"""
    LUT5 #(.INIT(32'h8EE896F0))
    LUT5_row{i}_inst{j} (
        .O (col{2*i+j}_wire{f"[{col_pointers[2*i+j]}]" if bitheap_list[2*i+j] > 1 else ""}),
        .I0({"1'b0" if i == 0 else f"OPB[{2*i-1}]"}),
        .I1(OPB[{2*i}]),
        .I2(OPB[{2*i+1}]),
        .I3(OPA[{j}]),
        .I4(OPA[{j-1}]));
    """
                else:
                    RTL_str += f"""
    LUT5 #(.INIT(32'h8E96E8F0))
    LUT5_row{i}_inst{j} (
        .O (col{2*i+j}_wire{f"[{col_pointers[2*i+j]}]" if bitheap_list[2*i+j] > 1 else ""}),
        .I0({"1'b0" if i == 0 else f"OPB[{2*i-1}]"}),
        .I1(OPB[{2*i}]),
        .I2(OPB[{2*i+1}]),
        .I3(OPA[{j-1}]),
        .I4(OPA[{j}]));
    """
                col_pointers[2*i+j] += 1

    # generate PART2: the rest, 1'b1 at column width_a and OPB[2*i+1] at column 2*i
    for i in range(num_of_rows):
        RTL_str += f"""
    assign col{2*i}_wire{f"[{col_pointers[2*i]}]" if bitheap_list[2*i] > 1 else ""} = OPB[{2*i+1}];"""
        col_pointers[2*i] += 1

    RTL_str += f"""
    assign col{width_a}_wire{f"[{col_pointers[width_a]}]" if bitheap_list[width_a] > 1 else ""} = 1'b1;
    """
    col_pointers[width_a] += 1

    # connect internial signal to the outputs
    if out_reg:
        RTL_str += f"""
    always_ff @(posedge clk) begin
    """
        for i in range(len(bitheap_list)):
            RTL_str += f"""    col{i} <= col{i}_wire;
    """
        RTL_str += f"""end
    """
    else:
        for i in range(len(bitheap_list)):
            RTL_str += f"""
    assign col{i} = col{i}_wire;"""

    RTL_str += f"""
endmodule"""

    # generate module .sv file
    folder = "RTL_generated"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{file_name}.sv")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(RTL_str)

    # generate the constraint files
    xdc_str = ""
    for i in range(1, num_of_rows):
        for j in range(2, width_a, 2):
            xdc_str += f"""
set pp_row{i}_i{j} [get_cells -hier -filter {{NAME =~ "*/LUT5_row{i}_inst{j}"}}]
set pp_row{i}_i{j+1} [get_cells -hier -filter {{NAME =~ "*/LUT5_row{i}_inst{j+1}"}}]
set_property LUTNM grp{j//2}_row{i} $pp_row{i}_i{j}
set_property LUTNM grp{j//2}_row{i} $pp_row{i}_i{j+1}
# set_property LOCK_PINS {{I0:A1 I1:A2 I2:A3 I3:A4 I4:A5}} $pp_row{i}_i{j}
# set_property LOCK_PINS {{I0:A1 I1:A2 I2:A3 I3:A4 I4:A6}} $pp_row{i}_i{j+1}

"""
    folder = "xdc_generated"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{file_name}.xdc")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(xdc_str)


def to_twos_complement_hex(x, n_bits):
    if x < 0:
        x = (1 << n_bits) + x
    hex_width = (n_bits + 3) // 4
    return f"{x:0{hex_width}X}"


def gen_Bmult_testvectors(width_a: int, width_b: int, test_size: int) -> None:
    A_ts = []
    B_ts = []
    P_ts = []
    for i in range(test_size):
        A = randint(-2**(width_a-1), 2**(width_a-1)-1)
        B = randint(-2**(width_b-1), 2**(width_b-1)-1)
        P = A * B
        A_ts.append(A)
        B_ts.append(B)
        P_ts.append(P)
    folder = "testvectors"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "A.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        for v in A_ts:
            f.write(to_twos_complement_hex(v, width_a) + "\n")
    file_path = os.path.join(folder, "B.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        for v in B_ts:
            f.write(to_twos_complement_hex(v, width_b) + "\n")
    file_path = os.path.join(folder, "P.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        for v in P_ts:
            f.write(to_twos_complement_hex(v, width_a + width_b) + "\n")


def Bmult_RTL_gen(width_a: int, width_b: int, pipeline_stages: int, gen_testbenches: bool, test_size: int) -> None:
    # both of the operands needs to be of no less than 6 bits
    # the operands are regarded as signed numbers; the multiplication is signed two's compliment multiplication

    ### First, extend two bit operands to even bits and take the one of more bits to recode
    if width_a % 2 == 0:
        OPA_width = width_a
        A_extend_flag = False
    else:
        OPA_width = width_a + 1
        A_extend_flag = True
    if width_b % 2 == 0:
        OPB_width = width_b
        B_extend_flag = False
    else:
        OPB_width = width_b + 1
        B_extend_flag = True
    if OPB_width < OPA_width:
        OPB_width = OPA_width
        B_extend_flag = A_extend_flag
        OPA_width = width_b
        switch_flag = True
    else:
        OPA_width = width_a
        switch_flag = False

    ### generate the list describing the bit heap
    bitheap_list = [0] * (OPA_width + OPB_width)
    num_rows = OPB_width // 2
    for i in range(num_rows):
        for j in range(OPA_width+2):
            bitheap_list[2*i+j] += 1
        bitheap_list[2*i] += 1
    bitheap_list[OPA_width] += 1

    ### generate reg_flag_list according to specified pipeline stages
    ### first, the number of layers should be obtained
    number_of_columns = len(bitheap_list)
    sum_max = 0
    for col in range(number_of_columns):
        sum_max += bitheap_list[col]*(2**col)
    width_bh = sum_max.bit_length()
    bh_layer_cal = BitHeap(width_bh, 0)
    for col in range(number_of_columns):
        bh_layer_cal.add_bits(col, bitheap_list[col])
    last_compression_layer_bitheap, raw_counter_list = compressAll(bh_layer_cal, 0, width_bh-1, False, False)
    counter_list = formGPCChain(raw_counter_list)
    number_of_layers = len(counter_list)
    if number_of_layers >= 2:
        merge_flag_temp, reduced_inputs = merge_last_stage(last_compression_layer_counter_list=counter_list[-1],
                                                           last_compression_layer_bitheap=last_compression_layer_bitheap)
    else:
        merge_flag_temp = False
    if merge_flag_temp:
        number_of_layers -= 1
    number_of_layers += 2
    reg_flag_list = reg_flag_list_gen(pipeline_stages=pipeline_stages,
                                      num_layers=number_of_layers)

    ### generate the RTL and XDC for partial product bit heap generation
    Bmult_bitheap_RTL_gen(width_a=OPA_width,
                          width_b=OPB_width,
                          bitheap_list=bitheap_list,
                          out_reg=reg_flag_list[0],
                          file_name=f"Bmult{width_a}x{width_b}_bitheap_gen")

    ### generate the RTL and XDC compressor for bit heap compression
    with open("bitheap.txt", "w", encoding="utf-8") as f:
        for val in bitheap_list:
            f.write(f"{val}\n")
    comp_reg_flag_list = reg_flag_list[1:]
    compressor_RTL_gen(txt_file_name="bitheap.txt",
                       sv_file_name=f"Bmult{width_a}x{width_b}_bitheap_cmp",
                       compressor_module_name=f"Bmult{width_a}x{width_b}_bitheap_cmp",
                       visualization=True,
                       tb_out_width=(OPA_width+OPB_width),
                       gen_testbench=gen_testbenches,
                       test_size=test_size,
                       reg_flag_list=comp_reg_flag_list)

    ### generate the top-level RTL for the multiplier
    left_vals = [0, width_a-1, width_b-1, width_a+width_b-1]
    left_w = max(len(str(v)) for v in left_vals)
    width_exprs = []
    width_expr_lens = []
    for val in left_vals:
        width_exprs.append(width_expr(val, left_w))
        width_expr_lens.append(len(width_expr(val, left_w)))
    w = max(width_expr_lens)
    RTL_str = f"""`timescale 1ns / 1ps

module Bmult{width_a}x{width_b} (
    input  logic {width_exprs[0]:<{w}} clk,
    input  logic {width_exprs[1]:<{w}} A,
    input  logic {width_exprs[2]:<{w}} B,
    output logic {width_exprs[3]:<{w}} P
    );
    """
    left_vals = [OPA_width-1, OPB_width-1]
    for val in bitheap_list:
        left_vals.append(val-1)
    left_vals.append(OPA_width+OPB_width)
    left_w = max(len(str(v)) for v in left_vals)
    width_exprs = []
    width_expr_lens = []
    for val in left_vals:
        width_exprs.append(width_expr(val, left_w))
        width_expr_lens.append(len(width_expr(val, left_w)))
    w = max(width_expr_lens)
    RTL_str += f"""
    logic {width_exprs[0]:<{w}} OPA;
    logic {width_exprs[1]:<{w}} OPB;
    """
    for i in range(2, len(width_exprs)-1):
        RTL_str += f"""logic {width_exprs[i]:<{w}} col{i-2};
    """
    RTL_str += f"""logic {width_exprs[-1]:<{w}} comp_out;
    """
    # connect module inputs with instance inputs
    if switch_flag:
        RTL_str += f"""
    assign OPA = B;"""
        if B_extend_flag:
            RTL_str += f"""
    assign OPB = {{A[{width_a-1}], A}};
    """
        else:
            RTL_str += f"""
    assign OPB = A;
    """
    else:
        RTL_str += f"""
    assign OPA = A;"""
        if B_extend_flag:
            RTL_str += f"""
    assign OPB = {{B[{width_b-1}], B}};
    """
        else:
            RTL_str += f"""
    assign OPB = B;
    """

    # instantiate the bit heap generation module
    RTL_str += f"""
    Bmult{width_a}x{width_b}_bitheap_gen Bmult{width_a}x{width_b}_bitheap_gen_inst (
        .clk(clk),
        .OPA(OPA),
        .OPB(OPB)"""
    for i in range(len(bitheap_list)):
        RTL_str += f""",
        .col{i}(col{i})"""
    RTL_str += f""");
    """

    # instantiate the compressor tree module
    RTL_str += f"""
    Bmult{width_a}x{width_b}_bitheap_cmp Bmult{width_a}x{width_b}_bitheap_cmp_inst(
        .clk(clk)"""
    for i in range(len(bitheap_list)):
        RTL_str += f""",
        .in_col{i}(col{i})"""
    RTL_str += f""",
        .comp_out(comp_out));
    """

    # connect the instance outputs to module outputs
    RTL_str += f"""
    assign P = comp_out[{width_a+width_b-1}:0];

endmodule
"""

    # write into .sv file
    folder = "RTL_generated"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"Bmult{width_a}x{width_b}.sv")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(RTL_str)

    ### generate testbench and testvectors if required
    if gen_testbenches:
        left_vals = [width_a-1, width_b-1, width_a+width_b-1]
        left_w = max(len(str(v)) for v in left_vals)
        width_exprs = []
        width_expr_lens = []
        for val in left_vals:
            width_exprs.append(width_expr(val, left_w))
            width_expr_lens.append(len(width_expr(val, left_w)))
        w = max(width_expr_lens)
        tb_str = f"""`timescale 1ns / 1ps

module Bmult{width_a}x{width_b}_tb ();
    // ============================== parameters ==============================
    `define CLK_P         10
    `define CLK_HP        5
    `define TS_SIZE       {test_size}
    `define INIT_RESET    200
    
    // ============================== clock ==============================
    logic clk;
    initial clk = 1'b0;
    always #`CLK_HP clk = ~clk;

    // ============================== in/out signals for DUT ==============================
    logic {width_exprs[0]:<{w}} A;
    logic {width_exprs[1]:<{w}} B;
    logic {width_exprs[2]:<{w}} P;
    logic {width_exprs[0]:<{w}} A_ts[`TS_SIZE-1 : 0];
    logic {width_exprs[1]:<{w}} B_ts[`TS_SIZE-1 : 0];
    logic {width_exprs[2]:<{w}} P_ts[`TS_SIZE-1 : 0];

    // ============================== read testvector values ==============================
    initial begin
        $readmemh("../../../../../testvectors/A.txt", A_ts);
        $readmemh("../../../../../testvectors/B.txt", B_ts);
        $readmemh("../../../../../testvectors/P.txt", P_ts);
    end
    
    // ============================== instantiate DUT and connect its ports ==============================
    Bmult{width_a}x{width_b} DUT (
        .clk(clk),
        .A  (A  ),
        .B  (B  ),
        .P  (P  ));
    
    // ============================== provide test input vectors ==============================
    int i;
    initial begin
        #`INIT_RESET;
        #`CLK_HP;
        #1;
        for (i = 0; i < `TS_SIZE; i = i + 1) begin
            A = A_ts[i];
            B = B_ts[i];
            #`CLK_P;
        end
    end
    
    // ============================== check the correctness of output ==============================    
    int j;
    int correct_cnt;
    initial begin
        correct_cnt = 0;
        #`INIT_RESET;
        #`CLK_HP;
        #(`CLK_P*{pipeline_stages});
        #1;
        for (j = 0; j < `TS_SIZE; j = j + 1) begin
            if (P == P_ts[j]) begin
                $display("Testvector-%d CORRECT!", j);
                correct_cnt = correct_cnt + 1;
            end else begin
                $display("=================================================================================");
                $display("Testvector-%d WRONG", j);
                $display("module    output: %b", P);
                $display("reference output: %b", P_ts[j]);
                $display("difference:       %b", P_ts[j] - P);
                $display("=================================================================================");
            end
            #`CLK_P;
        end
        if (correct_cnt == `TS_SIZE) begin
            $display("SUCCESS!");
            $display("PASS All %d Testvectors!", `TS_SIZE);
        end else begin
            $display("TO BE DEBUGGED...");
            $display("%d out of %d testvectors failed...", (`TS_SIZE-correct_cnt), `TS_SIZE);
        end
        $finish();
    end

endmodule
    """
        # write the testbench into .sv files
        folder = "RTL_generated"
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, f"Bmult{width_a}x{width_b}_tb.sv")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(tb_str)
        gen_Bmult_testvectors(width_a=width_a, width_b=width_b, test_size=test_size)




