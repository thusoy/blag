include:
    - postgis
    - postgres.server


postgres-vagrant-user:
    postgres_user.present:
        - name: vagrant
        - password: vagrant


{% for database in ('vagrant', 'testdb') %}
postgres-vagrant-database-{{ database }}:
    postgres_database.present:
        - name: {{ database }}
        - owner: vagrant
        - require:
            - postgres_user: postgres-vagrant-user


postgres-vagrant-database-{{ database }}-postgis:
    postgres_extension.present:
        - name: postgis
        - maintenance_db: {{ database }}
{% endfor %}
