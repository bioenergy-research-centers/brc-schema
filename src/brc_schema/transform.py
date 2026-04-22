'''Transform OSTI metadata to BRC schema or vice-versa'''

from pathlib import Path

from linkml_map.transformer.object_transformer import ObjectTransformer
from linkml_map.utils import eval_utils
from linkml_runtime import SchemaView


MODULE_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = MODULE_DIR / "schema"
TRANSFORM_DIR = MODULE_DIR / "transform"

BRC_SCHEMA_PATH = SCHEMA_DIR / "brc_schema.yaml"
OSTI_SCHEMA_PATH = SCHEMA_DIR / "osti_schema.yaml"
BRC_TO_OSTI_TR_PATH = TRANSFORM_DIR / "brc_to_osti.yaml"
OSTI_TO_BRC_TR_PATH = TRANSFORM_DIR / "osti_to_brc.yaml"


def _attr(obj, name, default=None):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_email(value):
    if isinstance(value, list):
        for item in value:
            if item:
                return item
        return None
    return value or None


def _full_name(first_name=None, middle_name=None, last_name=None):
    parts = [part for part in [first_name, middle_name, last_name] if part]
    return " ".join(parts) if parts else None


def _split_name(name):
    parts = str(name).split() if name else []
    if not parts:
        return "Unknown", None, "Unknown"
    first_name = parts[0]
    last_name = parts[-1] if len(parts) > 1 else "Unknown"
    middle_name = " ".join(parts[1:-1]) if len(parts) > 2 else None
    return first_name, middle_name, last_name


def _brc_contract(brc):
    return {
        "CABBI": "SC0018420",
        "GLBRC": "SC0018409",
        "CBI": "AC36-08GO28308",
        "JBEI": "AC02-05CH11231",
    }.get(brc)


def _brc_research_org(brc):
    return {
        "CABBI": {
            "type": "RESEARCHING",
            "name": "Center for Advanced Bioenergy and Bioproduct Innovation (CABBI), Urbana, IL (United States)",
        },
        "CBI": {
            "type": "RESEARCHING",
            "name": "Oak Ridge National Laboratory (ORNL), Oak Ridge, TN (United States)",
        },
        "GLBRC": {
            "type": "RESEARCHING",
            "name": "Great Lakes Bioenergy Research Center (GLBRC), Madison, WI (United States)",
            "ror_id": "01ca2by25",
        },
        "JBEI": {
            "type": "RESEARCHING",
            "name": "Joint Bioenergy Institute (JBEI), Emeryville, CA (United States)",
            "ror_id": "03ww55028",
        },
    }.get(brc)


def _dedupe(items):
    deduped = []
    for item in items:
        if item not in deduped:
            deduped.append(item)
    return deduped


def build_brc_keywords(keywords, subjects):
    source_keywords = keywords or subjects
    if not source_keywords:
        return None
    result = []
    for item in source_keywords:
        if isinstance(item, str):
            for keyword in item.split(","):
                keyword = keyword.strip()
                if keyword:
                    result.append(keyword)
        elif item:
            result.append(str(item))
    return result or None


def build_brc_creators(persons, authors, organizations):
    creators = []
    for person in _as_list(persons):
        if _attr(person, "type") != "AUTHOR":
            continue
        name = _full_name(
            _attr(person, "first_name"),
            _attr(person, "middle_name"),
            _attr(person, "last_name"),
        )
        if not name:
            continue
        creator = {"name": name, "primaryContact": len(creators) == 0}
        email = _normalize_email(_attr(person, "email"))
        if email:
            creator["email"] = email
        orcid = _attr(person, "orcid")
        if orcid:
            creator["orcid"] = orcid
        for affiliation in _as_list(_attr(person, "affiliations")):
            affiliation_name = _attr(affiliation, "name")
            if affiliation_name:
                creator["affiliation"] = affiliation_name
                break
        creators.append(creator)
    if creators:
        return creators

    author_list = [author for author in _as_list(authors) if author]
    if author_list:
        return [
            {"name": author, "primaryContact": idx == 0}
            for idx, author in enumerate(author_list)
        ]

    org_creators = []
    for org in _as_list(organizations):
        if _attr(org, "type") == "AUTHOR" and _attr(org, "name"):
            org_creators.append(
                {"name": _attr(org, "name"), "primaryContact": len(org_creators) == 0}
            )
    return org_creators or None


