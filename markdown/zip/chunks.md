### Chunk Size

We first try by computing our measures on raw file bytes. Then, 40% of files obtain less than 10% of error.
In a second time, we try we consider chunks of 2 bytes, meaning that we don't consider every byte, but every sequence of 2 bytes (like  16 bits integers).

[ 0x12, 0x34, 0x56, 0x78] $\rightarrow$ [ 0x1234, 0x5678]

After this change, 60% of files obtain less than 10% error.