import redis

from django.core.management.base import BaseCommand

from django.conf import settings

import os

class Command(BaseCommand):
    '''
        Insert/Update Data from CSV to redis
    '''
    help = 'Command to insert the data in redis for initial deployment'

    redis_client = redis.StrictRedis(host=settings.REDIS_HOST)
    pipe = redis_client.pipeline()

    def format_string(self,str):
        return str.lower().replace(' ','_')

    def handle(self, *args, **options):
        '''
            Handle function to inset data
        '''
        csv_file = open(os.path.abspath(os.path.join("",os.pardir)) + "/zipcode/zipapp/data/all_india_pin_code.csv","r")

        line_count = 0

        for line in csv_file:

        	if line_count == 0:
        		line_count =line_count+ 1
        		continue

        	data = line.split(",")  #split csv coulumns seperated by (,)

        	self.pipe.sadd("%s:%s:%s:%s:%s:%s:%s"%(self.format_string(data[1]),self.format_string(data[4]),\
                self.format_string(data[5]),self.format_string(data[7]),\
                self.format_string(data[8]),self.format_string(data[9]).strip(),self.format_string(data[0])),*[data[1]])
        	self.pipe.execute()


        