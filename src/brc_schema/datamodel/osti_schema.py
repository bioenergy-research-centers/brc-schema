from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "2.6.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'osti',
     'default_range': 'string',
     'description': 'This schema is a LinkML representation of the OSTI Submission '
                    'Metadata schema, as described here: '
                    'https://www.osti.gov/elink2api/ and here: '
                    'https://www.osti.gov/elink2api/record-schema OSTI uses the '
                    'E-Link API infrastructure. This schema corresponds to the '
                    'E-Link 2.0 API (2.6.0).',
     'id': 'https://w3id.org/brc/osti_schema',
     'imports': ['linkml:types'],
     'name': 'osti_schema',
     'prefixes': {'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'osti': {'prefix_prefix': 'osti',
                           'prefix_reference': 'https://www.osti.gov/biblio/'}},
     'source_file': 'src/brc_schema/schema/osti_schema.yaml',
     'title': 'LinkML schema of OSTI Submission Metadata'} )

class ContributorType(str, Enum):
    """
    Describes the type of contribution to the work.  Required for Persons or Organizations of CONTRIBUTING type.
    """
    Chair = "Chair"
    DataCollector = "DataCollector"
    """
    Person/institution responsible for finding or gathering data under the guidelines of the author(s) or Principal Investigator.
    """
    DataCurator = "DataCurator"
    """
    Person tasked with reviewing, enhancing, cleaning, or standardizing metadata and the associated data submitted.
    """
    DataManager = "DataManager"
    """
    Person (or organization with a staff of data managers, such as a data centre) responsible for maintaining the finished resource.
    """
    Distributor = "Distributor"
    """
    Institution tasked with responsibility to generate/disseminate copies of the resource in either electronic or print form.
    """
    Editor = "Editor"
    """
    A person who oversees the details related to the publication format of the resource.
    """
    HostingInstitution = "HostingInstitution"
    """
    The organization allowing the resource to be available on the internet.
    """
    Producer = "Producer"
    """
    Typically a person or organization responsible for the artistry and form of a media product.
    """
    ProjectLeader = "ProjectLeader"
    """
    Person officially designated as head of project team instrumental in the work necessary to development of the resource.
    """
    ProjectManager = "ProjectManager"
    """
    Person officially designated as manager of a project. Project may consist of one or many project teams and sub-teams.
    """
    ProjectMember = "ProjectMember"
    """
    Person on the membership list of a designated project/project team.
    """
    RegistrationAgency = "RegistrationAgency"
    """
    Institution officially appointed by a Registration Authority to handle specific tasks within a defined area of responsibility.
    """
    RegistrationAuthority = "RegistrationAuthority"
    """
    A standards-setting body from which Registration Agencies obtain official recognition and guidance.
    """
    RelatedPerson = "RelatedPerson"
    """
    Person with no specifically defined role in the development of the resource, but who is someone the author wishes to recognize.
    """
    Reviewer = "Reviewer"
    ReviewAssistant = "ReviewAssistant"
    ReviewerExternal = "ReviewerExternal"
    RightsHolder = "RightsHolder"
    """
    Person or institution owning or managing property rights, including intellectual property rights over the resource.
    """
    StatsReviewer = "StatsReviewer"
    Supervisor = "Supervisor"
    """
    Designated administrator over one or more groups working to produce a resource or over one or more steps of development process.
    """
    Translator = "Translator"
    WorkPackageLeader = "WorkPackageLeader"
    """
    A Work Package is a recognized data product, not all of which is included in publication.
    """
    Other = "Other"
    """
    Any person or institution making a significant contribution, but whose contribution does not "fit".
    """


class RelatedIdentifierType(str, Enum):
    """
    Identify the type of this related identifier

    """
    ARK = "ARK"
    arXiv = "arXiv"
    bibcode = "bibcode"
    DOI = "DOI"
    EAN13 = "EAN13"
    EISSN = "EISSN"
    IGSN = "IGSN"
    ISBN = "ISBN"
    ISSN = "ISSN"
    ISTC = "ISTC"
    Handle = "Handle"
    LISSN = "LISSN"
    LSID = "LSID"
    OTHER = "OTHER"
    PMCID = "PMCID"
    PMID = "PMID"
    PURL = "PURL"
    UPC = "UPC"
    URI = "URI"
    URL = "URL"
    URN = "URN"
    UUID = "UUID"
    w3id = "w3id"


class RelationType(str, Enum):
    """
    Indicates the relationship between this identifier and the source record.

    """
    BasedOnData = "BasedOnData"
    Cites = "Cites"
    """
    indicates that A includes B in a citation
    """
    Compiles = "Compiles"
    """
    indicates B is the result of a compile or creation event using A
    """
    Continues = "Continues"
    """
    indicates A is a continuation of the work B
    """
    Describes = "Describes"
    Documents = "Documents"
    """
    indicates A is documentation about B
    """
    Finances = "Finances"
    HasComment = "HasComment"
    HasDerivation = "HasDerivation"
    HasMetadata = "HasMetadata"
    """
    indicates resource A has additional metadata B
    """
    HasPart = "HasPart"
    """
    indicates A includes the part B
    """
    HasRelatedMaterial = "HasRelatedMaterial"
    HasReply = "HasReply"
    HasReview = "HasReview"
    HasVersion = "HasVersion"
    IsBasedOn = "IsBasedOn"
    IsBasisFor = "IsBasisFor"
    IsCitedBy = "IsCitedBy"
    """
    indicates that B includes A in a citation
    """
    IsCommentOn = "IsCommentOn"
    IsCompiledBy = "IsCompiledBy"
    """
    indicates B is used to compile or create A
    """
    IsContinuedBy = "IsContinuedBy"
    """
    indicates A is continued by the work B
    """
    IsDataBasisFor = "IsDataBasisFor"
    IsDerivedFrom = "IsDerivedFrom"
    """
    indicates B is a source upon which A is based
    """
    IsDescribedBy = "IsDescribedBy"
    IsDocumentedBy = "IsDocumentedBy"
    """
    indicates B is documentation about/explaining A
    """
    IsFinancedBy = "IsFinancedBy"
    IsIdenticalTo = "IsIdenticalTo"
    """
    indicates that A is identical to B, for use when there is a need to register two separate instances of the same resource
    """
    IsMetadataFor = "IsMetadataFor"
    """
    indicates additional metadata A for a resource B
    """
    IsNewVersionOf = "IsNewVersionOf"
    """
    indicates A is a new edition of B, where the new edition has been modified or updated
    """
    IsObsoletedBy = "IsObsoletedBy"
    """
    indicates that A is obsoleted by B
    """
    IsOriginalFormOf = "IsOriginalFormOf"
    """
    indicates A is the original form of B
    """
    IsPartOf = "IsPartOf"
    """
    indicates A is a portion of B; may be used for elements of a series
    """
    IsPreviousVersionOf = "IsPreviousVersionOf"
    """
    indicates A is a previous edition of B
    """
    IsReferencedBy = "IsReferencedBy"
    """
    indicates A is used as a source of information by B
    """
    IsRelatedMaterial = "IsRelatedMaterial"
    IsReplyTo = "IsReplyTo"
    IsRequiredBy = "IsRequiredBy"
    IsReviewedBy = "IsReviewedBy"
    """
    indicates that A is reviewed by B
    """
    IsReviewOf = "IsReviewOf"
    IsSourceOf = "IsSourceOf"
    """
    indicates A is a source upon which B is based
    """
    IsSupplementedBy = "IsSupplementedBy"
    """
    indicates that B is a supplement to A
    """
    IsSupplementTo = "IsSupplementTo"
    """
    indicates that A is a supplement to B
    """
    IsVariantFormOf = "IsVariantFormOf"
    """
    indicates A is a variant or different form of B, e.g. calculated or calibrated form or different packaging
    """
    IsVersionOf = "IsVersionOf"
    Obsoletes = "Obsoletes"
    """
    indicates that A obsoletes B
    """
    References = "References"
    """
    indicates B is used as a source of information for A
    """
    Requires = "Requires"
    Reviews = "Reviews"
    """
    indicates that A is a review of B
    """


