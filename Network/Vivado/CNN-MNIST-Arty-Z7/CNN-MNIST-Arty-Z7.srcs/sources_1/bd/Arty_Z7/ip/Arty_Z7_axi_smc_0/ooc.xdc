# aclk {FREQ_HZ 100000000 CLK_DOMAIN Arty_Z7_processing_system7_0_1_FCLK_CLK0 PHASE 0.000}
# Clock Domain: Arty_Z7_processing_system7_0_1_FCLK_CLK0
create_clock -name aclk -period 10.000 [get_ports aclk]
# Generated clocks