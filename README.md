# django-follow

django-follow enables your users to follow any model in your Django application.

## Installation:

    pip install django-follow

## Usage:

    * Put into your `INSTALLED_APPS` setting
    * Hook into your `urls.py` file
    * Register the models you want to be able to follow in your `models.py` files
    
## API:

Registering models:

        # Create your own model, then:
        from follow import util
        util.register(MyModel)

Querying models:

        Have a look at the models.py file :)
