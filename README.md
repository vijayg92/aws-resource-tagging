# Auto Tagging of AWS Resources

This framework can be used to automatically tag AWS resources based on Cloudtrail trail events.

## Configuration

Clone the repository from [aws-resource-tagging](aws-resource-tagging) and then follow the next section. 

```bash
git clone git@https://github.com/vijayg92/aws-resource-tagging.git
cd aws-resource-tagging
```

## Usage
To run this script, AWS KEY & Secret need to be explicitly passed at run time. 
```
pip3 install -r requirements.txt
python3 main.py -h
usage: AWSResourceTagging [options]

Framework to auto tag AWS resources

optional arguments:
  -h, --help       show this help message and exit
  --key KEY        AWS Secret Key
  --secret SECRET  AWS Secret
  --region REGION  AWS Region

python3 main.py --key ${AWS_ACCESS_KEY_ID} --secret ${AWS_SECRET_ACCESS_KEY} --region 'us-east-1'
```

## Note
This script will only support EC2 instance tagging for now, however, support for other resources will be added later. 

## Contributing
Pull requests are welcome. 


## License
[GPLv3](https://en.wikipedia.org/wiki/GNU_General_Public_License)
