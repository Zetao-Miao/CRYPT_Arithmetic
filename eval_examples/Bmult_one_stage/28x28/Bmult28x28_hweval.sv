`timescale 1ns / 1ps

module Bmult28x28_hweval (
    input  logic          clk,
    input  logic [27 : 0] A,
    input  logic [27 : 0] B,
    output logic [55 : 0] P
    );

    logic [27 : 0] A_reg;
    logic [27 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult28x28 Bmult28x28_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule