# Auto generated from brc_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-08-15T13:19:04
# Schema: brc_schema
#
# id: https://w3id.org/brc/brc_schema
# description: This schema defines the structure for metabolomics and proteomics datasets, capturing essential metadata including investigators, affiliations, data citation, organism details, analysis type, and more. These are datasets generated by the Bioenergy Research Centers (BRCs), including CABBI, CBI, GLBRC, and JBEI.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Date, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, XSDDate

metamodel_version = "1.7.0"
version = "2024-08-15"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ERO = CurieNamespace('ERO', 'http://purl.obolibrary.org/obo/ERO_')
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
MI = CurieNamespace('MI', 'http://purl.obolibrary.org/obo/MI_')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
SIO = CurieNamespace('SIO', 'http://semanticscience.org/resource/SIO_')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
BALD = CurieNamespace('bald', 'https://www.opengis.net/def/binary-array-ld/')
BIBO = CurieNamespace('bibo', 'http://purl.org/ontology/bibo/')
BRC = CurieNamespace('brc', 'https://w3id.org/brc/')
CABBI = CurieNamespace('cabbi', 'https://cabbitools.igb.illinois.edu/brc/')
CBI = CurieNamespace('cbi', 'https://fair.ornl.gov/CBI/')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
EDAM = CurieNamespace('edam', 'http://edamontology.org/')
GLBRC = CurieNamespace('glbrc', 'https://fair-data.glbrc.org/')
JBEI = CurieNamespace('jbei', 'https://hello.bioenergy.org/JBEI/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OSLC = CurieNamespace('oslc', 'http://open-services.net/ns/core#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
ROR = CurieNamespace('ror', 'https://ror.org/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
VOID = CurieNamespace('void', 'http://rdfs.org/ns/void#')
WIKIDATA = CurieNamespace('wikidata', 'https://www.wikidata.org/wiki/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = BRC


# Types
class RorIdentifier(Uriorcurie):
    """ Identifier from Research Organization Registry. """
    type_class_uri = XSD["anyURI"]
    type_class_curie = "xsd:anyURI"
    type_name = "ror_identifier"
    type_model_uri = BRC.RorIdentifier


class WikidataIdentifier(Uriorcurie):
    """ Identifier from Wikidata open knowledge base. """
    type_class_uri = XSD["anyURI"]
    type_class_curie = "xsd:anyURI"
    type_name = "wikidata_identifier"
    type_model_uri = BRC.WikidataIdentifier


# Class references



@dataclass
class DatasetCollection(YAMLRoot):
    """
    Container class for defining a collection of datasets.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BRC["DatasetCollection"]
    class_class_curie: ClassVar[str] = "brc:DatasetCollection"
    class_name: ClassVar[str] = "DatasetCollection"
    class_model_uri: ClassVar[URIRef] = BRC.DatasetCollection

    datasets: Optional[Union[Union[dict, "Dataset"], List[Union[dict, "Dataset"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.datasets, list):
            self.datasets = [self.datasets] if self.datasets is not None else []
        self.datasets = [v if isinstance(v, Dataset) else Dataset(**as_dict(v)) for v in self.datasets]

        super().__post_init__(**kwargs)


@dataclass
class Dataset(YAMLRoot):
    """
    A dataset containing metabolomics and proteomics data.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Dataset"]
    class_class_curie: ClassVar[str] = "schema:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = BRC.Dataset

    title: str = None
    date: Union[str, XSDDate] = None
    creator: Union[Union[dict, "Individual"], List[Union[dict, "Individual"]]] = None
    brc: Union[str, "BRCEnum"] = None
    bibliographicCitation: str = None
    identifier: str = None
    id: Optional[Union[str, URIorCURIE]] = None
    repository: Optional[Union[str, "RepositoryEnum"]] = None
    species: Optional[Union[Union[dict, "Organism"], List[Union[dict, "Organism"]]]] = empty_list()
    analysisType: Optional[str] = "not specified"
    description: Optional[str] = None
    relatedItem: Optional[Union[dict, "RelatedItem"]] = None
    keywords: Optional[Union[str, List[str]]] = empty_list()
    datasetName: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.date):
            self.MissingRequiredField("date")
        if not isinstance(self.date, XSDDate):
            self.date = XSDDate(self.date)

        if self._is_empty(self.creator):
            self.MissingRequiredField("creator")
        if not isinstance(self.creator, list):
            self.creator = [self.creator] if self.creator is not None else []
        self.creator = [v if isinstance(v, Individual) else Individual(**as_dict(v)) for v in self.creator]

        if self._is_empty(self.brc):
            self.MissingRequiredField("brc")
        if not isinstance(self.brc, BRCEnum):
            self.brc = BRCEnum(self.brc)

        if self._is_empty(self.bibliographicCitation):
            self.MissingRequiredField("bibliographicCitation")
        if not isinstance(self.bibliographicCitation, str):
            self.bibliographicCitation = str(self.bibliographicCitation)

        if self._is_empty(self.identifier):
            self.MissingRequiredField("identifier")
        if not isinstance(self.identifier, str):
            self.identifier = str(self.identifier)

        if self.id is not None and not isinstance(self.id, URIorCURIE):
            self.id = URIorCURIE(self.id)

        if self.repository is not None and not isinstance(self.repository, RepositoryEnum):
            self.repository = RepositoryEnum(self.repository)

        if not isinstance(self.species, list):
            self.species = [self.species] if self.species is not None else []
        self.species = [v if isinstance(v, Organism) else Organism(**as_dict(v)) for v in self.species]

        if self.analysisType is not None and not isinstance(self.analysisType, str):
            self.analysisType = str(self.analysisType)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.relatedItem is not None and not isinstance(self.relatedItem, RelatedItem):
            self.relatedItem = RelatedItem(**as_dict(self.relatedItem))

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if self.datasetName is not None and not isinstance(self.datasetName, str):
            self.datasetName = str(self.datasetName)

        super().__post_init__(**kwargs)


@dataclass
class Individual(YAMLRoot):
    """
    An individual involved in the dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Person"]
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Individual"
    class_model_uri: ClassVar[URIRef] = BRC.Individual

    creatorName: Optional[str] = None
    email: Optional[str] = None
    primaryContact: Optional[Union[bool, Bool]] = None
    affiliation: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.creatorName is not None and not isinstance(self.creatorName, str):
            self.creatorName = str(self.creatorName)

        if self.email is not None and not isinstance(self.email, str):
            self.email = str(self.email)

        if self.primaryContact is not None and not isinstance(self.primaryContact, Bool):
            self.primaryContact = Bool(self.primaryContact)

        if self.affiliation is not None and not isinstance(self.affiliation, str):
            self.affiliation = str(self.affiliation)

        super().__post_init__(**kwargs)


@dataclass
class Organization(YAMLRoot):
    """
    An organization involved in the dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BRC["Organization"]
    class_class_curie: ClassVar[str] = "brc:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = BRC.Organization

    organizationName: Optional[str] = None
    parentOrganization: Optional[Union[dict, "Organization"]] = None
    wikidata_id: Optional[Union[str, WikidataIdentifier]] = None
    ror_id: Optional[Union[str, RorIdentifier]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.organizationName is not None and not isinstance(self.organizationName, str):
            self.organizationName = str(self.organizationName)

        if self.parentOrganization is not None and not isinstance(self.parentOrganization, Organization):
            self.parentOrganization = Organization(**as_dict(self.parentOrganization))

        if self.wikidata_id is not None and not isinstance(self.wikidata_id, WikidataIdentifier):
            self.wikidata_id = WikidataIdentifier(self.wikidata_id)

        if self.ror_id is not None and not isinstance(self.ror_id, RorIdentifier):
            self.ror_id = RorIdentifier(self.ror_id)

        super().__post_init__(**kwargs)


@dataclass
class Organism(YAMLRoot):
    """
    An organism studied in the dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BRC["Organism"]
    class_class_curie: ClassVar[str] = "brc:Organism"
    class_name: ClassVar[str] = "Organism"
    class_model_uri: ClassVar[URIRef] = BRC.Organism

    scientificName: Optional[str] = None
    NCBITaxID: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.scientificName is not None and not isinstance(self.scientificName, str):
            self.scientificName = str(self.scientificName)

        if self.NCBITaxID is not None and not isinstance(self.NCBITaxID, int):
            self.NCBITaxID = int(self.NCBITaxID)

        super().__post_init__(**kwargs)


@dataclass
class RelatedItem(YAMLRoot):
    """
    A related publication or item, including cited publications.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BRC["RelatedItem"]
    class_class_curie: ClassVar[str] = "brc:RelatedItem"
    class_name: ClassVar[str] = "RelatedItem"
    class_model_uri: ClassVar[URIRef] = BRC.RelatedItem

    title: Optional[str] = None
    relatedItemType: Optional[Union[str, "CitedItemType"]] = None
    relatedItemIdentifier: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.relatedItemType is not None and not isinstance(self.relatedItemType, CitedItemType):
            self.relatedItemType = CitedItemType(self.relatedItemType)

        if self.relatedItemIdentifier is not None and not isinstance(self.relatedItemIdentifier, URIorCURIE):
            self.relatedItemIdentifier = URIorCURIE(self.relatedItemIdentifier)

        super().__post_init__(**kwargs)


# Enumerations
class BRCEnum(EnumDefinitionImpl):
    """
    Bioenergy Research Center affiliation.
    """
    CABBI = PermissibleValue(
        text="CABBI",
        description="Center for Advanced Bioenergy and Bioproducts Innovation")
    CBI = PermissibleValue(
        text="CBI",
        description="Center for Bioenergy Innovation")
    GLBRC = PermissibleValue(
        text="GLBRC",
        description="Great Lakes Bioenergy Research Center")
    JBEI = PermissibleValue(
        text="JBEI",
        description="Joint BioEnergy Institute")

    _defn = EnumDefinition(
        name="BRCEnum",
        description="Bioenergy Research Center affiliation.",
    )

class AnalysisType(EnumDefinitionImpl):
    """
    Type of analysis performed on the dataset.
    """
    affinity_purification = PermissibleValue(
        text="affinity_purification",
        meaning=MI["0004"])
    cross_linking = PermissibleValue(
        text="cross_linking",
        meaning=OBI["0000800"])
    image_analysis = PermissibleValue(
        text="image_analysis",
        meaning=NCIT["C17606"])
    Ms_imaging = PermissibleValue(text="Ms_imaging")
    shotgun_proteomics = PermissibleValue(
        text="shotgun_proteomics",
        meaning=ERO["0001660"])
    srm_mrm = PermissibleValue(text="srm_mrm")
    swath_ms = PermissibleValue(
        text="swath_ms",
        meaning=OBI["0002958"])

    _defn = EnumDefinition(
        name="AnalysisType",
        description="Type of analysis performed on the dataset.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "Expression profiling",
            PermissibleValue(
                text="Expression profiling",
                meaning=NCIT["C19771"]))
        setattr(cls, "Genomic - SNP calling",
            PermissibleValue(
                text="Genomic - SNP calling",
                meaning=NCIT["C188690"]))
        setattr(cls, "Targeted Locus (Loci)",
            PermissibleValue(
                text="Targeted Locus (Loci)",
                meaning=OBI["0001899"]))

class CitedItemType(EnumDefinitionImpl):
    """
    Type of cited item, e.g., journal article.
    """
    JournalArticle = PermissibleValue(
        text="JournalArticle",
        description="Journal article",
        meaning=IAO["0000013"])
    Book = PermissibleValue(
        text="Book",
        description="Book",
        meaning=SCHEMA["book"])
    Dataset = PermissibleValue(
        text="Dataset",
        description="Dataset",
        meaning=SCHEMA["dataset"])
    Software = PermissibleValue(
        text="Software",
        description="Software",
        meaning=IAO["0000010"])
    Thesis = PermissibleValue(
        text="Thesis",
        description="Thesis",
        meaning=SCHEMA["thesis"])
    Patent = PermissibleValue(
        text="Patent",
        description="Patent",
        meaning=IAO["0000313"])
    Preprint = PermissibleValue(
        text="Preprint",
        description="Preprint",
        meaning=SCHEMA["Publication"])
    Presentation = PermissibleValue(
        text="Presentation",
        description="Presentation",
        meaning=SCHEMA["PresentationDigitalDocument"])
    Report = PermissibleValue(
        text="Report",
        description="Report",
        meaning=IAO["0000088"])
    Webpage = PermissibleValue(
        text="Webpage",
        description="Webpage",
        meaning=SCHEMA["WebPage"])

    _defn = EnumDefinition(
        name="CitedItemType",
        description="Type of cited item, e.g., journal article.",
    )

class RepositoryEnum(EnumDefinitionImpl):
    """
    Repository where the dataset is stored.
    """
    GEO = PermissibleValue(
        text="GEO",
        description="Gene Expression Omnibus")
    ICE = PermissibleValue(
        text="ICE",
        description="Inventory of Composable Elements")
    iProX = PermissibleValue(
        text="iProX",
        description="Integrated Proteome Resources")
    jPOST = PermissibleValue(
        text="jPOST",
        description="Japan ProteOme STandard Repository/Database")
    MassIVE = PermissibleValue(
        text="MassIVE",
        description="Mass Spectrometry Interactive Virtual Environment")
    OSTI = PermissibleValue(
        text="OSTI",
        description="Office of Scientific and Technical Information")
    PanoramaPublic = PermissibleValue(
        text="PanoramaPublic",
        description="Panorama Public")
    PedtideAtlas = PermissibleValue(
        text="PedtideAtlas",
        description="PeptideAtlas")
    PRIDE = PermissibleValue(
        text="PRIDE",
        description="PRoteomics IDEntifications database")

    _defn = EnumDefinition(
        name="RepositoryEnum",
        description="Repository where the dataset is stored.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "NCBI BioProject",
            PermissibleValue(
                text="NCBI BioProject",
                description="National Center for Biotechnology Information BioProject"))

# Slots
class slots:
    pass

slots.datasetCollection__datasets = Slot(uri=BRC.datasets, name="datasetCollection__datasets", curie=BRC.curie('datasets'),
                   model_uri=BRC.datasetCollection__datasets, domain=None, range=Optional[Union[Union[dict, Dataset], List[Union[dict, Dataset]]]])

slots.dataset__id = Slot(uri=SCHEMA.identifier, name="dataset__id", curie=SCHEMA.curie('identifier'),
                   model_uri=BRC.dataset__id, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.dataset__title = Slot(uri=DCTERMS.title, name="dataset__title", curie=DCTERMS.curie('title'),
                   model_uri=BRC.dataset__title, domain=None, range=str)

slots.dataset__date = Slot(uri=DCTERMS.date, name="dataset__date", curie=DCTERMS.curie('date'),
                   model_uri=BRC.dataset__date, domain=None, range=Union[str, XSDDate])

slots.dataset__creator = Slot(uri=DCTERMS.creator, name="dataset__creator", curie=DCTERMS.curie('creator'),
                   model_uri=BRC.dataset__creator, domain=None, range=Union[Union[dict, Individual], List[Union[dict, Individual]]])

slots.dataset__brc = Slot(uri=PROV.wasAttributedTo, name="dataset__brc", curie=PROV.curie('wasAttributedTo'),
                   model_uri=BRC.dataset__brc, domain=None, range=Union[str, "BRCEnum"])

slots.dataset__repository = Slot(uri=BRC.repository, name="dataset__repository", curie=BRC.curie('repository'),
                   model_uri=BRC.dataset__repository, domain=None, range=Optional[Union[str, "RepositoryEnum"]])

slots.dataset__bibliographicCitation = Slot(uri=DCTERMS.bibliographicCitation, name="dataset__bibliographicCitation", curie=DCTERMS.curie('bibliographicCitation'),
                   model_uri=BRC.dataset__bibliographicCitation, domain=None, range=str)

slots.dataset__identifier = Slot(uri=SCHEMA.identifier, name="dataset__identifier", curie=SCHEMA.curie('identifier'),
                   model_uri=BRC.dataset__identifier, domain=None, range=str)

slots.dataset__species = Slot(uri=BRC.species, name="dataset__species", curie=BRC.curie('species'),
                   model_uri=BRC.dataset__species, domain=None, range=Optional[Union[Union[dict, Organism], List[Union[dict, Organism]]]])

slots.dataset__analysisType = Slot(uri=BRC.analysisType, name="dataset__analysisType", curie=BRC.curie('analysisType'),
                   model_uri=BRC.dataset__analysisType, domain=None, range=Optional[str])

slots.dataset__description = Slot(uri=DCTERMS.description, name="dataset__description", curie=DCTERMS.curie('description'),
                   model_uri=BRC.dataset__description, domain=None, range=Optional[str])

slots.dataset__relatedItem = Slot(uri=BRC.relatedItem, name="dataset__relatedItem", curie=BRC.curie('relatedItem'),
                   model_uri=BRC.dataset__relatedItem, domain=None, range=Optional[Union[dict, RelatedItem]])

slots.dataset__keywords = Slot(uri=DCAT.keyword, name="dataset__keywords", curie=DCAT.curie('keyword'),
                   model_uri=BRC.dataset__keywords, domain=None, range=Optional[Union[str, List[str]]])

slots.dataset__datasetName = Slot(uri=BRC.datasetName, name="dataset__datasetName", curie=BRC.curie('datasetName'),
                   model_uri=BRC.dataset__datasetName, domain=None, range=Optional[str])

slots.individual__creatorName = Slot(uri=SCHEMA.name, name="individual__creatorName", curie=SCHEMA.curie('name'),
                   model_uri=BRC.individual__creatorName, domain=None, range=Optional[str])

slots.individual__email = Slot(uri=SCHEMA.email, name="individual__email", curie=SCHEMA.curie('email'),
                   model_uri=BRC.individual__email, domain=None, range=Optional[str])

slots.individual__primaryContact = Slot(uri=BRC.primaryContact, name="individual__primaryContact", curie=BRC.curie('primaryContact'),
                   model_uri=BRC.individual__primaryContact, domain=None, range=Optional[Union[bool, Bool]])

slots.individual__affiliation = Slot(uri=BRC.affiliation, name="individual__affiliation", curie=BRC.curie('affiliation'),
                   model_uri=BRC.individual__affiliation, domain=None, range=Optional[str])

slots.organization__organizationName = Slot(uri=SCHEMA.name, name="organization__organizationName", curie=SCHEMA.curie('name'),
                   model_uri=BRC.organization__organizationName, domain=None, range=Optional[str])

slots.organization__parentOrganization = Slot(uri=BRC.parentOrganization, name="organization__parentOrganization", curie=BRC.curie('parentOrganization'),
                   model_uri=BRC.organization__parentOrganization, domain=None, range=Optional[Union[dict, Organization]])

slots.organization__wikidata_id = Slot(uri=BRC.wikidata_id, name="organization__wikidata_id", curie=BRC.curie('wikidata_id'),
                   model_uri=BRC.organization__wikidata_id, domain=None, range=Optional[Union[str, WikidataIdentifier]])

slots.organization__ror_id = Slot(uri=BRC.ror_id, name="organization__ror_id", curie=BRC.curie('ror_id'),
                   model_uri=BRC.organization__ror_id, domain=None, range=Optional[Union[str, RorIdentifier]])

slots.organism__scientificName = Slot(uri=BRC.scientificName, name="organism__scientificName", curie=BRC.curie('scientificName'),
                   model_uri=BRC.organism__scientificName, domain=None, range=Optional[str])

slots.organism__NCBITaxID = Slot(uri=BRC.NCBITaxID, name="organism__NCBITaxID", curie=BRC.curie('NCBITaxID'),
                   model_uri=BRC.organism__NCBITaxID, domain=None, range=Optional[int])

slots.relatedItem__title = Slot(uri=DCTERMS.title, name="relatedItem__title", curie=DCTERMS.curie('title'),
                   model_uri=BRC.relatedItem__title, domain=None, range=Optional[str])

slots.relatedItem__relatedItemType = Slot(uri=BRC.relatedItemType, name="relatedItem__relatedItemType", curie=BRC.curie('relatedItemType'),
                   model_uri=BRC.relatedItem__relatedItemType, domain=None, range=Optional[Union[str, "CitedItemType"]])

slots.relatedItem__relatedItemIdentifier = Slot(uri=BRC.relatedItemIdentifier, name="relatedItem__relatedItemIdentifier", curie=BRC.curie('relatedItemIdentifier'),
                   model_uri=BRC.relatedItem__relatedItemIdentifier, domain=None, range=Optional[Union[str, URIorCURIE]])