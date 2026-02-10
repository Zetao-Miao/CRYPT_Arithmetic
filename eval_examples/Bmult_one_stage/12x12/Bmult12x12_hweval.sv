`timescale 1ns / 1ps

module Bmult12x12_hweval (
    input  logic          clk,
    input  logic [11 : 0] A,
    input  logic [11 : 0] B,
    output logic [23 : 0] P
    );

    logic [11 : 0] A_reg;
    logic [11 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult12x12 Bmult12x12_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule