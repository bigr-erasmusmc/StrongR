#!/usr/bin/python
import salt.cloud
import jsonpickle
#from concurrent.futures import ThreadPoolExecutor as Pool


#def launchVm(name):
#  print "Launching " + name
#  client.profile(names=[name], profile='salt-minion')

if __name__ == '__main__':
  client = salt.cloud.CloudClient('/etc/salt/cloud')
  names = ["thomas-new-testvm-" + str(i+1) for i in range(0,4)]
  #p = Pool(3)
  #p.map(launchVm, names)
  vms = client.profile(names=names, profile='salt-minion', parallel=True)
  print jsonpickle.encode(vms)
