#!./venv/bin/python

import argparse
import csv
import datetime
import sys
import re
from collections import namedtuple

from blag import create_app, db
from blag.models import HikeDestination, Hike

DATE_FORMAT = '%d.%m.%Y'
COORDINATE_FORMAT = re.compile(r'^([0-9.-]+),\s*([0-9.-]+)$')
METHOD_MAP = {
    'fots': 'foot',
    'stegjern': 'crampons',
}

PeakTuple = namedtuple('PeakTuple', 'name method coordinates date notes')

def main():
    args = get_args()
    peaks = parse_csv(args.file)
    insert_to_database(peaks, args.database)


def parse_csv(input_file):
    '''Assumes fields are name,method,coordinate,date,notes'''
    parsed = []
    with open(input_file) as fh:
        csv_reader = csv.reader(fh)
        for row_num, row in enumerate(csv_reader):
            if row_num == 0:
                # Skip the header line
                continue
            assert len(row) == 5
            peak = PeakTuple(*(elem.strip() for elem in row))
            parsed.append(peak)
    return parsed


def insert_to_database(peaks, database):
    app = create_app(SQLALCHEMY_DATABASE_URI=database)
    with app.app_context():
        for peak in peaks:
            if not peak.coordinates:
                sys.stderr.write('Skipping %s due to missing coordinates\n' % peak.name)
                continue
            hike_destination = HikeDestination(
                name=peak.name,
                high_point_coord=point_from_coordinates(peak.coordinates),
                altitude=0,
                is_summit=True,
            )
            db.session.add(hike_destination)
            if not peak.method:
                sys.stderr.write('Skipping hike for %s since method is missing\n' % peak.name)
                continue
            hike = Hike(
                destination=hike_destination,
                method=METHOD_MAP.get(peak.method, peak.method),
                date=datetime.datetime.strptime(peak.date, DATE_FORMAT) if peak.date else None,
            )
            db.session.add(hike)
        db.session.commit()


def point_from_coordinates(coord):
    '''Transform a "float, float" string to POINT(float float)'''
    match = COORDINATE_FORMAT.match(coord)
    assert match, '%s didnt match coordinate format' % coord
    parsed_coords = (match.group(1), match.group(2))
    return 'POINT(%s %s)' % parsed_coords


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File to read the LCP from')
    parser.add_argument('-d', '--database', help='Address to the database to insert into',
        default='postgres://vagrant:vagrant@10.20.30.50/vagrant')
    return parser.parse_args()


if __name__ == '__main__':
    main()
