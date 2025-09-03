'''Transform OSTI metadata to BRC schema'''

from linkml_map.transformer.object_transformer import ObjectTransformer
from linkml_runtime import SchemaView

BRC_SCHEMA_PATH = "brc_schema/schema/brc_schema.yaml"
OSTI_SCHEMA_PATH = "brc_schema/schema/osti_schema.yaml"
OSTI_TO_BRC_TR_PATH = "brc_schema/transform/osti_to_brc.yaml"

def set_up_transformer() -> ObjectTransformer:
    """Instantiate the object transformer."""
    obj_tr = ObjectTransformer(unrestricted_eval=True)
    obj_tr.source_schemaview = SchemaView(str(BRC_SCHEMA_PATH))
    obj_tr.target_schemaview = SchemaView(str(OSTI_SCHEMA_PATH))
    obj_tr.load_transformer_specification(OSTI_TO_BRC_TR_PATH)
    return obj_tr
