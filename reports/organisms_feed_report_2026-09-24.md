# Organism feed report, 2026-09-24

Produced by `scripts/update_organisms_from_feeds.py` while generating the
`feed_organisms` block of `src/brc_schema/transform/organisms.yaml`.

Sources: the four BRC feeds imported by bioenergy.org
(JBEI, CABBI, CBI, GLBRC; 3,052 datasets, 816 distinct NCBI taxids).
Every taxid was checked against NCBI Taxonomy E-utilities.

Items below were left out of the vocabulary or changed. Several look like
errors in the feeds themselves (e.g. taxid 1753, labelled switchgrass, is
*Propioniferax innocua*; taxid 1960, labelled *Issatchenkia orientalis*, is
*Streptomyces vinaceus*) and are worth reporting to the BRC that owns them.

## feed name disagrees with NCBI name (not kept) (31)
- 470 feed 'Acinetobacter baumanii' vs NCBI 'Acinetobacter baumannii' [glbrc]
- 971 feed 'Selenomonas ruminantium' vs NCBI 'Pseudoselenomonas ruminantium' [jbei]
- 1140 feed 'Synechococcus elongatus PCC 7942' vs NCBI 'Synechococcus elongatus PCC 7942 = FACHB-805' [jbei]
- 1148 feed 'Synechocystis sp. strain PCC 6803' vs NCBI 'Synechocystis sp. PCC 6803' [jbei]
- 1409 feed 'Bacillus sp.' vs NCBI 'Bacillus sp. (in: firmicutes)' [jbei]
- 1753 feed 'switchgrass (Panicum virgatum L.)' vs NCBI 'Propioniferax innocua' [glbrc]
- 1753 feed 'Teucrium chamaedrys' vs NCBI 'Propioniferax innocua' [glbrc]
- 1960 feed 'Issatchenkia orientalis' vs NCBI 'Streptomyces vinaceus' [cabbi]
- 3690 feed 'hybrid Poplar (Populus × euramericana)' vs NCBI 'Populus x canadensis' [glbrc]
- 4097 feed 'Tobacco (Nicotina tabacum)' vs NCBI 'Nicotiana tabacum' [glbrc]
- 4558 feed 'Sorghum biocolor BTx623' vs NCBI 'Sorghum bicolor' [glbrc]
- 4927 feed 'Wickerhamomyces anomalus' vs NCBI 'Hansenula anomala' [jbei]
- 5480 feed 'Candida parapsilosis' vs NCBI 'Lodderomyces parapsilosis' [jbei]
- 15819 feed 'Saccharum hybrid' vs NCBI 'Saccharum sp.' [jbei]
- 32044 feed 'Pseudomonas mevalonii' vs NCBI "Pseudomonas sp. 'mevalonii'" [jbei]
- 39947 feed 'Oryza sativa ssp. japonica' vs NCBI 'Oryza sativa Japonica Group' [jbei]
- 45543 feed 'Candida diddensiae' vs NCBI 'Yamadazyma diddensiae' [jbei]
- 54092 feed 'Lipomyces tetrasporous' vs NCBI 'Lipomyces tetrasporus' [cabbi]
- 78579 feed 'Myceliopthora thermophila' vs NCBI 'Thermothelomyces thermophilus' [jbei]
- 104623 feed 'Serratia sp. ATCC 39006' vs NCBI 'Prodigiosinella confusarubida' [jbei]
- 228933 feed 'Populus alba x grandidentata' vs NCBI 'Populus alba x Populus grandidentata' [jbei]
- 264203 feed 'Zymomonas mobilis' vs NCBI 'Zymomonas mobilis subsp. mobilis ZM4 = ATCC 31821' [glbrc]
- 279238 feed 'Novosphingobium aromaticivorans DSM12444' vs NCBI 'Novosphingobium aromaticivorans DSM 12444' [glbrc]
- 310910 feed 'Linnemania elongata' vs NCBI 'Linnemannia elongata' [glbrc]
- 324833 feed 'Streptomyces lasaliensis' vs NCBI 'Streptomyces lasalocidi' [jbei]
- 1906605 feed 'Candidatus Reconcilibacillus cellulovorans' vs NCBI 'Candidatus Reconcilbacillus cellulovorans' [jbei]
- 2268192 feed 'uncultured Chlorobi bacterium' vs NCBI 'Chlorobiota bacterium' [jbei]
- 2720874 feed 'Aspergillus' vs NCBI 'Aspergillus subgen. Aspergillus' [jbei]
- 2872729 feed 'Rhodotorula toruloides' vs NCBI 'Rhodotorula cf. toruloides' [cabbi]
- 3044176 feed 'Saccharomycopsis praedatoria sp. nov.' vs NCBI 'Saccharomycopsis sp. KB-2023a' [glbrc]
- 3112614 feed 'Pichia sp. KDB-2024a' vs NCBI 'Pichia senei' [glbrc]

## merged taxid (entry uses current id) (2)
- 1842 -> 52699 'Aeromicrobium fastidiosum' [cabbi]
- 1940621 -> 2093743 'Pseudomonas alloputida' [jbei]

## taxid not found in NCBI (2)
- 0 'Aconitum carmichaelii' [glbrc]
- 24741 'Saturnispora mendoncae' [glbrc]
