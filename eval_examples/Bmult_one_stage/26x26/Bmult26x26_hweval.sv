`timescale 1ns / 1ps

module Bmult26x26_hweval (
    input  logic          clk,
    input  logic [25 : 0] A,
    input  logic [25 : 0] B,
    output logic [51 : 0] P
    );

    logic [25 : 0] A_reg;
    logic [25 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult26x26 Bmult26x26_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule