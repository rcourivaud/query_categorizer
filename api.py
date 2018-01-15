import falcon
import json
from query_categorizer.query_categorizer import QueryCategorizer
from wsgiref import simple_server

qc = QueryCategorizer()


class Categorize(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status

        query = req.get_param('query', True)
        results = req.get_param('results', False, default=None)
        prediction_result = qc.process_query(query=query, results=results)
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(prediction_result)


class Embed(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')


# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/categorized', Categorize())
app.add_route('/embedded', Embed())

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()

