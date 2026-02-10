`timescale 1ns / 1ps
    
module Bmult6x6_bitheap_cmp_tb ();
    // ============================== parameters ==============================
    `define CLK_P         10
    `define CLK_HP        5
    `define TS_SIZE       20000
    `define INIT_RESET    200
    
    // ============================== clock ==============================
    logic clk;
    initial clk = 1'b0;
    always #`CLK_HP clk = ~clk;

    // ============================== in/out signals for DUT ==============================
    logic [1  : 0] in_col0;
    logic          in_col1;
    logic [2  : 0] in_col2;
    logic [1  : 0] in_col3;
    logic [3  : 0] in_col4;
    logic [2  : 0] in_col5;
    logic [3  : 0] in_col6;
    logic [2  : 0] in_col7;
    logic [1  : 0] in_col8;
    logic [1  : 0] in_col9;
    logic          in_col10;
    logic          in_col11;
    logic [12 : 0] comp_out;
        
    // ============================== DUT and its port connections ==============================
    Bmult6x6_bitheap_cmp dut (
        .clk        (clk        ),
        .in_col0    (in_col0    ),
        .in_col1    (in_col1    ),
        .in_col2    (in_col2    ),
        .in_col3    (in_col3    ),
        .in_col4    (in_col4    ),
        .in_col5    (in_col5    ),
        .in_col6    (in_col6    ),
        .in_col7    (in_col7    ),
        .in_col8    (in_col8    ),
        .in_col9    (in_col9    ),
        .in_col10   (in_col10   ),
        .in_col11   (in_col11   ),
        .comp_out(comp_out));
    
    // ============================== testvectors ==============================
    logic [1  : 0] in_col0_ts [`TS_SIZE-1 : 0];
    logic          in_col1_ts [`TS_SIZE-1 : 0];
    logic [2  : 0] in_col2_ts [`TS_SIZE-1 : 0];
    logic [1  : 0] in_col3_ts [`TS_SIZE-1 : 0];
    logic [3  : 0] in_col4_ts [`TS_SIZE-1 : 0];
    logic [2  : 0] in_col5_ts [`TS_SIZE-1 : 0];
    logic [3  : 0] in_col6_ts [`TS_SIZE-1 : 0];
    logic [2  : 0] in_col7_ts [`TS_SIZE-1 : 0];
    logic [1  : 0] in_col8_ts [`TS_SIZE-1 : 0];
    logic [1  : 0] in_col9_ts [`TS_SIZE-1 : 0];
    logic          in_col10_ts [`TS_SIZE-1 : 0];
    logic          in_col11_ts [`TS_SIZE-1 : 0];
    logic [12 : 0] comp_out_ts [`TS_SIZE-1 : 0];
    
    // ============================== read testvector values ==============================
    initial begin
        $readmemh("../../../../../testvectors/in_col0.txt", in_col0_ts);
        $readmemh("../../../../../testvectors/in_col1.txt", in_col1_ts);
        $readmemh("../../../../../testvectors/in_col2.txt", in_col2_ts);
        $readmemh("../../../../../testvectors/in_col3.txt", in_col3_ts);
        $readmemh("../../../../../testvectors/in_col4.txt", in_col4_ts);
        $readmemh("../../../../../testvectors/in_col5.txt", in_col5_ts);
        $readmemh("../../../../../testvectors/in_col6.txt", in_col6_ts);
        $readmemh("../../../../../testvectors/in_col7.txt", in_col7_ts);
        $readmemh("../../../../../testvectors/in_col8.txt", in_col8_ts);
        $readmemh("../../../../../testvectors/in_col9.txt", in_col9_ts);
        $readmemh("../../../../../testvectors/in_col10.txt", in_col10_ts);
        $readmemh("../../../../../testvectors/in_col11.txt", in_col11_ts);
        $readmemh("../../../../../testvectors/comp_out.txt", comp_out_ts);
    end
    
    // ============================== provide test input vectors ==============================
    int i;
    initial begin
        #`INIT_RESET;
        #`CLK_HP;
        #1;
        for (i = 0; i < `TS_SIZE; i = i + 1) begin
            in_col0    = in_col0_ts[i];
            in_col1    = in_col1_ts[i];
            in_col2    = in_col2_ts[i];
            in_col3    = in_col3_ts[i];
            in_col4    = in_col4_ts[i];
            in_col5    = in_col5_ts[i];
            in_col6    = in_col6_ts[i];
            in_col7    = in_col7_ts[i];
            in_col8    = in_col8_ts[i];
            in_col9    = in_col9_ts[i];
            in_col10   = in_col10_ts[i];
            in_col11   = in_col11_ts[i];
            #`CLK_P;
        end
    end
    
    // ============================== check the correctness of output ==============================
    int j;
    int correct_cnt;
    initial begin
        correct_cnt = 0;
        #`INIT_RESET;
        #`CLK_HP;
        #(`CLK_P*1);
        #1;
        for (j = 0; j < `TS_SIZE; j = j + 1) begin
            if (comp_out[11:0] == comp_out_ts[j][11:0]) begin
                $display("Testvector-%d CORRECT!", j);
                correct_cnt = correct_cnt + 1;
            end else begin
                $display("=================================================================================");
                $display("Testvector-%d WRONG", j);
                $display("module    output: %b", comp_out[11:0]);
                $display("reference output: %b", comp_out_ts[j][11:0]);
                $display("difference:       %b", comp_out_ts[j][11:0] - comp_out[11:0]);
                $display("=================================================================================");
            end
            #`CLK_P;
        end
        if (correct_cnt == `TS_SIZE) begin
            $display("SUCCESS!");
            $display("PASS All %d Testvectors!", `TS_SIZE);
        end else begin
            $display("TO BE DEBUGGED...");
            $display("%d out of %d testvectors failed...", (`TS_SIZE-correct_cnt), `TS_SIZE);
        end
        $finish();
    end

endmodule