`timescale 1ns / 1ps

module Bmult18x18_hweval (
    input  logic          clk,
    input  logic [17 : 0] A,
    input  logic [17 : 0] B,
    output logic [35 : 0] P
    );

    logic [17 : 0] A_reg;
    logic [17 : 0] B_reg;

    always_ff @(posedge clk) begin
        A_reg <= A;
        B_reg <= B;
    end

    Bmult18x18 Bmult18x18_inst (
        .clk(clk  ),
        .A  (A_reg),
        .B  (B_reg),
        .P  (P    ));

endmodule