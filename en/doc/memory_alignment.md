# Memory Alignment

```c
struct a {
    char c;
    int n;
};

struct b {
    int n;
    char c;
};
```

## Structure a : char + int

On many systems nowadays, a `char` is a single byte and and `int` is 4 bytes.  
Thus we expect both `a` and `b` structures to take 5 bytes each, but instead it's very likely for them to take 8 bytes each.  
[We can see it on 6 different compilers.](https://godbolt.org/z/MqKMY8Y93)

The reason is that data must be <ins>memory-aligned</ins>, meaning that their address must be a multiple of a power of 2, usually their size (in bytes).  
It explains why, usually, a 4 bytes-wide `int` is 4 bytes-aligned, so it will be stored at an address which is a multiple of 4, as 0, 4 or 8, but not 1, 3 nor 7.  

As stated at the beginning, a `char` is often 1 byte, and 4 bytes for an `int`.  
As a consequence, the first byte is the `char`, but the `int` cannot be stored right after the `char`, as it needs to be 4 bytes-aligned, so the compiler inserts 3 padding bytes between the `char` and the `int`, to shift the `int`.  

## Why 3 bytes ?

As it's pretty common, we assumed the `int` was 4 bytes-aligned.  
But a structure also has an alignment, and it depends of its fields.  
In general, a structure alignment is <ins>at least</ins> qual to the alignment of the field with the biggest alignment.  
In our case, the structure has an `int` field (4 bytes-aligned), and a `char` (1 byte-aligned),
so the structure is at least 4 bytes-aligned.  

Alignment can only be a power of 2, so if the structure alignment is bigger than 4, it would be 8, 16, 32... so multiples of 4 (thus being 8 bytes-aligned is 4 bytes-aligned, but the opposite is wrong).  
Thus we know our structure (and the `char`, as it's the first field) would be 4 bytes-aligned.  

## Structure b : int + char

About structure `b`, we have just established that the structure is 4 bytes-aligned, and because the `int` is the first field, it is also 4 bytes-aligned.  
Then comes th `char`, but due to its 1 byte-alignment, it can be stored at every address without any restriction.  

### But why does this structure still takes 8 bytes ?

```c
struct b b_array[2];
```
Here we have an array of multiple `b` structures, so if the structure takes 5 bytes, `b[0]`, everything is file, it starts at a 4 bytes-aligned address, and we just showed that both the `int` and `char` are correctly aligned.  
On the other hand, `b[1]` starts at an address which isn't 4 bytes-aligned (we added 5 to a multiple of 4, it gives a multiple of 4 + 1 byte), so the first field (`int`) isn't correctly aligned !  
We thus have 3 padding bytes again (5 bytes structure, 3 bytes are needed to be 8 bytes, a multiple of 4) so that the structure size is a multiple of 4, so if we have an array, we avoid alignment issues.  

## Why must data be aligned ?

To give an answer, we must closely look at how the CPU fetches data in the memory (RAM).  
When we have data consisting of multiple bytes (in C, often everything else than a boolean and a `char`), the CPU won't read byte-per-byte, but will instead read 4 or 8 bytes at once (the amount depends of the architecture) and store these bytes in a cache.  

When a program requests to access data, if it's already in the cache then everything is fine and the CPU simply gives it to the program. Otherwise, the CPU needs to read in the RAM.  
To read in the RAM, thee CPU uses several buses to deliver some information related to the requested memory operation.
Here are the 3 buses :
1. Command bus : the CPU gives it a value depending on whether it wants to write or read data
2. Address bus : the CPU gives it the address of the requested read/write
3. Data bus : the CPU reads it in case of a memory read / the CPU gives it the data to write in case of a memory write

To limit the complexity of buses circuitry, the CPU can only read/write at addresses multiple of 4 or 8 (again, depends on the architecture), that's why alignment exists.  

If data isn't correctly aligned :
- some CPUs don't support operations on unaligned addresses, they may crash
- CPUs who can handle these memory operations may be slower with unaligned addresses than with aligned addresses

To explain the 2nd point, let an 4 bytes `int` from address 1 to address 4, thus stored in the 2nd, 3rd, 4th and 5th bytes of the memory.  
The CPU asks the buses to read the 4 first bytes of the memory, so from the 1st to the 4th, but the 5th byte isn't read.  
To fetch that 5th byte, the CPU asks the bus to read again, but from the 5th byte to the 8th byte.  
Thus we needed 2 read operations to read a data which could have been read in a single read operation, if it was aligned, so that's why it might be slower.  

However, that performance loss it nowadays less important than it was before.  

## Sources :

https://en.wikipedia.org/wiki/Data_structure_alignment
https://stackoverflow.com/questions/4306186/structure-padding-and-packing
http://www.catb.org/esr/structure-packing/
https://stackoverflow.com/questions/41251388/why-processor-read-only-aligned-addresses
https://www.reddit.com/r/osdev/comments/wwnl54/why_are_cache_line_accesses_aligned/
https://lemire.me/blog/2012/05/31/data-alignment-for-speed-myth-or-reality/