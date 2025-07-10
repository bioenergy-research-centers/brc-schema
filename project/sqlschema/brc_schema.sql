-- # Class: "DatasetCollection" Description: "Container class for defining a collection of datasets."
--     * Slot: id Description: 
--     * Slot: schema_version Description: Version of the schema used for the collection.
-- # Class: "Dataset" Description: "A dataset containing metabolomics and proteomics data."
--     * Slot: uid Description: 
--     * Slot: id Description: Unique identifier for the dataset, assigned prior to inclusion in bioenergy.org.
--     * Slot: active Description: Indicates whether the dataset is active or inactive. This is a boolean field - true indicates active, false indicates inactive.
--     * Slot: alert Description: Indicates whether availability of the dataset has encountered some inconsistency. This is a boolean field - true indicates alert, false indicates no alert. For example, if we have a Dataset object but the Dataset is missing from its source feed, this should be set to true.
--     * Slot: title Description: The title of the dataset.
--     * Slot: date Description: The date the dataset was created or published.
--     * Slot: brc Description: The primary Bioenergy Research Center affiliation. This is a single BRC name.
--     * Slot: repository Description: The repository where the dataset is stored.
--     * Slot: bibliographicCitation Description: Citation for the dataset.
--     * Slot: identifier Description: Unique identifier for the dataset.
--     * Slot: analysisType Description: The type of analysis performed on the dataset.
--     * Slot: datasetType Description: High-level type of the main content of the dataset.
--     * Slot: description Description: A detailed description of the dataset.
--     * Slot: datasetName Description: "Name of a overall dataset to which this data entry belongs."
--     * Slot: dataset_url Description: URL for the dataset landing page.
--     * Slot: DatasetCollection_id Description: Autocreated FK slot
-- # Class: "Individual" Description: "An individual involved in the dataset."
--     * Slot: id Description: 
--     * Slot: name Description: Name of the individual.
--     * Slot: email Description: Email address of the individual.
--     * Slot: primaryContact Description: Indicates if the individual is a primary contact.
--     * Slot: affiliation Description: Affiliation of the individual.
--     * Slot: orcid Description: ORCID for the individual. This should include the full URI with prefix, e.g., https://orcid.org/0000-0002-1825-0097.
--     * Slot: Dataset_uid Description: Autocreated FK slot
-- # Class: "Contributor" Description: "An individual who contributed to the dataset in some manner, not necessarily as an author."
--     * Slot: id Description: 
--     * Slot: contributorType Description: The contribution type.
--     * Slot: name Description: Name of the individual.
--     * Slot: email Description: Email address of the individual.
--     * Slot: primaryContact Description: Indicates if the individual is a primary contact.
--     * Slot: affiliation Description: Affiliation of the individual.
--     * Slot: orcid Description: ORCID for the individual. This should include the full URI with prefix, e.g., https://orcid.org/0000-0002-1825-0097.
--     * Slot: Dataset_uid Description: Autocreated FK slot
-- # Class: "Funding" Description: "Funding source for the dataset. Each item corresponds to a single award or grant."
--     * Slot: id Description: 
--     * Slot: awardNumber Description: Award number from the funding entity.
--     * Slot: awardTitle Description: Title of the award.
--     * Slot: awardURI Description: URI for the award. This may be a DOI. Include prefix.
--     * Slot: fundingOrganization_id Description: Details of the funding entity.
-- # Class: "Organization" Description: "An organization involved in the dataset."
--     * Slot: id Description: 
--     * Slot: organizationName Description: Name of the organization.
--     * Slot: wikidata_id Description: Wikidata identifier for the organization.
--     * Slot: ror_id Description: ROR identifier for the organization.
--     * Slot: parentOrganization_id Description: Higher-level parent of this organization.
-- # Class: "Organism" Description: "An organism studied in the dataset."
--     * Slot: id Description: 
--     * Slot: scientificName Description: Scientific name of the organism.
--     * Slot: NCBITaxID Description: NCBI taxonomy ID for the organism.
-- # Class: "Plasmid" Description: "Description of plasmid or other molecular vector features."
--     * Slot: uid Description: 
--     * Slot: id Description: Unique identifier for the plasmid. This must be unique within the dataset.
--     * Slot: description Description: Description of the plasmid, including any relevant features not captured in other fields.
--     * Slot: backbone Description: Name of the backbone of the plasmid, e.g., pUC19.
--     * Slot: ori Description: Origin of replication for the plasmid, e.g., ColE1.
--     * Slot: host_id Description: Host organism for the plasmid, e.g., E. coli. Includes both the scientific name and NCBI Taxonomy ID.
-- # Class: "RelatedItem" Description: "A related publication or item, including cited publications."
--     * Slot: id Description: 
--     * Slot: title Description: Title of the related item.
--     * Slot: relatedItemType Description: Type of the related item, e.g., JournalArticle.
--     * Slot: relatedItemIdentifier Description: Identifier or URL for the related item.
-- # Class: "Dataset_additional_brcs" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: additional_brcs Description: Additional Bioenergy Research Center affiliations. This is a list of one or more additional BRC names, for instances in which the dataset is associated with multiple centers.
-- # Class: "Dataset_has_related_ids" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: has_related_ids Description: "Related identifiers for the dataset. These should be identifiers to records in other repositories, and these records may be the same data or components of the dataset."
-- # Class: "Dataset_species" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: species_id Description: Species information for the organism(s) studied.
-- # Class: "Dataset_plasmid_features" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: plasmid_features_uid Description: Description of plasmid features, if applicable. This is a multivalued field.
-- # Class: "Dataset_relatedItem" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: relatedItem_id Description: Related publications or items.
-- # Class: "Dataset_keywords" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: keywords Description: Keywords associated with the dataset.
-- # Class: "Dataset_funding" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: funding_id Description: Funding source(s) for the dataset.
-- # Class: "Plasmid_promoters" Description: ""
--     * Slot: Plasmid_uid Description: Autocreated FK slot
--     * Slot: promoters Description: Promoters for the plasmid, e.g., T7.
-- # Class: "Plasmid_replicates_in" Description: ""
--     * Slot: Plasmid_uid Description: Autocreated FK slot
--     * Slot: replicates_in_id Description: Organism(s) in which the plasmid replicates. Includes both the scientific name and NCBI Taxonomy ID.
-- # Class: "Plasmid_selection_markers" Description: ""
--     * Slot: Plasmid_uid Description: Autocreated FK slot
--     * Slot: selection_markers Description: Selection markers for the plasmid, e.g, kan.

