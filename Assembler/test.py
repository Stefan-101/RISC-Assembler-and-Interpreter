def addr_to_bits(addr):
    return [int(bit) for bit in bin(addr)[2:].zfill(16)]

print(addr_to_bits(1))