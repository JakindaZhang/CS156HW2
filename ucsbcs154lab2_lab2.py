import pyrtl

### DECLARE WIRE VECTORS, INPUT, MEMBLOCK ###
instr = pyrtl.Input(32, 'instr')
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=5, name='rf')
alu_out = pyrtl.WireVector(32, 'alu_out')

### DECODE INSTRUCTION AND RETRIEVE RF DATA ###
op = instr[26:32]
rs = instr[21:26]
rt = instr[16:21]
rd = instr[11:16]
sh = instr[6:11]
func = instr[0:6]
rs_val = rf[rs]
rt_val = rf[rt]
is_rtype = op == pyrtl.Const(0, 6)

### ADD ALU LOGIC HERE ###
slt_bit = rs_val < rt_val

slt_val = pyrtl.concat(pyrtl.Const(0, 31), slt_bit)

add_val = rs_val + rt_val
sub_val = rs_val - rt_val
and_val = rs_val & rt_val
or_val  = rs_val | rt_val
xor_val = rs_val ^ rt_val
sll_val = pyrtl.shift_left_logical(rt_val, sh)
srl_val = pyrtl.shift_right_logical(rt_val, sh)
sra_val = pyrtl.shift_right_arithmetic(rt_val, sh)

result = pyrtl.Const(0, 32)
result = pyrtl.select(func == pyrtl.Const(0x20, 6), add_val, result)  # ADD
result = pyrtl.select(func == pyrtl.Const(0x22, 6), sub_val, result)  # SUB
result = pyrtl.select(func == pyrtl.Const(0x24, 6), and_val, result)  # AND
result = pyrtl.select(func == pyrtl.Const(0x25, 6), or_val,  result)  # OR
result = pyrtl.select(func == pyrtl.Const(0x26, 6), xor_val, result)  # XOR
result = pyrtl.select(func == pyrtl.Const(0x2A, 6), slt_val, result)  # SLT
result = pyrtl.select(func == pyrtl.Const(0x00, 6), sll_val, result)  # SLL
result = pyrtl.select(func == pyrtl.Const(0x02, 6), srl_val, result)  # SRL
result = pyrtl.select(func == pyrtl.Const(0x03, 6), sra_val, result)  # SRA
alu_out <<= pyrtl.select(is_rtype, result, pyrtl.Const(0, 32))
### WRITEBACK ###
regwrite = is_rtype & (rd != 0)
rf[rd] <<= pyrtl.MemBlock.EnabledWrite(alu_out, regwrite)