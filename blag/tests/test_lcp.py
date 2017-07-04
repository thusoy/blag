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


    def test_add_destination(self):
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


    def test_get_hike_form(self):
        with self.app.app_context():
            destination = HikeDestination(
                name='Peak 1',
                altitude=2048,
                high_point_coord='POINT(12.3 34.5)',
                is_summit=True,
            )
            db.session.add(destination)
            db.session.commit()
            destination_id = destination.id

        response = self.admin_user.get('/lcp/hikes')
        self.assert200(response)
        self.assertTrue('Peak 1 (2048)' in response.data.decode('utf-8'))


    def test_add_hike(self):
        with self.app.app_context():
            destination = HikeDestination(
                name='Peak 1',
                altitude=2048,
                high_point_coord='POINT(12.3 34.5)',
                is_summit=True,
            )
            db.session.add(destination)
            db.session.commit()
            destination_id = destination.id

        response = self.admin_user.post('/lcp/hikes', data={
            'destination_id': destination_id,
            'method': 'foot',
            'date': '2017-01-02',
        })
        self.assert302(response)
        with self.app.app_context():
            hikes = Hike.query.all()
            self.assertEqual(len(hikes), 1)
            self.assertEqual(hikes[0].destination_id, destination_id)


    def test_get_lcp(self):
        with self.app.app_context():
            peak1 = HikeDestination(
                name='Peak 1',
                altitude=2048,
                high_point_coord='POINT(32.1 12.3)',
                is_summit=True,
            )
            db.session.add(peak1)

            peak2 = HikeDestination(
                name='Peak 2',
                altitude=4096,
                high_point_coord='POINT(11.2 22.1)',
                is_summit=True,
            )
            db.session.add(peak2)

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
                destination=peak1,
                method='ski',
            ))
            db.session.add(Hike(
                destination=peak1,
                method='foot',
            ))
            db.session.add(Hike(
                destination=peak2,
                method='foot',
            ))
            db.session.add(Hike(
                destination=nonpeak,
                method='foot',
            ))
            db.session.commit()

        response = self.anon_user.get('/lcp/peaks')
        data = json.loads(self.assert200(response))
        data['peaks'].sort(key=lambda p: p['name'])
        self.assertEqual(data, {
            'peaks': [{
                'name': 'Peak 1',
                'coordinates': [32.1, 12.3],
            }, {
                'name': 'Peak 2',
                'coordinates': [11.2, 22.1],
            }]
        })
