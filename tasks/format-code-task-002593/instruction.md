Should not be able to close asset using clawback
An asset clawback transaction with a `closeRemainderTo` payFlag should throw an error (which is the behaviour of algorand network). Clawbacks cannot close assets from an address - only the actual owner can.
