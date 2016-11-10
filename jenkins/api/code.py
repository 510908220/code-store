# encoding:utf8
import jenkins

server = jenkins.Jenkins('http://192.168.33.10:8080/',
                         username='westdoorblowcola', password='a79c0cdfa6ff8883e1c263262488f0f3')
print server.jobs_count()
