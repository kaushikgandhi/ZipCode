from zipapp.celery import app
import redis
from django.conf import settings

@app.task
def execute_pipe(query):
	
	redis_client = redis.StrictRedis(host=settings.REDIS_HOST)
	pipe = redis_client.pipeline()

	pipe.keys("*%s*"%query.lower().replace(' ','_'))
	#print pipe.execute()
	results = pipe.execute()

	keys = reduce(lambda a, b: a and b, results, True)
	print keys
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

	return response_dict
