FILEPATH="data/"downloaded_`date +%Y_%m_%d`/

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

YEARS="_2015_2016"
mv 'itcont.txt' 'itcont.txt'$YEARS'.txt'
mv 'itoth.txt' 'itoth'$YEARS'.txt'
mv 'cm.txt' 'cm'$YEARS'.txt'
mv 'cn.txt' 'cn'$YEARS'.txt'
mv 'ccl.txt' 'ccl'$YEARS'.txt'
mv 'itpas2.txt' 'itpas2'$YEARS'.txt'
mv 'opexp.txt' 'opexp'$YEARS'.txt'
mv 'CampaignAndCommitteeSummary.csv' 'CampaignAndCommitteeSummary'$YEARS'.csv'
