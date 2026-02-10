`timescale 1ns / 1ps

module Comp_double256_hweval (
    input  logic          clk,
    input  logic          resetn,
    input  logic [15 : 0] in0,
    input  logic [15 : 0] in1,
    output logic [9  : 0] comp_out
    );


    logic [255 : 0] in_col0;
    logic [255 : 0] in_col1;


    LFSR #(.OUT_WIDTH(256))
    LFSR_inst0(
        .clk    (clk    ),
        .resetn (resetn ),
        .in_init(in0    ),
        .out    (in_col0));


    LFSR #(.OUT_WIDTH(256))
    LFSR_inst1(
        .clk    (clk    ),
        .resetn (resetn ),
        .in_init(in1    ),
        .out    (in_col1));


    Comp_double256 Comp_double256_inst (
        .clk     (clk     ),
        .in_col0 (in_col0 ),
        .in_col1 (in_col1 ),
        .comp_out(comp_out));

endmodule