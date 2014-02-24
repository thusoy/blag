ll ~/.aws
cat ~/.aws/config
aws s3 cp dist/static.tar.gz s3://thusoy.com/dist/blag-static.tar.gz --debug
aws s3 cp dist/thusoy-blag-0.1.0.tar.gz s3://thusoy.com/dist/blag.tar.gz --debug
