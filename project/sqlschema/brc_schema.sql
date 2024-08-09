-- # Class: "DatasetCollection" Description: "Container class for defining a collection of datasets."
--     * Slot: id Description: 
-- # Class: "Dataset" Description: "A dataset containing metabolomics and proteomics data."
--     * Slot: uid Description: 
--     * Slot: id Description: Unique identifier for the dataset, assigned prior to inclusion in bioenergy.org.
--     * Slot: title Description: The title of the dataset.
--     * Slot: date Description: The date the dataset was created or published.
--     * Slot: brc Description: Bioenergy Research Center affiliation.
--     * Slot: repository Description: The repository where the dataset is stored.
--     * Slot: bibliographiccitation Description: Citation for the dataset.
--     * Slot: identifier Description: Unique identifier for the dataset.
--     * Slot: analysistype Description: The type of analysis performed on the dataset.
--     * Slot: description Description: A detailed description of the dataset.
--     * Slot: datasetname Description: "Name of a overall dataset to which this data entry belongs."
--     * Slot: DatasetCollection_id Description: Autocreated FK slot
--     * Slot: relateditem_id Description: Related publication or item.
-- # Class: "Individual" Description: "An individual involved in the dataset."
--     * Slot: id Description: 
--     * Slot: creatorname Description: Name of the creator.
--     * Slot: email Description: Email address of the creator.
--     * Slot: primarycontact Description: Indicates if the creator is the primary contact.
--     * Slot: affiliation Description: Affiliation of the creator.
--     * Slot: Dataset_uid Description: Autocreated FK slot
-- # Class: "Organization" Description: "An organization involved in the dataset."
--     * Slot: id Description: 
--     * Slot: organizationname Description: Name of the organization.
--     * Slot: wikidata_id Description: Wikidata identifier for the organization.
--     * Slot: ror_id Description: ROR identifier for the organization.
--     * Slot: parentorganization_id Description: Higher-level parent of this organization.
-- # Class: "Organism" Description: "An organism studied in the dataset."
--     * Slot: id Description: 
--     * Slot: scientificname Description: Scientific name of the organism.
--     * Slot: ncbitaxid Description: NCBI taxonomy ID for the organism.
-- # Class: "RelatedItem" Description: "A related publication or item, including cited publications."
--     * Slot: id Description: 
--     * Slot: title Description: Title of the related item.
--     * Slot: relateditemtype Description: Type of the related item, e.g., JournalArticle.
--     * Slot: relateditemidentifier Description: Identifier or URL for the related item.
-- # Class: "Dataset_species" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: species_id Description: Species information for the organism(s) studied.
-- # Class: "Dataset_keywords" Description: ""
--     * Slot: Dataset_uid Description: Autocreated FK slot
--     * Slot: keywords Description: Keywords associated with the dataset.

CREATE TABLE "DatasetCollection" (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "Organization" (
	id INTEGER NOT NULL, 
	organizationname TEXT, 
	wikidata_id TEXT, 
	ror_id TEXT, 
	parentorganization_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parentorganization_id) REFERENCES "Organization" (id)
);
CREATE TABLE "Organism" (
	id INTEGER NOT NULL, 
	scientificname TEXT, 
	ncbitaxid INTEGER, 
	PRIMARY KEY (id)
);
CREATE TABLE "RelatedItem" (
	id INTEGER NOT NULL, 
	title TEXT, 
	relateditemtype VARCHAR(14), 
	relateditemidentifier TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "Dataset" (
	uid INTEGER NOT NULL, 
	id TEXT, 
	title TEXT NOT NULL, 
	date DATE NOT NULL, 
	brc VARCHAR(5) NOT NULL, 
	repository VARCHAR(14), 
	bibliographiccitation TEXT NOT NULL, 
	identifier TEXT NOT NULL, 
	analysistype VARCHAR(21), 
	description TEXT, 
	datasetname TEXT, 
	"DatasetCollection_id" INTEGER, 
	relateditem_id INTEGER, 
	PRIMARY KEY (uid), 
	FOREIGN KEY("DatasetCollection_id") REFERENCES "DatasetCollection" (id), 
	FOREIGN KEY(relateditem_id) REFERENCES "RelatedItem" (id)
);
CREATE TABLE "Individual" (
	id INTEGER NOT NULL, 
	creatorname TEXT, 
	email TEXT, 
	primarycontact BOOLEAN, 
	affiliation TEXT, 
	"Dataset_uid" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);
CREATE TABLE "Dataset_species" (
	"Dataset_uid" INTEGER, 
	species_id INTEGER, 
	PRIMARY KEY ("Dataset_uid", species_id), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid), 
	FOREIGN KEY(species_id) REFERENCES "Organism" (id)
);
CREATE TABLE "Dataset_keywords" (
	"Dataset_uid" INTEGER, 
	keywords TEXT, 
	PRIMARY KEY ("Dataset_uid", keywords), 
	FOREIGN KEY("Dataset_uid") REFERENCES "Dataset" (uid)
);