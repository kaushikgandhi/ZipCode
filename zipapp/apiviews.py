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

from .tasks import execute_pipe

class ZipApi(GenericViewSet):
	"""Api for searching Zip Codes"""



	@require_params("query")
	@list_route(methods=["get"])
	def search(self, request, pk=None):

		query =  request.QUERY_PARAMS.get("query", None) #search term

		

		response_dict = execute_pipe.apply_async([query])

		print response_dict
		return Response(response_dict.get())