def build_brc_contributors(persons, organizations):
    contributors = []
    for person in _as_list(persons):
        if _attr(person, "type") != "CONTRIBUTING":
            continue
        name = _full_name(
            _attr(person, "first_name"),
            _attr(person, "middle_name"),
            _attr(person, "last_name"),
        )
        if not name:
            continue
        contributor = {"name": name}
        email = _normalize_email(_attr(person, "email"))
        if email:
            contributor["email"] = email
        orcid = _attr(person, "orcid")
        if orcid:
            contributor["orcid"] = orcid
        contributor_type = _attr(person, "contributor_type")
        if contributor_type:
            contributor["contributorType"] = contributor_type
        for affiliation in _as_list(_attr(person, "affiliations")):
            affiliation_name = _attr(affiliation, "name")
            if affiliation_name:
                contributor["affiliation"] = affiliation_name
                break
        contributors.append(contributor)
    if contributors:
        return contributors

    org_contributors = []
    for org in _as_list(organizations):
        if _attr(org, "type") == "CONTRIBUTING" and _attr(org, "name"):
            contributor = {"name": _attr(org, "name")}
            contributor_type = _attr(org, "contributor_type")
            if contributor_type:
                contributor["contributorType"] = contributor_type
            org_contributors.append(contributor)
    return org_contributors or None


def build_brc_funding(organizations, sponsor_orgs):
    funding = []
    for org in _as_list(organizations):
        if _attr(org, "type") != "SPONSOR":
            continue
        org_name = _attr(org, "name")
        if not org_name:
            continue
        funding_obj = {"fundingOrganization": {"organizationName": org_name}}
        ror_id = _attr(org, "ror_id")
        if ror_id:
            funding_obj["fundingOrganization"]["ror_id"] = ror_id
        for identifier in _as_list(_attr(org, "identifiers")):
            id_type = _attr(identifier, "type")
            id_value = _attr(identifier, "value")
            if not id_value:
                continue
            if id_type in {"CN_DOE", "CN_NONDOE", "AWARD_DOI"} and "awardNumber" not in funding_obj:
                funding_obj["awardNumber"] = id_value
            if id_type == "AWARD_DOI" and "awardURI" not in funding_obj:
                funding_obj["awardURI"] = f"doi:{id_value}"
        funding.append(funding_obj)
    if funding:
        return funding

    sponsor_names = [name for name in _as_list(sponsor_orgs) if name]
    if sponsor_names:
        return [
            {"fundingOrganization": {"organizationName": org_name}}
            for org_name in sponsor_names
        ]
    return None


def build_brc_dataset_url(site_url, links):
    if site_url:
        return site_url
    link_values = [link for link in _as_list(links) if link]
    return link_values[0] if link_values else None


def build_brc_has_related_ids(
    identifiers,
    related_identifiers,
    identifier,
    other_identifiers,
    other_number,
    report_number,
):
    related_ids = []
    for item in _as_list(identifiers):
        item_type = _attr(item, "type")
        item_value = _attr(item, "value")
        if not item_value or str(item_value).lower() == "none":
            continue
        if item_type in {"CN_DOE", "CN_NONDOE", "CN"}:
            continue
        if item_type == "RN":
            related_ids.append(f"BIOPROJECT:{item_value}")
        elif item_type == "DOI":
            related_ids.append(f"doi:{item_value}")
        else:
            related_ids.append(str(item_value))

    for item in _as_list(related_identifiers):
        item_type = _attr(item, "type")
        item_value = _attr(item, "value")
        if not item_value or str(item_value).lower() == "none":
            continue
        item_value = str(item_value)
        if item_type == "DOI":
            related_ids.append(f"doi:{item_value}")
        elif item_type in {"URL", "URI"} and "bioproject" in item_value.lower() and "?term=" in item_value:
            related_ids.append(f"BIOPROJECT:{item_value.split('?term=')[-1].split('&')[0]}")
        else:
            related_ids.append(item_value)

    for legacy_values in [identifier, other_identifiers, other_number, report_number]:
        for value in _as_list(legacy_values):
            if not value or str(value).lower() == "none":
                continue
            value = str(value)
            related_ids.append(f"BIOPROJECT:{value}" if value.startswith("PRJNA") else value)

    return _dedupe(related_ids) or None


