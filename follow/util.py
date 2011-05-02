from django.db.models.fields.related import ManyToManyField, ForeignKey

registry = []
model_map = {}

def followers_for_object(self):
    from models import Follow
    return Follow.objects.get_followers_for_object(self)

def register(model, field_name = None, m2m = False):
    """
    This registers the model class so it can have followers
    """
    from models import Follow
    if model in registry:
        return
        
    registry.append(model)
    
    related_name = 'follow_%s' % model._meta.module_name
    
    if not field_name:
        field_name = model._meta.module_name
    
    # Create foreignkeys by default - less sql queries for lookups
    if m2m:
        field = ManyToManyField(
            model,
            related_name = related_name,
        )
    else:
        field = ForeignKey(
            model,
            related_name = related_name,
            blank = True,
            null = True,
        )
    
    field.contribute_to_class(Follow, field_name)
    setattr(model, 'followers', followers_for_object)
    
    # We need to keep track of which fields and which kind of fields point where
    model_map[model] = [related_name, field_name, m2m]
