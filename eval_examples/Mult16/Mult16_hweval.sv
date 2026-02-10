`timescale 1ns / 1ps

module Comp_Mult16_hweval (
    input  logic          clk,
    input  logic          in_col0,
    input  logic [1  : 0] in_col1,
    input  logic [2  : 0] in_col2,
    input  logic [3  : 0] in_col3,
    input  logic [4  : 0] in_col4,
    input  logic [5  : 0] in_col5,
    input  logic [6  : 0] in_col6,
    input  logic [7  : 0] in_col7,
    input  logic [8  : 0] in_col8,
    input  logic [9  : 0] in_col9,
    input  logic [10 : 0] in_col10,
    input  logic [11 : 0] in_col11,
    input  logic [12 : 0] in_col12,
    input  logic [13 : 0] in_col13,
    input  logic [14 : 0] in_col14,
    input  logic [15 : 0] in_col15,
    input  logic [14 : 0] in_col16,
    input  logic [13 : 0] in_col17,
    input  logic [12 : 0] in_col18,
    input  logic [11 : 0] in_col19,
    input  logic [10 : 0] in_col20,
    input  logic [9  : 0] in_col21,
    input  logic [8  : 0] in_col22,
    input  logic [7  : 0] in_col23,
    input  logic [6  : 0] in_col24,
    input  logic [5  : 0] in_col25,
    input  logic [4  : 0] in_col26,
    input  logic [3  : 0] in_col27,
    input  logic [2  : 0] in_col28,
    input  logic [1  : 0] in_col29,
    input  logic          in_col30,
    output logic [31 : 0] comp_out
    );


    logic          in_col0_reg;
    logic [1  : 0] in_col1_reg;
    logic [2  : 0] in_col2_reg;
    logic [3  : 0] in_col3_reg;
    logic [4  : 0] in_col4_reg;
    logic [5  : 0] in_col5_reg;
    logic [6  : 0] in_col6_reg;
    logic [7  : 0] in_col7_reg;
    logic [8  : 0] in_col8_reg;
    logic [9  : 0] in_col9_reg;
    logic [10 : 0] in_col10_reg;
    logic [11 : 0] in_col11_reg;
    logic [12 : 0] in_col12_reg;
    logic [13 : 0] in_col13_reg;
    logic [14 : 0] in_col14_reg;
    logic [15 : 0] in_col15_reg;
    logic [14 : 0] in_col16_reg;
    logic [13 : 0] in_col17_reg;
    logic [12 : 0] in_col18_reg;
    logic [11 : 0] in_col19_reg;
    logic [10 : 0] in_col20_reg;
    logic [9  : 0] in_col21_reg;
    logic [8  : 0] in_col22_reg;
    logic [7  : 0] in_col23_reg;
    logic [6  : 0] in_col24_reg;
    logic [5  : 0] in_col25_reg;
    logic [4  : 0] in_col26_reg;
    logic [3  : 0] in_col27_reg;
    logic [2  : 0] in_col28_reg;
    logic [1  : 0] in_col29_reg;
    logic          in_col30_reg;


    always_ff @(posedge clk) begin
        in_col0_reg  <= in_col0;
        in_col1_reg  <= in_col1;
        in_col2_reg  <= in_col2;
        in_col3_reg  <= in_col3;
        in_col4_reg  <= in_col4;
        in_col5_reg  <= in_col5;
        in_col6_reg  <= in_col6;
        in_col7_reg  <= in_col7;
        in_col8_reg  <= in_col8;
        in_col9_reg  <= in_col9;
        in_col10_reg <= in_col10;
        in_col11_reg <= in_col11;
        in_col12_reg <= in_col12;
        in_col13_reg <= in_col13;
        in_col14_reg <= in_col14;
        in_col15_reg <= in_col15;
        in_col16_reg <= in_col16;
        in_col17_reg <= in_col17;
        in_col18_reg <= in_col18;
        in_col19_reg <= in_col19;
        in_col20_reg <= in_col20;
        in_col21_reg <= in_col21;
        in_col22_reg <= in_col22;
        in_col23_reg <= in_col23;
        in_col24_reg <= in_col24;
        in_col25_reg <= in_col25;
        in_col26_reg <= in_col26;
        in_col27_reg <= in_col27;
        in_col28_reg <= in_col28;
        in_col29_reg <= in_col29;
        in_col30_reg <= in_col30;
    end



    Comp_Mult16 Comp_Mult16_inst (
        .clk     (clk         ),
        .in_col0 (in_col0_reg ),
        .in_col1 (in_col1_reg ),
        .in_col2 (in_col2_reg ),
        .in_col3 (in_col3_reg ),
        .in_col4 (in_col4_reg ),
        .in_col5 (in_col5_reg ),
        .in_col6 (in_col6_reg ),
        .in_col7 (in_col7_reg ),
        .in_col8 (in_col8_reg ),
        .in_col9 (in_col9_reg ),
        .in_col10(in_col10_reg),
        .in_col11(in_col11_reg),
        .in_col12(in_col12_reg),
        .in_col13(in_col13_reg),
        .in_col14(in_col14_reg),
        .in_col15(in_col15_reg),
        .in_col16(in_col16_reg),
        .in_col17(in_col17_reg),
        .in_col18(in_col18_reg),
        .in_col19(in_col19_reg),
        .in_col20(in_col20_reg),
        .in_col21(in_col21_reg),
        .in_col22(in_col22_reg),
        .in_col23(in_col23_reg),
        .in_col24(in_col24_reg),
        .in_col25(in_col25_reg),
        .in_col26(in_col26_reg),
        .in_col27(in_col27_reg),
        .in_col28(in_col28_reg),
        .in_col29(in_col29_reg),
        .in_col30(in_col30_reg),
        .comp_out(comp_out    ));

endmodule