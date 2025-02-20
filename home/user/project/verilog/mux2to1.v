module mux2to1 (
    input wire a,       // First input
    input wire b,       // Second input
    input wire sel,     // Select signal
    output wire y       // Output
);

    assign y = sel ? b : a;

endmodule