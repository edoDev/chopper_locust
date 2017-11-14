"""Define a locust swarm for testing a WMS service.
"""

from locust import HttpLocust, task
from locust import TaskSet
import random


centers = {
    "zoom out on Europe": (3.76, 47.70, 4.46),
    "zoom out on British Isles": (7.67, 54.637, -6.945),
    "zoom out on all Ireland": (6.23, 53.475, -7.563),
    "zoom out on Northern Ireland": (7.67, 54.637, -6.945),
    "Cork": (11.52, 51.9102, -8.4709),
    "Waterford": (12.27, 52.2555, -7.1169),
    "Wexford": (13.23, 52.3323, -6.4645),
    "Dublin": (11.1, 53.3391, -6.2598),
    "Dublin (Ballsbridge)": (16.37, 53.32891, -6.23133),
    "Dublin (St. Stephen's Green)": (16.57, 53.33816, -6.25913),
    "Belfast (Greater Area)": (10.86, 54.6098, -5.9528),

    "Belfast (Harbor Marina)": (16.04, 54.60473, -5.91630),
    "Killarney and lake": (11.77, 52.0461, -9.4843),
    "Killarney": (14.44, 52.0583, -9.5030),
    "Galway": (11.86, 53.2717, -9.0269),
    "Dundalk": (12.97, 54.0058, -6.4118),
    "Limerick": (11.78, 52.6556, -8.6261),
    "some Lough Corrib": (11.74, 53.4708, -9.2843),
    "Inishmicatreer": (14.46, 53.4976, -9.2548),
    "Newry": (15.4, 54.1773, -6.3383),
    "closeup Drogheda": (16.37, 53.71358, -6.35426),
    "Isle of Man": (9.43, 54.2294, -4.6263),
    "Liverpool": (10.48, 53.4071, -3.0120),

    # Failures
    # "Belfast (Center)": (14, 54.5979, -5.9328),
    # "closeup Dundalk": (17, 54.00501, -6.40261),
}
center_keys = list(centers.keys())


class TileTester(TaskSet):
    """Exercise WMS endpoints.
    """

    def on_start(self):
        """Startup method called by locust once for each new simulated user.
        """
        # Workaround for self-signed certificate
        self.client.verify = False

    @task(0)
    def get_demo_page(self):
        uri = "https://localhost:8000/demo"
        self.client.get(uri, catch_response=False)

    @task(1)
    def get_a_tile(self):
        # x = get "x" parameter
        # y = get "y" parameter, remove ".pbf"
        # z = get "z" parameter;
        # y = str(normalizeY(y, z))
        # t = GetTile(z, x, y)

        key = random.choice(center_keys)
        z, x, y = centers[key]
        # URL format from squirrelchopper/tiles/tile.go: GetUrl().
        uri = "/tiles/{0}/{1}/{2}.pbf".format(z, x, y)
        response = self.client.get(uri, name=key, catch_response=True)
        with response:
            # Rule of thumb
            # Real tile ~10k
            # Demo page ~644 bytes
            if not response.content:
                response.failure("Empty response body")


class TileUser(HttpLocust):
    """Specify how each simulated user will behave.
    """
    # Define the behavior of the user.
    task_set = TileTester

    # Parameters for generating the random wait between tasks.
    min_wait = 0
    max_wait = 0
