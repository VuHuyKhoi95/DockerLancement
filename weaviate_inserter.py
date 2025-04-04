from collections import defaultdict
import weaviate.classes.query as wvq

def insert_into_weaviate(client, splitted_docs):
    magazine_col = client.collections.get("Magazine")
    article_col = client.collections.get("Article")

    chunks_by_file = defaultdict(list)
    for chunk in splitted_docs:
        chunks_by_file[chunk.metadata["originalFile"]].append(chunk)

    total_magazines, total_articles = 0, 0
    skipped_magazines = 0

    for original_file, chunks in chunks_by_file.items():
        meta = chunks[0].metadata

        # Vérifier si le magazine existe déjà
        existing = magazine_col.query.fetch_objects(
            filters=wvq.Filter.by_property("originalFile").equal(original_file)
        )

        if len(existing.objects) > 0:
            print(f"Magazine déjà présent : {original_file} — insertion ignorée.")
            skipped_magazines += 1
            continue

        total_magazines += 1

        # Insertion dans Magazine
        magazine_id = magazine_col.data.insert({
            "title": meta["title"],
            "authors": meta["authors"],
            "creationDate": int(meta["creationDate"].replace("-", "")),
            "originalFile": meta["originalFile"],
            "pages": [int(p) for p in meta["pages"]],
            "file_name": meta["file_name"]
        })

        # Insertion des Articles (chunks)
        for idx, chunk in enumerate(chunks):
            article_col.data.insert(
                properties={
                    "text": chunk.page_content,
                    "chunk_index": idx,
                    "pages": chunk.metadata["pages"],
                    "authors": chunk.metadata["authors"]
                },
                references={
                    "magazine_ref": magazine_id
                }
            )
            total_articles += 1

        print(f"Magazine inséré : {meta['title']} ({meta['originalFile']})")
        print(f"   → {len(chunks)} article(s) associé(s)")

    print(f"\nInsertion terminée :")
    print(f"   - {total_magazines} magazines insérés")
    print(f"   - {skipped_magazines} magazines ignorés (déjà existants)")
    print(f"   - {total_articles} articles insérés")

