`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 30.10.2024 17:13:46
// Design Name: 
// Module Name: neuron_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module neuron_tb();

parameter numWeight=784,dataWidth=8,layerNum=1,sigmoidSize=10,weightIntWidth=4,actType="sigmoid";
reg           clk;
reg           rst;
reg [dataWidth-1:0] neuron_in;
reg           neuron_in_valid;
reg           weightValid;
reg           biasValid;
reg [31:0]    weightValue;
reg [31:0]    biasValue;
reg [31:0]    config_layer_num;
reg [31:0]    config_neuron_num;
wire [2*dataWidth-1:0] sum;
wire [dataWidth-1:0]    neuron_out;
wire      out_valid;   

neuron #(.numWeight(numWeight),.layerNo(layerNum),.neuronNo(0),
         .dataWidth(dataWidth),.sigmoidSize(sigmoidSize),.weightIntWidth(weightIntWidth),
         .actType(actType),.weightFile("w_1_0.mif"),.biasFile("b_1_0.mif"))
    test_neuron 
    (
        .clk(clk),
        .rst(rst),
        .myinput(neuron_in),
        .myinputValid(neuron_in_valid),
        .weightValid(weightValid),
        .biasValid(biasValid),
        .weightValue(weightValue),
        .biasValue(biasValue),
        .config_layer_num(config_layer_num),
        .config_neuron_num(config_neuron_num),
        .sum_o(sum),
        .out(neuron_out[0*dataWidth+:dataWidth]),
        .outvalid(out_valid)
    );

initial begin
    clk = 0;
    forever 
         #10 clk = ~clk; // Clock: 100MHz
end

initial rst = 0;
initial neuron_in_valid = 0;
initial neuron_in = 0;
initial weightValid = 0;
initial weightValue = 0;
initial biasValid = 0;
initial biasValue = 0;
initial config_layer_num = 0;
initial config_neuron_num = 0;

int file;
string line;
int r;
logic[15:0] data;
int i = 0;

initial 
begin
    file = $fopen("test_data.txt", "r");
    if (file == 0) 
    begin
        $display("Failed to open file.");
        $finish;
    end
    else
    begin
        rst = 1;
        #20;
        rst = 0;
        #20;
        neuron_in_valid = 1;
    
        while (!$feof(file)) 
        begin
        line = "";
          r = $fgets(line, file);
          // Parse line if it was read successfully
          if (r != 0) 
          begin
            r = $sscanf(line, "%b", data);
            neuron_in = data;
             #20;
             i = i + 1;
             if (i == 784)
                $display("Final Sum: %x", sum);
            
            //$display("Applied Vector: data=%b", data);
          end
        end
        neuron_in_valid = 0;
        #100;
        if (out_valid == 1)
            $display("Neuron Out after activation: %x",neuron_out);
        else    
            $error ("Operation did not finish in required time");
        $finish;
    end
end
        
endmodule
