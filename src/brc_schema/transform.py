'''Transform OSTI metadata to BRC schema or vice-versa'''

import sys

from linkml_map.transformer.object_transformer import ObjectTransformer
from linkml_runtime import SchemaView


BRC_SCHEMA_PATH = "src/brc_schema/schema/brc_schema.yaml"
OSTI_SCHEMA_PATH = "src/brc_schema/schema/osti_schema.yaml"
BRC_TO_OSTI_TR_PATH = "src/brc_schema/transform/brc_to_osti.yaml"
OSTI_TO_BRC_TR_PATH = "src/brc_schema/transform/osti_to_brc.yaml"


def set_up_transformer(tr_type: str) -> ObjectTransformer:
    """Instantiate the object transformer."""
    obj_tr = ObjectTransformer(unrestricted_eval=True)
    if tr_type == "osti_to_brc":
        obj_tr.source_schemaview = SchemaView(str(OSTI_SCHEMA_PATH))
        obj_tr.target_schemaview = SchemaView(str(BRC_SCHEMA_PATH))
        obj_tr.load_transformer_specification(OSTI_TO_BRC_TR_PATH)
    elif tr_type == "brc_to_osti":
        obj_tr.source_schemaview = SchemaView(str(BRC_SCHEMA_PATH))
        obj_tr.target_schemaview = SchemaView(str(OSTI_SCHEMA_PATH))
        obj_tr.load_transformer_specification(OSTI_TO_BRC_TR_PATH)
    return obj_tr


def do_transform(
    tr: ObjectTransformer,
    input_obj: dict,
    source_type: str,
) -> dict:
    """Perform the transformation."""
    #tr.index(input_obj, source_type)
    try:
        tr_obj = tr.map_object(input_obj, source_type)
    except ValueError as e:
        sys.exit(f"Error during transformation: {e}")
    return tr_obj
