from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework.viewsets import GenericViewSet
from decorators import require_params
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

import redis
from django.conf import settings


class ZipApi(GenericViewSet):
	"""Api for searching Zip Codes"""

	redis_client = redis.StrictRedis(host=settings.REDIS_HOST)
	pipe = redis_client.pipeline()

	def execute_pipe(self):
		''' Execute the statements in pipe'''
		results = self.pipe.execute()
		return reduce(lambda a, b: a and b, results, True)

	@require_params("query")
	@list_route(methods=["get"])
	def search(self, request, pk=None):

		query =  request.QUERY_PARAMS.get("query", None) #search term

		self.pipe.keys("*%s*"%query.lower().replace(' ','_'))


		keys = self.execute_pipe()
		response_dict = []
		for key in keys:
			data = key.split(":")
			response_dict.append({
				"pincode":data[0].replace('_',' '),
				"division":data[1].replace('_',' '),
				"region":data[2].replace('_',' '),
				"taluk":data[3].replace('_',' '),
				"district":data[4].replace('_',' '),
				"state":data[5].replace('_',' '),
				"address":data[6].replace('_',' ')
				})

		return Response(response_dict)