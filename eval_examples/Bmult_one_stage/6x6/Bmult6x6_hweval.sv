`timescale 1ns / 1ps

module Bmult6x6_hweval (
    input  logic          clk,
    input  logic [5  : 0] A,
    input  logic [5  : 0] B,
    output logic [11 : 0] P
    );

    logic [5 : 0] A_reg;
    logic [5 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult6x6 Bmult6x6_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule