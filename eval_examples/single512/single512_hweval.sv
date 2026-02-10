`timescale 1ns / 1ps

module Comp_single512_hweval (
    input  logic          clk,
    input  logic          resetn,
    input  logic [15 : 0] in,
    output logic [9  : 0] comp_out
    );


    logic [511 : 0] in_col0;


    LFSR #(.OUT_WIDTH(512))
    LFSR_inst(
        .clk     (clk    ),
        .resetn  (resetn ),
        .in_init (in     ),
        .out     (in_col0));


    Comp_single512 dut (
        .clk     (clk     ),
        .in_col0 (in_col0 ),
        .comp_out(comp_out));

endmodule