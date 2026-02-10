`timescale 1ns / 1ps

module Comp_single256_hweval (
    input  logic           clk,
    input  logic [255 : 0] in_col0,
    output logic [8   : 0] comp_out
    );

    logic [255 : 0] in_col0_reg;


    always_ff @(posedge clk) begin
        in_col0_reg <= in_col0;
    end


    Comp_single256 Comp_single256_inst (
        .clk     (clk        ),
        .in_col0 (in_col0_reg),
        .comp_out(comp_out   ));

endmodule