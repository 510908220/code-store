# encoding:utf8
import jenkins

server = jenkins.Jenkins('http://192.168.33.10:8080/',
                         username='westdoorblowcola', password='a79c0cdfa6ff8883e1c263262488f0f3')
print server.jobs_count()

# 可以根据配置创建job，这样可以通过基本批量创建job
# print server.create_job('pamc', jenkins.EMPTY_CONFIG_XML)
print server.get_job_config("pamc")
"""
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>resion</name>
          <description>svn commit num</description>
          <defaultValue>111</defaultValue>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <org.jvnet.hudson.plugins.SSHBuilder plugin="ssh@2.4">
      <siteName>root@1.9.9.9:22</siteName>
      <command>ls -a;
scp xxx;
./pamc restart
</command>
    </org.jvnet.hudson.plugins.SSHBuilder>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
"""
#    <org.jvnet.hudson.plugins.SSHBuilder plugin="ssh@2.4">, 2.4可以根据接口读取

# 配置页面，http://192.168.33.10:8080/configure如何修改配置以批量添加机器
