import logging
import app.db.models as models

def deferred_update_last_sitemap(post_key):
    models.Sitemap.update_last_sitemap(post_key)

def deferred_update_tags_counter(tags_new , tags_old = []):
    models.Tag.update_tags(tags_new, tags_old)

def deferred_update_category_counter(category_new, category_old = None ):
    models.Category.update_category(category_new, category_old)