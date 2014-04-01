#!/usr/bin/python
from influxdb import InfluxDBClient
import argparse
import whisper
import os
import time
import subprocess


DEFAULT_HOST="192.168.3.70"
DEFAULT_PORT="8086"
DEFAULT_USER="root"
DEFAULT_PASSWORD="root"
DEFAULT_DB="whisper"

now = int(time.time())

def write_influx(name,value,time):
  client.write_points()(
    [{
    "name":name,
    "columns":["time", "value"],
    "points":[[time,value]]
    }])

def whisper_read(whisper_file):
  (timeInfo, values) = whisper.fetch(whisper_file,0,now)
  return timeInfo,values

def search(pwd):
  whisper_files = []
  for path,directory,filenames in os.walk(pwd):
    for files in filenames:
      whisper_files.append('%s/%s' % (path,files))
  return whisper_files

def lame_whisper_read(whisper_file):
  linux_cmd = subprocess.Popen(["/usr/local/bin/whisper-fetch.py", "--from=0", whisper_file, ], stdout=subprocess.PIPE,)
  stdout = linux_cmd.communicate()[0]
  data = {}
  for line in stdout.split('\n'):
    try: time, value = line.split()[0], line.split()[1] 
    except:
      continue
    if value != 'None':
      data[time] = value
  return data

def main():
  parser = argparse.ArgumentParser(description='whisper file to influxDB migration script')
  parser.add_argument('path', help='path to whispers')
  parser.add_argument('-host', default=DEFAULT_HOST, metavar="host", help="influxDB host")
  parser.add_argument('-port', default=DEFAULT_PORT, metavar="port", help="influxDB port")
  parser.add_argument('-user', default=DEFAULT_USER, metavar="user", help="influxDB user")
  parser.add_argument('-password', default=DEFAULT_PASSWORD, metavar="password", help="influxDB password")
  parser.add_argument('-db', default=DEFAULT_DB, metavar="db", help="influxDB db!")
  args = parser.parse_args()
  #print args.host, args.port, args.user, args.password, args.db
  client = InfluxDBClient(args.host, args.port, args.user, args.password, args.db)
  try: client.create_database(args.db)
  except: pass
  for whisper_file in  search(args.path):
    data = lame_whisper_read(whisper_file) 
    value = whisper_file.split('/')[-1].split('.')[0]
    time_series = whisper_file.replace('//','/').split('/')[-2].split('/')[-1]
    for key in data.iterkeys():
      time = float(key)
      #value = whisper_file.split('/')[-1].split('.')[0]
      #time_series = whisper_file.replace('//','/').split('/')[-2].split('/')[-1]
      #print time_series, value, time, data[key]
      #time_info, values =  whisper_read(whisper_file)
      client.write_points(
        [{
          "name":time_series,
          "columns":["time",value],
          "points":[[time,data[key]]]
        }])
    
    

if __name__ == '__main__':
  main()
