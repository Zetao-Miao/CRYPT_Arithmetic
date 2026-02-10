`timescale 1ns / 1ps

module Bmult20x20_hweval (
    input  logic          clk,
    input  logic [19 : 0] A,
    input  logic [19 : 0] B,
    output logic [39 : 0] P
    );

    logic [19 : 0] A_reg;
    logic [19 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult20x20 Bmult20x20_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule