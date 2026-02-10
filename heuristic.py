from Counter_v import *
import copy


def isStartColumn(bitheap: BitHeap, col: int) -> bool:
    for i in range(col):
       if bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round <= 4:
            return False
    return True


# counter applicability function
### state: list[limited_chain: bool, position: int]
def isCounterApplicable(name: str, bitheap: BitHeap, col: int, cascade_in: bool, state: list) -> bool:
    if name == "(6 : 3]":
        if bitheap.heap[col].number_of_free_bits >= 6:
            return True
        else:
            return False
    elif name == "(3 : 2]":
        if cascade_in:
            if bitheap.heap[col].number_of_free_bits >= 2 and ((not state[0]) or state[0] and state[1] < 8):
                return True
            else:
                return False
        else:
            return True if bitheap.heap[col].number_of_free_bits >= 3 else False
    elif name == "(1,5 : 3]":
        if bitheap.heap[col].number_of_free_bits < 4 and cascade_in:
            return False
        if bitheap.heap[col].number_of_free_bits < 5 and (not cascade_in):
            return False
        if bitheap.heap[col+1].number_of_free_bits < 1:
            return False
        if cascade_in and state[0] and state[1] > 6:
            return False
        return True
    elif name == "(2,2,3 : 4]":
        if bitheap.heap[col].number_of_free_bits < 2 and cascade_in:
            return False
        if bitheap.heap[col].number_of_free_bits < 3 and (not cascade_in):
            return False
        if bitheap.heap[col+1].number_of_free_bits < 2:
            return False
        if bitheap.heap[col+2].number_of_free_bits < 2:
            return False
        if cascade_in and state[1] % 2 == 1:
            return False
        return True
    elif name == "(9 : 4,1)":
        if bitheap.heap[col].number_of_free_bits < 8 and cascade_in:
            return False
        if bitheap.heap[col].number_of_free_bits < 9 and (not cascade_in):
            return False
        if cascade_in and state[1] % 2 == 1:
            return False
        return True
    elif name == "(3,9 : 2,3,1)":
        if bitheap.heap[col].number_of_free_bits < 8 and cascade_in:
            return False
        if bitheap.heap[col].number_of_free_bits < 9 and (not cascade_in):
            return False
        if bitheap.heap[col+1].number_of_free_bits < 3:
            return False
        if cascade_in and state[1] % 2 == 1:
            return False
        return True
    elif name == "(4,13 : 3,4,1)":
        if bitheap.heap[col].number_of_free_bits < 12 and cascade_in:
            return False
        if bitheap.heap[col].number_of_free_bits < 13 and (not cascade_in):
            return False
        if bitheap.heap[col+1].number_of_free_bits < 4:
            return False
        return True
    elif name == "(5,17 : 4,5,1)":
        if bitheap.heap[col].number_of_free_bits < 17:
            return False
        if bitheap.heap[col+1].number_of_free_bits < 5:
            return False
        return True
    else:
        return False


# counter necessity function
def isCounterNecessary(name: str, bitheap: BitHeap, col: int) -> bool:
    if name == "(6 : 3]":
        if bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round == 9 and \
            bitheap.heap[col+1].number_of_free_bits + bitheap.heap[col+1].number_of_bits_next_round <= 3 and \
            bitheap.heap[col+2].number_of_free_bits + bitheap.heap[col+2].number_of_bits_next_round <= 3:
            return True
        return False
    elif name == "(9 : 4,1)":
        if bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round >= 12 and \
            (bitheap.heap[col+1].number_of_free_bits + bitheap.heap[col+1].number_of_bits_next_round)/5 < (bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round)/17:
            return True
        return False
    elif name == "(3,9 : 2,3,1)":
        if bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round >= 12:
            return True
        return False
    elif name == "(4,13 : 3,4,1)":
        if bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round >= 16:
            return True
        return False
    elif name == "(5,17 : 4,5,1)":
        return True
    elif name == "(3 : 2]":
        if 5 <= bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round <= 6:
            return True
        return False
    elif name == "(1,5 : 3]":
        return True
    elif name == "(2,2,3 : 4]":
        if 5 <= bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round <= 6 and \
            4 <= bitheap.heap[col+1].number_of_free_bits + bitheap.heap[col+1].number_of_bits_next_round <= 5 and \
            bitheap.heap[col+2].number_of_free_bits + bitheap.heap[col+2].number_of_bits_next_round == 5:
            return True
        if 5 <= bitheap.heap[col].number_of_free_bits + bitheap.heap[col].number_of_bits_next_round <= 6 and \
            4 <= bitheap.heap[col+1].number_of_free_bits + bitheap.heap[col+1].number_of_bits_next_round <= 5 and \
            bitheap.heap[col+2].number_of_free_bits + bitheap.heap[col+2].number_of_bits_next_round == 4 and \
            isStartColumn(bitheap, col):
            return True
        return False
    else:
        return False


