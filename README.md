# django-follow

django-follow enables your users to follow any model in your Django application.

## Installation:

    pip install django-follow

## Usage:

* Put into your `INSTALLED_APPS` setting
* Hook into your `urls.py` file
* Register the models you want to be able to follow in your `models.py` files

## Test

The repository includes a sample project and application that is configured
to test `django-follow`.

Clone the repository and cd into the project folder:

	cd project/
	python manage.py test follow
    
## API:

Registering models:

    # Create your own model, then:
    from follow import util
    util.register(MyModel)

Querying models:

    Have a look at the models.py file :)
