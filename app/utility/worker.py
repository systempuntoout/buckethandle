import logging
import app.db.models as models

def deferred_update_tags_counter(tags):
    for tag in set(tags):
        models.Tag.update_tag(tag)


def deferred_update_category_counter(category):
    models.Category.update_category(category)