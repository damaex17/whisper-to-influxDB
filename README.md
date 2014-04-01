# whisper-to-influxDB
# ===================

whisper-to-influxDB is a script which reads whisper files and creates datapoints in influxDB.

the script is currently in a early proof of concept version and might be using bulk commits or threading in the future.

the performance is currently not mindblowing.



usage: whisper-to-influxdb.py [-h] [-host host] [-port port] [-user user]
                              [-password password] [-db db]
                              path
                              
the script will parse the given path recursively and search for whisper files.
the found whisper files are being read and None values are omitted.

influxDB naming:

OS path:
tmp/tracker-001/cpu.wsp
tmp/tracker-001/eth0_rx.wsp
tmp/tracker-001/rabbit_queue.wsp
         

script will commit to the database "whisper":

timeseries: tracker-001
value: cpu

timeseries: tracker-001
value: eth0_rx

timeseries: tracker-001
value: rabbit_queue

