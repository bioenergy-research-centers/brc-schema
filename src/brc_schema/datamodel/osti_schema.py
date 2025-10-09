# Auto generated from osti_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-10-02T11:31:12
# Schema: osti_schema
#
# id: https://w3id.org/brc/osti_schema
# description: This schema is a LinkML representation of the OSTI Submission Metadata schema, as described here: https://www.osti.gov/elink2api/ and here: https://www.osti.gov/elink2api/record-schema OSTI uses the E-Link API infrastructure. This schema corresponds to the E-Link 2.0 API (2.6.2). It also contains some deprecated fields to support backward compatibility with older records (e.g., article_type has been replaced by product_type, but some records still use the former).
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Datetime, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDateTime

metamodel_version = "1.7.0"
version = "2.6.2"

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OSTI = CurieNamespace('osti', 'https://www.osti.gov/biblio/')
DEFAULT_ = OSTI


# Types

# Class references
class RecordOstiId(extended_int):
    pass


@dataclass(repr=False)
class Records(YAMLRoot):
    """
    A list of Record metadata.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Records"]
    class_class_curie: ClassVar[str] = "osti:Records"
    class_name: ClassVar[str] = "records"
    class_model_uri: ClassVar[URIRef] = OSTI.Records

    records: Optional[Union[Union[int, RecordOstiId], list[Union[int, RecordOstiId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.records, list):
            self.records = [self.records] if self.records is not None else []
        self.records = [v if isinstance(v, RecordOstiId) else RecordOstiId(v) for v in self.records]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Record(YAMLRoot):
    """
    Defines the bibliographic metadata about a particular work or record. Depending on product type, various elements
    are permitted, not permitted, or required.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Record"]
    class_class_curie: ClassVar[str] = "osti:Record"
    class_name: ClassVar[str] = "Record"
    class_model_uri: ClassVar[URIRef] = OSTI.Record

    osti_id: Union[int, RecordOstiId] = None
    access_limitations: Union[Union[str, "AccessLimitationsEnum"], list[Union[str, "AccessLimitationsEnum"]]] = None
    title: str = None
    publication_date: Union[str, XSDDateTime] = None
    identifiers: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()
    issue: Optional[str] = None
    journal_license_url: Optional[str] = None
    journal_name: Optional[str] = None
    journal_open_access_flag: Optional[str] = None
    journal_type: Optional[str] = None
    revision: Optional[int] = None
    workflow_status: Optional[Union[str, "WorkflowStatusEnum"]] = None
    access_limitation_other: Optional[str] = None
    added_by: Optional[int] = None
    added_by_email: Optional[str] = None
    added_by_name: Optional[str] = None
    announcement_codes: Optional[Union[str, list[str]]] = empty_list()
    edition: Optional[str] = None
    volume: Optional[str] = None
    collection_type: Optional[Union[str, "CollectionTypeEnum"]] = None
    conference_information: Optional[str] = None
    conference_type: Optional[str] = None
    contract_award_date: Optional[Union[str, XSDDateTime]] = None
    country_publication_code: Optional[str] = None
    date_metadata_added: Optional[Union[str, XSDDateTime]] = None
    date_metadata_updated: Optional[Union[str, XSDDateTime]] = None
    date_submitted_to_osti_first: Optional[Union[str, XSDDateTime]] = None
    date_submitted_to_osti_last: Optional[Union[str, XSDDateTime]] = None
    date_released_first: Optional[Union[str, XSDDateTime]] = None
    date_released_last: Optional[Union[str, XSDDateTime]] = None
    description: Optional[str] = None
    descriptors: Optional[Union[str, list[str]]] = empty_list()
    doe_funded_flag: Optional[str] = None
    doi: Optional[str] = None
    doi_infix: Optional[str] = None
    edited_by: Optional[int] = None
    edited_by_email: Optional[str] = None
    edited_by_name: Optional[str] = None
    edit_reason: Optional[str] = None
    edit_source: Optional[str] = None
    format_information: Optional[str] = None
    media_embargo_sunset_date: Optional[str] = None
    publication_date_text: Optional[str] = None
    publisher_information: Optional[str] = None
    related_doc_info: Optional[str] = None
    keywords: Optional[Union[str, list[str]]] = empty_list()
    languages: Optional[Union[str, list[str]]] = empty_list()
    audit_logs: Optional[Union[Union[dict, "AuditLog"], list[Union[dict, "AuditLog"]]]] = empty_list()
    media: Optional[Union[Union[dict, "MediaSet"], list[Union[dict, "MediaSet"]]]] = empty_list()
    opn_addressee: Optional[str] = None
    opn_declassified_date: Optional[str] = None
    opn_declassified_status: Optional[str] = None
    opn_document_categories: Optional[Union[str, list[str]]] = empty_list()
    opn_document_location: Optional[str] = None
    opn_fieldoffice_acronym_code: Optional[str] = None
    organizations: Optional[Union[Union[dict, "Organization"], list[Union[dict, "Organization"]]]] = empty_list()
    other_information: Optional[Union[str, list[str]]] = empty_list()
    ouo_release_date: Optional[str] = None
    paper_flag: Optional[Union[bool, Bool]] = None
    hidden_flag: Optional[Union[bool, Bool]] = None
    sensitivity_flag: Optional[str] = None
    doe_supported_flag: Optional[Union[bool, Bool]] = None
    peer_reviewed_flag: Optional[Union[bool, Bool]] = None
    patent_assignee: Optional[str] = None
    patent_file_date: Optional[Union[str, XSDDateTime]] = None
    patent_priority_date: Optional[Union[str, XSDDateTime]] = None
    pdouo_exemption_number: Optional[str] = None
    persons: Optional[Union[Union[dict, "Person"], list[Union[dict, "Person"]]]] = empty_list()
    product_size: Optional[str] = None
    product_type: Optional[Union[str, "ProductType"]] = None
    product_type_other: Optional[str] = None
    prot_flag: Optional[str] = None
    prot_data_other: Optional[str] = None
    prot_release_date: Optional[Union[str, XSDDateTime]] = None
    availability: Optional[str] = None
    subject_category_code: Optional[Union[str, list[str]]] = empty_list()
    subject_category_code_legacy: Optional[Union[str, list[str]]] = empty_list()
    related_identifiers: Optional[Union[Union[dict, "RelatedIdentifier"], list[Union[dict, "RelatedIdentifier"]]]] = empty_list()
    released_to_osti_date: Optional[Union[str, XSDDateTime]] = None
    releasing_official_comments: Optional[str] = None
    report_period_end_date: Optional[Union[str, XSDDateTime]] = None
    report_period_start_date: Optional[Union[str, XSDDateTime]] = None
    report_types: Optional[Union[str, list[str]]] = empty_list()
    report_type_other: Optional[str] = None
    sbiz_flag: Optional[str] = None
    sbiz_phase: Optional[str] = None
    sbiz_previous_contract_number: Optional[str] = None
    sbiz_release_date: Optional[Union[str, XSDDateTime]] = None
    site_ownership_code: Optional[str] = None
    site_unique_id: Optional[str] = None
    site_url: Optional[str] = None
    source_input_type: Optional[str] = None
    source_edit_type: Optional[str] = None
    geolocations: Optional[Union[Union[dict, "Geolocation"], list[Union[dict, "Geolocation"]]]] = empty_list()
    article_type: Optional[str] = None
    authors: Optional[Union[str, list[str]]] = empty_list()
    conference_info: Optional[str] = None
    contract_number: Optional[str] = None
    country_publication: Optional[str] = None
    doe_contract_number: Optional[str] = None
    entry_date: Optional[Union[str, XSDDateTime]] = None
    identifier: Optional[Union[str, list[str]]] = empty_list()
    language: Optional[Union[str, list[str]]] = empty_list()
    links: Optional[Union[str, list[str]]] = empty_list()
    other_identifiers: Optional[Union[str, list[str]]] = empty_list()
    other_number: Optional[Union[str, list[str]]] = empty_list()
    report_number: Optional[Union[str, list[str]]] = empty_list()
    research_orgs: Optional[Union[str, list[str]]] = empty_list()
    sponsor_orgs: Optional[Union[str, list[str]]] = empty_list()
    subjects: Optional[Union[str, list[str]]] = empty_list()
    journal_issn: Optional[str] = None
    journal_issue: Optional[str] = None
    journal_volume: Optional[str] = None
    publisher: Optional[str] = None
    relation: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.osti_id):
            self.MissingRequiredField("osti_id")
        if not isinstance(self.osti_id, RecordOstiId):
            self.osti_id = RecordOstiId(self.osti_id)

        if self._is_empty(self.access_limitations):
            self.MissingRequiredField("access_limitations")
        if not isinstance(self.access_limitations, list):
            self.access_limitations = [self.access_limitations] if self.access_limitations is not None else []
        self.access_limitations = [v if isinstance(v, AccessLimitationsEnum) else AccessLimitationsEnum(v) for v in self.access_limitations]

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.publication_date):
            self.MissingRequiredField("publication_date")
        if not isinstance(self.publication_date, XSDDateTime):
            self.publication_date = XSDDateTime(self.publication_date)

        if not isinstance(self.identifiers, list):
            self.identifiers = [self.identifiers] if self.identifiers is not None else []
        self.identifiers = [v if isinstance(v, Identifier) else Identifier(**as_dict(v)) for v in self.identifiers]

        if self.issue is not None and not isinstance(self.issue, str):
            self.issue = str(self.issue)

        if self.journal_license_url is not None and not isinstance(self.journal_license_url, str):
            self.journal_license_url = str(self.journal_license_url)

        if self.journal_name is not None and not isinstance(self.journal_name, str):
            self.journal_name = str(self.journal_name)

        if self.journal_open_access_flag is not None and not isinstance(self.journal_open_access_flag, str):
            self.journal_open_access_flag = str(self.journal_open_access_flag)

        if self.journal_type is not None and not isinstance(self.journal_type, str):
            self.journal_type = str(self.journal_type)

        if self.revision is not None and not isinstance(self.revision, int):
            self.revision = int(self.revision)

        if self.workflow_status is not None and not isinstance(self.workflow_status, WorkflowStatusEnum):
            self.workflow_status = WorkflowStatusEnum(self.workflow_status)

        if self.access_limitation_other is not None and not isinstance(self.access_limitation_other, str):
            self.access_limitation_other = str(self.access_limitation_other)

        if self.added_by is not None and not isinstance(self.added_by, int):
            self.added_by = int(self.added_by)

        if self.added_by_email is not None and not isinstance(self.added_by_email, str):
            self.added_by_email = str(self.added_by_email)

        if self.added_by_name is not None and not isinstance(self.added_by_name, str):
            self.added_by_name = str(self.added_by_name)

        if not isinstance(self.announcement_codes, list):
            self.announcement_codes = [self.announcement_codes] if self.announcement_codes is not None else []
        self.announcement_codes = [v if isinstance(v, str) else str(v) for v in self.announcement_codes]

        if self.edition is not None and not isinstance(self.edition, str):
            self.edition = str(self.edition)

        if self.volume is not None and not isinstance(self.volume, str):
            self.volume = str(self.volume)

        if self.collection_type is not None and not isinstance(self.collection_type, CollectionTypeEnum):
            self.collection_type = CollectionTypeEnum(self.collection_type)

        if self.conference_information is not None and not isinstance(self.conference_information, str):
            self.conference_information = str(self.conference_information)

        if self.conference_type is not None and not isinstance(self.conference_type, str):
            self.conference_type = str(self.conference_type)

        if self.contract_award_date is not None and not isinstance(self.contract_award_date, XSDDateTime):
            self.contract_award_date = XSDDateTime(self.contract_award_date)

        if self.country_publication_code is not None and not isinstance(self.country_publication_code, str):
            self.country_publication_code = str(self.country_publication_code)

        if self.date_metadata_added is not None and not isinstance(self.date_metadata_added, XSDDateTime):
            self.date_metadata_added = XSDDateTime(self.date_metadata_added)

        if self.date_metadata_updated is not None and not isinstance(self.date_metadata_updated, XSDDateTime):
            self.date_metadata_updated = XSDDateTime(self.date_metadata_updated)

        if self.date_submitted_to_osti_first is not None and not isinstance(self.date_submitted_to_osti_first, XSDDateTime):
            self.date_submitted_to_osti_first = XSDDateTime(self.date_submitted_to_osti_first)

        if self.date_submitted_to_osti_last is not None and not isinstance(self.date_submitted_to_osti_last, XSDDateTime):
            self.date_submitted_to_osti_last = XSDDateTime(self.date_submitted_to_osti_last)

        if self.date_released_first is not None and not isinstance(self.date_released_first, XSDDateTime):
            self.date_released_first = XSDDateTime(self.date_released_first)

        if self.date_released_last is not None and not isinstance(self.date_released_last, XSDDateTime):
            self.date_released_last = XSDDateTime(self.date_released_last)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.descriptors, list):
            self.descriptors = [self.descriptors] if self.descriptors is not None else []
        self.descriptors = [v if isinstance(v, str) else str(v) for v in self.descriptors]

        if self.doe_funded_flag is not None and not isinstance(self.doe_funded_flag, str):
            self.doe_funded_flag = str(self.doe_funded_flag)

        if self.doi is not None and not isinstance(self.doi, str):
            self.doi = str(self.doi)

        if self.doi_infix is not None and not isinstance(self.doi_infix, str):
            self.doi_infix = str(self.doi_infix)

        if self.edited_by is not None and not isinstance(self.edited_by, int):
            self.edited_by = int(self.edited_by)

        if self.edited_by_email is not None and not isinstance(self.edited_by_email, str):
            self.edited_by_email = str(self.edited_by_email)

        if self.edited_by_name is not None and not isinstance(self.edited_by_name, str):
            self.edited_by_name = str(self.edited_by_name)

        if self.edit_reason is not None and not isinstance(self.edit_reason, str):
            self.edit_reason = str(self.edit_reason)

        if self.edit_source is not None and not isinstance(self.edit_source, str):
            self.edit_source = str(self.edit_source)

        if self.format_information is not None and not isinstance(self.format_information, str):
            self.format_information = str(self.format_information)

        if self.media_embargo_sunset_date is not None and not isinstance(self.media_embargo_sunset_date, str):
            self.media_embargo_sunset_date = str(self.media_embargo_sunset_date)

        if self.publication_date_text is not None and not isinstance(self.publication_date_text, str):
            self.publication_date_text = str(self.publication_date_text)

        if self.publisher_information is not None and not isinstance(self.publisher_information, str):
            self.publisher_information = str(self.publisher_information)

        if self.related_doc_info is not None and not isinstance(self.related_doc_info, str):
            self.related_doc_info = str(self.related_doc_info)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if not isinstance(self.languages, list):
            self.languages = [self.languages] if self.languages is not None else []
        self.languages = [v if isinstance(v, str) else str(v) for v in self.languages]

        if not isinstance(self.audit_logs, list):
            self.audit_logs = [self.audit_logs] if self.audit_logs is not None else []
        self.audit_logs = [v if isinstance(v, AuditLog) else AuditLog(**as_dict(v)) for v in self.audit_logs]

        if not isinstance(self.media, list):
            self.media = [self.media] if self.media is not None else []
        self.media = [v if isinstance(v, MediaSet) else MediaSet(**as_dict(v)) for v in self.media]

        if self.opn_addressee is not None and not isinstance(self.opn_addressee, str):
            self.opn_addressee = str(self.opn_addressee)

        if self.opn_declassified_date is not None and not isinstance(self.opn_declassified_date, str):
            self.opn_declassified_date = str(self.opn_declassified_date)

        if self.opn_declassified_status is not None and not isinstance(self.opn_declassified_status, str):
            self.opn_declassified_status = str(self.opn_declassified_status)

        if not isinstance(self.opn_document_categories, list):
            self.opn_document_categories = [self.opn_document_categories] if self.opn_document_categories is not None else []
        self.opn_document_categories = [v if isinstance(v, str) else str(v) for v in self.opn_document_categories]

        if self.opn_document_location is not None and not isinstance(self.opn_document_location, str):
            self.opn_document_location = str(self.opn_document_location)

        if self.opn_fieldoffice_acronym_code is not None and not isinstance(self.opn_fieldoffice_acronym_code, str):
            self.opn_fieldoffice_acronym_code = str(self.opn_fieldoffice_acronym_code)

        self._normalize_inlined_as_dict(slot_name="organizations", slot_type=Organization, key_name="type", keyed=False)

        if not isinstance(self.other_information, list):
            self.other_information = [self.other_information] if self.other_information is not None else []
        self.other_information = [v if isinstance(v, str) else str(v) for v in self.other_information]

        if self.ouo_release_date is not None and not isinstance(self.ouo_release_date, str):
            self.ouo_release_date = str(self.ouo_release_date)

        if self.paper_flag is not None and not isinstance(self.paper_flag, Bool):
            self.paper_flag = Bool(self.paper_flag)

        if self.hidden_flag is not None and not isinstance(self.hidden_flag, Bool):
            self.hidden_flag = Bool(self.hidden_flag)

        if self.sensitivity_flag is not None and not isinstance(self.sensitivity_flag, str):
            self.sensitivity_flag = str(self.sensitivity_flag)

        if self.doe_supported_flag is not None and not isinstance(self.doe_supported_flag, Bool):
            self.doe_supported_flag = Bool(self.doe_supported_flag)

        if self.peer_reviewed_flag is not None and not isinstance(self.peer_reviewed_flag, Bool):
            self.peer_reviewed_flag = Bool(self.peer_reviewed_flag)

        if self.patent_assignee is not None and not isinstance(self.patent_assignee, str):
            self.patent_assignee = str(self.patent_assignee)

        if self.patent_file_date is not None and not isinstance(self.patent_file_date, XSDDateTime):
            self.patent_file_date = XSDDateTime(self.patent_file_date)

        if self.patent_priority_date is not None and not isinstance(self.patent_priority_date, XSDDateTime):
            self.patent_priority_date = XSDDateTime(self.patent_priority_date)

        if self.pdouo_exemption_number is not None and not isinstance(self.pdouo_exemption_number, str):
            self.pdouo_exemption_number = str(self.pdouo_exemption_number)

        self._normalize_inlined_as_dict(slot_name="persons", slot_type=Person, key_name="type", keyed=False)

        if self.product_size is not None and not isinstance(self.product_size, str):
            self.product_size = str(self.product_size)

        if self.product_type is not None and not isinstance(self.product_type, ProductType):
            self.product_type = ProductType(self.product_type)

        if self.product_type_other is not None and not isinstance(self.product_type_other, str):
            self.product_type_other = str(self.product_type_other)

        if self.prot_flag is not None and not isinstance(self.prot_flag, str):
            self.prot_flag = str(self.prot_flag)

        if self.prot_data_other is not None and not isinstance(self.prot_data_other, str):
            self.prot_data_other = str(self.prot_data_other)

        if self.prot_release_date is not None and not isinstance(self.prot_release_date, XSDDateTime):
            self.prot_release_date = XSDDateTime(self.prot_release_date)

        if self.availability is not None and not isinstance(self.availability, str):
            self.availability = str(self.availability)

        if not isinstance(self.subject_category_code, list):
            self.subject_category_code = [self.subject_category_code] if self.subject_category_code is not None else []
        self.subject_category_code = [v if isinstance(v, str) else str(v) for v in self.subject_category_code]

        if not isinstance(self.subject_category_code_legacy, list):
            self.subject_category_code_legacy = [self.subject_category_code_legacy] if self.subject_category_code_legacy is not None else []
        self.subject_category_code_legacy = [v if isinstance(v, str) else str(v) for v in self.subject_category_code_legacy]

        self._normalize_inlined_as_dict(slot_name="related_identifiers", slot_type=RelatedIdentifier, key_name="type", keyed=False)

        if self.released_to_osti_date is not None and not isinstance(self.released_to_osti_date, XSDDateTime):
            self.released_to_osti_date = XSDDateTime(self.released_to_osti_date)

        if self.releasing_official_comments is not None and not isinstance(self.releasing_official_comments, str):
            self.releasing_official_comments = str(self.releasing_official_comments)

        if self.report_period_end_date is not None and not isinstance(self.report_period_end_date, XSDDateTime):
            self.report_period_end_date = XSDDateTime(self.report_period_end_date)

        if self.report_period_start_date is not None and not isinstance(self.report_period_start_date, XSDDateTime):
            self.report_period_start_date = XSDDateTime(self.report_period_start_date)

        if not isinstance(self.report_types, list):
            self.report_types = [self.report_types] if self.report_types is not None else []
        self.report_types = [v if isinstance(v, str) else str(v) for v in self.report_types]

        if self.report_type_other is not None and not isinstance(self.report_type_other, str):
            self.report_type_other = str(self.report_type_other)

        if self.sbiz_flag is not None and not isinstance(self.sbiz_flag, str):
            self.sbiz_flag = str(self.sbiz_flag)

        if self.sbiz_phase is not None and not isinstance(self.sbiz_phase, str):
            self.sbiz_phase = str(self.sbiz_phase)

        if self.sbiz_previous_contract_number is not None and not isinstance(self.sbiz_previous_contract_number, str):
            self.sbiz_previous_contract_number = str(self.sbiz_previous_contract_number)

        if self.sbiz_release_date is not None and not isinstance(self.sbiz_release_date, XSDDateTime):
            self.sbiz_release_date = XSDDateTime(self.sbiz_release_date)

        if self.site_ownership_code is not None and not isinstance(self.site_ownership_code, str):
            self.site_ownership_code = str(self.site_ownership_code)

        if self.site_unique_id is not None and not isinstance(self.site_unique_id, str):
            self.site_unique_id = str(self.site_unique_id)

        if self.site_url is not None and not isinstance(self.site_url, str):
            self.site_url = str(self.site_url)

        if self.source_input_type is not None and not isinstance(self.source_input_type, str):
            self.source_input_type = str(self.source_input_type)

        if self.source_edit_type is not None and not isinstance(self.source_edit_type, str):
            self.source_edit_type = str(self.source_edit_type)

        self._normalize_inlined_as_dict(slot_name="geolocations", slot_type=Geolocation, key_name="points", keyed=False)

        if self.article_type is not None and not isinstance(self.article_type, str):
            self.article_type = str(self.article_type)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [v if isinstance(v, str) else str(v) for v in self.authors]

        if self.conference_info is not None and not isinstance(self.conference_info, str):
            self.conference_info = str(self.conference_info)

        if self.contract_number is not None and not isinstance(self.contract_number, str):
            self.contract_number = str(self.contract_number)

        if self.country_publication is not None and not isinstance(self.country_publication, str):
            self.country_publication = str(self.country_publication)

        if self.doe_contract_number is not None and not isinstance(self.doe_contract_number, str):
            self.doe_contract_number = str(self.doe_contract_number)

        if self.entry_date is not None and not isinstance(self.entry_date, XSDDateTime):
            self.entry_date = XSDDateTime(self.entry_date)

        if not isinstance(self.identifier, list):
            self.identifier = [self.identifier] if self.identifier is not None else []
        self.identifier = [v if isinstance(v, str) else str(v) for v in self.identifier]

        if not isinstance(self.language, list):
            self.language = [self.language] if self.language is not None else []
        self.language = [v if isinstance(v, str) else str(v) for v in self.language]

        if not isinstance(self.links, list):
            self.links = [self.links] if self.links is not None else []
        self.links = [v if isinstance(v, str) else str(v) for v in self.links]

        if not isinstance(self.other_identifiers, list):
            self.other_identifiers = [self.other_identifiers] if self.other_identifiers is not None else []
        self.other_identifiers = [v if isinstance(v, str) else str(v) for v in self.other_identifiers]

        if not isinstance(self.other_number, list):
            self.other_number = [self.other_number] if self.other_number is not None else []
        self.other_number = [v if isinstance(v, str) else str(v) for v in self.other_number]

        if not isinstance(self.report_number, list):
            self.report_number = [self.report_number] if self.report_number is not None else []
        self.report_number = [v if isinstance(v, str) else str(v) for v in self.report_number]

        if not isinstance(self.research_orgs, list):
            self.research_orgs = [self.research_orgs] if self.research_orgs is not None else []
        self.research_orgs = [v if isinstance(v, str) else str(v) for v in self.research_orgs]

        if not isinstance(self.sponsor_orgs, list):
            self.sponsor_orgs = [self.sponsor_orgs] if self.sponsor_orgs is not None else []
        self.sponsor_orgs = [v if isinstance(v, str) else str(v) for v in self.sponsor_orgs]

        if not isinstance(self.subjects, list):
            self.subjects = [self.subjects] if self.subjects is not None else []
        self.subjects = [v if isinstance(v, str) else str(v) for v in self.subjects]

        if self.journal_issn is not None and not isinstance(self.journal_issn, str):
            self.journal_issn = str(self.journal_issn)

        if self.journal_issue is not None and not isinstance(self.journal_issue, str):
            self.journal_issue = str(self.journal_issue)

        if self.journal_volume is not None and not isinstance(self.journal_volume, str):
            self.journal_volume = str(self.journal_volume)

        if self.publisher is not None and not isinstance(self.publisher, str):
            self.publisher = str(self.publisher)

        if self.relation is not None and not isinstance(self.relation, str):
            self.relation = str(self.relation)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RelatedIdentifier(YAMLRoot):
    """
    Identifies other resources that are related in some manner to this record
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["RelatedIdentifier"]
    class_class_curie: ClassVar[str] = "osti:RelatedIdentifier"
    class_name: ClassVar[str] = "RelatedIdentifier"
    class_model_uri: ClassVar[URIRef] = OSTI.RelatedIdentifier

    type: Union[str, "RelatedIdentifierType"] = None
    relation: Union[str, "RelationType"] = None
    value: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, RelatedIdentifierType):
            self.type = RelatedIdentifierType(self.type)

        if self._is_empty(self.relation):
            self.MissingRequiredField("relation")
        if not isinstance(self.relation, RelationType):
            self.relation = RelationType(self.relation)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Geolocation(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Geolocation"]
    class_class_curie: ClassVar[str] = "osti:Geolocation"
    class_name: ClassVar[str] = "Geolocation"
    class_model_uri: ClassVar[URIRef] = OSTI.Geolocation

    points: Union[Union[dict, "Point"], list[Union[dict, "Point"]]] = None
    type: Optional[Union[str, "GeolocationType"]] = None
    label: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.points):
            self.MissingRequiredField("points")
        self._normalize_inlined_as_dict(slot_name="points", slot_type=Point, key_name="latitude", keyed=False)

        if self.type is not None and not isinstance(self.type, GeolocationType):
            self.type = GeolocationType(self.type)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Point(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Point"]
    class_class_curie: ClassVar[str] = "osti:Point"
    class_name: ClassVar[str] = "point"
    class_model_uri: ClassVar[URIRef] = OSTI.Point

    latitude: float = None
    longitude: float = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.latitude):
            self.MissingRequiredField("latitude")
        if not isinstance(self.latitude, float):
            self.latitude = float(self.latitude)

        if self._is_empty(self.longitude):
            self.MissingRequiredField("longitude")
        if not isinstance(self.longitude, float):
            self.longitude = float(self.longitude)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Identifier(YAMLRoot):
    """
    Values of various identifying numbers, such as DOE contract number, product numbers, ISBN, ISSN, and other various
    forms of identifying markings or numbers pertaining to the product or metadata.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Identifier"]
    class_class_curie: ClassVar[str] = "osti:Identifier"
    class_name: ClassVar[str] = "Identifier"
    class_model_uri: ClassVar[URIRef] = OSTI.Identifier

    type: Optional[Union[str, "IdentifierType"]] = None
    value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.type is not None and not isinstance(self.type, IdentifierType):
            self.type = IdentifierType(self.type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AuditLog(YAMLRoot):
    """
    Indicates status and information about back-end processing on a given metadata record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["AuditLog"]
    class_class_curie: ClassVar[str] = "osti:AuditLog"
    class_name: ClassVar[str] = "AuditLog"
    class_model_uri: ClassVar[URIRef] = OSTI.AuditLog

    type: Optional[str] = None
    audit_date: Optional[Union[str, XSDDateTime]] = None
    status: Optional[str] = None
    messages: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.audit_date is not None and not isinstance(self.audit_date, XSDDateTime):
            self.audit_date = XSDDateTime(self.audit_date)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if not isinstance(self.messages, list):
            self.messages = [self.messages] if self.messages is not None else []
        self.messages = [v if isinstance(v, str) else str(v) for v in self.messages]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MediaSet(YAMLRoot):
    """
    Metadata about files associated with this product. Summarizes the main media file associated with this product,
    usually an off-site URL or PDF uploaded to OSTI, with its state, URL if applicable, and other identifying state
    information pertaining to the media files as a group. Each media set is uniquely identified by its `MEDIA_ID`
    value.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["MediaSet"]
    class_class_curie: ClassVar[str] = "osti:MediaSet"
    class_name: ClassVar[str] = "MediaSet"
    class_model_uri: ClassVar[URIRef] = OSTI.MediaSet

    media_id: Optional[int] = None
    revision: Optional[int] = None
    access_limitations: Optional[Union[Union[str, "AccessLimitationsEnum"], list[Union[str, "AccessLimitationsEnum"]]]] = empty_list()
    osti_id: Optional[int] = None
    status: Optional[str] = None
    added_by: Optional[int] = None
    document_page_count: Optional[int] = None
    mime_type: Optional[str] = None
    media_title: Optional[str] = None
    media_location: Optional[Union[str, "MediaLocationEnum"]] = None
    media_source: Optional[str] = None
    date_added: Optional[Union[str, XSDDateTime]] = None
    date_updated: Optional[Union[str, XSDDateTime]] = None
    date_valid_end: Optional[Union[str, XSDDateTime]] = None
    files: Optional[Union[Union[dict, "MediaFile"], list[Union[dict, "MediaFile"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.media_id is not None and not isinstance(self.media_id, int):
            self.media_id = int(self.media_id)

        if self.revision is not None and not isinstance(self.revision, int):
            self.revision = int(self.revision)

        if not isinstance(self.access_limitations, list):
            self.access_limitations = [self.access_limitations] if self.access_limitations is not None else []
        self.access_limitations = [v if isinstance(v, AccessLimitationsEnum) else AccessLimitationsEnum(v) for v in self.access_limitations]

        if self.osti_id is not None and not isinstance(self.osti_id, int):
            self.osti_id = int(self.osti_id)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.added_by is not None and not isinstance(self.added_by, int):
            self.added_by = int(self.added_by)

        if self.document_page_count is not None and not isinstance(self.document_page_count, int):
            self.document_page_count = int(self.document_page_count)

        if self.mime_type is not None and not isinstance(self.mime_type, str):
            self.mime_type = str(self.mime_type)

        if self.media_title is not None and not isinstance(self.media_title, str):
            self.media_title = str(self.media_title)

        if self.media_location is not None and not isinstance(self.media_location, MediaLocationEnum):
            self.media_location = MediaLocationEnum(self.media_location)

        if self.media_source is not None and not isinstance(self.media_source, str):
            self.media_source = str(self.media_source)

        if self.date_added is not None and not isinstance(self.date_added, XSDDateTime):
            self.date_added = XSDDateTime(self.date_added)

        if self.date_updated is not None and not isinstance(self.date_updated, XSDDateTime):
            self.date_updated = XSDDateTime(self.date_updated)

        if self.date_valid_end is not None and not isinstance(self.date_valid_end, XSDDateTime):
            self.date_valid_end = XSDDateTime(self.date_valid_end)

        if not isinstance(self.files, list):
            self.files = [self.files] if self.files is not None else []
        self.files = [v if isinstance(v, MediaFile) else MediaFile(**as_dict(v)) for v in self.files]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MediaFile(YAMLRoot):
    """
    Metadata information pertaining to a particular media resource associated with this product. Contains information
    about its disposition, content, and processing state. Each individual file is uniquely identified by its
    `MEDIA_FILE_ID` value.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["MediaFile"]
    class_class_curie: ClassVar[str] = "osti:MediaFile"
    class_name: ClassVar[str] = "MediaFile"
    class_model_uri: ClassVar[URIRef] = OSTI.MediaFile

    media_file_id: Optional[int] = None
    media_id: Optional[int] = None
    checksum: Optional[str] = None
    revision: Optional[int] = None
    parent_media_file_id: Optional[int] = None
    status: Optional[str] = None
    media_type: Optional[str] = None
    url_type: Optional[Union[str, "MediaLocationEnum"]] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None
    added_by_user_id: Optional[int] = None
    media_source: Optional[str] = None
    file_size_bytes: Optional[int] = None
    duration_seconds: Optional[int] = None
    document_page_count: Optional[int] = None
    subtitle_tracks: Optional[int] = None
    video_tracks: Optional[int] = None
    pdf_version: Optional[str] = None
    pdfa_conformance: Optional[str] = None
    pdfa_part: Optional[str] = None
    pdfua_part: Optional[str] = None
    processing_exceptions: Optional[str] = None
    date_file_added: Optional[Union[str, XSDDateTime]] = None
    date_file_updated: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.media_file_id is not None and not isinstance(self.media_file_id, int):
            self.media_file_id = int(self.media_file_id)

        if self.media_id is not None and not isinstance(self.media_id, int):
            self.media_id = int(self.media_id)

        if self.checksum is not None and not isinstance(self.checksum, str):
            self.checksum = str(self.checksum)

        if self.revision is not None and not isinstance(self.revision, int):
            self.revision = int(self.revision)

        if self.parent_media_file_id is not None and not isinstance(self.parent_media_file_id, int):
            self.parent_media_file_id = int(self.parent_media_file_id)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.media_type is not None and not isinstance(self.media_type, str):
            self.media_type = str(self.media_type)

        if self.url_type is not None and not isinstance(self.url_type, MediaLocationEnum):
            self.url_type = MediaLocationEnum(self.url_type)

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        if self.mime_type is not None and not isinstance(self.mime_type, str):
            self.mime_type = str(self.mime_type)

        if self.added_by_user_id is not None and not isinstance(self.added_by_user_id, int):
            self.added_by_user_id = int(self.added_by_user_id)

        if self.media_source is not None and not isinstance(self.media_source, str):
            self.media_source = str(self.media_source)

        if self.file_size_bytes is not None and not isinstance(self.file_size_bytes, int):
            self.file_size_bytes = int(self.file_size_bytes)

        if self.duration_seconds is not None and not isinstance(self.duration_seconds, int):
            self.duration_seconds = int(self.duration_seconds)

        if self.document_page_count is not None and not isinstance(self.document_page_count, int):
            self.document_page_count = int(self.document_page_count)

        if self.subtitle_tracks is not None and not isinstance(self.subtitle_tracks, int):
            self.subtitle_tracks = int(self.subtitle_tracks)

        if self.video_tracks is not None and not isinstance(self.video_tracks, int):
            self.video_tracks = int(self.video_tracks)

        if self.pdf_version is not None and not isinstance(self.pdf_version, str):
            self.pdf_version = str(self.pdf_version)

        if self.pdfa_conformance is not None and not isinstance(self.pdfa_conformance, str):
            self.pdfa_conformance = str(self.pdfa_conformance)

        if self.pdfa_part is not None and not isinstance(self.pdfa_part, str):
            self.pdfa_part = str(self.pdfa_part)

        if self.pdfua_part is not None and not isinstance(self.pdfua_part, str):
            self.pdfua_part = str(self.pdfua_part)

        if self.processing_exceptions is not None and not isinstance(self.processing_exceptions, str):
            self.processing_exceptions = str(self.processing_exceptions)

        if self.date_file_added is not None and not isinstance(self.date_file_added, XSDDateTime):
            self.date_file_added = XSDDateTime(self.date_file_added)

        if self.date_file_updated is not None and not isinstance(self.date_file_updated, XSDDateTime):
            self.date_file_updated = XSDDateTime(self.date_file_updated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Organization(YAMLRoot):
    """
    Describes a particular organization associated with the bibliographic record. Organizations may be author
    collaborations, sponsors, research laboratories, or contributors to the work, as indicated by their associated
    type. For identification purposes, at least one of either 'name' or 'ror_id' is required for validation. If ROR ID
    is specified, it will be validated against the ROR authority at OSTI.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Organization"]
    class_class_curie: ClassVar[str] = "osti:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = OSTI.Organization

    type: Union[str, "OrganizationType"] = None
    name: str = None
    contributor_type: Optional[Union[str, "ContributorType"]] = None
    ror_id: Optional[str] = None
    identifiers: Optional[Union[Union[dict, "OrganizationIdentifier"], list[Union[dict, "OrganizationIdentifier"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, OrganizationType):
            self.type = OrganizationType(self.type)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.contributor_type is not None and not isinstance(self.contributor_type, ContributorType):
            self.contributor_type = ContributorType(self.contributor_type)

        if self.ror_id is not None and not isinstance(self.ror_id, str):
            self.ror_id = str(self.ror_id)

        self._normalize_inlined_as_dict(slot_name="identifiers", slot_type=OrganizationIdentifier, key_name="type", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OrganizationIdentifier(YAMLRoot):
    """
    One or more identifying numbers or references associated with this organization. Please note that only sponsoring
    organizations may have associated identifier values.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["OrganizationIdentifier"]
    class_class_curie: ClassVar[str] = "osti:OrganizationIdentifier"
    class_name: ClassVar[str] = "OrganizationIdentifier"
    class_model_uri: ClassVar[URIRef] = OSTI.OrganizationIdentifier

    type: Union[str, "OrganizationIdentifierType"] = None
    value: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, OrganizationIdentifierType):
            self.type = OrganizationIdentifierType(self.type)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(YAMLRoot):
    """
    Information about a particular person involved in the production or maintenance of this record
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Person"]
    class_class_curie: ClassVar[str] = "osti:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = OSTI.Person

    type: Union[str, "PersonType"] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[Union[str, list[str]]] = empty_list()
    orcid: Optional[str] = None
    phone: Optional[str] = None
    osti_user_id: Optional[int] = None
    contributor_type: Optional[Union[str, "ContributorType"]] = None
    affiliations: Optional[Union[Union[dict, "Affiliation"], list[Union[dict, "Affiliation"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, PersonType):
            self.type = PersonType(self.type)

        if self.first_name is not None and not isinstance(self.first_name, str):
            self.first_name = str(self.first_name)

        if self.middle_name is not None and not isinstance(self.middle_name, str):
            self.middle_name = str(self.middle_name)

        if self.last_name is not None and not isinstance(self.last_name, str):
            self.last_name = str(self.last_name)

        if not isinstance(self.email, list):
            self.email = [self.email] if self.email is not None else []
        self.email = [v if isinstance(v, str) else str(v) for v in self.email]

        if self.orcid is not None and not isinstance(self.orcid, str):
            self.orcid = str(self.orcid)

        if self.phone is not None and not isinstance(self.phone, str):
            self.phone = str(self.phone)

        if self.osti_user_id is not None and not isinstance(self.osti_user_id, int):
            self.osti_user_id = int(self.osti_user_id)

        if self.contributor_type is not None and not isinstance(self.contributor_type, ContributorType):
            self.contributor_type = ContributorType(self.contributor_type)

        if not isinstance(self.affiliations, list):
            self.affiliations = [self.affiliations] if self.affiliations is not None else []
        self.affiliations = [v if isinstance(v, Affiliation) else Affiliation(**as_dict(v)) for v in self.affiliations]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Affiliation(YAMLRoot):
    """
    An affiliation for a person, such as an organization or institution.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OSTI["Affiliation"]
    class_class_curie: ClassVar[str] = "osti:Affiliation"
    class_name: ClassVar[str] = "Affiliation"
    class_model_uri: ClassVar[URIRef] = OSTI.Affiliation

    name: Optional[str] = None
    ror_id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.ror_id is not None and not isinstance(self.ror_id, str):
            self.ror_id = str(self.ror_id)

        super().__post_init__(**kwargs)


# Enumerations
class ContributorType(EnumDefinitionImpl):
    """
    Describes the type of contribution to the work.  Required for Persons or Organizations of CONTRIBUTING type.
    """
    Chair = PermissibleValue(text="Chair")
    DataCollector = PermissibleValue(
        text="DataCollector",
        description="""Person/institution responsible for finding or gathering data under the guidelines of the author(s) or Principal Investigator.""")
    DataCurator = PermissibleValue(
        text="DataCurator",
        description="""Person tasked with reviewing, enhancing, cleaning, or standardizing metadata and the associated data submitted.""")
    DataManager = PermissibleValue(
        text="DataManager",
        description="""Person (or organization with a staff of data managers, such as a data centre) responsible for maintaining the finished resource.""")
    Distributor = PermissibleValue(
        text="Distributor",
        description="""Institution tasked with responsibility to generate/disseminate copies of the resource in either electronic or print form.""")
    Editor = PermissibleValue(
        text="Editor",
        description="A person who oversees the details related to the publication format of the resource.")
    HostingInstitution = PermissibleValue(
        text="HostingInstitution",
        description="The organization allowing the resource to be available on the internet.")
    Producer = PermissibleValue(
        text="Producer",
        description="Typically a person or organization responsible for the artistry and form of a media product.")
    ProjectLeader = PermissibleValue(
        text="ProjectLeader",
        description="""Person officially designated as head of project team instrumental in the work necessary to development of the resource.""")
    ProjectManager = PermissibleValue(
        text="ProjectManager",
        description="""Person officially designated as manager of a project. Project may consist of one or many project teams and sub-teams.""")
    ProjectMember = PermissibleValue(
        text="ProjectMember",
        description="Person on the membership list of a designated project/project team.")
    RegistrationAgency = PermissibleValue(
        text="RegistrationAgency",
        description="""Institution officially appointed by a Registration Authority to handle specific tasks within a defined area of responsibility.""")
    RegistrationAuthority = PermissibleValue(
        text="RegistrationAuthority",
        description="""A standards-setting body from which Registration Agencies obtain official recognition and guidance.""")
    RelatedPerson = PermissibleValue(
        text="RelatedPerson",
        description="""Person with no specifically defined role in the development of the resource, but who is someone the author wishes to recognize.""")
    Reviewer = PermissibleValue(text="Reviewer")
    ReviewAssistant = PermissibleValue(text="ReviewAssistant")
    ReviewerExternal = PermissibleValue(text="ReviewerExternal")
    RightsHolder = PermissibleValue(
        text="RightsHolder",
        description="""Person or institution owning or managing property rights, including intellectual property rights over the resource.""")
    StatsReviewer = PermissibleValue(text="StatsReviewer")
    Supervisor = PermissibleValue(
        text="Supervisor",
        description="""Designated administrator over one or more groups working to produce a resource or over one or more steps of development process.""")
    Translator = PermissibleValue(text="Translator")
    WorkPackageLeader = PermissibleValue(
        text="WorkPackageLeader",
        description="A Work Package is a recognized data product, not all of which is included in publication.")
    Other = PermissibleValue(
        text="Other",
        description="""Any person or institution making a significant contribution, but whose contribution does not \"fit\".""")

    _defn = EnumDefinition(
        name="ContributorType",
        description="""Describes the type of contribution to the work.  Required for Persons or Organizations of CONTRIBUTING type.""",
    )

class RelatedIdentifierType(EnumDefinitionImpl):
    """
    Identify the type of this related identifier
    """
    ARK = PermissibleValue(text="ARK")
    arXiv = PermissibleValue(text="arXiv")
    bibcode = PermissibleValue(text="bibcode")
    DOI = PermissibleValue(text="DOI")
    EAN13 = PermissibleValue(text="EAN13")
    EISSN = PermissibleValue(text="EISSN")
    IGSN = PermissibleValue(text="IGSN")
    ISBN = PermissibleValue(text="ISBN")
    ISSN = PermissibleValue(text="ISSN")
    ISTC = PermissibleValue(text="ISTC")
    Handle = PermissibleValue(text="Handle")
    LISSN = PermissibleValue(text="LISSN")
    LSID = PermissibleValue(text="LSID")
    OTHER = PermissibleValue(text="OTHER")
    PMCID = PermissibleValue(text="PMCID")
    PMID = PermissibleValue(text="PMID")
    PURL = PermissibleValue(text="PURL")
    UPC = PermissibleValue(text="UPC")
    URI = PermissibleValue(text="URI")
    URL = PermissibleValue(text="URL")
    URN = PermissibleValue(text="URN")
    UUID = PermissibleValue(text="UUID")
    w3id = PermissibleValue(text="w3id")

    _defn = EnumDefinition(
        name="RelatedIdentifierType",
        description="""Identify the type of this related identifier""",
    )

class RelationType(EnumDefinitionImpl):
    """
    Indicates the relationship between this identifier and the source record.
    """
    BasedOnData = PermissibleValue(text="BasedOnData")
    Cites = PermissibleValue(
        text="Cites",
        description="indicates that A includes B in a citation")
    Compiles = PermissibleValue(
        text="Compiles",
        description="indicates B is the result of a compile or creation event using A")
    Continues = PermissibleValue(
        text="Continues",
        description="indicates A is a continuation of the work B")
    Describes = PermissibleValue(text="Describes")
    Documents = PermissibleValue(
        text="Documents",
        description="indicates A is documentation about B")
    Finances = PermissibleValue(text="Finances")
    HasComment = PermissibleValue(text="HasComment")
    HasDerivation = PermissibleValue(text="HasDerivation")
    HasMetadata = PermissibleValue(
        text="HasMetadata",
        description="indicates resource A has additional metadata B")
    HasPart = PermissibleValue(
        text="HasPart",
        description="indicates A includes the part B")
    HasRelatedMaterial = PermissibleValue(text="HasRelatedMaterial")
    HasReply = PermissibleValue(text="HasReply")
    HasReview = PermissibleValue(text="HasReview")
    HasVersion = PermissibleValue(text="HasVersion")
    IsBasedOn = PermissibleValue(text="IsBasedOn")
    IsBasisFor = PermissibleValue(text="IsBasisFor")
    IsCitedBy = PermissibleValue(
        text="IsCitedBy",
        description="indicates that B includes A in a citation")
    IsCommentOn = PermissibleValue(text="IsCommentOn")
    IsCompiledBy = PermissibleValue(
        text="IsCompiledBy",
        description="indicates B is used to compile or create A")
    IsContinuedBy = PermissibleValue(
        text="IsContinuedBy",
        description="indicates A is continued by the work B")
    IsDataBasisFor = PermissibleValue(text="IsDataBasisFor")
    IsDerivedFrom = PermissibleValue(
        text="IsDerivedFrom",
        description="indicates B is a source upon which A is based")
    IsDescribedBy = PermissibleValue(text="IsDescribedBy")
    IsDocumentedBy = PermissibleValue(
        text="IsDocumentedBy",
        description="indicates B is documentation about/explaining A")
    IsFinancedBy = PermissibleValue(text="IsFinancedBy")
    IsIdenticalTo = PermissibleValue(
        text="IsIdenticalTo",
        description="""indicates that A is identical to B, for use when there is a need to register two separate instances of the same resource""")
    IsMetadataFor = PermissibleValue(
        text="IsMetadataFor",
        description="indicates additional metadata A for a resource B")
    IsNewVersionOf = PermissibleValue(
        text="IsNewVersionOf",
        description="indicates A is a new edition of B, where the new edition has been modified or updated")
    IsObsoletedBy = PermissibleValue(
        text="IsObsoletedBy",
        description="indicates that A is obsoleted by B")
    IsOriginalFormOf = PermissibleValue(
        text="IsOriginalFormOf",
        description="indicates A is the original form of B")
    IsPartOf = PermissibleValue(
        text="IsPartOf",
        description="indicates A is a portion of B; may be used for elements of a series")
    IsPreviousVersionOf = PermissibleValue(
        text="IsPreviousVersionOf",
        description="indicates A is a previous edition of B")
    IsReferencedBy = PermissibleValue(
        text="IsReferencedBy",
        description="indicates A is used as a source of information by B")
    IsRelatedMaterial = PermissibleValue(text="IsRelatedMaterial")
    IsReplyTo = PermissibleValue(text="IsReplyTo")
    IsRequiredBy = PermissibleValue(text="IsRequiredBy")
    IsReviewedBy = PermissibleValue(
        text="IsReviewedBy",
        description="indicates that A is reviewed by B")
    IsReviewOf = PermissibleValue(text="IsReviewOf")
    IsSourceOf = PermissibleValue(
        text="IsSourceOf",
        description="indicates A is a source upon which B is based")
    IsSupplementedBy = PermissibleValue(
        text="IsSupplementedBy",
        description="indicates that B is a supplement to A")
    IsSupplementTo = PermissibleValue(
        text="IsSupplementTo",
        description="indicates that A is a supplement to B")
    IsVariantFormOf = PermissibleValue(
        text="IsVariantFormOf",
        description="""indicates A is a variant or different form of B, e.g. calculated or calibrated form or different packaging""")
    IsVersionOf = PermissibleValue(text="IsVersionOf")
    Obsoletes = PermissibleValue(
        text="Obsoletes",
        description="indicates that A obsoletes B")
    References = PermissibleValue(
        text="References",
        description="indicates B is used as a source of information for A")
    Requires = PermissibleValue(text="Requires")
    Reviews = PermissibleValue(
        text="Reviews",
        description="indicates that A is a review of B")

    _defn = EnumDefinition(
        name="RelationType",
        description="""Indicates the relationship between this identifier and the source record.""",
    )

class WorkflowStatusEnum(EnumDefinitionImpl):
    """
    The workflow status of the record.
    """
    R = PermissibleValue(
        text="R",
        description="Fully released")
    SA = PermissibleValue(
        text="SA",
        description="Saved")
    SR = PermissibleValue(
        text="SR",
        description="Submitted to releasing official")
    SO = PermissibleValue(
        text="SO",
        description="Submitted to OSTI awaiting validation")
    SF = PermissibleValue(
        text="SF",
        description="Submitted to OSTI and failed validation")
    SX = PermissibleValue(
        text="SX",
        description="Submitted to OSTI and failed to release")
    SV = PermissibleValue(
        text="SV",
        description="Submitted to OSTI and failed validation")
    X = PermissibleValue(
        text="X",
        description="Error Status")
    D = PermissibleValue(
        text="D",
        description="Deleted:")

    _defn = EnumDefinition(
        name="WorkflowStatusEnum",
        description="The workflow status of the record.",
    )

class AccessLimitationsEnum(EnumDefinitionImpl):
    """
    Access limitation codes to describe the distribution rules and limitations for this work.
    """
    UNL = PermissibleValue(
        text="UNL",
        description="Unlimited announcement")
    OPN = PermissibleValue(
        text="OPN",
        description="OpenNET; requires opn_declassified_status, opn_declassified_date, identifier of type OPN_ACC")
    CPY = PermissibleValue(
        text="CPY",
        description="Copyright restriction on part or all of the contents of this product")
    OUO = PermissibleValue(
        text="OUO",
        description="Official use only")
    PROT = PermissibleValue(
        text="PROT",
        description="""Protected data (e.g., CRADA); requires prot_flag and pdouo_exemption_number; OTHER requires prot_data_other""")
    PDOUO = PermissibleValue(
        text="PDOUO",
        description="Program-determined OUO; requires pdouo_exemption_number")
    ECI = PermissibleValue(
        text="ECI",
        description="Export-controlled information; requires pdouo_exemption_number")
    PDSH = PermissibleValue(
        text="PDSH",
        description="Protected Data Sensitive Homeland")
    USO = PermissibleValue(
        text="USO",
        description="US Only")
    LRD = PermissibleValue(
        text="LRD",
        description="Limited Rights Data; requires pdouo_exemption_number")
    NAT = PermissibleValue(
        text="NAT",
        description="National Security")
    NNPI = PermissibleValue(
        text="NNPI",
        description="Naval Navigation Propulsion Info")
    INTL = PermissibleValue(
        text="INTL",
        description="International data")
    PROP = PermissibleValue(
        text="PROP",
        description="Proprietary")
    PAT = PermissibleValue(
        text="PAT",
        description="Patented information; requires pdouo_exemption_number")
    OTHR = PermissibleValue(
        text="OTHR",
        description="Other")
    CUI = PermissibleValue(
        text="CUI",
        description="""Controlled Unclassified Information; include specific or basic categories/controls in access_limitation_other""")

    _defn = EnumDefinition(
        name="AccessLimitationsEnum",
        description="""Access limitation codes to describe the distribution rules and limitations for this work.""",
    )

class CollectionTypeEnum(EnumDefinitionImpl):
    """
    The OSTI collection type originally creating this record.
    """
    DOE_LAB = PermissibleValue(text="DOE_LAB")
    DOE_GRANT = PermissibleValue(text="DOE_GRANT")
    CHORUS = PermissibleValue(text="CHORUS")

    _defn = EnumDefinition(
        name="CollectionTypeEnum",
        description="The OSTI collection type originally creating this record.",
    )

class IdentifierType(EnumDefinitionImpl):
    """
    Describe the type of identifier
    """
    AUTH_REV = PermissibleValue(text="AUTH_REV")
    CN_DOE = PermissibleValue(text="CN_DOE")
    CN_NONDOE = PermissibleValue(text="CN_NONDOE")
    CODEN = PermissibleValue(text="CODEN")
    DOE_DOCKET = PermissibleValue(
        text="DOE_DOCKET",
        description="""DOE Docket number, used for documents submitted to the DOE Electronic Docket Room (e-Docket Room) system.""")
    EDB = PermissibleValue(text="EDB")
    ETDE_RN = PermissibleValue(text="ETDE_RN")
    INIS_RN = PermissibleValue(text="INIS_RN")
    ISBN = PermissibleValue(
        text="ISBN",
        description="International Standard Book Number")
    ISSN = PermissibleValue(
        text="ISSN",
        description="International Standard Serial Number")
    LEGACY = PermissibleValue(text="LEGACY")
    NSA = PermissibleValue(text="NSA")
    OPN_ACC = PermissibleValue(text="OPN_ACC")
    OTHER_ID = PermissibleValue(text="OTHER_ID")
    PATENT = PermissibleValue(
        text="PATENT",
        description="Patent number")
    PROJ_ID = PermissibleValue(
        text="PROJ_ID",
        description="Project identifier")
    PROP_REV = PermissibleValue(text="PROP_REV")
    REF = PermissibleValue(text="REF")
    REL_TRN = PermissibleValue(text="REL_TRN")
    RN = PermissibleValue(text="RN")
    TRN = PermissibleValue(text="TRN")
    TVI = PermissibleValue(text="TVI")
    USER_VER = PermissibleValue(text="USER_VER")
    WORK_AUTH = PermissibleValue(text="WORK_AUTH")
    WORK_PROP = PermissibleValue(text="WORK_PROP")

    _defn = EnumDefinition(
        name="IdentifierType",
        description="Describe the type of identifier",
    )

class MediaLocationEnum(EnumDefinitionImpl):
    """
    Indicates if a media file is stored locally or off-site.
    """
    L = PermissibleValue(
        text="L",
        description="Local")
    O = PermissibleValue(
        text="O",
        description="Off-Site")

    _defn = EnumDefinition(
        name="MediaLocationEnum",
        description="Indicates if a media file is stored locally or off-site.",
    )

class OrganizationType(EnumDefinitionImpl):
    """
    Indicates type of organization.
    """
    AUTHOR = PermissibleValue(text="AUTHOR")
    CONTRIBUTING = PermissibleValue(text="CONTRIBUTING")
    RESEARCHING = PermissibleValue(text="RESEARCHING")
    SPONSOR = PermissibleValue(text="SPONSOR")

    _defn = EnumDefinition(
        name="OrganizationType",
        description="Indicates type of organization.",
    )

class OrganizationIdentifierType(EnumDefinitionImpl):
    """
    Describe the type of identifier.
    """
    AWARD_DOI = PermissibleValue(text="AWARD_DOI")
    CN_DOE = PermissibleValue(text="CN_DOE")
    CN_NONDOE = PermissibleValue(text="CN_NONDOE")

    _defn = EnumDefinition(
        name="OrganizationIdentifierType",
        description="Describe the type of identifier.",
    )

class PersonType(EnumDefinitionImpl):
    """
    Indicates type of person.
    """
    AUTHOR = PermissibleValue(
        text="AUTHOR",
        description="""Authors are the main scientists or researchers involved in creating, authoring, or producing the research output/scientific and technical information resource.""")
    RELEASE = PermissibleValue(
        text="RELEASE",
        description="Releasing Official")
    CONTACT = PermissibleValue(
        text="CONTACT",
        description="""Contact Information Persons of these types require at least one valid email address be specified.""")
    CONTRIBUTING = PermissibleValue(
        text="CONTRIBUTING",
        description="""Contributors are people who may have been involved in acquiring resources, collecting data, analyzing resources, developing methodologies, validating information, visualizing data, or otherwise contributing to the output, but would not be considered authors. (A valid contributor_type is required.)""")
    PROT_CE = PermissibleValue(
        text="PROT_CE",
        description="""Protected Data Courtesy Email Information Persons of these types require at least one valid email address be specified.""")
    PROT_RO = PermissibleValue(
        text="PROT_RO",
        description="""Protected Data Actual Releasing Official This field is only applicable to Grantee records that are protected by submitting with the \"PROT\" access limitation.""")
    SBIZ_PI = PermissibleValue(
        text="SBIZ_PI",
        description="""SBIR/STTR Principal Investigator Persons of these types require at least one valid email address be specified.""")
    SBIZ_BO = PermissibleValue(
        text="SBIZ_BO",
        description="""SBIR/STTR Business Official Business official persons require exactly two valid email addresses be specified.""")

    _defn = EnumDefinition(
        name="PersonType",
        description="Indicates type of person.",
    )

class ProductType(EnumDefinitionImpl):
    """
    Define the type of product represented by this metadata information. Values presented *in italics* are considered
    Legacy types.
    """
    AR = PermissibleValue(
        text="AR",
        description="Accomplishment Report")
    B = PermissibleValue(
        text="B",
        description="Book")
    CO = PermissibleValue(
        text="CO",
        description="Conference")
    DA = PermissibleValue(
        text="DA",
        description="Dataset")
    FS = PermissibleValue(
        text="FS",
        description="Factsheet")
    JA = PermissibleValue(
        text="JA",
        description="Journal Article")
    MI = PermissibleValue(
        text="MI",
        description="Miscellaneous")
    OT = PermissibleValue(
        text="OT",
        description="Other")
    P = PermissibleValue(
        text="P",
        description="Patent")
    PD = PermissibleValue(
        text="PD",
        description="Program Document")
    SM = PermissibleValue(
        text="SM",
        description="Software Manual")
    TD = PermissibleValue(
        text="TD",
        description="Thesis/Dissertation")
    TR = PermissibleValue(
        text="TR",
        description="Technical Report")
    PA = PermissibleValue(
        text="PA",
        description="Patent Application")

    _defn = EnumDefinition(
        name="ProductType",
        description="""Define the type of product represented by this metadata information. Values presented *in italics* are considered Legacy types.""",
    )

class GeolocationType(EnumDefinitionImpl):

    POINT = PermissibleValue(text="POINT")
    BOX = PermissibleValue(text="BOX")
    POLYGON = PermissibleValue(text="POLYGON")

    _defn = EnumDefinition(
        name="GeolocationType",
    )

# Slots
class slots:
    pass

slots.records__records = Slot(uri=OSTI.records, name="records__records", curie=OSTI.curie('records'),
                   model_uri=OSTI.records__records, domain=None, range=Optional[Union[Union[int, RecordOstiId], list[Union[int, RecordOstiId]]]])

slots.record__osti_id = Slot(uri=OSTI.osti_id, name="record__osti_id", curie=OSTI.curie('osti_id'),
                   model_uri=OSTI.record__osti_id, domain=None, range=URIRef)

slots.record__identifiers = Slot(uri=OSTI.identifiers, name="record__identifiers", curie=OSTI.curie('identifiers'),
                   model_uri=OSTI.record__identifiers, domain=None, range=Optional[Union[Union[dict, Identifier], list[Union[dict, Identifier]]]])

slots.record__issue = Slot(uri=OSTI.issue, name="record__issue", curie=OSTI.curie('issue'),
                   model_uri=OSTI.record__issue, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,80}$'))

slots.record__journal_license_url = Slot(uri=OSTI.journal_license_url, name="record__journal_license_url", curie=OSTI.curie('journal_license_url'),
                   model_uri=OSTI.record__journal_license_url, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,255}$'))

slots.record__journal_name = Slot(uri=OSTI.journal_name, name="record__journal_name", curie=OSTI.curie('journal_name'),
                   model_uri=OSTI.record__journal_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,250}$'))

slots.record__journal_open_access_flag = Slot(uri=OSTI.journal_open_access_flag, name="record__journal_open_access_flag", curie=OSTI.curie('journal_open_access_flag'),
                   model_uri=OSTI.record__journal_open_access_flag, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,1}$'))

slots.record__journal_type = Slot(uri=OSTI.journal_type, name="record__journal_type", curie=OSTI.curie('journal_type'),
                   model_uri=OSTI.record__journal_type, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,2}$'))

slots.record__revision = Slot(uri=OSTI.revision, name="record__revision", curie=OSTI.curie('revision'),
                   model_uri=OSTI.record__revision, domain=None, range=Optional[int])

slots.record__workflow_status = Slot(uri=OSTI.workflow_status, name="record__workflow_status", curie=OSTI.curie('workflow_status'),
                   model_uri=OSTI.record__workflow_status, domain=None, range=Optional[Union[str, "WorkflowStatusEnum"]])

slots.record__access_limitations = Slot(uri=OSTI.access_limitations, name="record__access_limitations", curie=OSTI.curie('access_limitations'),
                   model_uri=OSTI.record__access_limitations, domain=None, range=Union[Union[str, "AccessLimitationsEnum"], list[Union[str, "AccessLimitationsEnum"]]],
                   pattern=re.compile(r'^.{0,5}$'))

slots.record__access_limitation_other = Slot(uri=OSTI.access_limitation_other, name="record__access_limitation_other", curie=OSTI.curie('access_limitation_other'),
                   model_uri=OSTI.record__access_limitation_other, domain=None, range=Optional[str])

slots.record__added_by = Slot(uri=OSTI.added_by, name="record__added_by", curie=OSTI.curie('added_by'),
                   model_uri=OSTI.record__added_by, domain=None, range=Optional[int])

slots.record__added_by_email = Slot(uri=OSTI.added_by_email, name="record__added_by_email", curie=OSTI.curie('added_by_email'),
                   model_uri=OSTI.record__added_by_email, domain=None, range=Optional[str])

slots.record__added_by_name = Slot(uri=OSTI.added_by_name, name="record__added_by_name", curie=OSTI.curie('added_by_name'),
                   model_uri=OSTI.record__added_by_name, domain=None, range=Optional[str])

slots.record__announcement_codes = Slot(uri=OSTI.announcement_codes, name="record__announcement_codes", curie=OSTI.curie('announcement_codes'),
                   model_uri=OSTI.record__announcement_codes, domain=None, range=Optional[Union[str, list[str]]])

slots.record__edition = Slot(uri=OSTI.edition, name="record__edition", curie=OSTI.curie('edition'),
                   model_uri=OSTI.record__edition, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,10}$'))

slots.record__volume = Slot(uri=OSTI.volume, name="record__volume", curie=OSTI.curie('volume'),
                   model_uri=OSTI.record__volume, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,68}$'))

slots.record__collection_type = Slot(uri=OSTI.collection_type, name="record__collection_type", curie=OSTI.curie('collection_type'),
                   model_uri=OSTI.record__collection_type, domain=None, range=Optional[Union[str, "CollectionTypeEnum"]])

slots.record__conference_information = Slot(uri=OSTI.conference_information, name="record__conference_information", curie=OSTI.curie('conference_information'),
                   model_uri=OSTI.record__conference_information, domain=None, range=Optional[str])

slots.record__conference_type = Slot(uri=OSTI.conference_type, name="record__conference_type", curie=OSTI.curie('conference_type'),
                   model_uri=OSTI.record__conference_type, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,1}$'))

slots.record__contract_award_date = Slot(uri=OSTI.contract_award_date, name="record__contract_award_date", curie=OSTI.curie('contract_award_date'),
                   model_uri=OSTI.record__contract_award_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__country_publication_code = Slot(uri=OSTI.country_publication_code, name="record__country_publication_code", curie=OSTI.curie('country_publication_code'),
                   model_uri=OSTI.record__country_publication_code, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,5}$'))

slots.record__date_metadata_added = Slot(uri=OSTI.date_metadata_added, name="record__date_metadata_added", curie=OSTI.curie('date_metadata_added'),
                   model_uri=OSTI.record__date_metadata_added, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__date_metadata_updated = Slot(uri=OSTI.date_metadata_updated, name="record__date_metadata_updated", curie=OSTI.curie('date_metadata_updated'),
                   model_uri=OSTI.record__date_metadata_updated, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__date_submitted_to_osti_first = Slot(uri=OSTI.date_submitted_to_osti_first, name="record__date_submitted_to_osti_first", curie=OSTI.curie('date_submitted_to_osti_first'),
                   model_uri=OSTI.record__date_submitted_to_osti_first, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__date_submitted_to_osti_last = Slot(uri=OSTI.date_submitted_to_osti_last, name="record__date_submitted_to_osti_last", curie=OSTI.curie('date_submitted_to_osti_last'),
                   model_uri=OSTI.record__date_submitted_to_osti_last, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__date_released_first = Slot(uri=OSTI.date_released_first, name="record__date_released_first", curie=OSTI.curie('date_released_first'),
                   model_uri=OSTI.record__date_released_first, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__date_released_last = Slot(uri=OSTI.date_released_last, name="record__date_released_last", curie=OSTI.curie('date_released_last'),
                   model_uri=OSTI.record__date_released_last, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__title = Slot(uri=OSTI.title, name="record__title", curie=OSTI.curie('title'),
                   model_uri=OSTI.record__title, domain=None, range=str)

slots.record__description = Slot(uri=OSTI.description, name="record__description", curie=OSTI.curie('description'),
                   model_uri=OSTI.record__description, domain=None, range=Optional[str])

slots.record__descriptors = Slot(uri=OSTI.descriptors, name="record__descriptors", curie=OSTI.curie('descriptors'),
                   model_uri=OSTI.record__descriptors, domain=None, range=Optional[Union[str, list[str]]])

slots.record__doe_funded_flag = Slot(uri=OSTI.doe_funded_flag, name="record__doe_funded_flag", curie=OSTI.curie('doe_funded_flag'),
                   model_uri=OSTI.record__doe_funded_flag, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,1}$'))

slots.record__doi = Slot(uri=OSTI.doi, name="record__doi", curie=OSTI.curie('doi'),
                   model_uri=OSTI.record__doi, domain=None, range=Optional[str])

slots.record__doi_infix = Slot(uri=OSTI.doi_infix, name="record__doi_infix", curie=OSTI.curie('doi_infix'),
                   model_uri=OSTI.record__doi_infix, domain=None, range=Optional[str])

slots.record__edited_by = Slot(uri=OSTI.edited_by, name="record__edited_by", curie=OSTI.curie('edited_by'),
                   model_uri=OSTI.record__edited_by, domain=None, range=Optional[int])

slots.record__edited_by_email = Slot(uri=OSTI.edited_by_email, name="record__edited_by_email", curie=OSTI.curie('edited_by_email'),
                   model_uri=OSTI.record__edited_by_email, domain=None, range=Optional[str])

slots.record__edited_by_name = Slot(uri=OSTI.edited_by_name, name="record__edited_by_name", curie=OSTI.curie('edited_by_name'),
                   model_uri=OSTI.record__edited_by_name, domain=None, range=Optional[str])

slots.record__edit_reason = Slot(uri=OSTI.edit_reason, name="record__edit_reason", curie=OSTI.curie('edit_reason'),
                   model_uri=OSTI.record__edit_reason, domain=None, range=Optional[str])

slots.record__edit_source = Slot(uri=OSTI.edit_source, name="record__edit_source", curie=OSTI.curie('edit_source'),
                   model_uri=OSTI.record__edit_source, domain=None, range=Optional[str])

slots.record__format_information = Slot(uri=OSTI.format_information, name="record__format_information", curie=OSTI.curie('format_information'),
                   model_uri=OSTI.record__format_information, domain=None, range=Optional[str])

slots.record__media_embargo_sunset_date = Slot(uri=OSTI.media_embargo_sunset_date, name="record__media_embargo_sunset_date", curie=OSTI.curie('media_embargo_sunset_date'),
                   model_uri=OSTI.record__media_embargo_sunset_date, domain=None, range=Optional[str])

slots.record__publication_date = Slot(uri=OSTI.publication_date, name="record__publication_date", curie=OSTI.curie('publication_date'),
                   model_uri=OSTI.record__publication_date, domain=None, range=Union[str, XSDDateTime])

slots.record__publication_date_text = Slot(uri=OSTI.publication_date_text, name="record__publication_date_text", curie=OSTI.curie('publication_date_text'),
                   model_uri=OSTI.record__publication_date_text, domain=None, range=Optional[str])

slots.record__publisher_information = Slot(uri=OSTI.publisher_information, name="record__publisher_information", curie=OSTI.curie('publisher_information'),
                   model_uri=OSTI.record__publisher_information, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,400}$'))

slots.record__related_doc_info = Slot(uri=OSTI.related_doc_info, name="record__related_doc_info", curie=OSTI.curie('related_doc_info'),
                   model_uri=OSTI.record__related_doc_info, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,2255}$'))

slots.record__keywords = Slot(uri=OSTI.keywords, name="record__keywords", curie=OSTI.curie('keywords'),
                   model_uri=OSTI.record__keywords, domain=None, range=Optional[Union[str, list[str]]])

slots.record__languages = Slot(uri=OSTI.languages, name="record__languages", curie=OSTI.curie('languages'),
                   model_uri=OSTI.record__languages, domain=None, range=Optional[Union[str, list[str]]])

slots.record__audit_logs = Slot(uri=OSTI.audit_logs, name="record__audit_logs", curie=OSTI.curie('audit_logs'),
                   model_uri=OSTI.record__audit_logs, domain=None, range=Optional[Union[Union[dict, AuditLog], list[Union[dict, AuditLog]]]])

slots.record__media = Slot(uri=OSTI.media, name="record__media", curie=OSTI.curie('media'),
                   model_uri=OSTI.record__media, domain=None, range=Optional[Union[Union[dict, MediaSet], list[Union[dict, MediaSet]]]])

slots.record__opn_addressee = Slot(uri=OSTI.opn_addressee, name="record__opn_addressee", curie=OSTI.curie('opn_addressee'),
                   model_uri=OSTI.record__opn_addressee, domain=None, range=Optional[str])

slots.record__opn_declassified_date = Slot(uri=OSTI.opn_declassified_date, name="record__opn_declassified_date", curie=OSTI.curie('opn_declassified_date'),
                   model_uri=OSTI.record__opn_declassified_date, domain=None, range=Optional[str])

slots.record__opn_declassified_status = Slot(uri=OSTI.opn_declassified_status, name="record__opn_declassified_status", curie=OSTI.curie('opn_declassified_status'),
                   model_uri=OSTI.record__opn_declassified_status, domain=None, range=Optional[str])

slots.record__opn_document_categories = Slot(uri=OSTI.opn_document_categories, name="record__opn_document_categories", curie=OSTI.curie('opn_document_categories'),
                   model_uri=OSTI.record__opn_document_categories, domain=None, range=Optional[Union[str, list[str]]])

slots.record__opn_document_location = Slot(uri=OSTI.opn_document_location, name="record__opn_document_location", curie=OSTI.curie('opn_document_location'),
                   model_uri=OSTI.record__opn_document_location, domain=None, range=Optional[str])

slots.record__opn_fieldoffice_acronym_code = Slot(uri=OSTI.opn_fieldoffice_acronym_code, name="record__opn_fieldoffice_acronym_code", curie=OSTI.curie('opn_fieldoffice_acronym_code'),
                   model_uri=OSTI.record__opn_fieldoffice_acronym_code, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,10}$'))

slots.record__organizations = Slot(uri=OSTI.organizations, name="record__organizations", curie=OSTI.curie('organizations'),
                   model_uri=OSTI.record__organizations, domain=None, range=Optional[Union[Union[dict, Organization], list[Union[dict, Organization]]]])

slots.record__other_information = Slot(uri=OSTI.other_information, name="record__other_information", curie=OSTI.curie('other_information'),
                   model_uri=OSTI.record__other_information, domain=None, range=Optional[Union[str, list[str]]])

slots.record__ouo_release_date = Slot(uri=OSTI.ouo_release_date, name="record__ouo_release_date", curie=OSTI.curie('ouo_release_date'),
                   model_uri=OSTI.record__ouo_release_date, domain=None, range=Optional[str])

slots.record__paper_flag = Slot(uri=OSTI.paper_flag, name="record__paper_flag", curie=OSTI.curie('paper_flag'),
                   model_uri=OSTI.record__paper_flag, domain=None, range=Optional[Union[bool, Bool]])

slots.record__hidden_flag = Slot(uri=OSTI.hidden_flag, name="record__hidden_flag", curie=OSTI.curie('hidden_flag'),
                   model_uri=OSTI.record__hidden_flag, domain=None, range=Optional[Union[bool, Bool]])

slots.record__sensitivity_flag = Slot(uri=OSTI.sensitivity_flag, name="record__sensitivity_flag", curie=OSTI.curie('sensitivity_flag'),
                   model_uri=OSTI.record__sensitivity_flag, domain=None, range=Optional[str])

slots.record__doe_supported_flag = Slot(uri=OSTI.doe_supported_flag, name="record__doe_supported_flag", curie=OSTI.curie('doe_supported_flag'),
                   model_uri=OSTI.record__doe_supported_flag, domain=None, range=Optional[Union[bool, Bool]])

slots.record__peer_reviewed_flag = Slot(uri=OSTI.peer_reviewed_flag, name="record__peer_reviewed_flag", curie=OSTI.curie('peer_reviewed_flag'),
                   model_uri=OSTI.record__peer_reviewed_flag, domain=None, range=Optional[Union[bool, Bool]])

slots.record__patent_assignee = Slot(uri=OSTI.patent_assignee, name="record__patent_assignee", curie=OSTI.curie('patent_assignee'),
                   model_uri=OSTI.record__patent_assignee, domain=None, range=Optional[str])

slots.record__patent_file_date = Slot(uri=OSTI.patent_file_date, name="record__patent_file_date", curie=OSTI.curie('patent_file_date'),
                   model_uri=OSTI.record__patent_file_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__patent_priority_date = Slot(uri=OSTI.patent_priority_date, name="record__patent_priority_date", curie=OSTI.curie('patent_priority_date'),
                   model_uri=OSTI.record__patent_priority_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__pdouo_exemption_number = Slot(uri=OSTI.pdouo_exemption_number, name="record__pdouo_exemption_number", curie=OSTI.curie('pdouo_exemption_number'),
                   model_uri=OSTI.record__pdouo_exemption_number, domain=None, range=Optional[str])

slots.record__persons = Slot(uri=OSTI.persons, name="record__persons", curie=OSTI.curie('persons'),
                   model_uri=OSTI.record__persons, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.record__product_size = Slot(uri=OSTI.product_size, name="record__product_size", curie=OSTI.curie('product_size'),
                   model_uri=OSTI.record__product_size, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,50}$'))

slots.record__product_type = Slot(uri=OSTI.product_type, name="record__product_type", curie=OSTI.curie('product_type'),
                   model_uri=OSTI.record__product_type, domain=None, range=Optional[Union[str, "ProductType"]],
                   pattern=re.compile(r'^.{0,2}$'))

slots.record__product_type_other = Slot(uri=OSTI.product_type_other, name="record__product_type_other", curie=OSTI.curie('product_type_other'),
                   model_uri=OSTI.record__product_type_other, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,200}$'))

slots.record__prot_flag = Slot(uri=OSTI.prot_flag, name="record__prot_flag", curie=OSTI.curie('prot_flag'),
                   model_uri=OSTI.record__prot_flag, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,5}$'))

slots.record__prot_data_other = Slot(uri=OSTI.prot_data_other, name="record__prot_data_other", curie=OSTI.curie('prot_data_other'),
                   model_uri=OSTI.record__prot_data_other, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,80}$'))

slots.record__prot_release_date = Slot(uri=OSTI.prot_release_date, name="record__prot_release_date", curie=OSTI.curie('prot_release_date'),
                   model_uri=OSTI.record__prot_release_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__availability = Slot(uri=OSTI.availability, name="record__availability", curie=OSTI.curie('availability'),
                   model_uri=OSTI.record__availability, domain=None, range=Optional[str])

slots.record__subject_category_code = Slot(uri=OSTI.subject_category_code, name="record__subject_category_code", curie=OSTI.curie('subject_category_code'),
                   model_uri=OSTI.record__subject_category_code, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^.{0,2}$'))

slots.record__subject_category_code_legacy = Slot(uri=OSTI.subject_category_code_legacy, name="record__subject_category_code_legacy", curie=OSTI.curie('subject_category_code_legacy'),
                   model_uri=OSTI.record__subject_category_code_legacy, domain=None, range=Optional[Union[str, list[str]]])

slots.record__related_identifiers = Slot(uri=OSTI.related_identifiers, name="record__related_identifiers", curie=OSTI.curie('related_identifiers'),
                   model_uri=OSTI.record__related_identifiers, domain=None, range=Optional[Union[Union[dict, RelatedIdentifier], list[Union[dict, RelatedIdentifier]]]])

slots.record__released_to_osti_date = Slot(uri=OSTI.released_to_osti_date, name="record__released_to_osti_date", curie=OSTI.curie('released_to_osti_date'),
                   model_uri=OSTI.record__released_to_osti_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__releasing_official_comments = Slot(uri=OSTI.releasing_official_comments, name="record__releasing_official_comments", curie=OSTI.curie('releasing_official_comments'),
                   model_uri=OSTI.record__releasing_official_comments, domain=None, range=Optional[str])

slots.record__report_period_end_date = Slot(uri=OSTI.report_period_end_date, name="record__report_period_end_date", curie=OSTI.curie('report_period_end_date'),
                   model_uri=OSTI.record__report_period_end_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__report_period_start_date = Slot(uri=OSTI.report_period_start_date, name="record__report_period_start_date", curie=OSTI.curie('report_period_start_date'),
                   model_uri=OSTI.record__report_period_start_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__report_types = Slot(uri=OSTI.report_types, name="record__report_types", curie=OSTI.curie('report_types'),
                   model_uri=OSTI.record__report_types, domain=None, range=Optional[Union[str, list[str]]])

slots.record__report_type_other = Slot(uri=OSTI.report_type_other, name="record__report_type_other", curie=OSTI.curie('report_type_other'),
                   model_uri=OSTI.record__report_type_other, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,80}$'))

slots.record__sbiz_flag = Slot(uri=OSTI.sbiz_flag, name="record__sbiz_flag", curie=OSTI.curie('sbiz_flag'),
                   model_uri=OSTI.record__sbiz_flag, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,6}$'))

slots.record__sbiz_phase = Slot(uri=OSTI.sbiz_phase, name="record__sbiz_phase", curie=OSTI.curie('sbiz_phase'),
                   model_uri=OSTI.record__sbiz_phase, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,3}$'))

slots.record__sbiz_previous_contract_number = Slot(uri=OSTI.sbiz_previous_contract_number, name="record__sbiz_previous_contract_number", curie=OSTI.curie('sbiz_previous_contract_number'),
                   model_uri=OSTI.record__sbiz_previous_contract_number, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,14}$'))

slots.record__sbiz_release_date = Slot(uri=OSTI.sbiz_release_date, name="record__sbiz_release_date", curie=OSTI.curie('sbiz_release_date'),
                   model_uri=OSTI.record__sbiz_release_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__site_ownership_code = Slot(uri=OSTI.site_ownership_code, name="record__site_ownership_code", curie=OSTI.curie('site_ownership_code'),
                   model_uri=OSTI.record__site_ownership_code, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,10}$'))

slots.record__site_unique_id = Slot(uri=OSTI.site_unique_id, name="record__site_unique_id", curie=OSTI.curie('site_unique_id'),
                   model_uri=OSTI.record__site_unique_id, domain=None, range=Optional[str])

slots.record__site_url = Slot(uri=OSTI.site_url, name="record__site_url", curie=OSTI.curie('site_url'),
                   model_uri=OSTI.record__site_url, domain=None, range=Optional[str])

slots.record__source_input_type = Slot(uri=OSTI.source_input_type, name="record__source_input_type", curie=OSTI.curie('source_input_type'),
                   model_uri=OSTI.record__source_input_type, domain=None, range=Optional[str])

slots.record__source_edit_type = Slot(uri=OSTI.source_edit_type, name="record__source_edit_type", curie=OSTI.curie('source_edit_type'),
                   model_uri=OSTI.record__source_edit_type, domain=None, range=Optional[str])

slots.record__geolocations = Slot(uri=OSTI.geolocations, name="record__geolocations", curie=OSTI.curie('geolocations'),
                   model_uri=OSTI.record__geolocations, domain=None, range=Optional[Union[Union[dict, Geolocation], list[Union[dict, Geolocation]]]])

slots.record__article_type = Slot(uri=OSTI.article_type, name="record__article_type", curie=OSTI.curie('article_type'),
                   model_uri=OSTI.record__article_type, domain=None, range=Optional[str])

slots.record__authors = Slot(uri=OSTI.authors, name="record__authors", curie=OSTI.curie('authors'),
                   model_uri=OSTI.record__authors, domain=None, range=Optional[Union[str, list[str]]])

slots.record__conference_info = Slot(uri=OSTI.conference_info, name="record__conference_info", curie=OSTI.curie('conference_info'),
                   model_uri=OSTI.record__conference_info, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,255}$'))

slots.record__contract_number = Slot(uri=OSTI.contract_number, name="record__contract_number", curie=OSTI.curie('contract_number'),
                   model_uri=OSTI.record__contract_number, domain=None, range=Optional[str])

slots.record__country_publication = Slot(uri=OSTI.country_publication, name="record__country_publication", curie=OSTI.curie('country_publication'),
                   model_uri=OSTI.record__country_publication, domain=None, range=Optional[str])

slots.record__doe_contract_number = Slot(uri=OSTI.doe_contract_number, name="record__doe_contract_number", curie=OSTI.curie('doe_contract_number'),
                   model_uri=OSTI.record__doe_contract_number, domain=None, range=Optional[str])

slots.record__entry_date = Slot(uri=OSTI.entry_date, name="record__entry_date", curie=OSTI.curie('entry_date'),
                   model_uri=OSTI.record__entry_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.record__identifier = Slot(uri=OSTI.identifier, name="record__identifier", curie=OSTI.curie('identifier'),
                   model_uri=OSTI.record__identifier, domain=None, range=Optional[Union[str, list[str]]])

slots.record__language = Slot(uri=OSTI.language, name="record__language", curie=OSTI.curie('language'),
                   model_uri=OSTI.record__language, domain=None, range=Optional[Union[str, list[str]]])

slots.record__links = Slot(uri=OSTI.links, name="record__links", curie=OSTI.curie('links'),
                   model_uri=OSTI.record__links, domain=None, range=Optional[Union[str, list[str]]])

slots.record__other_identifiers = Slot(uri=OSTI.other_identifiers, name="record__other_identifiers", curie=OSTI.curie('other_identifiers'),
                   model_uri=OSTI.record__other_identifiers, domain=None, range=Optional[Union[str, list[str]]])

slots.record__other_number = Slot(uri=OSTI.other_number, name="record__other_number", curie=OSTI.curie('other_number'),
                   model_uri=OSTI.record__other_number, domain=None, range=Optional[Union[str, list[str]]])

slots.record__report_number = Slot(uri=OSTI.report_number, name="record__report_number", curie=OSTI.curie('report_number'),
                   model_uri=OSTI.record__report_number, domain=None, range=Optional[Union[str, list[str]]])

slots.record__research_orgs = Slot(uri=OSTI.research_orgs, name="record__research_orgs", curie=OSTI.curie('research_orgs'),
                   model_uri=OSTI.record__research_orgs, domain=None, range=Optional[Union[str, list[str]]])

slots.record__sponsor_orgs = Slot(uri=OSTI.sponsor_orgs, name="record__sponsor_orgs", curie=OSTI.curie('sponsor_orgs'),
                   model_uri=OSTI.record__sponsor_orgs, domain=None, range=Optional[Union[str, list[str]]])

slots.record__subjects = Slot(uri=OSTI.subjects, name="record__subjects", curie=OSTI.curie('subjects'),
                   model_uri=OSTI.record__subjects, domain=None, range=Optional[Union[str, list[str]]])

slots.record__journal_issn = Slot(uri=OSTI.journal_issn, name="record__journal_issn", curie=OSTI.curie('journal_issn'),
                   model_uri=OSTI.record__journal_issn, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,9}$'))

slots.record__journal_issue = Slot(uri=OSTI.journal_issue, name="record__journal_issue", curie=OSTI.curie('journal_issue'),
                   model_uri=OSTI.record__journal_issue, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,80}$'))

slots.record__journal_volume = Slot(uri=OSTI.journal_volume, name="record__journal_volume", curie=OSTI.curie('journal_volume'),
                   model_uri=OSTI.record__journal_volume, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,68}$'))

slots.record__publisher = Slot(uri=OSTI.publisher, name="record__publisher", curie=OSTI.curie('publisher'),
                   model_uri=OSTI.record__publisher, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,400}$'))

slots.record__relation = Slot(uri=OSTI.relation, name="record__relation", curie=OSTI.curie('relation'),
                   model_uri=OSTI.record__relation, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,20}$'))

slots.relatedIdentifier__type = Slot(uri=OSTI.type, name="relatedIdentifier__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.relatedIdentifier__type, domain=None, range=Union[str, "RelatedIdentifierType"])

slots.relatedIdentifier__relation = Slot(uri=OSTI.relation, name="relatedIdentifier__relation", curie=OSTI.curie('relation'),
                   model_uri=OSTI.relatedIdentifier__relation, domain=None, range=Union[str, "RelationType"],
                   pattern=re.compile(r'^.{0,20}$'))

slots.relatedIdentifier__value = Slot(uri=OSTI.value, name="relatedIdentifier__value", curie=OSTI.curie('value'),
                   model_uri=OSTI.relatedIdentifier__value, domain=None, range=str,
                   pattern=re.compile(r'^.{0,2000}$'))

slots.geolocation__type = Slot(uri=OSTI.type, name="geolocation__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.geolocation__type, domain=None, range=Optional[Union[str, "GeolocationType"]])

slots.geolocation__label = Slot(uri=OSTI.label, name="geolocation__label", curie=OSTI.curie('label'),
                   model_uri=OSTI.geolocation__label, domain=None, range=Optional[str])

slots.geolocation__points = Slot(uri=OSTI.points, name="geolocation__points", curie=OSTI.curie('points'),
                   model_uri=OSTI.geolocation__points, domain=None, range=Union[Union[dict, Point], list[Union[dict, Point]]])

slots.point__latitude = Slot(uri=OSTI.latitude, name="point__latitude", curie=OSTI.curie('latitude'),
                   model_uri=OSTI.point__latitude, domain=None, range=float)

slots.point__longitude = Slot(uri=OSTI.longitude, name="point__longitude", curie=OSTI.curie('longitude'),
                   model_uri=OSTI.point__longitude, domain=None, range=float)

slots.identifier__type = Slot(uri=OSTI.type, name="identifier__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.identifier__type, domain=None, range=Optional[Union[str, "IdentifierType"]])

slots.identifier__value = Slot(uri=OSTI.value, name="identifier__value", curie=OSTI.curie('value'),
                   model_uri=OSTI.identifier__value, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,100}$'))

slots.auditLog__type = Slot(uri=OSTI.type, name="auditLog__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.auditLog__type, domain=None, range=Optional[str])

slots.auditLog__audit_date = Slot(uri=OSTI.audit_date, name="auditLog__audit_date", curie=OSTI.curie('audit_date'),
                   model_uri=OSTI.auditLog__audit_date, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.auditLog__status = Slot(uri=OSTI.status, name="auditLog__status", curie=OSTI.curie('status'),
                   model_uri=OSTI.auditLog__status, domain=None, range=Optional[str])

slots.auditLog__messages = Slot(uri=OSTI.messages, name="auditLog__messages", curie=OSTI.curie('messages'),
                   model_uri=OSTI.auditLog__messages, domain=None, range=Optional[Union[str, list[str]]])

slots.mediaSet__media_id = Slot(uri=OSTI.media_id, name="mediaSet__media_id", curie=OSTI.curie('media_id'),
                   model_uri=OSTI.mediaSet__media_id, domain=None, range=Optional[int])

slots.mediaSet__revision = Slot(uri=OSTI.revision, name="mediaSet__revision", curie=OSTI.curie('revision'),
                   model_uri=OSTI.mediaSet__revision, domain=None, range=Optional[int])

slots.mediaSet__access_limitations = Slot(uri=OSTI.access_limitations, name="mediaSet__access_limitations", curie=OSTI.curie('access_limitations'),
                   model_uri=OSTI.mediaSet__access_limitations, domain=None, range=Optional[Union[Union[str, "AccessLimitationsEnum"], list[Union[str, "AccessLimitationsEnum"]]]],
                   pattern=re.compile(r'^.{0,5}$'))

slots.mediaSet__osti_id = Slot(uri=OSTI.osti_id, name="mediaSet__osti_id", curie=OSTI.curie('osti_id'),
                   model_uri=OSTI.mediaSet__osti_id, domain=None, range=Optional[int])

slots.mediaSet__status = Slot(uri=OSTI.status, name="mediaSet__status", curie=OSTI.curie('status'),
                   model_uri=OSTI.mediaSet__status, domain=None, range=Optional[str])

slots.mediaSet__added_by = Slot(uri=OSTI.added_by, name="mediaSet__added_by", curie=OSTI.curie('added_by'),
                   model_uri=OSTI.mediaSet__added_by, domain=None, range=Optional[int])

slots.mediaSet__document_page_count = Slot(uri=OSTI.document_page_count, name="mediaSet__document_page_count", curie=OSTI.curie('document_page_count'),
                   model_uri=OSTI.mediaSet__document_page_count, domain=None, range=Optional[int])

slots.mediaSet__mime_type = Slot(uri=OSTI.mime_type, name="mediaSet__mime_type", curie=OSTI.curie('mime_type'),
                   model_uri=OSTI.mediaSet__mime_type, domain=None, range=Optional[str])

slots.mediaSet__media_title = Slot(uri=OSTI.media_title, name="mediaSet__media_title", curie=OSTI.curie('media_title'),
                   model_uri=OSTI.mediaSet__media_title, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,500}$'))

slots.mediaSet__media_location = Slot(uri=OSTI.media_location, name="mediaSet__media_location", curie=OSTI.curie('media_location'),
                   model_uri=OSTI.mediaSet__media_location, domain=None, range=Optional[Union[str, "MediaLocationEnum"]])

slots.mediaSet__media_source = Slot(uri=OSTI.media_source, name="mediaSet__media_source", curie=OSTI.curie('media_source'),
                   model_uri=OSTI.mediaSet__media_source, domain=None, range=Optional[str])

slots.mediaSet__date_added = Slot(uri=OSTI.date_added, name="mediaSet__date_added", curie=OSTI.curie('date_added'),
                   model_uri=OSTI.mediaSet__date_added, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.mediaSet__date_updated = Slot(uri=OSTI.date_updated, name="mediaSet__date_updated", curie=OSTI.curie('date_updated'),
                   model_uri=OSTI.mediaSet__date_updated, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.mediaSet__date_valid_end = Slot(uri=OSTI.date_valid_end, name="mediaSet__date_valid_end", curie=OSTI.curie('date_valid_end'),
                   model_uri=OSTI.mediaSet__date_valid_end, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.mediaSet__files = Slot(uri=OSTI.files, name="mediaSet__files", curie=OSTI.curie('files'),
                   model_uri=OSTI.mediaSet__files, domain=None, range=Optional[Union[Union[dict, MediaFile], list[Union[dict, MediaFile]]]])

slots.mediaFile__media_file_id = Slot(uri=OSTI.media_file_id, name="mediaFile__media_file_id", curie=OSTI.curie('media_file_id'),
                   model_uri=OSTI.mediaFile__media_file_id, domain=None, range=Optional[int])

slots.mediaFile__media_id = Slot(uri=OSTI.media_id, name="mediaFile__media_id", curie=OSTI.curie('media_id'),
                   model_uri=OSTI.mediaFile__media_id, domain=None, range=Optional[int])

slots.mediaFile__checksum = Slot(uri=OSTI.checksum, name="mediaFile__checksum", curie=OSTI.curie('checksum'),
                   model_uri=OSTI.mediaFile__checksum, domain=None, range=Optional[str])

slots.mediaFile__revision = Slot(uri=OSTI.revision, name="mediaFile__revision", curie=OSTI.curie('revision'),
                   model_uri=OSTI.mediaFile__revision, domain=None, range=Optional[int])

slots.mediaFile__parent_media_file_id = Slot(uri=OSTI.parent_media_file_id, name="mediaFile__parent_media_file_id", curie=OSTI.curie('parent_media_file_id'),
                   model_uri=OSTI.mediaFile__parent_media_file_id, domain=None, range=Optional[int])

slots.mediaFile__status = Slot(uri=OSTI.status, name="mediaFile__status", curie=OSTI.curie('status'),
                   model_uri=OSTI.mediaFile__status, domain=None, range=Optional[str])

slots.mediaFile__media_type = Slot(uri=OSTI.media_type, name="mediaFile__media_type", curie=OSTI.curie('media_type'),
                   model_uri=OSTI.mediaFile__media_type, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,1}$'))

slots.mediaFile__url_type = Slot(uri=OSTI.url_type, name="mediaFile__url_type", curie=OSTI.curie('url_type'),
                   model_uri=OSTI.mediaFile__url_type, domain=None, range=Optional[Union[str, "MediaLocationEnum"]],
                   pattern=re.compile(r'^.{0,1}$'))

slots.mediaFile__url = Slot(uri=OSTI.url, name="mediaFile__url", curie=OSTI.curie('url'),
                   model_uri=OSTI.mediaFile__url, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,255}$'))

slots.mediaFile__mime_type = Slot(uri=OSTI.mime_type, name="mediaFile__mime_type", curie=OSTI.curie('mime_type'),
                   model_uri=OSTI.mediaFile__mime_type, domain=None, range=Optional[str])

slots.mediaFile__added_by_user_id = Slot(uri=OSTI.added_by_user_id, name="mediaFile__added_by_user_id", curie=OSTI.curie('added_by_user_id'),
                   model_uri=OSTI.mediaFile__added_by_user_id, domain=None, range=Optional[int])

slots.mediaFile__media_source = Slot(uri=OSTI.media_source, name="mediaFile__media_source", curie=OSTI.curie('media_source'),
                   model_uri=OSTI.mediaFile__media_source, domain=None, range=Optional[str])

slots.mediaFile__file_size_bytes = Slot(uri=OSTI.file_size_bytes, name="mediaFile__file_size_bytes", curie=OSTI.curie('file_size_bytes'),
                   model_uri=OSTI.mediaFile__file_size_bytes, domain=None, range=Optional[int])

slots.mediaFile__duration_seconds = Slot(uri=OSTI.duration_seconds, name="mediaFile__duration_seconds", curie=OSTI.curie('duration_seconds'),
                   model_uri=OSTI.mediaFile__duration_seconds, domain=None, range=Optional[int])

slots.mediaFile__document_page_count = Slot(uri=OSTI.document_page_count, name="mediaFile__document_page_count", curie=OSTI.curie('document_page_count'),
                   model_uri=OSTI.mediaFile__document_page_count, domain=None, range=Optional[int])

slots.mediaFile__subtitle_tracks = Slot(uri=OSTI.subtitle_tracks, name="mediaFile__subtitle_tracks", curie=OSTI.curie('subtitle_tracks'),
                   model_uri=OSTI.mediaFile__subtitle_tracks, domain=None, range=Optional[int])

slots.mediaFile__video_tracks = Slot(uri=OSTI.video_tracks, name="mediaFile__video_tracks", curie=OSTI.curie('video_tracks'),
                   model_uri=OSTI.mediaFile__video_tracks, domain=None, range=Optional[int])

slots.mediaFile__pdf_version = Slot(uri=OSTI.pdf_version, name="mediaFile__pdf_version", curie=OSTI.curie('pdf_version'),
                   model_uri=OSTI.mediaFile__pdf_version, domain=None, range=Optional[str])

slots.mediaFile__pdfa_conformance = Slot(uri=OSTI.pdfa_conformance, name="mediaFile__pdfa_conformance", curie=OSTI.curie('pdfa_conformance'),
                   model_uri=OSTI.mediaFile__pdfa_conformance, domain=None, range=Optional[str])

slots.mediaFile__pdfa_part = Slot(uri=OSTI.pdfa_part, name="mediaFile__pdfa_part", curie=OSTI.curie('pdfa_part'),
                   model_uri=OSTI.mediaFile__pdfa_part, domain=None, range=Optional[str])

slots.mediaFile__pdfua_part = Slot(uri=OSTI.pdfua_part, name="mediaFile__pdfua_part", curie=OSTI.curie('pdfua_part'),
                   model_uri=OSTI.mediaFile__pdfua_part, domain=None, range=Optional[str])

slots.mediaFile__processing_exceptions = Slot(uri=OSTI.processing_exceptions, name="mediaFile__processing_exceptions", curie=OSTI.curie('processing_exceptions'),
                   model_uri=OSTI.mediaFile__processing_exceptions, domain=None, range=Optional[str])

slots.mediaFile__date_file_added = Slot(uri=OSTI.date_file_added, name="mediaFile__date_file_added", curie=OSTI.curie('date_file_added'),
                   model_uri=OSTI.mediaFile__date_file_added, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.mediaFile__date_file_updated = Slot(uri=OSTI.date_file_updated, name="mediaFile__date_file_updated", curie=OSTI.curie('date_file_updated'),
                   model_uri=OSTI.mediaFile__date_file_updated, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.organization__type = Slot(uri=OSTI.type, name="organization__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.organization__type, domain=None, range=Union[str, "OrganizationType"],
                   pattern=re.compile(r'^.{0,20}$'))

slots.organization__name = Slot(uri=OSTI.name, name="organization__name", curie=OSTI.curie('name'),
                   model_uri=OSTI.organization__name, domain=None, range=str,
                   pattern=re.compile(r'^.{0,800}$'))

slots.organization__contributor_type = Slot(uri=OSTI.contributor_type, name="organization__contributor_type", curie=OSTI.curie('contributor_type'),
                   model_uri=OSTI.organization__contributor_type, domain=None, range=Optional[Union[str, "ContributorType"]],
                   pattern=re.compile(r'^.{0,25}$'))

slots.organization__ror_id = Slot(uri=OSTI.ror_id, name="organization__ror_id", curie=OSTI.curie('ror_id'),
                   model_uri=OSTI.organization__ror_id, domain=None, range=Optional[str])

slots.organization__identifiers = Slot(uri=OSTI.identifiers, name="organization__identifiers", curie=OSTI.curie('identifiers'),
                   model_uri=OSTI.organization__identifiers, domain=None, range=Optional[Union[Union[dict, OrganizationIdentifier], list[Union[dict, OrganizationIdentifier]]]])

slots.organizationIdentifier__type = Slot(uri=OSTI.type, name="organizationIdentifier__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.organizationIdentifier__type, domain=None, range=Union[str, "OrganizationIdentifierType"],
                   pattern=re.compile(r'^.{0,20}$'))

slots.organizationIdentifier__value = Slot(uri=OSTI.value, name="organizationIdentifier__value", curie=OSTI.curie('value'),
                   model_uri=OSTI.organizationIdentifier__value, domain=None, range=str)

slots.person__type = Slot(uri=OSTI.type, name="person__type", curie=OSTI.curie('type'),
                   model_uri=OSTI.person__type, domain=None, range=Union[str, "PersonType"],
                   pattern=re.compile(r'^.{0,20}$'))

slots.person__first_name = Slot(uri=OSTI.first_name, name="person__first_name", curie=OSTI.curie('first_name'),
                   model_uri=OSTI.person__first_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,50}$'))

slots.person__middle_name = Slot(uri=OSTI.middle_name, name="person__middle_name", curie=OSTI.curie('middle_name'),
                   model_uri=OSTI.person__middle_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,50}$'))

slots.person__last_name = Slot(uri=OSTI.last_name, name="person__last_name", curie=OSTI.curie('last_name'),
                   model_uri=OSTI.person__last_name, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,60}$'))

slots.person__email = Slot(uri=OSTI.email, name="person__email", curie=OSTI.curie('email'),
                   model_uri=OSTI.person__email, domain=None, range=Optional[Union[str, list[str]]])

slots.person__orcid = Slot(uri=OSTI.orcid, name="person__orcid", curie=OSTI.curie('orcid'),
                   model_uri=OSTI.person__orcid, domain=None, range=Optional[str])

slots.person__phone = Slot(uri=OSTI.phone, name="person__phone", curie=OSTI.curie('phone'),
                   model_uri=OSTI.person__phone, domain=None, range=Optional[str],
                   pattern=re.compile(r'^.{0,30}$'))

slots.person__osti_user_id = Slot(uri=OSTI.osti_user_id, name="person__osti_user_id", curie=OSTI.curie('osti_user_id'),
                   model_uri=OSTI.person__osti_user_id, domain=None, range=Optional[int])

slots.person__contributor_type = Slot(uri=OSTI.contributor_type, name="person__contributor_type", curie=OSTI.curie('contributor_type'),
                   model_uri=OSTI.person__contributor_type, domain=None, range=Optional[Union[str, "ContributorType"]],
                   pattern=re.compile(r'^.{0,25}$'))

slots.person__affiliations = Slot(uri=OSTI.affiliations, name="person__affiliations", curie=OSTI.curie('affiliations'),
                   model_uri=OSTI.person__affiliations, domain=None, range=Optional[Union[Union[dict, Affiliation], list[Union[dict, Affiliation]]]])

slots.affiliation__name = Slot(uri=OSTI.name, name="affiliation__name", curie=OSTI.curie('name'),
                   model_uri=OSTI.affiliation__name, domain=None, range=Optional[str])

slots.affiliation__ror_id = Slot(uri=OSTI.ror_id, name="affiliation__ror_id", curie=OSTI.curie('ror_id'),
                   model_uri=OSTI.affiliation__ror_id, domain=None, range=Optional[str])

