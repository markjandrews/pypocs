import sys
import requests

def main(argv):
    print(argv)

    xmlstr = ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\" standalone=\"yes\"?>\n"
              "<Siri version=\"2.0\" xmlns:ns2=\"http://www.ifopt.org.uk/acsb\" "
              "     xmlns=\"http://www.siri.org.uk/siri\" "
              "     xmlns:ns4=\"http://datex2.eu/schema/2_0RC1/2_0\" "
              "     xmlns:ns3=\"http://www.ifopt.org.uk/ifopt\">\n"
              "     <CheckStatusRequest>\n"
              "         <RequestTimestamp>2015-06-01T12:22:27.568000</RequestTimestamp>\n"
              "         <RequestorRef>E5F73</RequestorRef>\n"
              "     </CheckStatusRequest>\n"
              "</Siri>\n")

    xmlstr = ("<?xml version=\"1.0\" encoding=\"iso-8859-1\" standalone=\"yes\"?>\n"
              "<Siri version=\"2.0\" xmlns:ns2=\"http://www.ifopt.org.uk/acsb\"\n"
              "xmlns=\"http://www.siri.org.uk/siri\" xmlns:ns4=\"http://datex2.eu/schema/2_0RC1/2_0\"\n"
              "xmlns:ns3=\"http://www.ifopt.org.uk/ifopt\">\n"
              " <ServiceRequest>\n"
              " <RequestTimestamp>2015-06-01T12:22:27.568000</RequestTimestamp>\n"
              " <RequestorRef>E5F73</RequestorRef>\n"
              " <VehicleMonitoringRequest version=\"2.0\">\n"
              " <RequestTimestamp>2015-06-01T12:22:27.568000</RequestTimestamp>\n"
              " <VehicleMonitoringRef>VM_ACT_0200</VehicleMonitoringRef>\n"
              " </VehicleMonitoringRequest>\n"
              " </ServiceRequest>\n"
              "</Siri>")

    url = 'http://siri.nxtbus.act.gov.au:11000/E5F73/sm/status.xml'
    url = 'http://siri.nxtbus.act.gov.au:11000/E5F73/vm/status.xml'
    url = 'http://siri.nxtbus.act.gov.au:11000/E5F73/pt/status.xml'
    url = 'http://siri.nxtbus.act.gov.au:11000/E5F73/et/status.xml'
    url = 'http://siri.nxtbus.act.gov.au:11000/E5F73/vm/service.xml'

    response = requests.post(url, data=xmlstr)
    print(response.text)

if __name__ == '__main__':
    main(sys.argv[1:])