def build_osti_site_url(dataset_url, identifier):
    if dataset_url:
        return dataset_url
    if identifier and str(identifier).startswith("http") and "osti.gov/biblio/" not in str(identifier):
        return identifier
    return None


def build_osti_links(dataset_url, identifier):
    site_url = build_osti_site_url(dataset_url, identifier)
    return [site_url] if site_url else None


def build_osti_authors(creators):
    authors = [_attr(creator, "name") for creator in _as_list(creators) if _attr(creator, "name")]
    return authors or None


def build_osti_persons(creators, contributors):
    persons = []
    for creator in _as_list(creators):
        name = _attr(creator, "name")
        first_name, middle_name, last_name = _split_name(name)
        person = {"type": "AUTHOR", "first_name": first_name, "last_name": last_name}
        if middle_name:
            person["middle_name"] = middle_name
        email = _attr(creator, "email")
        if email:
            person["email"] = [email]
        orcid = _attr(creator, "orcid")
        if orcid:
            person["orcid"] = orcid
        affiliation = _attr(creator, "affiliation")
        if affiliation:
            person["affiliations"] = [{"name": affiliation}]
        persons.append(person)

    for contributor in _as_list(contributors):
        name = _attr(contributor, "name")
        first_name, middle_name, last_name = _split_name(name)
        person = {"type": "CONTRIBUTING", "first_name": first_name, "last_name": last_name}
        if middle_name:
            person["middle_name"] = middle_name
        email = _attr(contributor, "email")
        if email:
            person["email"] = [email]
        orcid = _attr(contributor, "orcid")
        if orcid:
            person["orcid"] = orcid
        affiliation = _attr(contributor, "affiliation")
        if affiliation:
            person["affiliations"] = [{"name": affiliation}]
        contributor_type = _attr(contributor, "contributorType")
        if contributor_type:
            person["contributor_type"] = contributor_type
        persons.append(person)
    return persons or None


def build_osti_organizations(funding, brc):
    organizations = []
    for fund in _as_list(funding):
        funding_org = _attr(fund, "fundingOrganization")
        org_name = _attr(funding_org, "organizationName")
        if not org_name:
            continue
        organization = {"type": "SPONSOR", "name": org_name}
        ror_id = _attr(funding_org, "ror_id")
        if ror_id:
            organization["ror_id"] = str(ror_id).replace("ror:", "", 1)
        identifiers = []
        award_uri = _attr(fund, "awardURI")
        if award_uri and str(award_uri).startswith("doi:"):
            identifiers.append({"type": "AWARD_DOI", "value": str(award_uri).replace("doi:", "", 1)})
        award_number = _attr(fund, "awardNumber")
        if award_number:
            identifiers.append({"type": "CN_DOE", "value": award_number})
        if identifiers:
            organization["identifiers"] = identifiers
        organizations.append(organization)

    if not organizations:
        default_org = {
            "type": "SPONSOR",
            "name": "USDOE Office of Science (SC), Biological and Environmental Research (BER)",
        }
        contract_num = _brc_contract(brc)
        if contract_num:
            default_org["identifiers"] = [{"type": "CN_DOE", "value": contract_num}]
        organizations.append(default_org)

    research_org = _brc_research_org(brc)
    if research_org:
        organizations.append(research_org)
    return organizations or None


def build_osti_sponsor_orgs(funding, brc):
    sponsor_orgs = [
        _attr(_attr(fund, "fundingOrganization"), "organizationName")
        for fund in _as_list(funding)
        if _attr(_attr(fund, "fundingOrganization"), "organizationName")
    ]
    if sponsor_orgs:
        return sponsor_orgs
    return ["USDOE Office of Science (SC), Biological and Environmental Research (BER)"] if brc else None


