`timescale 1ns / 1ps

module Bmult10x10_hweval (
    input  logic          clk,
    input  logic [9  : 0] A,
    input  logic [9  : 0] B,
    output logic [19 : 0] P
    );

    logic [9 : 0] A_reg;
    logic [9 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult10x10 Bmult10x10_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule