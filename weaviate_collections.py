import weaviate.classes as wvc
from weaviate.classes.config import ReferenceProperty


def suppr_collections(client):
    # Nettoyage : suppression si les collections existent
    for name in ["Magazine", "Article"]:
        if client.collections.exists(name):
            client.collections.delete(name)


def setup_collections(client):
    # Créer Magazine si absent
    if not client.collections.exists("Magazine"):
        print("Collection Magazine n existe pas, creation...")
        client.collections.create(
            name="Magazine",
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            generative_config=wvc.config.Configure.Generative.cohere(),
            properties=[
                wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="authors", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="creationDate", data_type=wvc.config.DataType.INT),
                wvc.config.Property(name="originalFile", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="pages", data_type=wvc.config.DataType.INT_ARRAY),
                wvc.config.Property(name="file_name", data_type=wvc.config.DataType.TEXT),
            ]
        )

    # Créer Article si absent
    if not client.collections.exists("Article"):
        print("Collection Article n existe pas, creation...")
        client.collections.create(
            name="Article",
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            properties=[
                wvc.config.Property(name="text", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="chunk_index", data_type=wvc.config.DataType.INT),
                wvc.config.Property(name="pages", data_type=wvc.config.DataType.INT_ARRAY),
                wvc.config.Property(name="authors", data_type=wvc.config.DataType.TEXT),
            ],
            references=[
                ReferenceProperty(
                    name="magazine_ref",
                    target_collection="Magazine"
                )
            ]
        )