CREATE TABLE "DatasetCollection" (
	id INTEGER NOT NULL, 
	schema_version TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Organization" (
	id INTEGER NOT NULL, 
	"organizationName" TEXT, 
	wikidata_id TEXT, 
	ror_id TEXT, 
	"parentOrganization_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("parentOrganization_id") REFERENCES "Organization" (id)
);
CREATE TABLE "Organism" (
	id INTEGER NOT NULL, 
	"scientificName" TEXT, 
	"NCBITaxID" INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE "RelatedItem" (
	id INTEGER NOT NULL, 
	title TEXT, 
	"relatedItemType" VARCHAR(14), 
	"relatedItemIdentifier" TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Dataset" (
	uid INTEGER NOT NULL, 
	id TEXT, 
	active BOOLEAN, 
	alert BOOLEAN, 
	title TEXT NOT NULL, 
	date DATE NOT NULL, 
	brc VARCHAR(5) NOT NULL, 
	repository VARCHAR(42), 
	"bibliographicCitation" TEXT, 
	identifier TEXT NOT NULL, 
	"analysisType" TEXT, 
	"datasetType" VARCHAR(2), 
	description TEXT, 
	"datasetName" TEXT, 
	dataset_url TEXT, 
	"DatasetCollection_id" INTEGER, 
	PRIMARY KEY (uid), 
	FOREIGN KEY("DatasetCollection_id") REFERENCES "DatasetCollection" (id)
);
CREATE TABLE "Funding" (
	id INTEGER NOT NULL, 
	"awardNumber" TEXT, 
	"awardTitle" TEXT, 
	"awardURI" TEXT, 
	"fundingOrganization_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("fundingOrganization_id") REFERENCES "Organization" (id)
);
CREATE TABLE "Plasmid" (
	uid INTEGER NOT NULL, 
	id TEXT, 
	description TEXT, 
	backbone TEXT, 
	ori TEXT, 
	host_id INTEGER, 
	PRIMARY KEY (uid), 
	FOREIGN KEY(host_id) REFERENCES "Organism" (id)
);
CREATE TABLE "Individual" (
	id INTEGER NOT NULL, 
	name TEXT, 
	email TEXT, 
	"primaryContact" BOOLEAN, 
	affiliation TEXT, 
	orcid TEXT, 
	"Dataset_uid" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);
CREATE TABLE "Contributor" (
	id INTEGER NOT NULL, 
	"contributorType" VARCHAR(21), 
	name TEXT, 
	email TEXT, 
	"primaryContact" BOOLEAN, 
	affiliation TEXT, 
	orcid TEXT, 
	"Dataset_uid" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);
CREATE TABLE "Dataset_additional_brcs" (
	"Dataset_uid" INTEGER, 
	additional_brcs VARCHAR(5), 
	PRIMARY KEY ("Dataset_uid", additional_brcs), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);
CREATE TABLE "Dataset_has_related_ids" (
	"Dataset_uid" INTEGER, 
	has_related_ids TEXT, 
	PRIMARY KEY ("Dataset_uid", has_related_ids), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);
CREATE TABLE "Dataset_species" (
	"Dataset_uid" INTEGER, 
	species_id INTEGER, 
	PRIMARY KEY ("Dataset_uid", species_id), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid), 
	FOREIGN KEY(species_id) REFERENCES "Organism" (id)
);
CREATE TABLE "Dataset_plasmid_features" (
	"Dataset_uid" INTEGER, 
	plasmid_features_uid INTEGER, 
	PRIMARY KEY ("Dataset_uid", plasmid_features_uid), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid), 
	FOREIGN KEY(plasmid_features_uid) REFERENCES "Plasmid" (uid)
);
CREATE TABLE "Dataset_relatedItem" (
	"Dataset_uid" INTEGER, 
	"relatedItem_id" INTEGER, 
	PRIMARY KEY ("Dataset_uid", "relatedItem_id"), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid), 
	FOREIGN KEY("relatedItem_id") REFERENCES "RelatedItem" (id)
);
CREATE TABLE "Dataset_keywords" (
	"Dataset_uid" INTEGER, 
	keywords TEXT, 
	PRIMARY KEY ("Dataset_uid", keywords), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);
