import ujson as json

from . import UserTestCase, HTTPTestMixin

from .. import db
from ..models import HikeDestination, Hike


class LcpTest(UserTestCase, HTTPTestMixin):

    def test_main_page(self):
        response = self.anon_user.get('/lcp')
        data = self.assert200(response)


    def test_add_entry_anon(self):
        response = self.anon_user.post('/lcp/destinations')
        self.assert401(response)


    def test_add_entry_auth(self):
        response = self.auth_user.post('/lcp/destinations')
        self.assert403(response)


    def test_add_entry_form(self):
        response = self.admin_user.get('/lcp/destinations')
        self.assert200(response)


    def test_add_entry(self):
        response = self.admin_user.post('/lcp/destinations', data={
            'name': 'My Peak',
            'altitude': 2048,
            'high_point_coord': '32.4,43.2',
            'is_summit': True,
        })
        self.assert302(response)
        with self.app.app_context():
            destinations = HikeDestination.query.all()
            self.assertEqual(len(destinations), 1)
            self.assertEqual(destinations[0].name, 'My Peak')
            self.assertTrue(destinations[0].is_summit)


    def test_get_lcp(self):
        with self.app.app_context():
            peak = HikeDestination(
                name='Peak 1',
                altitude=2048,
                high_point_coord='POINT(32.1 12.3)',
                is_summit=True,
            )
            db.session.add(peak)
            nonpeak = HikeDestination(
                name='Nonpeak',
                altitude=765,
                high_point_coord='POINT(54.3 34.5)',
                is_summit=False,
            )
            db.session.add(nonpeak)
            db.session.add(HikeDestination(
                name='Peak without hikes',
                altitude=1234,
                high_point_coord='POINT(12.3 32.1)',
                is_summit=True,
            ))
            db.session.add(Hike(
                destination=peak,
                method='ski',
            ))
            db.session.add(Hike(
                destination=nonpeak,
                method='foot',
            ))
            db.session.commit()

        response = self.anon_user.get('/lcp/peaks')
        data = json.loads(self.assert200(response))
        self.assertEqual(data, {
            'peaks': [{
                'name': 'Peak 1',
                'altitude': 2048,
                'coordinates': [32.1, 12.3],
            }]
        })
