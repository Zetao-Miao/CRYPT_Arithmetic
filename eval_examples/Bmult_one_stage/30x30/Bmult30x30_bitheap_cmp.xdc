
### constraints for c9_41_l0_c3_i8 ###
set lut_hi_l0_c3_i8 [get_cells -hier -filter {NAME =~ "*/c9_41_l0_c3_i8/LUT3_inst0"}]
set lut_lo_l0_c3_i8 [get_cells -hier -filter {NAME =~ "*/c9_41_l0_c3_i8/LUT3_inst1"}]
set_property LUTNM grp_l0_c3_i8 $lut_hi_l0_c3_i8
set_property LUTNM grp_l0_c3_i8 $lut_lo_l0_c3_i8


### constraints for c9_41_l0_f8 ###
set lut_hi_l0_f8 [get_cells -hier -filter {NAME =~ "*/c9_41_l0_f8/LUT3_inst0"}]
set lut_lo_l0_f8 [get_cells -hier -filter {NAME =~ "*/c9_41_l0_f8/LUT3_inst1"}]
set_property LUTNM grp_l0_f8 $lut_hi_l0_f8
set_property LUTNM grp_l0_f8 $lut_lo_l0_f8



### constraints for c9_41_l0_f10 ###
set lut_hi_l0_f10 [get_cells -hier -filter {NAME =~ "*/c9_41_l0_f10/LUT3_inst0"}]
set lut_lo_l0_f10 [get_cells -hier -filter {NAME =~ "*/c9_41_l0_f10/LUT3_inst1"}]
set_property LUTNM grp_l0_f10 $lut_hi_l0_f10
set_property LUTNM grp_l0_f10 $lut_lo_l0_f10