def build_osti_research_orgs(brc):
    research_org = _brc_research_org(brc)
    return [research_org["name"]] if research_org else None


def build_osti_identifiers(has_related_ids, identifier, brc):
    identifiers = []
    for related_id in _as_list(has_related_ids):
        if not isinstance(related_id, str) or not related_id or related_id.lower() == "none":
            continue
        if related_id.startswith("BIOPROJECT:"):
            identifiers.append({"type": "RN", "value": related_id.replace("BIOPROJECT:", "", 1)})
        elif not related_id.startswith("doi:"):
            identifiers.append({"type": "OTHER_ID", "value": related_id})

    if identifier and "osti.gov/biblio/" not in str(identifier):
        identifiers.append({"type": "OTHER_ID", "value": identifier})

    contract_num = _brc_contract(brc)
    if contract_num:
        identifiers.append({"type": "CN_DOE", "value": contract_num})
    return identifiers or None


def build_osti_related_identifiers(has_related_ids):
    related_identifiers = []
    for related_id in _as_list(has_related_ids):
        if not isinstance(related_id, str):
            continue
        if related_id.startswith("doi:"):
            doi = related_id.replace("doi:", "", 1)
            if doi:
                related_identifiers.append({"type": "DOI", "relation": "References", "value": doi})
        elif related_id.startswith("BIOPROJECT:"):
            project_id = related_id.replace("BIOPROJECT:", "", 1)
            if project_id:
                related_identifiers.append(
                    {
                        "type": "URL",
                        "relation": "References",
                        "value": f"https://www.ncbi.nlm.nih.gov/bioproject/?term={project_id}",
                    }
                )
    return related_identifiers or None


def _register_transform_functions():
    eval_utils.FUNCTIONS.update(
        {
            "brc_contract": _brc_contract,
            "build_brc_keywords": build_brc_keywords,
            "build_brc_creators": build_brc_creators,
            "build_brc_contributors": build_brc_contributors,
            "build_brc_funding": build_brc_funding,
            "build_brc_dataset_url": build_brc_dataset_url,
            "build_brc_has_related_ids": build_brc_has_related_ids,
            "build_osti_site_url": build_osti_site_url,
            "build_osti_links": build_osti_links,
            "build_osti_authors": build_osti_authors,
            "build_osti_persons": build_osti_persons,
            "build_osti_organizations": build_osti_organizations,
            "build_osti_sponsor_orgs": build_osti_sponsor_orgs,
            "build_osti_research_orgs": build_osti_research_orgs,
            "build_osti_identifiers": build_osti_identifiers,
            "build_osti_related_identifiers": build_osti_related_identifiers,
        }
    )


class TransformationError(ValueError):
    """Raised when an object transformation cannot be completed."""


def set_up_transformer(tr_type: str) -> ObjectTransformer:
    """Instantiate the object transformer."""
    _register_transform_functions()
    obj_tr = ObjectTransformer(unrestricted_eval=True)
    if tr_type == "osti_to_brc":
        obj_tr.source_schemaview = SchemaView(str(OSTI_SCHEMA_PATH))
        obj_tr.target_schemaview = SchemaView(str(BRC_SCHEMA_PATH))
        obj_tr.load_transformer_specification(OSTI_TO_BRC_TR_PATH)
    elif tr_type == "brc_to_osti":
        obj_tr.source_schemaview = SchemaView(str(BRC_SCHEMA_PATH))
        obj_tr.target_schemaview = SchemaView(str(OSTI_SCHEMA_PATH))
        obj_tr.load_transformer_specification(BRC_TO_OSTI_TR_PATH)
    return obj_tr


def do_transform(
    tr: ObjectTransformer,
    input_obj: dict,
    source_type: str,
) -> dict:
    """Perform the transformation."""
    # tr.index(input_obj, source_type)
    try:
        tr_obj = tr.map_object(input_obj, source_type)
    except ValueError as e:
        raise TransformationError(f"Error during transformation: {e}") from e
    return tr_obj