def placeGPCs(BitHeap: BitHeap, startColumn: int, stopColumn: int) -> tuple[list, bool]:
    col = startColumn
    counter_list = []
    advance_flag = True
    state = [False, 0]
    while col <= stopColumn:
        # try column counters first
        if isCounterApplicable(name="(5,17 : 4,5,1)", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(5,17 : 4,5,1)", bitheap=BitHeap, col=col):
            name = "(5,17 : 4,5,1)"
            inputs = [5, 17]
            outputs = [4, 5, 1]
            in_cascade = False
            out_cascade = False
            applied_column = col
            LUT_cost = 8
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 1
            advance_flag = False
            state[0] = False
            state[1] = 0
            continue
        if isCounterApplicable(name="(4,13 : 3,4,1)", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(4,13 : 3,4,1)", bitheap=BitHeap, col=col):
            name = "(4,13 : 3,4,1)"
            inputs = [4, 13]
            outputs = [3, 4, 1]
            in_cascade = False
            out_cascade = False
            applied_column = col
            LUT_cost = 6
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 1
            advance_flag = False
            state[0] = False
            state[1] = 0
            continue
        if BitHeap.heap[col].have_cascade_bits:
            if isCounterApplicable(name="(3,9 : 2,3,1)", bitheap=BitHeap, col=col, cascade_in=True, state=state) and \
                    isCounterNecessary(name="(3,9 : 2,3,1)", bitheap=BitHeap, col=col):
                name = "(3,9 : 2,3,1)"
                inputs = [3, 9]
                outputs = [2, 3, 1]
                in_cascade = True
                out_cascade = True
                applied_column = col
                LUT_cost = 4
                counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
                counter_inst.commit(bitheap=BitHeap, check_bound=False)
                counter_list.append(counter_inst)
                col += 2
                advance_flag = False
                state[0] = True
                state[1] = 2
                continue
        if isCounterApplicable(name="(3,9 : 2,3,1)", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(3,9 : 2,3,1)", bitheap=BitHeap, col=col):
            name = "(3,9 : 2,3,1)"
            inputs = [3, 9]
            outputs = [2, 3, 1]
            in_cascade = False
            out_cascade = True
            applied_column = col
            LUT_cost = 4
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 2
            advance_flag = False
            state[0] = True
            state[1] = 2
            continue
        if BitHeap.heap[col].have_cascade_bits:
            if isCounterApplicable(name="(9 : 4,1)", bitheap=BitHeap, col=col, cascade_in=True, state=state) and \
                    isCounterNecessary(name="(9 : 4,1)", bitheap=BitHeap, col=col):
                name = "(9 : 4,1)"
                inputs = [9]
                outputs = [4, 1]
                in_cascade = True
                out_cascade = False
                applied_column = col
                LUT_cost = 3
                counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
                counter_inst.commit(bitheap=BitHeap, check_bound=False)
                counter_list.append(counter_inst)
                # col += 1
                advance_flag = False
                state[0] = False
                state[1] = 0
                continue
        if isCounterApplicable(name="(9 : 4,1)", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(9 : 4,1)", bitheap=BitHeap, col=col):
            name = "(9 : 4,1)"
            inputs = [9]
            outputs = [4, 1]
            in_cascade = False
            out_cascade = True
            applied_column = col
            LUT_cost = 3
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            # col += 1
            advance_flag = False
            state[0] = True
            state[1] = 2
            continue
        if isCounterApplicable(name="(6 : 3]", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(6 : 3]", bitheap=BitHeap, col=col):
            name = "(6 : 3]"
            inputs = [6]
            outputs = [1, 1, 1]
            in_cascade = False
            out_cascade = True
            applied_column = col
            LUT_cost = 3
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 2
            advance_flag = False
            state[0] = True
            state[1] = 1
            continue
        if BitHeap.heap[col].have_cascade_bits:
            if isCounterApplicable(name="(2,2,3 : 4]", bitheap=BitHeap, col=col, cascade_in=True, state=state) and \
                    isCounterNecessary(name="(2,2,3 : 4]", bitheap=BitHeap, col=col):
                name = "(2,2,3 : 4]"
                inputs = [2, 2, 3]
                outputs = [1, 1, 1, 1]
                in_cascade = True
                out_cascade = False
                applied_column = col
                LUT_cost = 2
                counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
                counter_inst.commit(bitheap=BitHeap, check_bound=False)
                counter_list.append(counter_inst)
                col += 1
                advance_flag = False
                state[0] = False
                state[1] = 0
                continue
        if isCounterApplicable(name="(2,2,3 : 4]", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(2,2,3 : 4]", bitheap=BitHeap, col=col):
            name = "(2,2,3 : 4]"
            inputs = [2, 2, 3]
            outputs = [1, 1, 1, 1]
            in_cascade = False
            out_cascade = True
            applied_column = col
            LUT_cost = 2
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 3
            advance_flag = False
            state[0] = True
            state[1] = 2
            continue
        if BitHeap.heap[col].have_cascade_bits:
            if isCounterApplicable(name="(3 : 2]", bitheap=BitHeap, col=col, cascade_in=True, state=state) and \
                    isCounterNecessary(name="(3 : 2]", bitheap=BitHeap, col=col):
                name = "(3 : 2]"
                inputs = [3]
                outputs = [1, 1]
                in_cascade = True
                out_cascade = True
                applied_column = col
                LUT_cost = 1
                counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
                counter_inst.commit(bitheap=BitHeap, check_bound=False)
                counter_list.append(counter_inst)
                col += 1
                advance_flag = False
                state[1] += 1
                continue
        if isCounterApplicable(name="(3 : 2]", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(3 : 2]", bitheap=BitHeap, col=col):
            name = "(3 : 2]"
            inputs = [3]
            outputs = [1, 1]
            in_cascade = False
            out_cascade = True
            applied_column = col
            LUT_cost = 1
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 1
            advance_flag = False
            state[0] = False
            state[1] = 1
            continue
        if BitHeap.heap[col].have_cascade_bits:
            if isCounterApplicable(name="(1,5 : 3]", bitheap=BitHeap, col=col, cascade_in=True, state=state) and \
                    isCounterNecessary(name="(1,5 : 3]", bitheap=BitHeap, col=col):
                name = "(1,5 : 3]"
                inputs = [1, 5]
                outputs = [1, 1, 1]
                in_cascade = True
                out_cascade = True
                applied_column = col
                LUT_cost = 2
                counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
                counter_inst.commit(bitheap=BitHeap, check_bound=False)
                counter_list.append(counter_inst)
                col += 2
                advance_flag = False
                state[1] += 2
                continue
        if isCounterApplicable(name="(1,5 : 3]", bitheap=BitHeap, col=col, cascade_in=False, state=state) and \
                isCounterNecessary(name="(1,5 : 3]", bitheap=BitHeap, col=col):
            name = "(1,5 : 3]"
            inputs = [1, 5]
            outputs = [1, 1, 1]
            in_cascade = False
            out_cascade = True
            applied_column = col
            LUT_cost = 2
            counter_inst = counter(name, inputs, outputs, in_cascade, out_cascade, applied_column, LUT_cost)
            counter_inst.commit(bitheap=BitHeap, check_bound=False)
            counter_list.append(counter_inst)
            col += 2
            advance_flag = False
            state[0] = False
            state[1] = 2
            continue
        col += 1
        BitHeap.clear_cascade_bits()
    return counter_list, advance_flag


def compressLayer(bitheap: BitHeap, startColumn: int, stopColumn: int) -> list:
    advance_flag = False
    counter_layer = []
    while not advance_flag:
        counter_list, advance_flag = placeGPCs(bitheap, startColumn, stopColumn)
        counter_layer.extend(counter_list)
    return counter_layer


def compressAll(bitheap: BitHeap, startColumn: int, stopColumn: int, plotBitHeap: bool, printUsage: bool) -> tuple[BitHeap, list]:
    finish_flag = False
    layer_list = []
    layer_no = 0
    LUTUsage = 0
    previous_bitheap = copy.deepcopy(bitheap)
    while not finish_flag:
        counter_layer = compressLayer(bitheap, startColumn, stopColumn)
        layer_list.append(counter_layer)
        bitheap.advance_round()
        if plotBitHeap:
            bitheap.visualize(filename=f"after_layer_{layer_no}", use_next_round=False)
            layer_no += 1
        finish_flag, _ = bitheap.check_last_layer()
        if not finish_flag:
            previous_bitheap.advance_round()
            _ = compressLayer(previous_bitheap, startColumn, stopColumn)
    if printUsage:
        for layer in layer_list:
            for counter in layer:
                LUTUsage += counter.LUT_cost
        print(f"The LUT Usage without terminal addition is {LUTUsage}")

    return previous_bitheap, layer_list


def formGPCChain(all_layers: list[list]) -> list[list]:
    all_layers_local = all_layers
    all_layers_formed = []
    for layer in all_layers_local:
        layer_list = []
        while len(layer):
            new_chain = [layer[0]]
            col_pointer = layer[0].applied_column + len(layer[0].outputs) - 1
            for counter in layer[1:]:
                if counter.applied_column == col_pointer and counter.in_cascade and new_chain[-1].out_cascade:
                    new_chain.append(counter)
                    col_pointer += len(counter.outputs) - 1
            layer_list.append(new_chain)
            for counter in new_chain:
                layer.remove(counter)
        all_layers_formed.append(layer_list)
    return all_layers_formed


# def formGPCChain(layer_counters: list[counter]) -> list[list]:
#     """
#     This function forms the GPC chains and floating GPCs and putting each of them in a separate list
#     """
#     layer_counters_local = layer_counters
#     layer_counters_formed = []
#     while len(layer_counters_local):
#         new_chain = [layer_counters_local[0]]
#         col_pointer = layer_counters_local[0].applied_column + len(layer_counters_local[0].outputs) - 1
#         if len(layer_counters_local) > 1:
#             for counter in layer_counters_local[1:]:
#                 if counter.applied_column == col_pointer and counter.in_cascade:
#                     new_chain.append(counter)
#                     col_pointer += len(counter.outputs) - 1
#         layer_counters_formed.append(new_chain)
#         for counter in new_chain:
#             layer_counters_local.remove(counter)
#     return layer_counters_formed
#
#
# def reformGPCChain(layer_counters_formed: list[list[counter]]) -> list[list]:
#     """
#     This function reforms the GPC chains due to the logic and timing limits of LOOKAHEAD8 blocks:
#         - if the chain starts with a GPC that cannot utilize LOOKAHEAD logic at the first two-bit sector,
#           it cannot utilize the last two-bit sector of that LOOKAHEAD8, and the lack of timing arc CYH -> COUTH requires breaking the chain into two
#         - if the chain ends with a GPC that cannot utilize LOOKAHEAD logic and that has to be placed across the CARRY MUX,
#           first check if it can be changed to a floating counter, if not possible
#           second check if it can be broken apart and the second part can act like a floating counter, if not possible either
#           finally add one buffer LUT in the chain to map the carry propagation on the LUT cascade path, which costs one more LUT usage of course
#     """
#     layer_counters_formed_local = layer_counters_formed
#     layer_counters_reformed = []


### doesn't really need this function to be honest, makes almost no difference and only takes more time to run...
def rearrange_layers(bitheap: BitHeap, all_layers_formed: list[list], visualization: bool = False) -> list[list]:
    all_layers_formed_local = all_layers_formed
    rearranged_layer_list = []
    num_layers = len(all_layers_formed_local)
    for i in range(num_layers):
        if all_layers_formed_local[i]:
            rearranged_layer_list.append(all_layers_formed_local[i])
        for chain in all_layers_formed_local[i]:
            for counter in chain:
                counter.commit(bitheap=bitheap, check_bound=True)
        if i != num_layers - 1:
            to_remove = []
            for chain in all_layers_formed_local[i+1]:
                rearrange_flag = True
                for counter in chain:
                    if not isCounterApplicable(name=counter.name, bitheap=bitheap, col=counter.applied_column, cascade_in=counter.in_cascade, state=[False, 0]):
                        rearrange_flag = False
                        break
                if rearrange_flag:
                    rearranged_layer_list[-1].append(chain)
                    to_remove.append(chain)
                    for counter in chain:
                        counter.commit(bitheap=bitheap, check_bound=True)
            for chain in to_remove:
                all_layers_formed_local[i+1].remove(chain)
        bitheap.advance_round()
        if visualization:
            bitheap.visualize(filename=f"after_layer_{i}_rearr", use_next_round=False)
    return rearranged_layer_list


# function to check whether the last compression stage can be merged with its previous stage by allowing insufficient use of GPCs
# currently, only allow insufficient use of (3 : 2] counter and (1,5 : 3] counter
def merge_last_stage(last_compression_layer_counter_list: list[list], last_compression_layer_bitheap: BitHeap) -> tuple[bool, list[list[list[int]]]]:
    # first check if all counters are (3 : 2] counters and (1,5 : 3] counters
    reduced_inputs_list = []
    for chain in last_compression_layer_counter_list:
        chain_reduced_inputs = []
        for counter in chain:
            if counter.name == "(3 : 2]" and (not counter.in_cascade):
                if last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round == 3 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 2:
                    chain_reduced_inputs.append([1])
                else:
                    return False, [[[0]]]
            elif counter.name == "(3 : 2]" and counter.in_cascade:
                if last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round == 3 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 1:
                    chain_reduced_inputs.append([1])
                elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round == 3 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 2:
                    chain_reduced_inputs.append([0])
                elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round == 2 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 2:
                    chain_reduced_inputs.append([0])
                elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round == 2 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 3:
                    chain_reduced_inputs.append([0])
                else:
                    return False, [[[0]]]
            elif counter.name == "(1,5 : 3]" and (not counter.in_cascade):
                if last_compression_layer_bitheap.heap[counter.applied_column+1].number_of_free_bits == 0:
                    if last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round < 4 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 4:
                        chain_reduced_inputs.append([1, 1])
                    elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits >= 5:
                        chain_reduced_inputs.append([1, 0])
                    else:
                        return False, [[[0]]]
                else:
                    if last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round < 4 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 4:
                        chain_reduced_inputs.append([0, 1])
                    else:
                        return False, [[[0]]]
            elif counter.name == "(1,5 : 3]" and counter.in_cascade:
                if last_compression_layer_bitheap.heap[counter.applied_column+1].number_of_free_bits == 0:
                    if last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round < 4 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 3:
                        chain_reduced_inputs.append([1, 1])
                    elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round < 4 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 2:
                        chain_reduced_inputs.append([1, 2])
                    elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits >= 5:
                        chain_reduced_inputs.append([1, 0])
                    else:
                        return False, [[[0]]]
                else:
                    if last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round < 4 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 3:
                        chain_reduced_inputs.append([0, 1])
                    elif last_compression_layer_bitheap.heap[counter.applied_column].number_of_bits_next_round < 4 and last_compression_layer_bitheap.heap[counter.applied_column].number_of_free_bits == 2:
                        chain_reduced_inputs.append([0, 2])
                    else:
                        return False, [[[0]]]
            else:
                return False, [[[0]]]
        reduced_inputs_list.append(chain_reduced_inputs)
    return True, reduced_inputs_list

