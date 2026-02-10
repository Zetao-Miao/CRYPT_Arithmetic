`timescale 1ns / 1ps

module Comp_single128_hweval (
    input  logic           clk,
    input  logic [127 : 0] in_col0,
    output logic [7   : 0] comp_out
    );


    logic [127 : 0] in_col0_reg;


    always_ff @(posedge clk) begin
        in_col0_reg <= in_col0;
    end


    Comp_single128 Comp_single128_inst (
        .clk     (clk        ),
        .in_col0 (in_col0_reg),
        .comp_out(comp_out   ));

endmodule