class WorkflowStatusEnum(str, Enum):
    """
    The workflow status of the record.
    """
    R = "R"
    """
    Fully released
    """
    SA = "SA"
    """
    Saved
    """
    SR = "SR"
    """
    Submitted to releasing official
    """
    SO = "SO"
    """
    Submitted to OSTI awaiting validation
    """
    SF = "SF"
    """
    Submitted to OSTI and failed validation
    """
    SX = "SX"
    """
    Submitted to OSTI and failed to release
    """
    SV = "SV"
    """
    Submitted to OSTI and failed validation
    """
    X = "X"
    """
    Error Status
    """
    D = "D"
    """
    Deleted:
    """


class AccessLimitationsEnum(str, Enum):
    """
    Access limitation codes to describe the distribution rules and limitations for this work.

    """
    UNL = "UNL"
    """
    Unlimited announcement
    """
    OPN = "OPN"
    """
    OpenNET; requires opn_declassified_status, opn_declassified_date, identifier of type OPN_ACC
    """
    CPY = "CPY"
    """
    Copyright restriction on part or all of the contents of this product
    """
    OUO = "OUO"
    """
    Official use only
    """
    PROT = "PROT"
    """
    Protected data (e.g., CRADA); requires prot_flag and pdouo_exemption_number; OTHER requires prot_data_other
    """
    PDOUO = "PDOUO"
    """
    Program-determined OUO; requires pdouo_exemption_number
    """
    ECI = "ECI"
    """
    Export-controlled information; requires pdouo_exemption_number
    """
    PDSH = "PDSH"
    """
    Protected Data Sensitive Homeland
    """
    USO = "USO"
    """
    US Only
    """
    LRD = "LRD"
    """
    Limited Rights Data; requires pdouo_exemption_number
    """
    NAT = "NAT"
    """
    National Security
    """
    NNPI = "NNPI"
    """
    Naval Navigation Propulsion Info
    """
    INTL = "INTL"
    """
    International data
    """
    PROP = "PROP"
    """
    Proprietary
    """
    PAT = "PAT"
    """
    Patented information; requires pdouo_exemption_number
    """
    OTHR = "OTHR"
    """
    Other
    """
    CUI = "CUI"
    """
    Controlled Unclassified Information; include specific or basic categories/controls in access_limitation_other
    """


class CollectionTypeEnum(str, Enum):
    """
    The OSTI collection type originally creating this record.
    """
    DOE_LAB = "DOE_LAB"
    DOE_GRANT = "DOE_GRANT"
    CHORUS = "CHORUS"


class IdentifierType(str, Enum):
    """
    Describe the type of identifier
    """
    AUTH_REV = "AUTH_REV"
    CN_DOE = "CN_DOE"
    CN_NONDOE = "CN_NONDOE"
    CODEN = "CODEN"
    DOE_DOCKET = "DOE_DOCKET"
    """
    DOE Docket number, used for documents submitted to the DOE Electronic Docket Room (e-Docket Room) system.
    """
    EDB = "EDB"
    ETDE_RN = "ETDE_RN"
    INIS_RN = "INIS_RN"
    ISBN = "ISBN"
    """
    International Standard Book Number
    """
    ISSN = "ISSN"
    """
    International Standard Serial Number
    """
    LEGACY = "LEGACY"
    NSA = "NSA"
    OPN_ACC = "OPN_ACC"
    OTHER_ID = "OTHER_ID"
    PATENT = "PATENT"
    """
    Patent number
    """
    PROJ_ID = "PROJ_ID"
    """
    Project identifier
    """
    PROP_REV = "PROP_REV"
    REF = "REF"
    REL_TRN = "REL_TRN"
    RN = "RN"
    TRN = "TRN"
    TVI = "TVI"
    USER_VER = "USER_VER"
    WORK_AUTH = "WORK_AUTH"
    WORK_PROP = "WORK_PROP"


class MediaLocationEnum(str, Enum):
    """
    Indicates if a media file is stored locally or off-site.
    """
    L = "L"
    """
    Local
    """
    O = "O"
    """
    Off-Site
    """


class OrganizationType(str, Enum):
    """
    Indicates type of organization.
    """
    AUTHOR = "AUTHOR"
    CONTRIBUTING = "CONTRIBUTING"
    RESEARCHING = "RESEARCHING"
    SPONSOR = "SPONSOR"


class OrganizationIdentifierType(str, Enum):
    """
    Describe the type of identifier.
    """
    AWARD_DOI = "AWARD_DOI"
    CN_DOE = "CN_DOE"
    CN_NONDOE = "CN_NONDOE"


class PersonType(str, Enum):
    """
    Indicates type of person.
    """
    AUTHOR = "AUTHOR"
    """
    Authors are the main scientists or researchers involved in creating, authoring, or producing the research output/scientific and technical information resource.
    """
    RELEASE = "RELEASE"
    """
    Releasing Official
    """
    CONTACT = "CONTACT"
    """
    Contact Information Persons of these types require at least one valid email address be specified.
    """
    CONTRIBUTING = "CONTRIBUTING"
    """
    Contributors are people who may have been involved in acquiring resources, collecting data, analyzing resources, developing methodologies, validating information, visualizing data, or otherwise contributing to the output, but would not be considered authors. (A valid contributor_type is required.)
    """
    PROT_CE = "PROT_CE"
    """
    Protected Data Courtesy Email Information Persons of these types require at least one valid email address be specified.
    """
    PROT_RO = "PROT_RO"
    """
    Protected Data Actual Releasing Official This field is only applicable to Grantee records that are protected by submitting with the "PROT" access limitation.
    """
    SBIZ_PI = "SBIZ_PI"
    """
    SBIR/STTR Principal Investigator Persons of these types require at least one valid email address be specified.
    """
    SBIZ_BO = "SBIZ_BO"
    """
    SBIR/STTR Business Official Business official persons require exactly two valid email addresses be specified.
    """


class ProductType(str, Enum):
    """
    Define the type of product represented by this metadata information. Values presented *in italics* are considered Legacy types.
    """
    AR = "AR"
    """
    Accomplishment Report
    """
    B = "B"
    """
    Book
    """
    CO = "CO"
    """
    Conference
    """
    DA = "DA"
    """
    Dataset
    """
    FS = "FS"
    """
    Factsheet
    """
    JA = "JA"
    """
    Journal Article
    """
    MI = "MI"
    """
    Miscellaneous
    """
    OT = "OT"
    """
    Other
    """
    P = "P"
    """
    Patent
    """
    PD = "PD"
    """
    Program Document
    """
    SM = "SM"
    """
    Software Manual
    """
    TD = "TD"
    """
    Thesis/Dissertation
    """
    TR = "TR"
    """
    Technical Report
    """
    PA = "PA"
    """
    Patent Application
    """


class GeolocationType(str, Enum):
    POINT = "POINT"
    BOX = "BOX"
    POLYGON = "POLYGON"



class Records(ConfiguredBaseModel):
    """
    A list of Record metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema', 'tree_root': True})

    records: Optional[list[int]] = Field(default=None, description="""List of records in the collection.""", json_schema_extra = { "linkml_meta": {'alias': 'records', 'domain_of': ['records']} })


class Record(ConfiguredBaseModel):
    """
    Defines the bibliographic metadata about a particular work or record. Depending on product type, various elements are permitted, not permitted, or required.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    osti_id: int = Field(default=..., description="""Unique identifier for OSTI record, only required for updates.""", json_schema_extra = { "linkml_meta": {'alias': 'osti_id',
         'domain_of': ['Record', 'MediaSet'],
         'examples': [{'value': '9999'}]} })
    identifiers: Optional[list[Identifier]] = Field(default=None, description="""List of identifying numbers related to this record""", json_schema_extra = { "linkml_meta": {'alias': 'identifiers', 'domain_of': ['Record', 'Organization']} })
    issue: Optional[str] = Field(default=None, description="""Issue number for journals or other applicable products if any.""", json_schema_extra = { "linkml_meta": {'alias': 'issue', 'domain_of': ['Record'], 'examples': [{'value': '44'}]} })
    journal_license_url: Optional[str] = Field(default=None, description="""URL for information regarding the journal license for information""", json_schema_extra = { "linkml_meta": {'alias': 'journal_license_url',
         'domain_of': ['Record'],
         'examples': [{'value': 'https://journal-publishers.com/license/3.02/text'}]} })
    journal_name: Optional[str] = Field(default=None, description="""Name of journal publishing this information""", json_schema_extra = { "linkml_meta": {'alias': 'journal_name',
         'domain_of': ['Record'],
         'examples': [{'value': 'Proceedings of the National Academy of Sciences'}]} })
    journal_open_access_flag: Optional[str] = Field(default=None, description="""Indicates if the journal article is available in an open access journal, indicated as Y for open, N for not, or left blank/omitted if not applicable or unknown status.""", json_schema_extra = { "linkml_meta": {'alias': 'journal_open_access_flag',
         'domain_of': ['Record'],
         'examples': [{'value': 'N'}]} })
    journal_type: Optional[str] = Field(default=None, description="""Specific sub-type of the journal article.  For product type JA only. Further qualifies the type of record.""", json_schema_extra = { "linkml_meta": {'alias': 'journal_type',
         'domain_of': ['Record'],
         'examples': [{'value': 'AM'}]} })
    revision: Optional[int] = Field(default=None, description="""Revision number (sequence) for this record.""", json_schema_extra = { "linkml_meta": {'alias': 'revision',
         'domain_of': ['Record', 'MediaSet', 'MediaFile'],
         'examples': [{'value': '1'}]} })
    workflow_status: Optional[WorkflowStatusEnum] = Field(default=None, description="""Workflow status of current revision of record.""", json_schema_extra = { "linkml_meta": {'alias': 'workflow_status',
         'domain_of': ['Record'],
         'examples': [{'value': 'SO'}]} })
    access_limitations: list[AccessLimitationsEnum] = Field(default=..., description="""Access limitation codes to describe the distribution rules and limitations for this work.""", json_schema_extra = { "linkml_meta": {'alias': 'access_limitations',
         'domain_of': ['Record', 'MediaSet'],
         'examples': [{'value': 'UNL'}, {'value': 'OPN'}]} })
    access_limitation_other: Optional[str] = Field(default=None, description="""Additional information about access limitation for this record, if needed. Required for CUI or PDOUO designations in access limitation. May contain information about the following: Special handling instructions, Copyright restrictions, Other criteria pertinent to the review, access limitation, announcement, and/or restriction of this STI product.""", json_schema_extra = { "linkml_meta": {'alias': 'access_limitation_other',
         'domain_of': ['Record'],
         'examples': [{'value': 'Restricted to US Distribution Only by DOE Order.'}]} })
    added_by: Optional[int] = Field(default=None, description="""E-Link user ID that initially entered this record. Value internally maintained by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'added_by',
         'domain_of': ['Record', 'MediaSet'],
         'examples': [{'value': '28931'}]} })
    announcement_codes: Optional[list[str]] = Field(default=None, description="""List of announcement codes for this record.""", json_schema_extra = { "linkml_meta": {'alias': 'announcement_codes',
         'domain_of': ['Record'],
         'examples': [{'value': 'EDB'}, {'value': 'INIS'}]} })
    edition: Optional[str] = Field(default=None, description="""Edition number, as applicable to Books or other products.""", json_schema_extra = { "linkml_meta": {'alias': 'edition', 'domain_of': ['Record'], 'examples': [{'value': '2023'}]} })
    volume: Optional[str] = Field(default=None, description="""A volume number as applicable, usually for journals or books.""", json_schema_extra = { "linkml_meta": {'alias': 'volume', 'domain_of': ['Record'], 'examples': [{'value': '1'}]} })
    collection_type: Optional[CollectionTypeEnum] = Field(default=None, description="""Indicates the OSTI collection type originally creating this record. Maintained internally by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'collection_type',
         'domain_of': ['Record'],
         'examples': [{'value': 'DOE_LAB'}]} })
    conference_information: Optional[str] = Field(default=None, description="""\"Describes the conference pertaining to this record, if any; usually name and / or location the event took place.\"\"""", json_schema_extra = { "linkml_meta": {'alias': 'conference_information',
         'domain_of': ['Record'],
         'examples': [{'value': 'ApacheCON 2019 discussion panel'}]} })
    conference_type: Optional[str] = Field(default=None, description="""Code representing the type of conference-related work of this record. Generally, only applicable to CO type submissions.""", json_schema_extra = { "linkml_meta": {'alias': 'conference_type',
         'domain_of': ['Record'],
         'examples': [{'value': 'O'}]} })
    contract_award_date: Optional[datetime ] = Field(default=None, description="""Date contract for this record was awarded.""", json_schema_extra = { "linkml_meta": {'alias': 'contract_award_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2012-02-19T00:00:00.000Z'}]} })
    country_publication_code: Optional[str] = Field(default=None, description="""Country of publication for this record""", json_schema_extra = { "linkml_meta": {'alias': 'country_publication_code',
         'domain_of': ['Record'],
         'examples': [{'value': 'US'}]} })
    date_metadata_added: Optional[datetime ] = Field(default=None, description="""Date record first entered the OSTI system. Value internally maintained by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'date_metadata_added',
         'domain_of': ['Record'],
         'examples': [{'value': '2023-09-22T18:31:32.043Z'}]} })
    date_metadata_updated: Optional[datetime ] = Field(default=None, description="""Date of this revision of the record. Value internally maintained by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'date_metadata_updated',
         'domain_of': ['Record'],
         'examples': [{'value': '2020-04-02T12:33:17.553Z'}]} })
    date_submitted_to_osti_first: Optional[datetime ] = Field(default=None, description="""Date record was first submitted to OSTI for publication. Maintained internally by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'date_submitted_to_osti_first',
         'domain_of': ['Record'],
         'examples': [{'value': '2019-04-04T08:25:12.234Z'}]} })
    date_submitted_to_osti_last: Optional[datetime ] = Field(default=None, description="""Most recent date record information was submitted to OSTI. Maintained internally by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'date_submitted_to_osti_last',
         'domain_of': ['Record'],
         'examples': [{'value': '2018-05-04T11:44:23.864Z'}]} })
    title: str = Field(default=..., description="""Title of record.  For Book Chapters, the title of the chapter.""", json_schema_extra = { "linkml_meta": {'alias': 'title',
         'domain_of': ['Record'],
         'examples': [{'value': 'Sample document title'}]} })
    description: Optional[str] = Field(default=None, description="""Description or abstract for this record. Required to have a value for grantee submissions.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Record'],
         'examples': [{'value': 'Information about a particular record, report, or '
                                'other document, or executive summary or abstract of '
                                'same.'}]} })
    descriptors: Optional[list[str]] = Field(default=None, description="""List of descriptor codes for this record""", json_schema_extra = { "linkml_meta": {'alias': 'descriptors',
         'domain_of': ['Record'],
         'examples': [{'value': 'ATMOSPHERE'}, {'value': 'ELECTRONS'}]} })
    doe_funded_flag: Optional[str] = Field(default=None, description="""Indicates if the record is primarily DOE-funded. Indicate Y for Yes, N for no, or leave blank/omit if unknown status.""", json_schema_extra = { "linkml_meta": {'alias': 'doe_funded_flag',
         'domain_of': ['Record'],
         'examples': [{'value': 'Y'}]} })
    doi: Optional[str] = Field(default=None, description="""The DOI for this record, if any.  Enter value if previously assigned a DOI for the record from an outside service.  If not supplied, OSTI may assign a DOI for the work for certain applicable record types.""", json_schema_extra = { "linkml_meta": {'alias': 'doi',
         'domain_of': ['Record'],
         'examples': [{'value': '10.5072/2020/238479ax'}]} })
    doi_infix: Optional[str] = Field(default=None, description="""\"Any customized infix value for the DOI used when generating a DOI reference. The following characters should be avoided in the infix value: ;/?:@&=+$,.\"""", json_schema_extra = { "linkml_meta": {'alias': 'doi_infix',
         'domain_of': ['Record'],
         'examples': [{'value': 'Climate2019'}]} })
    edited_by: Optional[int] = Field(default=None, description="""OSTI user ID making this revision of the metadata record. Value internally maintained by E-Link.""", json_schema_extra = { "linkml_meta": {'alias': 'edited_by',
         'domain_of': ['Record'],
         'examples': [{'value': '112389'}]} })
    edit_reason: Optional[str] = Field(default=None, description="""Value provided by user editing a record describing the reason for the edit.""", json_schema_extra = { "linkml_meta": {'alias': 'edit_reason',
         'domain_of': ['Record'],
         'examples': [{'value': 'Modified title and authors.'}]} })
    edit_source: Optional[str] = Field(default=None, description="""Value determined based on type of edit and user performing the association.""", json_schema_extra = { "linkml_meta": {'alias': 'edit_source',
         'domain_of': ['Record'],
         'examples': [{'value': 'NORMAL_WEBFORM'}]} })
    format_information: Optional[str] = Field(default=None, description="""Information about the format of the product, including any operating system or program requirements for use of the data, as applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'format_information',
         'domain_of': ['Record'],
         'examples': [{'value': 'Originally Word Perfect 4.2 document'}]} })
    media_embargo_sunset_date: Optional[str] = Field(default=None, description="""Indicates date on which the document embargo ends, if applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'media_embargo_sunset_date',
         'domain_of': ['Record'],
         'examples': [{'value': '7/6/2022'}]} })
    publication_date: datetime  = Field(default=..., description="""Date of publication of this record.  For Thesis/Dissertation records, this may also be the completion date of the Thesis.  For Patents, the date the patent was issued or approved.""", json_schema_extra = { "linkml_meta": {'alias': 'publication_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2009-06-12T00:00:00.000Z'}]} })
    publication_date_text: Optional[str] = Field(default=None, description="""String representation of the publication date (e.g., Summer 2001)""", json_schema_extra = { "linkml_meta": {'alias': 'publication_date_text',
         'domain_of': ['Record'],
         'examples': [{'value': 'Winter 2012'}]} })
    publisher_information: Optional[str] = Field(default=None, description="""Publisher-specific information if applicable""", json_schema_extra = { "linkml_meta": {'alias': 'publisher_information',
         'domain_of': ['Record'],
         'examples': [{'value': 'University Press, Volume III Spring 2001'}]} })
    related_doc_info: Optional[str] = Field(default=None, description="""Additional information regarding the document.  Considered historical or deprecated information, provided for access to historical data. This field is NOT recommended for new submissions.""", json_schema_extra = { "linkml_meta": {'alias': 'related_doc_info',
         'domain_of': ['Record'],
         'examples': [{'value': 'Reprint Spring 2012'}]} })
    keywords: Optional[list[str]] = Field(default=None, description="""Concise set of key words for this record""", json_schema_extra = { "linkml_meta": {'alias': 'keywords',
         'domain_of': ['Record'],
         'examples': [{'value': 'NUCLEAR'}, {'value': 'REACTIONS'}]} })
    languages: Optional[list[str]] = Field(default=None, description="""Language codes for this record""", json_schema_extra = { "linkml_meta": {'alias': 'languages',
         'domain_of': ['Record'],
         'examples': [{'value': 'English'}]} })
    audit_logs: Optional[list[AuditLog]] = Field(default=None, description="""Listing of any audit logs of actions taken and worker interactions performed on this metadata revision, if any.""", json_schema_extra = { "linkml_meta": {'alias': 'audit_logs', 'domain_of': ['Record']} })
    media: Optional[list[MediaSet]] = Field(default=None, description="""Listing of any media and files associated with this record, along with various metadata information and status data for each.  Empty if no media is currently associated with this record.""", json_schema_extra = { "linkml_meta": {'alias': 'media', 'domain_of': ['Record']} })
    opn_addressee: Optional[str] = Field(default=None, description="""For OpenNET records, the addressee information""", json_schema_extra = { "linkml_meta": {'alias': 'opn_addressee',
         'domain_of': ['Record'],
         'examples': [{'value': 'Forestall Bldg A-113'}]} })
    opn_declassified_date: Optional[str] = Field(default=None, description="""For OpenNET records, the date information was declassified""", json_schema_extra = { "linkml_meta": {'alias': 'opn_declassified_date',
         'domain_of': ['Record'],
         'examples': [{'value': '03/02/2018'}]} })
    opn_declassified_status: Optional[str] = Field(default=None, description="""For OpenNET records, status of declassification of information""", json_schema_extra = { "linkml_meta": {'alias': 'opn_declassified_status',
         'domain_of': ['Record'],
         'examples': [{'value': 'N'}]} })
    opn_document_categories: Optional[list[str]] = Field(default=None, description="""For OpenNET records, list of any document categories pertaining to this record""", json_schema_extra = { "linkml_meta": {'alias': 'opn_document_categories',
         'domain_of': ['Record'],
         'examples': [{'value': 'Chemistry'}, {'value': 'Geothermal'}]} })
    opn_document_location: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'opn_document_location',
         'domain_of': ['Record'],
         'examples': [{'value': 'US Department of Science, Office 201'}]} })
    opn_fieldoffice_acronym_code: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'opn_fieldoffice_acronym_code',
         'domain_of': ['Record'],
         'examples': [{'value': 'THX-1138'}]} })
    organizations: Optional[list[Organization]] = Field(default=None, description="""List of organizations related to this record. For submissions, at least SPONSOR and RESEARCHING organization is required.""", json_schema_extra = { "linkml_meta": {'alias': 'organizations', 'domain_of': ['Record']} })
    other_information: Optional[list[str]] = Field(default=None, description="""Information useful to include in published announcements which is not suited for other fields.""", json_schema_extra = { "linkml_meta": {'alias': 'other_information',
         'domain_of': ['Record'],
         'examples': [{'value': 'Published in Nature, Fall 2012'}]} })
    ouo_release_date: Optional[str] = Field(default=None, description="""Date of OUO access limitation expiration if applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'ouo_release_date',
         'domain_of': ['Record'],
         'examples': [{'value': '1997-05-09 10:23:44'}]} })
    paper_flag: Optional[bool] = Field(default=None, description="""Indicates if OSTI has or had a paper copy of this product.""", json_schema_extra = { "linkml_meta": {'alias': 'paper_flag',
         'domain_of': ['Record'],
         'examples': [{'value': 'true'}]} })
    patent_assignee: Optional[str] = Field(default=None, description="""The holder of property rights to a patent.""", json_schema_extra = { "linkml_meta": {'alias': 'patent_assignee',
         'domain_of': ['Record'],
         'examples': [{'value': 'United Property Holdings, LLC'}]} })
    patent_file_date: Optional[datetime ] = Field(default=None, description="""Date patent was filed with US Patent Office.""", json_schema_extra = { "linkml_meta": {'alias': 'patent_file_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2018-04-08T00:00:00.000Z'}]} })
    patent_priority_date: Optional[datetime ] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'patent_priority_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2004-07-12T00:00:00.000Z'}]} })
    pdouo_exemption_number: Optional[str] = Field(default=None, description="""Exception number for PDOUO access limitation records. Multiple values may be delimited by semi-colons.""", json_schema_extra = { "linkml_meta": {'alias': 'pdouo_exemption_number',
         'domain_of': ['Record'],
         'examples': [{'value': '278324'}]} })
    persons: Optional[list[Person]] = Field(default=None, description="""List of persons (authors, contributors, etc.) related to this record. For submissions, at least one AUTHOR or CONTRIBUTING Person, along with a RELEASE contact, is required.""", json_schema_extra = { "linkml_meta": {'alias': 'persons', 'domain_of': ['Record']} })
    product_size: Optional[str] = Field(default=None, description="""Information regarding physical size of media or report, if applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'product_size',
         'domain_of': ['Record'],
         'examples': [{'value': '227 pages'}]} })
    product_type: Optional[ProductType] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'product_type', 'domain_of': ['Record']} })
    product_type_other: Optional[str] = Field(default=None, description="""Additional information for 'OTHER' product types.  Required if 'OT' product type is specified for this record.""", json_schema_extra = { "linkml_meta": {'alias': 'product_type_other',
         'domain_of': ['Record'],
         'examples': [{'value': 'Preprint'}]} })
    prot_flag: Optional[str] = Field(default=None, description="""Indicates the type of protected data described by this record. PROT must be specified in the access limitations.""", json_schema_extra = { "linkml_meta": {'alias': 'prot_flag',
         'domain_of': ['Record'],
         'examples': [{'value': 'EPACT'}]} })
    prot_data_other: Optional[str] = Field(default=None, description="""Information regarding why the information is protected if not a CRADA product.""", json_schema_extra = { "linkml_meta": {'alias': 'prot_data_other',
         'domain_of': ['Record'],
         'examples': [{'value': 'PROTECTED'}]} })
    prot_release_date: Optional[datetime ] = Field(default=None, description="""The date on which data protections for this record will end.""", json_schema_extra = { "linkml_meta": {'alias': 'prot_release_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2023-07-23T00:00:00.000Z'}]} })
    availability: Optional[str] = Field(default=None, description="""Describes record's availibility information.""", json_schema_extra = { "linkml_meta": {'alias': 'availability',
         'domain_of': ['Record'],
         'examples': [{'value': 'Also available at '
                                'https://sample.com/document/report.pdf'}]} })
    subject_category_code: Optional[list[str]] = Field(default=None, description="""Set two-character subject category code values for this record""", json_schema_extra = { "linkml_meta": {'alias': 'subject_category_code',
         'domain_of': ['Record'],
         'examples': [{'value': '2'}, {'value': '31'}]} })
    subject_category_code_legacy: Optional[list[str]] = Field(default=None, description="""Any legacy or historical subject category codes for this report""", json_schema_extra = { "linkml_meta": {'alias': 'subject_category_code_legacy',
         'domain_of': ['Record'],
         'examples': [{'value': 'Political Science'},
                      {'value': 'Geosciences'},
                      {'value': 'Physics'}]} })
    related_identifiers: Optional[list[RelatedIdentifier]] = Field(default=None, description="""List of related identifiers connected to this record""", json_schema_extra = { "linkml_meta": {'alias': 'related_identifiers', 'domain_of': ['Record']} })
    released_to_osti_date: Optional[datetime ] = Field(default=None, description="""Date record information was released to OSTI, as entered by releasing official.""", json_schema_extra = { "linkml_meta": {'alias': 'released_to_osti_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2019-06-03T00:00:00.000Z'}]} })
    releasing_official_comments: Optional[str] = Field(default=None, description="""Any comments made by the releasing official on the record.""", json_schema_extra = { "linkml_meta": {'alias': 'releasing_official_comments',
         'domain_of': ['Record'],
         'examples': [{'value': 'Final report due January 2021.'}]} })
    report_period_end_date: Optional[datetime ] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'report_period_end_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2023-01-14T00:00:00.000Z'}]} })
    report_period_start_date: Optional[datetime ] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'report_period_start_date',
         'domain_of': ['Record'],
         'examples': [{'value': '2023-01-05T00:00:00.000Z'}]} })
    report_types: Optional[list[str]] = Field(default=None, description="""The type(s) of information or frequency of reporting of information in this report.""", json_schema_extra = { "linkml_meta": {'alias': 'report_types',
         'domain_of': ['Record'],
         'examples': [{'value': 'F'}, {'value': 'B'}]} })
    report_type_other: Optional[str] = Field(default=None, description="""Detail information about 'Other' report types.""", json_schema_extra = { "linkml_meta": {'alias': 'report_type_other',
         'domain_of': ['Record'],
         'examples': [{'value': 'OTHERVALUE'}]} })
    sbiz_flag: Optional[str] = Field(default=None, description="""Indicates if this metadata is SBIR or STTR related.""", json_schema_extra = { "linkml_meta": {'alias': 'sbiz_flag',
         'domain_of': ['Record'],
         'examples': [{'value': 'SBIR'}, {'value': 'STTR'}]} })
    sbiz_phase: Optional[str] = Field(default=None, description="""A three-character field constrained to 'I', 'II', 'IIA', 'IIB', or 'III' indicating the phase of this SBIR/STTR report.""", json_schema_extra = { "linkml_meta": {'alias': 'sbiz_phase', 'domain_of': ['Record'], 'examples': [{'value': 'IIB'}]} })
    sbiz_previous_contract_number: Optional[str] = Field(default=None, description="""The previous SBIR/STTR contract number if a Phase III SBIR/STTR report.""", json_schema_extra = { "linkml_meta": {'alias': 'sbiz_previous_contract_number',
         'domain_of': ['Record'],
         'examples': [{'value': 'SMPL-2023-1291'}]} })
    sbiz_release_date: Optional[datetime ] = Field(default=None, description="""Date data protections on this SBIR/STTR record will expire.""", json_schema_extra = { "linkml_meta": {'alias': 'sbiz_release_date', 'domain_of': ['Record']} })
    site_ownership_code: Optional[str] = Field(default=None, description="""Code of the DOE site submitting this document""", json_schema_extra = { "linkml_meta": {'alias': 'site_ownership_code',
         'domain_of': ['Record'],
         'examples': [{'value': 'BNL'}]} })
    site_unique_id: Optional[str] = Field(default=None, description="""Site-specified unique accession number for this record""", json_schema_extra = { "linkml_meta": {'alias': 'site_unique_id',
         'domain_of': ['Record'],
         'examples': [{'value': '89345'}]} })
    site_url: Optional[str] = Field(default=None, description="""(DATASET product type only) The URL of the data set landing page, containing links to data set content or additional information as required.""", json_schema_extra = { "linkml_meta": {'alias': 'site_url', 'domain_of': ['Record']} })
    source_input_type: Optional[str] = Field(default=None, description="""Value determined by submission type at record creation time. Defines how E-Link record was first entered into the system.""", json_schema_extra = { "linkml_meta": {'alias': 'source_input_type',
         'domain_of': ['Record'],
         'examples': [{'value': 'DOE_GRANT_WEBFORM'}]} })
    source_edit_type: Optional[str] = Field(default=None, description="""Value determined by submission type for each edit or revision of a record. Changes on a per-revision basis.""", json_schema_extra = { "linkml_meta": {'alias': 'source_edit_type',
         'domain_of': ['Record'],
         'examples': [{'value': 'DOE_LAB_API'}]} })
    geolocations: Optional[list[Geolocation]] = Field(default=None, description="""List of geolocation references for this record.""", json_schema_extra = { "linkml_meta": {'alias': 'geolocations', 'domain_of': ['Record']} })

    @field_validator('issue')
    def pattern_issue(cls, v):
        pattern=re.compile(r"^.{0,80}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid issue format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid issue format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('journal_license_url')
    def pattern_journal_license_url(cls, v):
        pattern=re.compile(r"^.{0,255}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid journal_license_url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid journal_license_url format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('journal_name')
    def pattern_journal_name(cls, v):
        pattern=re.compile(r"^.{0,250}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid journal_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid journal_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('journal_open_access_flag')
    def pattern_journal_open_access_flag(cls, v):
        pattern=re.compile(r"^.{0,1}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid journal_open_access_flag format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid journal_open_access_flag format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('journal_type')
    def pattern_journal_type(cls, v):
        pattern=re.compile(r"^.{0,2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid journal_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid journal_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('access_limitations')
    def pattern_access_limitations(cls, v):
        pattern=re.compile(r"^.{0,5}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid access_limitations format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid access_limitations format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('edition')
    def pattern_edition(cls, v):
        pattern=re.compile(r"^.{0,10}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid edition format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid edition format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('volume')
    def pattern_volume(cls, v):
        pattern=re.compile(r"^.{0,68}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid volume format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid volume format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('conference_type')
    def pattern_conference_type(cls, v):
        pattern=re.compile(r"^.{0,1}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid conference_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid conference_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('country_publication_code')
    def pattern_country_publication_code(cls, v):
        pattern=re.compile(r"^.{0,5}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid country_publication_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid country_publication_code format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('doe_funded_flag')
    def pattern_doe_funded_flag(cls, v):
        pattern=re.compile(r"^.{0,1}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid doe_funded_flag format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid doe_funded_flag format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('publisher_information')
    def pattern_publisher_information(cls, v):
        pattern=re.compile(r"^.{0,400}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid publisher_information format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid publisher_information format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('related_doc_info')
    def pattern_related_doc_info(cls, v):
        pattern=re.compile(r"^.{0,2255}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid related_doc_info format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid related_doc_info format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('opn_fieldoffice_acronym_code')
    def pattern_opn_fieldoffice_acronym_code(cls, v):
        pattern=re.compile(r"^.{0,10}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid opn_fieldoffice_acronym_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid opn_fieldoffice_acronym_code format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('product_size')
    def pattern_product_size(cls, v):
        pattern=re.compile(r"^.{0,50}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid product_size format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid product_size format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('product_type')
    def pattern_product_type(cls, v):
        pattern=re.compile(r"^.{0,2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid product_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid product_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('product_type_other')
    def pattern_product_type_other(cls, v):
        pattern=re.compile(r"^.{0,200}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid product_type_other format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid product_type_other format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('prot_flag')
    def pattern_prot_flag(cls, v):
        pattern=re.compile(r"^.{0,5}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid prot_flag format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid prot_flag format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('prot_data_other')
    def pattern_prot_data_other(cls, v):
        pattern=re.compile(r"^.{0,80}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid prot_data_other format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid prot_data_other format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('subject_category_code')
    def pattern_subject_category_code(cls, v):
        pattern=re.compile(r"^.{0,2}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid subject_category_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid subject_category_code format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('report_type_other')
    def pattern_report_type_other(cls, v):
        pattern=re.compile(r"^.{0,80}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid report_type_other format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid report_type_other format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('sbiz_flag')
    def pattern_sbiz_flag(cls, v):
        pattern=re.compile(r"^.{0,6}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid sbiz_flag format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid sbiz_flag format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('sbiz_phase')
    def pattern_sbiz_phase(cls, v):
        pattern=re.compile(r"^.{0,3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid sbiz_phase format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid sbiz_phase format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('sbiz_previous_contract_number')
    def pattern_sbiz_previous_contract_number(cls, v):
        pattern=re.compile(r"^.{0,14}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid sbiz_previous_contract_number format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid sbiz_previous_contract_number format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('site_ownership_code')
    def pattern_site_ownership_code(cls, v):
        pattern=re.compile(r"^.{0,10}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid site_ownership_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid site_ownership_code format: {v}"
            raise ValueError(err_msg)
        return v


class RelatedIdentifier(ConfiguredBaseModel):
    """
    Identifies other resources that are related in some manner to this record
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: RelatedIdentifierType = Field(default=..., description="""Identify the type of this related identifier""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person'],
         'examples': [{'value': 'DOI'}]} })
    relation: RelationType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'relation', 'domain_of': ['RelatedIdentifier']} })
    value: str = Field(default=..., description="""The value of the identifier""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['RelatedIdentifier', 'Identifier', 'OrganizationIdentifier'],
         'examples': [{'value': '10.11578/2020/28383'}]} })

    @field_validator('relation')
    def pattern_relation(cls, v):
        pattern=re.compile(r"^.{0,20}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid relation format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid relation format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('value')
    def pattern_value(cls, v):
        pattern=re.compile(r"^.{0,2000}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid value format: {v}"
            raise ValueError(err_msg)
        return v


class Geolocation(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: Optional[GeolocationType] = Field(default=None, description="""Describes the shape of this geolocation attribute. (Optional, type may be determined by examination of the points.) Single point in 'points' indicates this is a POINT; two points, indicating NW and SE location, indicate a BOX; any other number of points is assumed to be a POLYGON.  Note that POLYGONs should begin and end on the same point, in order to properly express a 'closed polygon' shape.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person'],
         'examples': [{'value': 'POINT'}]} })
    label: Optional[str] = Field(default=None, description="""Optional place name for this location or set of geolocation points.""", json_schema_extra = { "linkml_meta": {'alias': 'label',
         'domain_of': ['Geolocation'],
         'examples': [{'value': 'Maryland coastal waters'}]} })
    points: list[Point] = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'points', 'domain_of': ['Geolocation']} })


class Point(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    latitude: float = Field(default=..., description="""Latitude of this point in the geolocation; limited to -90 to 90, inclusive.""", ge=-90, le=90, json_schema_extra = { "linkml_meta": {'alias': 'latitude',
         'domain_of': ['point'],
         'examples': [{'value': '38.75096'}]} })
    longitude: float = Field(default=..., description="""Longitude of this point in the geolocation; limited to -180 to 180, inclusive.""", ge=-180, le=180, json_schema_extra = { "linkml_meta": {'alias': 'longitude',
         'domain_of': ['point'],
         'examples': [{'value': '-76.51239'}]} })


class Identifier(ConfiguredBaseModel):
    """
    Values of various identifying numbers, such as DOE contract number, product numbers, ISBN, ISSN, and other various forms of identifying markings or numbers pertaining to the product or metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: Optional[IdentifierType] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person']} })
    value: Optional[str] = Field(default=None, description="""Value of this identifier""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['RelatedIdentifier', 'Identifier', 'OrganizationIdentifier'],
         'examples': [{'value': '9234782'}]} })

    @field_validator('value')
    def pattern_value(cls, v):
        pattern=re.compile(r"^.{0,100}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid value format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid value format: {v}"
            raise ValueError(err_msg)
        return v


class AuditLog(ConfiguredBaseModel):
    """
    Indicates status and information about back-end processing on a given metadata record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: Optional[str] = Field(default=None, description="""Indicates the source of the status message, generally the backend process performing the action in question.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person'],
         'examples': [{'value': 'VALIDATOR'}]} })
    audit_date: Optional[datetime ] = Field(default=None, description="""Timestamp of the operation detailed in this audit log.""", json_schema_extra = { "linkml_meta": {'alias': 'audit_date',
         'domain_of': ['AuditLog'],
         'examples': [{'value': '2024-11-04T15:08:44.438Z'}]} })
    status: Optional[str] = Field(default=None, description="""Indicates state or notification level of worker action detailed in this audit log.  Generally SUCCESS or FAIL, but may additionally indicate INFO, WARN, or ERROR status messages.""", json_schema_extra = { "linkml_meta": {'alias': 'status',
         'domain_of': ['AuditLog', 'MediaSet', 'MediaFile'],
         'examples': [{'value': 'SUCCESS'}]} })
    messages: Optional[list[str]] = Field(default=None, description="""One or more messages pertaining to the action taken or results of worker processing for this audit log.""", json_schema_extra = { "linkml_meta": {'alias': 'messages',
         'domain_of': ['AuditLog'],
         'examples': [{'value': 'Validation Successful.'}]} })


class MediaSet(ConfiguredBaseModel):
    """
    Metadata about files associated with this product.  Summarizes the main media file associated with this product, usually an off-site URL or PDF uploaded to OSTI, with its state, URL if applicable, and other identifying state information pertaining to the media files as a group. Each media set is uniquely identified by its `MEDIA_ID` value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    media_id: Optional[int] = Field(default=None, description="""Unique ID for this MEDIA SET.""", json_schema_extra = { "linkml_meta": {'alias': 'media_id',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': '233743'}]} })
    revision: Optional[int] = Field(default=None, description="""Revision number of this media association set.""", json_schema_extra = { "linkml_meta": {'alias': 'revision',
         'domain_of': ['Record', 'MediaSet', 'MediaFile'],
         'examples': [{'value': '3'}]} })
    access_limitations: Optional[list[AccessLimitationsEnum]] = Field(default=None, description="""Access limitations are inherited from the parent metadata record at time of association.""", json_schema_extra = { "linkml_meta": {'alias': 'access_limitations',
         'domain_of': ['Record', 'MediaSet'],
         'examples': [{'value': 'UNL'}]} })
    osti_id: Optional[int] = Field(default=None, description="""Links to Record OSTI_ID value for a Media Set.""", json_schema_extra = { "linkml_meta": {'alias': 'osti_id',
         'domain_of': ['Record', 'MediaSet'],
         'examples': [{'value': '99238'}]} })
    status: Optional[str] = Field(default=None, description="""Indicate the current processing of the media file set.""", json_schema_extra = { "linkml_meta": {'alias': 'status',
         'domain_of': ['AuditLog', 'MediaSet', 'MediaFile'],
         'examples': [{'value': 'P'}]} })
    added_by: Optional[int] = Field(default=None, description="""Indicates user ID that added this media set.""", json_schema_extra = { "linkml_meta": {'alias': 'added_by',
         'domain_of': ['Record', 'MediaSet'],
         'examples': [{'value': '34582'}]} })
    document_page_count: Optional[int] = Field(default=None, description="""Number of pages, if applicable, found in the processing of this file.""", json_schema_extra = { "linkml_meta": {'alias': 'document_page_count',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': '23'}]} })
    mime_type: Optional[str] = Field(default=None, description="""MIME type description of the file content of this media file. This value is set by OSTI media processing.""", json_schema_extra = { "linkml_meta": {'alias': 'mime_type',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': 'application/pdf'}]} })
    media_title: Optional[str] = Field(default=None, description="""Optional title provided for the given media set.""", json_schema_extra = { "linkml_meta": {'alias': 'media_title',
         'domain_of': ['MediaSet'],
         'examples': [{'value': 'PDF of technical report content'}]} })
    media_location: Optional[MediaLocationEnum] = Field(default=None, description="""Indicates if this media set's main content is LOCAL or OFF-SITE.""", json_schema_extra = { "linkml_meta": {'alias': 'media_location',
         'domain_of': ['MediaSet'],
         'examples': [{'value': 'L'}]} })
    media_source: Optional[str] = Field(default=None, description="""Indicates the initial primary source of the media set.""", json_schema_extra = { "linkml_meta": {'alias': 'media_source',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': 'MEDIA_API_UPLOAD'}]} })
    date_added: Optional[datetime ] = Field(default=None, description="""Date this media set was first created. (UTC)""", json_schema_extra = { "linkml_meta": {'alias': 'date_added',
         'domain_of': ['MediaSet'],
         'examples': [{'value': '1992-03-08T11:23:44.123+00:00'}]} })
    date_updated: Optional[datetime ] = Field(default=None, description="""Date this media set was most recently modified. (UTC)""", json_schema_extra = { "linkml_meta": {'alias': 'date_updated',
         'domain_of': ['MediaSet'],
         'examples': [{'value': '2009-11-05T08:33:12.231+00:00'}]} })
    date_valid_end: Optional[datetime ] = Field(default=None, description="""If present, date and time when media association was removed or replaced. (UTC)""", json_schema_extra = { "linkml_meta": {'alias': 'date_valid_end',
         'domain_of': ['MediaSet'],
         'examples': [{'value': '2021-02-15T12:32:11.332+00:00'}]} })
    files: Optional[list[MediaFile]] = Field(default=None, description="""Array of all files, including original submission of file or URL along with any derived files during processing of media.""", json_schema_extra = { "linkml_meta": {'alias': 'files', 'domain_of': ['MediaSet']} })

    @field_validator('access_limitations')
    def pattern_access_limitations(cls, v):
        pattern=re.compile(r"^.{0,5}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid access_limitations format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid access_limitations format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('media_title')
    def pattern_media_title(cls, v):
        pattern=re.compile(r"^.{0,500}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid media_title format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid media_title format: {v}"
            raise ValueError(err_msg)
        return v


class MediaFile(ConfiguredBaseModel):
    """
    Metadata information pertaining to a particular media resource associated with this product.  Contains information about its disposition, content, and processing state.  Each individual file is uniquely identified by its `MEDIA_FILE_ID` value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    media_file_id: Optional[int] = Field(default=None, description="""Unique identifier for a given MEDIA FILE.""", json_schema_extra = { "linkml_meta": {'alias': 'media_file_id',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '983445'}]} })
    media_id: Optional[int] = Field(default=None, description="""Link to parent MEDIA SET ID.""", json_schema_extra = { "linkml_meta": {'alias': 'media_id',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': '233743'}]} })
    checksum: Optional[str] = Field(default=None, description="""Calculated hash or checksum value of the physical file as applicable, from media processing.""", json_schema_extra = { "linkml_meta": {'alias': 'checksum',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '85a88fc60dab52214508631f3dd93f1ada3e6e8cd00d09a58608054d8e5ded38'}]} })
    revision: Optional[int] = Field(default=None, description="""Revision number of this media file, associated with the MEDIA SET""", json_schema_extra = { "linkml_meta": {'alias': 'revision',
         'domain_of': ['Record', 'MediaSet', 'MediaFile'],
         'examples': [{'value': '1'}]} })
    parent_media_file_id: Optional[int] = Field(default=None, description="""If non-zero, indicates unique MEDIA FILE ID this MEDIA FILE is derived from.""", json_schema_extra = { "linkml_meta": {'alias': 'parent_media_file_id',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '0'}]} })
    status: Optional[str] = Field(default=None, description="""Indiciates current processing status for this MEDIA FILE. Other values may indicate awaiting additional processing, such as 'OCR', pending text processing.""", json_schema_extra = { "linkml_meta": {'alias': 'status',
         'domain_of': ['AuditLog', 'MediaSet', 'MediaFile'],
         'examples': [{'value': 'DONE'}]} })
    media_type: Optional[str] = Field(default=None, description="""Indicates TYPE of media file, detected or set during media processing.""", json_schema_extra = { "linkml_meta": {'alias': 'media_type',
         'domain_of': ['MediaFile'],
         'examples': [{'value': 'T'}]} })
    url_type: Optional[MediaLocationEnum] = Field(default=None, description="""Indicates if the file is LOCALLY HOSTED ('L') or OFF-SITE URL ('O').""", json_schema_extra = { "linkml_meta": {'alias': 'url_type', 'domain_of': ['MediaFile'], 'examples': [{'value': 'L'}]} })
    url: Optional[str] = Field(default=None, description="""Either the file name for local files, or URL path to off-site resource.""", json_schema_extra = { "linkml_meta": {'alias': 'url',
         'domain_of': ['MediaFile'],
         'examples': [{'value': 'report.pdf'}]} })
    mime_type: Optional[str] = Field(default=None, description="""Mime type describing the MEDIA FILE content.""", json_schema_extra = { "linkml_meta": {'alias': 'mime_type',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': 'application/pdf'}]} })
    added_by_user_id: Optional[int] = Field(default=None, description="""Indicates the E-Link USER ID that attached this MEDIA FILE.""", json_schema_extra = { "linkml_meta": {'alias': 'added_by_user_id',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '118678'}]} })
    media_source: Optional[str] = Field(default=None, description="""Describes method of file production or association with this media set.""", json_schema_extra = { "linkml_meta": {'alias': 'media_source',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': 'TEXT_FILE_EXTRACTION'}]} })
    file_size_bytes: Optional[int] = Field(default=None, description="""If local file, the file size in bytes.""", json_schema_extra = { "linkml_meta": {'alias': 'file_size_bytes',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '993834'}]} })
    duration_seconds: Optional[int] = Field(default=None, description="""For audio-visual media, the duration of the resource in seconds.""", json_schema_extra = { "linkml_meta": {'alias': 'duration_seconds',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '77'}]} })
    document_page_count: Optional[int] = Field(default=None, description="""For document-based media, the number of printed pages if applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'document_page_count',
         'domain_of': ['MediaSet', 'MediaFile'],
         'examples': [{'value': '22'}]} })
    subtitle_tracks: Optional[int] = Field(default=None, description="""Indicates the number of subtitle tracks for audio-visual media.""", json_schema_extra = { "linkml_meta": {'alias': 'subtitle_tracks',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '2'}]} })
    video_tracks: Optional[int] = Field(default=None, description="""Indicates the number of video tracks in audio-visual media.""", json_schema_extra = { "linkml_meta": {'alias': 'video_tracks',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '1'}]} })
    pdf_version: Optional[str] = Field(default=None, description="""For PDF media files, indicates the version of PDF.""", json_schema_extra = { "linkml_meta": {'alias': 'pdf_version',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '1.5'}]} })
    pdfa_conformance: Optional[str] = Field(default=None, description="""For PDF media that is PDF/A compliant, the conformance level, generally A, B, or U.""", json_schema_extra = { "linkml_meta": {'alias': 'pdfa_conformance',
         'domain_of': ['MediaFile'],
         'examples': [{'value': 'A'}]} })
    pdfa_part: Optional[str] = Field(default=None, description="""For PDF media that is PDF/A compliant, the level of compliance, as a value between 1 and 4.""", json_schema_extra = { "linkml_meta": {'alias': 'pdfa_part', 'domain_of': ['MediaFile'], 'examples': [{'value': '1'}]} })
    pdfua_part: Optional[str] = Field(default=None, description="""For PDF media that is PDF/UA compliant, its compliance level, generally 1 or 2.""", json_schema_extra = { "linkml_meta": {'alias': 'pdfua_part',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '2'}]} })
    date_file_added: Optional[datetime ] = Field(default=None, description="""Indicates the date and time this media file was created.""", json_schema_extra = { "linkml_meta": {'alias': 'date_file_added',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '2012-08-33T15:33:22.504+00:00'}]} })
    date_file_updated: Optional[datetime ] = Field(default=None, description="""Indicates the last date and time this media file was modified.""", json_schema_extra = { "linkml_meta": {'alias': 'date_file_updated',
         'domain_of': ['MediaFile'],
         'examples': [{'value': '2013-04-22T18:33:28.234+00:00'}]} })

    @field_validator('media_type')
    def pattern_media_type(cls, v):
        pattern=re.compile(r"^.{0,1}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid media_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid media_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('url_type')
    def pattern_url_type(cls, v):
        pattern=re.compile(r"^.{0,1}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid url_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid url_type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('url')
    def pattern_url(cls, v):
        pattern=re.compile(r"^.{0,255}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid url format: {v}"
            raise ValueError(err_msg)
        return v


class Organization(ConfiguredBaseModel):
    """
    Describes a particular organization associated with the bibliographic record. Organizations may be author collaborations, sponsors, research laboratories, or contributors to the work, as indicated by their associated type. For identification purposes, at least one of either 'name' or 'ror_id' is required for validation.  If ROR ID is specified, it will be validated against the ROR authority at OSTI.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: OrganizationType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person']} })
    name: str = Field(default=..., description="""Name of the organization""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Organization', 'Affiliation'],
         'examples': [{'value': 'Quantum Physics of America, Inc.'}]} })
    contributor_type: Optional[ContributorType] = Field(default=None, description="""Indicate the contribution made by this Organization.  Required for CONTRIBUTING 'type'.""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_type',
         'domain_of': ['Organization', 'Person'],
         'examples': [{'value': 'DataCollector'}]} })
    ror_id: Optional[str] = Field(default=None, description="""ROR ID for this organization, if any. This value will be validated against the ROR authority.""", json_schema_extra = { "linkml_meta": {'alias': 'ror_id',
         'domain_of': ['Organization', 'Affiliation'],
         'examples': [{'value': '31478740'}]} })
    identifiers: Optional[list[OrganizationIdentifier]] = Field(default=None, description="""List of any identifiers for this Organization.  Only applicable to Sponsoring organizations.""", json_schema_extra = { "linkml_meta": {'alias': 'identifiers', 'domain_of': ['Record', 'Organization']} })

    @field_validator('type')
    def pattern_type(cls, v):
        pattern=re.compile(r"^.{0,20}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('name')
    def pattern_name(cls, v):
        pattern=re.compile(r"^.{0,800}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('contributor_type')
    def pattern_contributor_type(cls, v):
        pattern=re.compile(r"^.{0,25}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid contributor_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid contributor_type format: {v}"
            raise ValueError(err_msg)
        return v


class OrganizationIdentifier(ConfiguredBaseModel):
    """
    One or more identifying numbers or references associated with this organization.  Please note that only sponsoring organizations may have associated identifier values.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: OrganizationIdentifierType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person'],
         'examples': [{'value': 'AWARD_DOI'}]} })
    value: str = Field(default=..., description="""Indicates the value of this identifier.  May be validated according to its particular type.""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['RelatedIdentifier', 'Identifier', 'OrganizationIdentifier'],
         'examples': [{'value': '10.11578/289342'}]} })

    @field_validator('type')
    def pattern_type(cls, v):
        pattern=re.compile(r"^.{0,20}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v


class Person(ConfiguredBaseModel):
    """
    Information about a particular person involved in the production or maintenance of this record
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    type: PersonType = Field(default=..., json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['RelatedIdentifier',
                       'Geolocation',
                       'Identifier',
                       'AuditLog',
                       'Organization',
                       'OrganizationIdentifier',
                       'Person']} })
    first_name: Optional[str] = Field(default=None, description="""First (or 'Given') name of the person""", json_schema_extra = { "linkml_meta": {'alias': 'first_name',
         'domain_of': ['Person'],
         'examples': [{'value': 'Sample'}]} })
    middle_name: Optional[str] = Field(default=None, description="""Middle name or initial of the person""", json_schema_extra = { "linkml_meta": {'alias': 'middle_name', 'domain_of': ['Person'], 'examples': [{'value': 'Q.'}]} })
    last_name: Optional[str] = Field(default=None, description="""Last (or 'Family') name of this person""", json_schema_extra = { "linkml_meta": {'alias': 'last_name',
         'domain_of': ['Person'],
         'examples': [{'value': 'Person'}]} })
    email: Optional[list[str]] = Field(default=None, description="""List of any email address(es) associated with this person. Email addresses are validated to be well-formed.""", json_schema_extra = { "linkml_meta": {'alias': 'email',
         'domain_of': ['Person'],
         'examples': [{'value': 'persons@sample.org'}]} })
    orcid: Optional[str] = Field(default=None, description="""ORCID (https://orcid.org/) value for this person. ORCID values, if provided, must be of valid format.""", json_schema_extra = { "linkml_meta": {'alias': 'orcid',
         'domain_of': ['Person'],
         'examples': [{'value': '0000-0001-2345-6789'}]} })
    phone: Optional[str] = Field(default=None, description="""Contact phone number for this person, if available. If provided, must be a valid phone number expression.""", json_schema_extra = { "linkml_meta": {'alias': 'phone',
         'domain_of': ['Person'],
         'examples': [{'value': '(555) 860-9923'}]} })
    osti_user_id: Optional[int] = Field(default=None, description="""OSTI-assigned identifier for this person, if any""", json_schema_extra = { "linkml_meta": {'alias': 'osti_user_id', 'domain_of': ['Person']} })
    contributor_type: Optional[ContributorType] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'contributor_type', 'domain_of': ['Organization', 'Person']} })
    affiliations: Optional[list[Affiliation]] = Field(default=None, description="""List of any affiliations for this person.  At least one of either 'name' and/or 'ror_id' is required; if ROR ID is provided, the value will be validated against the OSTI ROR authority.""", json_schema_extra = { "linkml_meta": {'alias': 'affiliations', 'domain_of': ['Person']} })

    @field_validator('type')
    def pattern_type(cls, v):
        pattern=re.compile(r"^.{0,20}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('first_name')
    def pattern_first_name(cls, v):
        pattern=re.compile(r"^.{0,50}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid first_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid first_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('middle_name')
    def pattern_middle_name(cls, v):
        pattern=re.compile(r"^.{0,50}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid middle_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid middle_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('last_name')
    def pattern_last_name(cls, v):
        pattern=re.compile(r"^.{0,60}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid last_name format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid last_name format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('phone')
    def pattern_phone(cls, v):
        pattern=re.compile(r"^.{0,30}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid phone format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid phone format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('contributor_type')
    def pattern_contributor_type(cls, v):
        pattern=re.compile(r"^.{0,25}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid contributor_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid contributor_type format: {v}"
            raise ValueError(err_msg)
        return v


class Affiliation(ConfiguredBaseModel):
    """
    An affiliation for a person, such as an organization or institution.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/brc/osti_schema'})

    name: Optional[str] = Field(default=None, description="""Name of the institution or laboratory with which this person is affiliated.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Organization', 'Affiliation'],
         'examples': [{'value': 'Dutch Industries Research Laboratory, Oakland, CA'}]} })
    ror_id: Optional[str] = Field(default=None, description="""ROR ID of this affiliation, if any.  Will be validated against ROR organization authority if present.""", json_schema_extra = { "linkml_meta": {'alias': 'ror_id',
         'domain_of': ['Organization', 'Affiliation'],
         'examples': [{'value': '02x0wxr53'}]} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Records.model_rebuild()
Record.model_rebuild()
RelatedIdentifier.model_rebuild()
Geolocation.model_rebuild()
Point.model_rebuild()
Identifier.model_rebuild()
AuditLog.model_rebuild()
MediaSet.model_rebuild()
MediaFile.model_rebuild()
Organization.model_rebuild()
OrganizationIdentifier.model_rebuild()
Person.model_rebuild()
Affiliation.model_rebuild()

