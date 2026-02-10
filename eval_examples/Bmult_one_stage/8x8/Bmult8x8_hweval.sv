`timescale 1ns / 1ps

module Bmult8x8_hweval (
    input  logic          clk,
    input  logic [7  : 0] A,
    input  logic [7  : 0] B,
    output logic [15 : 0] P
    );

    logic [7 : 0] A_reg;
    logic [7 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult8x8 Bmult8x8_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule