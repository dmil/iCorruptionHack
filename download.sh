FILEPATH="data/2013_2014/"downloaded_`date +%Y_%m_%d`"_tmp/"

mkdir -p $FILEPATH
cd $FILEPATH

wget 'ftp://ftp.fec.gov/FEC/2016/indiv16.zip'
wget 'ftp://ftp.fec.gov/FEC/2016/cn16.zip'
wget 'ftp://ftp.fec.gov/FEC/2016/ccl16.zip'
wget 'ftp://ftp.fec.gov/FEC/2016/oth16.zip'
wget 'ftp://ftp.fec.gov/FEC/2016/pas216.zip'
wget 'ftp://ftp.fec.gov/FEC/2016/opexp16.zip'

wget -O 'CampaignAndCommitteeSummary.csv' 'http://www.fec.gov/data/CampaignAndCommitteeSummary.do?format=csv'

unzip '*.zip'
rm *.zip
