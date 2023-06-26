# Finances
## This is an ongoing project and is dependant on envoirmental variables not stored in this git repository. As such it will not work when just pulled.

This web application is a project designed to help me manage my finances. As I have specific needs when it comes to processing my transactions, I thought this would be better than a 3rd party solution.

### Functionality
- Fetching transactions using GoCardless API
- Grouping monthly spendings
- Modyfying transactions - editing transaction names, dates
- Calculating monthly spendings and income
- Spendings graphs, pie charts

### Used Technologies:
- Python
- Django
- Django Rest Framework
- Jinja2
- Bootstrap
- CSS
- Redis
- Celery
- PostgreSQL

### Frontend:
The interface is mainly built using bootstrap components and functionality with overritten CSS for styling.

### Backend:
The server is built using Django. The page uses default Django Views for funcitonality and Django Rest Framework API for managing individual transations. \
In the future I plan to expand the server to be deployed on my Raspberry Pi using an Apache web server and mod-wsgi.
