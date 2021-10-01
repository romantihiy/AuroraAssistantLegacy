from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import gpt_2_simple as gpt2
from datetime import datetime


#white_list = ['45.147.177.105']
white_list = []

class NeuronServer(BaseHTTPRequestHandler):

    def do_GET(self):
        for ip in white_list:
            if ip == self.client_address[0]:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"This site used only for POST request")

    def do_POST(self):
        for ip in white_list:
            if ip == self.client_address[0]:
                self.send_response(200)
                self.end_headers()
                content_len = int(self.headers.get('Content-Length'))
                post_body = self.rfile.read(content_len)
                post = post_body.decode('utf-8') # В переменной post запрос, в res надо положить ответ
                #res = ' '.join(gpt2.generate(sess, length=600, temperature=0.7, prefix='Error: ' + post + ' Answer: ' , nsamples=2, return_as_list=True, include_prefix=False))
                #res =  '''This problem was found by using for_each_range_with_parameters() instead of for_each_range_without_parameters()'''
                res = ' '.join(gpt2.generate(sess, length=600, temperature=0.7, prefix=('Error: ' + post + ' Answer: ') , nsamples=2, return_as_list=True))
                res = res.encode('utf-8')
                self.wfile.write(res)


if __name__ == "__main__":
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name='/home/romantihiy/checkpoint/run1')
    port = sys.argv[1:]
    httpd = HTTPServer((port[0], int(port[1])), NeuronServer)
    print("Сервер запущен на ip:", port[0], "на порту:", port[1])
    httpd.serve_forever()
