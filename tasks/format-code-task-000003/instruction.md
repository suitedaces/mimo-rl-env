## SHL opcode not implemented

I'm running some Solidity-compiled bytecode through smol-evm and it bails out partway with an `UnknownOpcode` error. Disassembling the bytecode I can see it's hitting a `SHL` (shift left) — and looking through `opcodes.py` I notice `SHR` is implemented but `SHL` isn't there at all.

Could we add it? The Solidity compiler emits `SHL` pretty routinely (bit packing, struct layout, masking, etc.), so right now smol-evm can't really get through most real contract bytecode. Behavior should match what the yellow paper / EVM spec defines for `SHL`.
