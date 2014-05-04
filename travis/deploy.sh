# Compute the file hashes
sha1sum dist/static.tar.gz | cut -f 1 -d " " > dist/static.tar.gz.sha1
sha1sum dist/thusoy-blag-0.1.0.tar.gz | cut -f 1 -d " " > dist/thusoy-blag-0.1.0.tar.gz.sha1

# Upload hashes and files
aws s3 cp --acl public-read dist/thusoy-blag-0.1.0.tar.gz s3://thusoy.com/dist/blag.tar.gz
aws s3 cp --acl public-read dist/thusoy-blag-0.1.0.tar.gz.sha1 s3://thusoy.com/dist/blag.tar.gz.sha1

aws s3 cp --acl public-read dist/static.tar.gz s3://thusoy.com/dist/blag-static.tar.gz
aws s3 cp --acl public-read dist/static.tar.gz.sha1 s3://thusoy.com/dist/blag-static.tar.gz.sha1
