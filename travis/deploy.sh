cd dist
aws s3 cp static.tar.gz s3://thusoy.com/dist/blag-static.tar.gz --debug
aws s3 cp thusoy-blag-0.1.0.tar.gz s3://thusoy.com/dist/blag.tar.gz --debug
