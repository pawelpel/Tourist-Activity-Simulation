import tornado.web
import tornado.escape
from tornado.ioloop import IOLoop
import simplejson

from sim.main import run_simulation, main_sim
from sim.main import get_default_options, options


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_user_options(self):
        # Returns dict with default options updated by user options
        ret_options = get_default_options()
        for k, v in ret_options.items():
            o = self.get_argument(k, default=None)
            if o is not None:
                ret_options[k] = int(o) if o.isdigit() else o
        return ret_options


class MainHandler(BaseHandler):
    def post(self):
        # Iter over all simulation and send all
        runner = run_simulation(self.get_user_options())
        for i, r in enumerate(runner):
            self.write(simplejson.dumps([i, r])+"\n",)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


def main():
    app = Application()
    app.listen(8888, address='127.0.0.1')
    IOLoop.instance().start()


if __name__ == '__main__':

    # To run server
    # main()

    # To run simulation
    main_sim()
