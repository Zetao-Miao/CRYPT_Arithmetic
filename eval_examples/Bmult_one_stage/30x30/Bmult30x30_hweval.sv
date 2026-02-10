`timescale 1ns / 1ps

module Bmult30x30_hweval (
    input  logic          clk,
    input  logic [29 : 0] A,
    input  logic [29 : 0] B,
    output logic [59 : 0] P
    );

    logic [29 : 0] A_reg;
    logic [29 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult30x30 Bmult30x30_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule