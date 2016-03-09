import time
import BaseHTTPServer
import urllib2, urllib
import json
import pprint

HOST_NAME = '127.0.0.1'  # localhost
PORT_NUMBER = 8085  # port parameter
parameters = {
    'mac': 'AB-12-34-BC-56-78',
    # mac example: 'AB-12-34-BC-56-78'
    'device': 'm2 note',
    # device example: 'm2 note'
    'serial': '12ab34c5-678d-9012-ef34-abcd1234ef56:m2 note.m2note:10'
    # serial example: '12ab34c5-678d-9012-ef34-abcd1234ef56:m2 note.m2note:10'
}
debug = 1  # console debug mode 1 - on / 0 - off

# ################################
# ###    DO NOT EDIT CODE BELOW
# ################################
last_answer = {}


def get_url(method, query_param='', debug=0):
    host = 'http://androidsmart.devices.oll.tv/smartAPI/'
    append = '&mac=%s&serial_number=%s&device_type=android&device_model=%s&ver=2&lang=ua&component=android' \
             % (urllib.quote_plus(parameters['mac']),
                urllib.quote_plus(parameters['serial']),
                urllib.quote_plus(parameters['device']))
    headers = {'User-Agent': 'OllAndroid'}
    query = urllib.urlencode(query_param)

    request = urllib2.Request(host + method + '?' + query + append, None, headers)
    response = urllib2.urlopen(request)
    html = response.read()

    if debug > 0:
        print "Response:", response
        # Get the URL. This gets the real URL.
        print "The URL is: ", response.geturl()
        # Getting the code
        print "This gets the code: ", response.code
        # Get the Headers.
        # This returns a dictionary-like object that describes the page fetched,
        # particularly the headers sent by the server
        print "The Headers are: ", response.info()
        # Get the date part of the header
        print "The Date is: ", response.info()['date']
        # Get the server part of the header
        print "The Server is: ", response.info()['server']
        print "Cookie: ", response.info()['set-cookie']
        #print "Get all data: ", html
        # Get only the length
        print "Get the length :", len(html)
        print '++++++++++++++++++++++++++++++++'

    return json.loads(html)


def parse_response(json_string, last_answer_param):
    return json_string


def dorequest(method, method_params=''):
    resp = get_url(method, method_params, debug)
    return parse_response(resp, last_answer)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html;charset=utf-8")
        s.send_header("Accept-Charset", "utf-8")
        s.end_headers()
        s.wfile.write("<html><head><title>Oll.tv - live stream links</title>" \
                      "<style  type='text/css'>"
                      "#content { \n"
                      "  width: 900px; \n" \
                      "  display: inline;" \
                      "}\n" \
                      "div.item { \n" \
                      "  width: 12%; \n" \
                      "  min-width: 165px; \n" \
                      "  display: inline-block; \n" \
                      "  -webkit-box-shadow: 3px -1px 20px -1px rgba(0,0,0,0.6); \n" \
                      "  -moz-box-shadow: 3px -1px 20px -1px rgba(0,0,0,0.6); \n" \
                      "  box-shadow: 3px -1px 20px -1px rgba(0,0,0,0.6); \n" \
                      "  margin: 15px; \n" \
                      "  text-align: center; \n" \
                      "  padding: 10px; \n" \
                      "  padding-bottom: 10px; \n" \
                      "  vertical-align: top; \n" \
                      "} \n" \
                      "</style>" \
                      "</head>")
        s.wfile.write("<body><p><a href='/index/'>Oll.tv</a> - Get channel stream links</p><div id='content'>")
        myid = 0
        try:
            path_list = s.path.split('/')
            if len(path_list[2]) != 0:
                myid = path_list[2]
        except IndexError:
                pass

        if path_list[1] == 'channel':
            channel_data = dorequest('GetTVChannel', {'item_id': myid, 'afterDays': 7})
            s.wfile.write("<h2>%s</h2><img src='%s' border=0><br/>" % (
                channel_data[u'name'].encode('utf8', 'ignore'),
                channel_data[u'poster'].encode('utf8', 'ignore')
            ))
            # s.wfile.write("<a href='/item/%s'>Get Online Link</a><ul>" % (channel_data[u'item_id']))
            channel_link_data = dorequest('media', {'id': channel_data[u'item_id']})
            if len(channel_link_data) > 0:
                s.wfile.write("Your live stream link here:<br/><input type='text' size='140' value='%s'/><ul>" % (
                    channel_link_data[u'media_url'].encode('utf-8', 'ignore'),
                ))
            print pprint.pprint(channel_data[u'nextThree'])
            print pprint.pprint(channel_data[u'program'])
            for line in channel_data[u'nextThree']:
                s.wfile.write("<li><a href='/programm/%s'>%s</a> (%s / %s) - %s</li>" % (
                    line[u'programm_id'],
                    line[u'name'].encode('utf8', 'ignore'),
                    line[u'start'].encode('utf8', 'ignore'),
                    line[u'stop'].encode('utf8', 'ignore'),
                    ''))
            s.wfile.write("</ul><br/>History:<ul>")
            for line in channel_data[u'program']:
                s.wfile.write("<li><a href='/programm/%s'>%s</a> (%s / %s) - %s</li>" % (
                    line[u'programm_id'],
                    line[u'name'].encode('utf8', 'ignore'),
                    line[u'start'].encode('utf8', 'ignore'),
                    line[u'stop'].encode('utf8', 'ignore'),
                    ''))
        elif path_list[1] == 'item':
            channel_data = dorequest('media', {'id': myid})
            if len(channel_data) > 0:
                s.wfile.write("<ul><li>%s</li><li>%s</li><li>%s</li></ul>" % (
                    channel_data[u'category_name'].encode('utf-8', 'ignore'),
                    channel_data[u'title'].encode('utf-8', 'ignore'),
                    channel_data[u'media_url'].encode('utf-8', 'ignore'),
                ))
            print pprint.pprint(channel_data)

        elif path_list[1] == 'index' or s.path == '/':
            channels = dorequest('getAllTVChannels')
            for line in channels:
                for item in line[u'items']:
                    try:
                        if item[u'is_free'] != 1:
                            continue
                    except KeyError:
                        continue
                    s.wfile.write("<div class='item'><a href='/channel/%s'><img src='%s' border=0/>" \
                                  % (item[u'id'],
                                     item[u'src']))

                    s.wfile.write("<br/>%s (%s)</a><br/>%s</div>" \
                                  % (item[u'title'].encode('utf8', 'ignore'),
                                     item[u'genre'].encode('utf8', 'ignore'),
                                     item[u'descr'].encode('utf8', 'ignore')))
        # s.wfile.write("<p>You accessed path: %s</p>" % s.path)  # debug info
        s.wfile.write("</div></body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