CREATE TABLE "Dataset_funding" (
	"Dataset_uid" INTEGER, 
	funding_id INTEGER, 
	PRIMARY KEY ("Dataset_uid", funding_id), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid), 
	FOREIGN KEY(funding_id) REFERENCES "Funding" (id)
);
CREATE TABLE "Plasmid_promoters" (
	"Plasmid_uid" INTEGER, 
	promoters TEXT, 
	PRIMARY KEY ("Plasmid_uid", promoters), 
	FOREIGN KEY("Plasmid_uid") REFERENCES "Plasmid" (uid)
);
CREATE TABLE "Plasmid_replicates_in" (
	"Plasmid_uid" INTEGER, 
	replicates_in_id INTEGER, 
	PRIMARY KEY ("Plasmid_uid", replicates_in_id), 
	FOREIGN KEY("Plasmid_uid") REFERENCES "Plasmid" (uid), 
	FOREIGN KEY(replicates_in_id) REFERENCES "Organism" (id)
);
CREATE TABLE "Plasmid_selection_markers" (
	"Plasmid_uid" INTEGER, 
	selection_markers TEXT, 
	PRIMARY KEY ("Plasmid_uid", selection_markers), 
	FOREIGN KEY("Plasmid_uid") REFERENCES "Plasmid" (uid)
);