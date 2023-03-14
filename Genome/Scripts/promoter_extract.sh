# Convert GFF3 file to BED format
gffread < all.gff3 > all.bed

# Extract gene regions from BED file
grep "gene" all.bed > all.gene.bed

# Index the reference genome file
samtools faidx -i all.chrs.con

# Generate a file with chromosome sizes for use with BEDTools
cat all.chrs.con.fai | awk '{print $1"\t"$2}' > all.chrs.con.sizes

# Get sequences 1kb upstream of gene start sites and write them to a FASTA file
bedtools flank -i all.gene.bed -g all.chrs.con.sizes -l 1000 -r 0 -s > all.chrs.con.1kb.promoter.bed
bedtools getfasta -fi all.chrs.con -bed all.chrs.con.1kb.promoter.bed -nameOnly -fo promoters.fa

