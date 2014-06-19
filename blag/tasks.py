from . import make_celery, db
from .models import BlogImage

from contextlib import contextmanager
from flask import current_app
from functools import partial, wraps
from logging import getLogger
from paramiko import SSHClient
import os

celery = make_celery()
task = partial(celery.task, base=celery.Task, ignore_result=True)
_logger = getLogger('blag.tasks')

def log_errors(msg):
    """ Decorator to wrap a function in a try/except, and log errors with `msg` and stacktrace. """

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                _logger.exception(msg)

        return wrapper

    return decorator


@contextmanager
def fileserver_ssh_client():
    """ Context-manager to get ssh connection to the fileserver. """
    fileserver = current_app.config.get_namespace('FILESERVER_')
    ssh = SSHClient()
    host_keys = os.path.join(os.path.dirname(__file__), 'server-assets', 'host_keys')
    ssh.load_host_keys(host_keys)
    try:
        ssh.connect(fileserver['URL'], username=fileserver['USERNAME'],
            key_filename=fileserver['key_file'])
        _logger.info('SSH connection to fileserver established')
        yield ssh
    finally:
        ssh.close()


def _ensure_parent_directory_exists(path, ssh_client):
    parent_dir = os.path.dirname(path)
    _logger.debug('Creating target dir if necessary: %s', parent_dir)
    ssh_client.exec_command('test -d {0} || mkdir -p {0}'.format(parent_dir))


@task(name='upload-image-to-fileserver')
@log_errors('Image upload failed')
def upload_image_to_fileserver(image_id):
    image = BlogImage.query.get(image_id)
    src = os.path.join(current_app.config['LOCAL_UPLOAD_DIR'], '%d%s' % (image_id, image.extension))
    dest = image.orig_basepath
    upload_to_fileserver(src, dest)
    image.state = BlogImage.STATE_READY
    db.session.commit()


@task(name='upload-to-fileserver')
def upload_to_fileserver(src, dest):
    target_path = current_app.config['FILESERVER_MEDIA_DIR'] + dest
    with fileserver_ssh_client() as ssh:
        _ensure_parent_directory_exists(target_path, ssh)
        _logger.info('Uploading %s to %s', src, target_path)
        sftp = ssh.open_sftp()
        sftp.put(src, target_path)
    _logger.info('File upload completed')


@task(name='delete-from-fileserver')
def delete_from_fileserver(path):
    pass
