`timescale 1ns / 1ps

module Comp_double128_hweval (
    input  logic           clk,
    input  logic [127 : 0] in_col0,
    input  logic [127 : 0] in_col1,
    output logic [8   : 0] comp_out
    );


    logic [127 : 0] in_col0_reg;
    logic [127 : 0] in_col1_reg;


    always_ff @(posedge clk) begin
        in_col0_reg <= in_col0;
        in_col1_reg <= in_col1;
    end


    Comp_double128 Comp_double128_inst (
        .clk     (clk        ),
        .in_col0 (in_col0_reg),
        .in_col1 (in_col1_reg),
        .comp_out(comp_out   ));

endmodule