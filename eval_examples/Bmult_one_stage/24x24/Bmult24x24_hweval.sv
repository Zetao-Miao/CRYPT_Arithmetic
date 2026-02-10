`timescale 1ns / 1ps

module Bmult24x24_hweval (
    input  logic          clk,
    input  logic [23 : 0] A,
    input  logic [23 : 0] B,
    output logic [47 : 0] P
    );

    logic [23 : 0] A_reg;
    logic [23 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult24x24 Bmult24x24_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule