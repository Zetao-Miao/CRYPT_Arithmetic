`timescale 1ns / 1ps

module Bmult16x16_hweval (
    input  logic          clk,
    input  logic [15 : 0] A,
    input  logic [15 : 0] B,
    output logic [31 : 0] P
    );

    logic [15 : 0] A_reg;
    logic [15 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult16x16 Bmult16x16_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule