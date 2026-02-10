`timescale 1ns / 1ps

module Bmult22x22_hweval (
    input  logic          clk,
    input  logic [21 : 0] A,
    input  logic [21 : 0] B,
    output logic [43 : 0] P
    );

    logic [21 : 0] A_reg;
    logic [21 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult22x22 Bmult22x22_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule