#!/usr/bin/env python3.5
import tornado.web
import tornado.escape
from tornado.ioloop import IOLoop
import simplejson
import copy

# from sim import main_sim
from sim import run_simulation
from sim import get_default_options
from sim import main_sim


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_user_options(self):
        # Returns dict with default options updated by user options
        ret_options = get_default_options()

        print("Chosen options for simulation: ")
        for k, v in ret_options.items():
            o = self.get_argument(k, default=None)
            if o is not None:
                ret_options[k] = int(o) if o.isdigit() else o
            print("{:25} : {}".format(k, ret_options[k]))
        return ret_options


class MainHandler(BaseHandler):
    def post(self):
        print('-'*80)
        print('New request came!')
        # Iter over all simulation and send all
        runner = run_simulation(self.get_user_options())

        report = []
        for i, r in enumerate(runner):
            report.append([i, copy.deepcopy(r)])

        self.write(simplejson.dumps(report, separators=(',', ':')))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


def main():
    print('Starting the server!')
    app = Application()

    PORT = 8888
    IP = '127.0.0.1'

    app.listen(PORT, address=IP)
    print('Working on {}:{}'.format(IP, PORT))
    IOLoop.instance().start()

if __name__ == '__main__':

    # To run server
    main()

    # To run simulation
    # main_sim()
