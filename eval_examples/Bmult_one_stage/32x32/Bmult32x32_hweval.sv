`timescale 1ns / 1ps

module Bmult32x32_hweval (
    input  logic          clk,
    input  logic [31 : 0] A,
    input  logic [31 : 0] B,
    output logic [63 : 0] P
    );

    logic [31 : 0] A_reg;
    logic [31 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult32x32 Bmult32x32_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule