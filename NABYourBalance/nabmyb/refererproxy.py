from __future__ import print_function, unicode_literals
import threading

from libmproxy import controller


class RefererMaster(controller.Master):

    def __init__(self, server, referer):
        self.referer = referer.encode('latin-1')
        self.server_thread = None
        super(RefererMaster, self).__init__(server)

    def run(self):
        print('Running...')
        return super(RefererMaster, self).run()

    def run_async(self):
        self.server_thread = threading.Thread(target=self.run)
        self.server_thread.daemon = True
        self.server_thread.start()

    def shutdown_async(self):
        if self.server_thread is None:
            return

        print('Shutting down...', end='')
        self.should_exit.set()
        self.server_thread.join()
        print('OK')

    def handle_request(self, flow):
        try:
            flow.request.headers[b'referer'] = self.referer
        except:
            self.shutdown()
            raise

        print(flow.request)
        flow.reply()

    def handle_response(self, flow):

        print(flow.response)
        flow.reply()
