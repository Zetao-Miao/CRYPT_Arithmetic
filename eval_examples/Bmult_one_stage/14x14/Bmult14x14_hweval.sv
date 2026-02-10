`timescale 1ns / 1ps

module Bmult14x14_hweval (
    input  logic          clk,
    input  logic [13 : 0] A,
    input  logic [13 : 0] B,
    output logic [27 : 0] P
    );

    logic [13 : 0] A_reg;
    logic [13 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult14x14 Bmult14x14_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule