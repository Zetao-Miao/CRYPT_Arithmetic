from RTL_gen import *
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    The generator currently support generating the following arithmetic operators:
        Compressor Tree Using GPCs;  Radix-4 Booth Tree Multiplier on LUTs
        
        0. Specify The Desired Operator
                  Args        Type                      Description                                        Default Value
            -operator          str     specify the type of operator to generate; current support:             bmult
                                       Compressor Tree:                         cmp
                                       Radix-4 Booth Tree Multiplier on LUTs:   bmult
    
        1. Compressor Tree
                  Args        Type                      Description                                        Default Value
            -txt_file_name     str     specify the txt file which describe your bit heap to compress        bitheap.txt
            -sv_file_name      str     specify the name of the generated sv files                           bitheap_cmp
            -cmp_module_name   str     specify the name of the generated compressor module;                 bitheap_cmp
            -pipeline_stages   int     specify the number of pipeline stages, 0 means pure combinatorial         1
            -visualization     bool    whether to generate the png files for bit heap compression process      True
            -tb_out_width      int     the width of output that is tested in the testbench                       1
            -gen_testbench     bool    whether to generate the testbench                                       True
            -test_size         int     if generating testbench, the number of testvectors                      1000

        2. Radix-4 Booth Tree Multiplier on LUTs
                  Args        Type                      Description                                        Default Value
            -width_a           int     the bit-width of input operand A                                          8
            -width_b           int     the bit-width of input operand B                                          8
            -pipeline_stages   int     specify the number of pipeline stages, 0 means pure combinatorial         1
            -gen_testbench     bool    whether to generate the testbench                                       True
            -test_size         int     if generating testbench, the number of testvectors                      1000
    """)


    parser.add_argument("-operator", type=str, default="bmult",
                        help="""
    specify the type of operator to generate; current support:
    Compressor Tree:                         cmp
    Radix-4 Booth Tree Multiplier on LUTs:   bmult""")

    parser.add_argument("-txt_file_name", type=str, default="bitheap.txt",
                        help="""
    specify the txt file which describe your bit heap to compress
    """)

    parser.add_argument("-sv_file_name", type=str, default="bitheap_cmp",
                        help="""
    specify the txt file which describe your bit heap to compress
    """)

    parser.add_argument("-cmp_module_name", type=str, default="bitheap_cmp",
                        help="""
    specify the name of the generated compressor module;
    """)

    parser.add_argument("-pipeline_stages", type=int, default=1,
                        help="""
    specify the number of pipeline stages, 0 means pure combinatorial
    """)

    parser.add_argument("-visualization", type=bool, default=True,
                        help="""
    whether to generate the png files for bit heap compression process
    """)

    parser.add_argument("-tb_out_width", type=int, default=44,
                        help="""
    the width of output that is tested in the testbench
    """)

    parser.add_argument("-gen_testbench", type=bool, default=True,
                        help="""
    whether to generate the testbench
    """)

    parser.add_argument("-test_size", type=int, default=1000,
                        help="""
    if generating testbench, the number of testvectors
    """)

    parser.add_argument("-width_a", type=int, default=8,
                        help="""
    the width of input operand A
    """)

    parser.add_argument("-width_b", type=int, default=8,
                        help="""
    the width of input operand B
    """)

    args = parser.parse_args()


    if args.operator == "bmult":
        Bmult_RTL_gen(width_a=args.width_a,
                      width_b=args.width_b,
                      pipeline_stages=args.pipeline_stages,
                      gen_testbenches=args.gen_testbench,
                      test_size=args.test_size)

    elif args.operator == "cmp":
        pipe_stages = args.pipeline_stages
        # first get the number of layers in total
        ### future TO-DO: this currently involves repetitive bitheap compression; somehow merge it with compressor_RTL_gen
        number_list = read_nonneg_int_list(args.txt_file_name)
        number_of_columns = len(number_list)
        sum_max = 0
        for col in range(number_of_columns):
            sum_max += number_list[col]*(2**col)
        width_bh = sum_max.bit_length()
        bh_layer_cal = BitHeap(width_bh, 0)
        for col in range(number_of_columns):
            bh_layer_cal.add_bits(col, number_list[col])
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
        number_of_layers += 1
        reg_flag_list = reg_flag_list_gen(pipeline_stages=pipe_stages,
                                          num_layers=number_of_layers)

        # generate compressor
        compressor_RTL_gen(txt_file_name=args.txt_file_name,
                           sv_file_name=args.sv_file_name,
                           compressor_module_name=args.cmp_module_name,
                           visualization=args.visualization,
                           tb_out_width=args.tb_out_width,
                           gen_testbench=args.gen_testbench,
                           test_size=args.test_size,
                           reg_flag_list=reg_flag_list)








