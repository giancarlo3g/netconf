from ncclient import manager
import ncclient
import xmltodict
import xml.dom.minidom
import sys
from lxml import etree

#def open_xml_request():
    
def open_connection(host,user,passwd):
    return manager.connect(host=host,port=830,username=user,password=passwd,hostkey_verify=False,device_params={'name':'alu'})
def write_xml(host,operation,data_xml):
    print('writing xml reply...')
    with open(f"{host}_{operation}.xml",'w') as f:
        f.write(data_xml)
def print_xml(xml_file):
    t = xml.dom.minidom.parseString(str(xml_file)).toprettyxml()
    formatted_xml = "".join([s for s in t.strip().splitlines(True) if s.strip()])
    print(formatted_xml)
def close_connection(m):
    m.close_session()

if __name__ == "__main__":

    # enter connection info
    host = str(input('host ip: '))
    user = str(input('user: '))
    passwd = str(input('password: '))

    filter_interface_system='''
    <filter type="subtree">
      <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
        <router>
          <router-name>Base</router-name>
          <interface>
            <interface-name>system</interface-name>
          </interface>
        </router>
      </configure>
    </filter>
    '''
    filter_port='''
    <filter type="subtree">
      <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
	    <port>
          <port-id></port-id>
          <oper-state></oper-state>
          <type></type>
          <statistics></statistics>
        </port>
      </state>
    </filter> 
    '''

    filter_card = '''
    <filter type="subtree">
      <state xmlns="urn:nokia.com:sros:ns:yang:sr:state">
      <card/>
      </state>
    </filter> 
    '''

    #request_xml = str(sys.argv[1])
    #operation = request_xml.split('.xml')[0]
    #data = nc_session.get_config(filter_interface_system).data_xml

    # parse xml file and send request via netconf
    operation = 'ports'
    nc_session = open_connection(host,user,passwd)
    data = nc_session.get(filter_port).data_xml
    
    # print and save reply
    write_xml(host,operation,data)
    print_xml(data)

    # close connection
    close_connection(nc_session)
    sys.exit(2)


