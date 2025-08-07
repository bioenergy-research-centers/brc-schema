-- # Class: "DatasetCollection" Description: "Container class for defining a collection of datasets."
--     * Slot: id Description: 
--     * Slot: schema_version Description: Version of the schema used for the collection.
-- # Class: "Dataset" Description: "A body of structured information describing some topic or topics of interest. This includes metadata about the dataset."
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
-- # Class: "BRCOrganization" Description: "An organization involved in the dataset. The name denotes this is the BRC-specific model of an organization, rather than that defined by OSTI, though the classes are similar."
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
-- # Class: "records" Description: "A list of Record metadata."
--     * Slot: id Description: 
-- # Class: "Record" Description: "Defines the bibliographic metadata about a particular work or record. Depending on product type, various elements are permitted, not permitted, or required."
--     * Slot: osti_id Description: Unique identifier for OSTI record, only required for updates.
--     * Slot: issue Description: Issue number for journals or other applicable products if any.
--     * Slot: journal_license_url Description: URL for information regarding the journal license for information
--     * Slot: journal_name Description: Name of journal publishing this information
--     * Slot: journal_open_access_flag Description: Indicates if the journal article is available in an open access journal, indicated as Y for open, N for not, or left blank/omitted if not applicable or unknown status.
--     * Slot: journal_type Description: Specific sub-type of the journal article.  For product type JA only. Further qualifies the type of record.
--     * Slot: revision Description: Revision number (sequence) for this record.
--     * Slot: workflow_status Description: Workflow status of current revision of record.
--     * Slot: access_limitation_other Description: Additional information about access/distribution limitation for this record, if needed. Required for CUI or PDOUO designations in access limitation. May contain information about the following: Special handling instructions, Copyright restrictions, Other criteria pertinent to the review, access limitation, announcement, and/or restriction of this STI product.
--     * Slot: added_by Description: E-Link user ID that initially entered this record. Value internally maintained by E-Link.
--     * Slot: added_by_email Description: E-Link account email address initially entering this record. Value maintained by E-Link.
--     * Slot: added_by_name Description: E-Link user name initially entering this record. Value maintained by E-Link.
--     * Slot: edition Description: Edition number, as applicable to Books or other products.
--     * Slot: volume Description: A volume number as applicable, usually for journals or books.
--     * Slot: collection_type Description: Indicates the OSTI collection type originally creating this record. Maintained internally by E-Link.
--     * Slot: conference_information Description: "Describes the conference pertaining to this record, if any; usually name and / or location the event took place.""
--     * Slot: conference_type Description: Code representing the type of conference-related work of this record. Generally, only applicable to CO type submissions.
--     * Slot: contract_award_date Description: Date contract for this record was awarded.
--     * Slot: country_publication_code Description: Country of publication for this record
--     * Slot: date_metadata_added Description: Date record first entered the OSTI system. Value internally maintained by E-Link.
--     * Slot: date_metadata_updated Description: Date of this revision of the record. Value internally maintained by E-Link.
--     * Slot: date_submitted_to_osti_first Description: Date record was first submitted to OSTI for publication. Maintained internally by E-Link.
--     * Slot: date_submitted_to_osti_last Description: Most recent date record information was submitted to OSTI. Maintained internally by E-Link.
--     * Slot: title Description: Title of record.  For Book Chapters, the title of the chapter.
--     * Slot: description Description: Description or abstract for this record. Required to have a value for grantee submissions.
--     * Slot: doe_funded_flag Description: Indicates if the record is primarily DOE-funded. Indicate Y for Yes, N for no, or leave blank/omit if unknown status.
--     * Slot: doi Description: The DOI for this record, if any.  Enter value if previously assigned a DOI for the record from an outside service.  If not supplied, OSTI may assign a DOI for the work for certain applicable record types.
--     * Slot: doi_infix Description: "Any customized infix value for the DOI used when generating a DOI reference. The following characters should be avoided in the infix value: ;/?:@&=+$,."
--     * Slot: edited_by Description: OSTI user ID making this revision of the metadata record. Value internally maintained by E-Link.
--     * Slot: edited_by_email Description: E-Link user email address that created this revision of the metadata record. Value maintained by E-Link.
--     * Slot: edited_by_name Description: E-Link user name that created this revision of the metadata record. Value maintained by E-Link.
--     * Slot: edit_reason Description: Value provided by user editing a record describing the reason for the edit.
--     * Slot: edit_source Description: Value determined based on type of edit and user performing the association.
--     * Slot: format_information Description: Information about the format of the product, including any operating system or program requirements for use of the data, as applicable.
--     * Slot: media_embargo_sunset_date Description: Indicates date on which the document embargo ends, if applicable.
--     * Slot: publication_date Description: Date of publication of this record.  For Thesis/Dissertation records, this may also be the completion date of the Thesis.  For Patents, the date the patent was issued or approved.
--     * Slot: publication_date_text Description: String representation of the publication date (e.g., Summer 2001)
--     * Slot: publisher_information Description: Publisher-specific information if applicable
--     * Slot: related_doc_info Description: Additional information regarding the document.  Considered historical or deprecated information, provided for access to historical data. This field is NOT recommended for new submissions.
--     * Slot: opn_addressee Description: For OpenNET records, the addressee information
--     * Slot: opn_declassified_date Description: For OpenNET records, the date information was declassified
--     * Slot: opn_declassified_status Description: For OpenNET records, status of declassification of information
--     * Slot: opn_document_location Description: 
--     * Slot: opn_fieldoffice_acronym_code Description: 
--     * Slot: ouo_release_date Description: Date of OUO access limitation expiration if applicable.
--     * Slot: paper_flag Description: Indicates if OSTI has or had a paper copy of this product.
--     * Slot: patent_assignee Description: The holder of property rights to a patent.
--     * Slot: patent_file_date Description: Date patent was filed with US Patent Office.
--     * Slot: patent_priority_date Description: 
--     * Slot: pdouo_exemption_number Description: Exception number for PDOUO access limitation records. Multiple values may be delimited by semi-colons.
--     * Slot: product_size Description: Information regarding physical size of media or report, if applicable.
--     * Slot: product_type Description: 
--     * Slot: product_type_other Description: Additional information for 'OTHER' product types.  Required if 'OT' product type is specified for this record.
--     * Slot: prot_flag Description: Indicates the type of protected data described by this record. PROT must be specified in the access limitations.
--     * Slot: prot_data_other Description: Information regarding why the information is protected if not a CRADA product.
--     * Slot: prot_release_date Description: The date on which data protections for this record will end.
--     * Slot: availability Description: Describes record's availibility information.
--     * Slot: released_to_osti_date Description: Date record information was released to OSTI, as entered by releasing official.
--     * Slot: releasing_official_comments Description: Any comments made by the releasing official on the record.
--     * Slot: report_period_end_date Description: 
--     * Slot: report_period_start_date Description: 
--     * Slot: report_type_other Description: Detail information about 'Other' report types.
--     * Slot: sbiz_flag Description: Indicates if this metadata is SBIR or STTR related.
--     * Slot: sbiz_phase Description: A three-character field constrained to 'I', 'II', 'IIA', 'IIB', or 'III' indicating the phase of this SBIR/STTR report.
--     * Slot: sbiz_previous_contract_number Description: The previous SBIR/STTR contract number if a Phase III SBIR/STTR report.
--     * Slot: sbiz_release_date Description: Date data protections on this SBIR/STTR record will expire.
--     * Slot: site_ownership_code Description: Code of the DOE site submitting this document
--     * Slot: site_unique_id Description: Site-specified unique accession number for this record
--     * Slot: site_url Description: (DATASET product type only) The URL of the data set landing page, containing links to data set content or additional information as required.
--     * Slot: source_input_type Description: Value determined by submission type at record creation time. Defines how E-Link record was first entered into the system.
--     * Slot: source_edit_type Description: Value determined by submission type for each edit or revision of a record. Changes on a per-revision basis.
-- # Class: "RelatedIdentifier" Description: "Identifies other resources that are related in some manner to this record"
--     * Slot: id Description: 
--     * Slot: type Description: Identify the type of this related identifier
--     * Slot: relation Description: 
--     * Slot: value Description: The value of the identifier
-- # Class: "Geolocation" Description: ""
--     * Slot: id Description: 
--     * Slot: type Description: Describes the shape of this geolocation attribute. (Optional, type may be determined by examination of the points.) Single point in 'points' indicates this is a POINT; two points, indicating NW and SE location, indicate a BOX; any other number of points is assumed to be a POLYGON.  Note that POLYGONs should begin and end on the same point, in order to properly express a 'closed polygon' shape.
--     * Slot: label Description: Optional place name for this location or set of geolocation points.
-- # Class: "point" Description: ""
--     * Slot: id Description: 
--     * Slot: latitude Description: Latitude of this point in the geolocation; limited to -90 to 90, inclusive.
--     * Slot: longitude Description: Longitude of this point in the geolocation; limited to -180 to 180, inclusive.
-- # Class: "Identifier" Description: "Values of various identifying numbers, such as DOE contract number, product numbers, ISBN, ISSN, and other various forms of identifying markings or numbers pertaining to the product or metadata."
--     * Slot: id Description: 
--     * Slot: type Description: 
--     * Slot: value Description: Value of this identifier
-- # Class: "AuditLog" Description: "Indicates status and information about back-end processing on a given metadata record."
--     * Slot: id Description: 
--     * Slot: type Description: Indicates the source of the status message, generally the backend process performing the action in question.
--     * Slot: audit_date Description: Timestamp of the operation detailed in this audit log.
--     * Slot: status Description: Indicates state or notification level of worker action detailed in this audit log.  Generally SUCCESS or FAIL, but may additionally indicate INFO, WARN, or ERROR status messages.
-- # Class: "MediaSet" Description: "Metadata about files associated with this product.  Summarizes the main media file associated with this product, usually an off-site URL or PDF uploaded to OSTI, with its state, URL if applicable, and other identifying state information pertaining to the media files as a group. Each media set is uniquely identified by its `MEDIA_ID` value."
--     * Slot: id Description: 
--     * Slot: media_id Description: Unique ID for this MEDIA SET.
--     * Slot: revision Description: Revision number of this media association set.
--     * Slot: osti_id Description: Links to Record OSTI_ID value for a Media Set.
--     * Slot: status Description: Indicate the current processing of the media file set.
--     * Slot: added_by Description: Indicates user ID that added this media set.
--     * Slot: document_page_count Description: Number of pages, if applicable, found in the processing of this file.
--     * Slot: mime_type Description: MIME type description of the file content of this media file. This value is set by OSTI media processing.
--     * Slot: media_title Description: Optional title provided for the given media set.
--     * Slot: media_location Description: Indicates if this media set's main content is LOCAL or OFF-SITE.
--     * Slot: media_source Description: Indicates the initial primary source of the media set.
--     * Slot: date_added Description: Date this media set was first created. (UTC)
--     * Slot: date_updated Description: Date this media set was most recently modified. (UTC)
--     * Slot: date_valid_end Description: If present, date and time when media association was removed or replaced. (UTC)
-- # Class: "MediaFile" Description: "Metadata information pertaining to a particular media resource associated with this product.  Contains information about its disposition, content, and processing state.  Each individual file is uniquely identified by its `MEDIA_FILE_ID` value."
--     * Slot: id Description: 
--     * Slot: media_file_id Description: Unique identifier for a given MEDIA FILE.
--     * Slot: media_id Description: Link to parent MEDIA SET ID.
--     * Slot: checksum Description: Calculated hash or checksum value of the physical file as applicable, from media processing.
--     * Slot: revision Description: Revision number of this media file, associated with the MEDIA SET
--     * Slot: parent_media_file_id Description: If non-zero, indicates unique MEDIA FILE ID this MEDIA FILE is derived from.
--     * Slot: status Description: Indiciates current processing status for this MEDIA FILE. Other values may indicate awaiting additional processing, such as 'OCR', pending text processing.
--     * Slot: media_type Description: Indicates TYPE of media file, detected or set during media processing.
--     * Slot: url_type Description: Indicates if the file is LOCALLY HOSTED ('L') or OFF-SITE URL ('O').
--     * Slot: url Description: Either the file name for local files, or URL path to off-site resource.
--     * Slot: mime_type Description: Mime type describing the MEDIA FILE content.
--     * Slot: added_by_user_id Description: Indicates the E-Link USER ID that attached this MEDIA FILE.
--     * Slot: media_source Description: Describes method of file production or association with this media set.
--     * Slot: file_size_bytes Description: If local file, the file size in bytes.
--     * Slot: duration_seconds Description: For audio-visual media, the duration of the resource in seconds.
--     * Slot: document_page_count Description: For document-based media, the number of printed pages if applicable.
--     * Slot: subtitle_tracks Description: Indicates the number of subtitle tracks for audio-visual media.
--     * Slot: video_tracks Description: Indicates the number of video tracks in audio-visual media.
--     * Slot: pdf_version Description: For PDF media files, indicates the version of PDF.
--     * Slot: pdfa_conformance Description: For PDF media that is PDF/A compliant, the conformance level, generally A, B, or U.
--     * Slot: pdfa_part Description: For PDF media that is PDF/A compliant, the level of compliance, as a value between 1 and 4.
--     * Slot: pdfua_part Description: For PDF media that is PDF/UA compliant, its compliance level, generally 1 or 2.
--     * Slot: processing_exceptions Description: If present, the reason why media processing failed, or description of problem encountered processing this particular file.
--     * Slot: date_file_added Description: Indicates the date and time this media file was created.
--     * Slot: date_file_updated Description: Indicates the last date and time this media file was modified.
-- # Class: "Organization" Description: "Describes a particular organization associated with the bibliographic record. Organizations may be author collaborations, sponsors, research laboratories, or contributors to the work, as indicated by their associated type. For identification purposes, at least one of either 'name' or 'ror_id' is required for validation.  If ROR ID is specified, it will be validated against the ROR authority at OSTI."
--     * Slot: id Description: 
--     * Slot: type Description: 
--     * Slot: name Description: Name of the organization
--     * Slot: contributor_type Description: Indicate the contribution made by this Organization.  Required for CONTRIBUTING 'type'.
--     * Slot: ror_id Description: ROR ID for this organization, if any. This value will be validated against the ROR authority.
-- # Class: "OrganizationIdentifier" Description: "One or more identifying numbers or references associated with this organization.  Please note that only sponsoring organizations may have associated identifier values."
--     * Slot: id Description: 
--     * Slot: type Description: 
--     * Slot: value Description: Indicates the value of this identifier.  May be validated according to its particular type.
-- # Class: "Person" Description: "Information about a particular person involved in the production or maintenance of this record"
--     * Slot: id Description: 
--     * Slot: type Description: 
--     * Slot: first_name Description: First (or 'Given') name of the person
--     * Slot: middle_name Description: Middle name or initial of the person
--     * Slot: last_name Description: Last (or 'Family') name of this person
--     * Slot: orcid Description: ORCID (https://orcid.org/) value for this person. ORCID values, if provided, must be of valid format.
--     * Slot: phone Description: Contact phone number for this person, if available. If provided, must be a valid phone number expression.
--     * Slot: osti_user_id Description: OSTI-assigned identifier for this person, if any
--     * Slot: contributor_type Description: 
-- # Class: "Affiliation" Description: "An affiliation for a person, such as an organization or institution."
--     * Slot: id Description: 
--     * Slot: name Description: Name of the institution or laboratory with which this person is affiliated.
--     * Slot: ror_id Description: ROR ID of this affiliation, if any.  Will be validated against ROR organization authority if present.
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
-- # Class: "records_records" Description: ""
--     * Slot: records_id Description: Autocreated FK slot
--     * Slot: records_osti_id Description: List of records in the collection.
-- # Class: "Record_identifiers" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: identifiers_id Description: List of identifying numbers related to this record
-- # Class: "Record_access_limitations" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: access_limitations Description: Access/distribution limitation codes to describe the distribution rules and limitations for this work.
-- # Class: "Record_announcement_codes" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: announcement_codes Description: List of announcement codes for this record.
-- # Class: "Record_descriptors" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: descriptors Description: List of descriptor codes for this record
-- # Class: "Record_keywords" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: keywords Description: Concise set of key words for this record
-- # Class: "Record_languages" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: languages Description: Language codes for this record
-- # Class: "Record_audit_logs" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: audit_logs_id Description: Listing of any audit logs of actions taken and worker interactions performed on this metadata revision, if any.
-- # Class: "Record_media" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: media_id Description: Listing of any media and files associated with this record, along with various metadata information and status data for each.  Empty if no media is currently associated with this record.
-- # Class: "Record_opn_document_categories" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: opn_document_categories Description: For OpenNET records, list of any document categories pertaining to this record
-- # Class: "Record_organizations" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: organizations_id Description: List of organizations related to this record. For submissions, at least SPONSOR and RESEARCHING organization is required.
-- # Class: "Record_other_information" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: other_information Description: Information useful to include in published announcements which is not suited for other fields.
-- # Class: "Record_persons" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: persons_id Description: List of persons (authors, contributors, etc.) related to this record. For submissions, at least one AUTHOR or CONTRIBUTING Person, along with a RELEASE contact, is required.
-- # Class: "Record_subject_category_code" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: subject_category_code Description: Set two-character subject category code values for this record
-- # Class: "Record_subject_category_code_legacy" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: subject_category_code_legacy Description: Any legacy or historical subject category codes for this report
-- # Class: "Record_related_identifiers" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: related_identifiers_id Description: List of related identifiers connected to this record
-- # Class: "Record_report_types" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: report_types Description: The type(s) of information or frequency of reporting of information in this report.
-- # Class: "Record_geolocations" Description: ""
--     * Slot: Record_osti_id Description: Autocreated FK slot
--     * Slot: geolocations_id Description: List of geolocation references for this record.
-- # Class: "Geolocation_points" Description: ""
--     * Slot: Geolocation_id Description: Autocreated FK slot
--     * Slot: points_id Description: 
-- # Class: "AuditLog_messages" Description: ""
--     * Slot: AuditLog_id Description: Autocreated FK slot
--     * Slot: messages Description: One or more messages pertaining to the action taken or results of worker processing for this audit log.
-- # Class: "MediaSet_access_limitations" Description: ""
--     * Slot: MediaSet_id Description: Autocreated FK slot
--     * Slot: access_limitations Description: Access limitations are inherited from the parent metadata record at time of association.
-- # Class: "MediaSet_files" Description: ""
--     * Slot: MediaSet_id Description: Autocreated FK slot
--     * Slot: files_id Description: Array of all files, including original submission of file or URL along with any derived files during processing of media.
-- # Class: "Organization_identifiers" Description: ""
--     * Slot: Organization_id Description: Autocreated FK slot
--     * Slot: identifiers_id Description: List of any identifiers for this Organization.  Only applicable to Sponsoring organizations.
-- # Class: "Person_email" Description: ""
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: email Description: List of any email address(es) associated with this person. Email addresses are validated to be well-formed.
-- # Class: "Person_affiliations" Description: ""
--     * Slot: Person_id Description: Autocreated FK slot
--     * Slot: affiliations_id Description: List of any affiliations for this person.  At least one of either 'name' and/or 'ror_id' is required; if ROR ID is provided, the value will be validated against the OSTI ROR authority.

CREATE TABLE "DatasetCollection" (
	id INTEGER NOT NULL, 
	schema_version TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "BRCOrganization" (
	id INTEGER NOT NULL, 
	"organizationName" TEXT, 
	wikidata_id TEXT, 
	ror_id TEXT, 
	"parentOrganization_id" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("parentOrganization_id") REFERENCES "BRCOrganization" (id)
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
CREATE TABLE records (
	id INTEGER NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "Record" (
	osti_id INTEGER NOT NULL, 
	issue TEXT, 
	journal_license_url TEXT, 
	journal_name TEXT, 
	journal_open_access_flag TEXT, 
	journal_type TEXT, 
	revision INTEGER, 
	workflow_status VARCHAR(2), 
	access_limitation_other TEXT, 
	added_by INTEGER, 
	added_by_email TEXT, 
	added_by_name TEXT, 
	edition TEXT, 
	volume TEXT, 
	collection_type VARCHAR(9), 
	conference_information TEXT, 
	conference_type TEXT, 
	contract_award_date DATETIME, 
	country_publication_code TEXT, 
	date_metadata_added DATETIME, 
	date_metadata_updated DATETIME, 
	date_submitted_to_osti_first DATETIME, 
	date_submitted_to_osti_last DATETIME, 
	title TEXT NOT NULL, 
	description TEXT, 
	doe_funded_flag TEXT, 
	doi TEXT, 
	doi_infix TEXT, 
	edited_by INTEGER, 
	edited_by_email TEXT, 
	edited_by_name TEXT, 
	edit_reason TEXT, 
	edit_source TEXT, 
	format_information TEXT, 
	media_embargo_sunset_date TEXT, 
	publication_date DATETIME NOT NULL, 
	publication_date_text TEXT, 
	publisher_information TEXT, 
	related_doc_info TEXT, 
	opn_addressee TEXT, 
	opn_declassified_date TEXT, 
	opn_declassified_status TEXT, 
	opn_document_location TEXT, 
	opn_fieldoffice_acronym_code TEXT, 
	ouo_release_date TEXT, 
	paper_flag BOOLEAN, 
	patent_assignee TEXT, 
	patent_file_date DATETIME, 
	patent_priority_date DATETIME, 
	pdouo_exemption_number TEXT, 
	product_size TEXT, 
	product_type VARCHAR(2), 
	product_type_other TEXT, 
	prot_flag TEXT, 
	prot_data_other TEXT, 
	prot_release_date DATETIME, 
	availability TEXT, 
	released_to_osti_date DATETIME, 
	releasing_official_comments TEXT, 
	report_period_end_date DATETIME, 
	report_period_start_date DATETIME, 
	report_type_other TEXT, 
	sbiz_flag TEXT, 
	sbiz_phase TEXT, 
	sbiz_previous_contract_number TEXT, 
	sbiz_release_date DATETIME, 
	site_ownership_code TEXT, 
	site_unique_id TEXT, 
	site_url TEXT, 
	source_input_type TEXT, 
	source_edit_type TEXT, 
	PRIMARY KEY (osti_id)
);
CREATE TABLE "RelatedIdentifier" (
	id INTEGER NOT NULL, 
	type VARCHAR(7) NOT NULL, 
	relation VARCHAR(19) NOT NULL, 
	value TEXT NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "Geolocation" (
	id INTEGER NOT NULL, 
	type VARCHAR(7), 
	label TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE point (
	id INTEGER NOT NULL, 
	latitude FLOAT NOT NULL, 
	longitude FLOAT NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "Identifier" (
	id INTEGER NOT NULL, 
	type VARCHAR(10), 
	value TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "AuditLog" (
	id INTEGER NOT NULL, 
	type TEXT, 
	audit_date DATETIME, 
	status TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "MediaSet" (
	id INTEGER NOT NULL, 
	media_id INTEGER, 
	revision INTEGER, 
	osti_id INTEGER, 
	status TEXT, 
	added_by INTEGER, 
	document_page_count INTEGER, 
	mime_type TEXT, 
	media_title TEXT, 
	media_location VARCHAR(1), 
	media_source TEXT, 
	date_added DATETIME, 
	date_updated DATETIME, 
	date_valid_end DATETIME, 
	PRIMARY KEY (id)
);
CREATE TABLE "MediaFile" (
	id INTEGER NOT NULL, 
	media_file_id INTEGER, 
	media_id INTEGER, 
	checksum TEXT, 
	revision INTEGER, 
	parent_media_file_id INTEGER, 
	status TEXT, 
	media_type TEXT, 
	url_type VARCHAR(1), 
	url TEXT, 
	mime_type TEXT, 
	added_by_user_id INTEGER, 
	media_source TEXT, 
	file_size_bytes INTEGER, 
	duration_seconds INTEGER, 
	document_page_count INTEGER, 
	subtitle_tracks INTEGER, 
	video_tracks INTEGER, 
	pdf_version TEXT, 
	pdfa_conformance TEXT, 
	pdfa_part TEXT, 
	pdfua_part TEXT, 
	processing_exceptions TEXT, 
	date_file_added DATETIME, 
	date_file_updated DATETIME, 
	PRIMARY KEY (id)
);
CREATE TABLE "Organization" (
	id INTEGER NOT NULL, 
	type VARCHAR(12) NOT NULL, 
	name TEXT NOT NULL, 
	contributor_type VARCHAR(21), 
	ror_id TEXT, 
	PRIMARY KEY (id)
);
CREATE TABLE "OrganizationIdentifier" (
	id INTEGER NOT NULL, 
	type VARCHAR(9) NOT NULL, 
	value TEXT NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE "Person" (
	id INTEGER NOT NULL, 
	type VARCHAR(12) NOT NULL, 
	first_name TEXT, 
	middle_name TEXT, 
	last_name TEXT, 
	orcid TEXT, 
	phone TEXT, 
	osti_user_id INTEGER, 
	contributor_type VARCHAR(21), 
	PRIMARY KEY (id)
);
CREATE TABLE "Affiliation" (
	id INTEGER NOT NULL, 
	name TEXT, 
	ror_id TEXT, 
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
	FOREIGN KEY("fundingOrganization_id") REFERENCES "BRCOrganization" (id)
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
CREATE TABLE records_records (
	records_id INTEGER, 
	records_osti_id INTEGER, 
	PRIMARY KEY (records_id, records_osti_id), 
	FOREIGN KEY(records_id) REFERENCES records (id), 
	FOREIGN KEY(records_osti_id) REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_identifiers" (
	"Record_osti_id" INTEGER, 
	identifiers_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", identifiers_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(identifiers_id) REFERENCES "Identifier" (id)
);
CREATE TABLE "Record_access_limitations" (
	"Record_osti_id" INTEGER, 
	access_limitations VARCHAR(5) NOT NULL, 
	PRIMARY KEY ("Record_osti_id", access_limitations), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_announcement_codes" (
	"Record_osti_id" INTEGER, 
	announcement_codes TEXT, 
	PRIMARY KEY ("Record_osti_id", announcement_codes), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_descriptors" (
	"Record_osti_id" INTEGER, 
	descriptors TEXT, 
	PRIMARY KEY ("Record_osti_id", descriptors), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_keywords" (
	"Record_osti_id" INTEGER, 
	keywords TEXT, 
	PRIMARY KEY ("Record_osti_id", keywords), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_languages" (
	"Record_osti_id" INTEGER, 
	languages TEXT, 
	PRIMARY KEY ("Record_osti_id", languages), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_audit_logs" (
	"Record_osti_id" INTEGER, 
	audit_logs_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", audit_logs_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(audit_logs_id) REFERENCES "AuditLog" (id)
);
CREATE TABLE "Record_media" (
	"Record_osti_id" INTEGER, 
	media_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", media_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(media_id) REFERENCES "MediaSet" (id)
);
CREATE TABLE "Record_opn_document_categories" (
	"Record_osti_id" INTEGER, 
	opn_document_categories TEXT, 
	PRIMARY KEY ("Record_osti_id", opn_document_categories), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_organizations" (
	"Record_osti_id" INTEGER, 
	organizations_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", organizations_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(organizations_id) REFERENCES "Organization" (id)
);
CREATE TABLE "Record_other_information" (
	"Record_osti_id" INTEGER, 
	other_information TEXT, 
	PRIMARY KEY ("Record_osti_id", other_information), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_persons" (
	"Record_osti_id" INTEGER, 
	persons_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", persons_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(persons_id) REFERENCES "Person" (id)
);
CREATE TABLE "Record_subject_category_code" (
	"Record_osti_id" INTEGER, 
	subject_category_code TEXT, 
	PRIMARY KEY ("Record_osti_id", subject_category_code), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_subject_category_code_legacy" (
	"Record_osti_id" INTEGER, 
	subject_category_code_legacy TEXT, 
	PRIMARY KEY ("Record_osti_id", subject_category_code_legacy), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_related_identifiers" (
	"Record_osti_id" INTEGER, 
	related_identifiers_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", related_identifiers_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(related_identifiers_id) REFERENCES "RelatedIdentifier" (id)
);
CREATE TABLE "Record_report_types" (
	"Record_osti_id" INTEGER, 
	report_types TEXT, 
	PRIMARY KEY ("Record_osti_id", report_types), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id)
);
CREATE TABLE "Record_geolocations" (
	"Record_osti_id" INTEGER, 
	geolocations_id INTEGER, 
	PRIMARY KEY ("Record_osti_id", geolocations_id), 
	FOREIGN KEY("Record_osti_id") REFERENCES "Record" (osti_id), 
	FOREIGN KEY(geolocations_id) REFERENCES "Geolocation" (id)
);
CREATE TABLE "Geolocation_points" (
	"Geolocation_id" INTEGER, 
	points_id INTEGER NOT NULL, 
	PRIMARY KEY ("Geolocation_id", points_id), 
	FOREIGN KEY("Geolocation_id") REFERENCES "Geolocation" (id), 
	FOREIGN KEY(points_id) REFERENCES point (id)
);
CREATE TABLE "AuditLog_messages" (
	"AuditLog_id" INTEGER, 
	messages TEXT, 
	PRIMARY KEY ("AuditLog_id", messages), 
	FOREIGN KEY("AuditLog_id") REFERENCES "AuditLog" (id)
);
CREATE TABLE "MediaSet_access_limitations" (
	"MediaSet_id" INTEGER, 
	access_limitations VARCHAR(5), 
	PRIMARY KEY ("MediaSet_id", access_limitations), 
	FOREIGN KEY("MediaSet_id") REFERENCES "MediaSet" (id)
);
CREATE TABLE "MediaSet_files" (
	"MediaSet_id" INTEGER, 
	files_id INTEGER, 
	PRIMARY KEY ("MediaSet_id", files_id), 
	FOREIGN KEY("MediaSet_id") REFERENCES "MediaSet" (id), 
	FOREIGN KEY(files_id) REFERENCES "MediaFile" (id)
);
CREATE TABLE "Organization_identifiers" (
	"Organization_id" INTEGER, 
	identifiers_id INTEGER, 
	PRIMARY KEY ("Organization_id", identifiers_id), 
	FOREIGN KEY("Organization_id") REFERENCES "Organization" (id), 
	FOREIGN KEY(identifiers_id) REFERENCES "OrganizationIdentifier" (id)
);
CREATE TABLE "Person_email" (
	"Person_id" INTEGER, 
	email TEXT, 
	PRIMARY KEY ("Person_id", email), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id)
);
CREATE TABLE "Person_affiliations" (
	"Person_id" INTEGER, 
	affiliations_id INTEGER, 
	PRIMARY KEY ("Person_id", affiliations_id), 
	FOREIGN KEY("Person_id") REFERENCES "Person" (id), 
	FOREIGN KEY(affiliations_id) REFERENCES "Affiliation" (id)
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