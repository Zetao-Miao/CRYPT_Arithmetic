`timescale 1ns / 1ps

module Bmult28x28 (
    input  logic          clk,
    input  logic [27 : 0] A,
    input  logic [27 : 0] B,
    output logic [55 : 0] P
    );
    
    logic [27 : 0] OPA;
    logic [27 : 0] OPB;
    logic [1  : 0] col0;
    logic          col1;
    logic [2  : 0] col2;
    logic [1  : 0] col3;
    logic [3  : 0] col4;
    logic [2  : 0] col5;
    logic [4  : 0] col6;
    logic [3  : 0] col7;
    logic [5  : 0] col8;
    logic [4  : 0] col9;
    logic [6  : 0] col10;
    logic [5  : 0] col11;
    logic [7  : 0] col12;
    logic [6  : 0] col13;
    logic [8  : 0] col14;
    logic [7  : 0] col15;
    logic [9  : 0] col16;
    logic [8  : 0] col17;
    logic [10 : 0] col18;
    logic [9  : 0] col19;
    logic [11 : 0] col20;
    logic [10 : 0] col21;
    logic [12 : 0] col22;
    logic [11 : 0] col23;
    logic [13 : 0] col24;
    logic [12 : 0] col25;
    logic [14 : 0] col26;
    logic [13 : 0] col27;
    logic [14 : 0] col28;
    logic [13 : 0] col29;
    logic [12 : 0] col30;
    logic [12 : 0] col31;
    logic [11 : 0] col32;
    logic [11 : 0] col33;
    logic [10 : 0] col34;
    logic [10 : 0] col35;
    logic [9  : 0] col36;
    logic [9  : 0] col37;
    logic [8  : 0] col38;
    logic [8  : 0] col39;
    logic [7  : 0] col40;
    logic [7  : 0] col41;
    logic [6  : 0] col42;
    logic [6  : 0] col43;
    logic [5  : 0] col44;
    logic [5  : 0] col45;
    logic [4  : 0] col46;
    logic [4  : 0] col47;
    logic [3  : 0] col48;
    logic [3  : 0] col49;
    logic [2  : 0] col50;
    logic [2  : 0] col51;
    logic [1  : 0] col52;
    logic [1  : 0] col53;
    logic          col54;
    logic          col55;
    logic [56 : 0] comp_out;
    
    assign OPA = A;
    assign OPB = B;
    
    Bmult28x28_bitheap_gen Bmult28x28_bitheap_gen_inst (
        .clk(clk),
        .OPA(OPA),
        .OPB(OPB),
        .col0(col0),
        .col1(col1),
        .col2(col2),
        .col3(col3),
        .col4(col4),
        .col5(col5),
        .col6(col6),
        .col7(col7),
        .col8(col8),
        .col9(col9),
        .col10(col10),
        .col11(col11),
        .col12(col12),
        .col13(col13),
        .col14(col14),
        .col15(col15),
        .col16(col16),
        .col17(col17),
        .col18(col18),
        .col19(col19),
        .col20(col20),
        .col21(col21),
        .col22(col22),
        .col23(col23),
        .col24(col24),
        .col25(col25),
        .col26(col26),
        .col27(col27),
        .col28(col28),
        .col29(col29),
        .col30(col30),
        .col31(col31),
        .col32(col32),
        .col33(col33),
        .col34(col34),
        .col35(col35),
        .col36(col36),
        .col37(col37),
        .col38(col38),
        .col39(col39),
        .col40(col40),
        .col41(col41),
        .col42(col42),
        .col43(col43),
        .col44(col44),
        .col45(col45),
        .col46(col46),
        .col47(col47),
        .col48(col48),
        .col49(col49),
        .col50(col50),
        .col51(col51),
        .col52(col52),
        .col53(col53),
        .col54(col54),
        .col55(col55));
    
    Bmult28x28_bitheap_cmp Bmult28x28_bitheap_cmp_inst(
        .clk(clk),
        .in_col0(col0),
        .in_col1(col1),
        .in_col2(col2),
        .in_col3(col3),
        .in_col4(col4),
        .in_col5(col5),
        .in_col6(col6),
        .in_col7(col7),
        .in_col8(col8),
        .in_col9(col9),
        .in_col10(col10),
        .in_col11(col11),
        .in_col12(col12),
        .in_col13(col13),
        .in_col14(col14),
        .in_col15(col15),
        .in_col16(col16),
        .in_col17(col17),
        .in_col18(col18),
        .in_col19(col19),
        .in_col20(col20),
        .in_col21(col21),
        .in_col22(col22),
        .in_col23(col23),
        .in_col24(col24),
        .in_col25(col25),
        .in_col26(col26),
        .in_col27(col27),
        .in_col28(col28),
        .in_col29(col29),
        .in_col30(col30),
        .in_col31(col31),
        .in_col32(col32),
        .in_col33(col33),
        .in_col34(col34),
        .in_col35(col35),
        .in_col36(col36),
        .in_col37(col37),
        .in_col38(col38),
        .in_col39(col39),
        .in_col40(col40),
        .in_col41(col41),
        .in_col42(col42),
        .in_col43(col43),
        .in_col44(col44),
        .in_col45(col45),
        .in_col46(col46),
        .in_col47(col47),
        .in_col48(col48),
        .in_col49(col49),
        .in_col50(col50),
        .in_col51(col51),
        .in_col52(col52),
        .in_col53(col53),
        .in_col54(col54),
        .in_col55(col55),
        .comp_out(comp_out));
    
    assign P = comp_out[55:0];

endmodule
